"""
Multilingual RAG Engine for Sai Baba spiritual guidance chatbot.
Supports English, Hindi, Telugu, and Kannada with automatic language detection.
"""

import re
from typing import Optional, Dict, List
from loguru import logger

# Optional imports for LangChain-related features. These are guarded so the
# module can be imported in simpler environments (CLI or tests) without
# requiring the full set of optional dependencies to be installed.
try:
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_openai import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.documents import Document
    HAS_LANGCHAIN = True
except Exception:
    FAISS = None
    HuggingFaceEmbeddings = None
    ChatOpenAI = None
    ChatGoogleGenerativeAI = None
    PromptTemplate = None
    Document = None
    HAS_LANGCHAIN = False

from config import settings

# Lazy import placeholder for DataIngestionPipeline (heavy optional dependency)
DataIngestionPipeline = None

from language_utils import LanguageDetector, get_language_specific_prompt, format_multilingual_response


class SafetyFilter:
    """Implements safety and ethical guardrails for responses."""
    
    # Prohibited topics
    MEDICAL_KEYWORDS = [
        'disease', 'cure', 'medicine', 'treatment', 'diagnosis', 'symptom',
        'cancer', 'diabetes', 'covid', 'illness', 'drug', 'prescription',
        'surgery', 'therapy', 'medical', 'health problem', 'sick'
    ]
    
    LEGAL_KEYWORDS = [
        'lawsuit', 'legal advice', 'court', 'lawyer', 'attorney', 'sue',
        'contract', 'divorce', 'custody', 'will', 'testament', 'rights',
        'law', 'illegal', 'criminal'
    ]
    
    PREDICTIVE_KEYWORDS = [
        'predict', 'future', 'will happen', 'fortune', 'lottery', 'winning',
        'stock market', 'investment', 'when will', 'prediction', 'foretell'
    ]
    
    DIVINE_CLAIMS = [
        'i am god', 'i am divine', 'i am sai baba', 'worship me',
        'i am omnipotent', 'i am all-knowing'
    ]
    
    @staticmethod
    def is_prohibited_topic(question: str) -> Optional[str]:
        """
        Check if question contains prohibited topics.
        
        Args:
            question: User's question
        
        Returns:
            Warning message if prohibited, None otherwise
        """
        question_lower = question.lower()
        
        # Check for medical topics
        if any(keyword in question_lower for keyword in SafetyFilter.MEDICAL_KEYWORDS):
            return (
                "I cannot provide medical advice. For health concerns, "
                "please consult qualified healthcare professionals. "
                "I can only share general spiritual wisdom from Sai Baba's teachings."
            )
        
        # Check for legal topics
        if any(keyword in question_lower for keyword in SafetyFilter.LEGAL_KEYWORDS):
            return (
                "I cannot provide legal advice. For legal matters, "
                "please consult qualified legal professionals. "
                "I can only share spiritual guidance from Sai Baba's teachings."
            )
        
        # Check for predictive/fortune-telling
        if any(keyword in question_lower for keyword in SafetyFilter.PREDICTIVE_KEYWORDS):
            return (
                "I cannot predict the future or provide fortune-telling. "
                "I can only share timeless spiritual wisdom from Sai Baba's teachings "
                "to help guide your present journey."
            )
        
        return None
    
    @staticmethod
    def sanitize_response(response: str) -> str:
        """
        Ensure response doesn't contain divine claims.
        
        Args:
            response: Generated response
        
        Returns:
            Sanitized response
        """
        response_lower = response.lower()
        
        # Check for divine claims
        for claim in SafetyFilter.DIVINE_CLAIMS:
            if claim in response_lower:
                logger.warning(f"Detected divine claim in response: {claim}")
                response = response.replace(claim, "Sai Baba teaches")
        
        # Add disclaimer if response is very short or uncertain
        if len(response) < 50 or "i don't know" in response_lower:
            response += (
                "\n\nNote: This guidance is based on the available teachings. "
                "For deeper spiritual understanding, consider studying Sai Baba's "
                "original works and seeking guidance from qualified spiritual teachers."
            )
        
        return response


class MultilingualRAGEngine:
    """Multilingual Retrieval-Augmented Generation engine for question answering."""
    
    def __init__(self):
        """Initialize the multilingual RAG engine."""
        logger.info("Initializing Multilingual RAG engine")
        # Load vector store (lazy import of ingestion pipeline to avoid import-time errors)
        try:
            if DataIngestionPipeline is None:
                from ingest import DataIngestionPipeline as _DIP
                globals()['DataIngestionPipeline'] = _DIP
            self.pipeline = DataIngestionPipeline()
            # Only attempt to LOAD an existing vector store; do NOT build here.
            try:
                self.vector_store = self.pipeline.load_vector_store()
                if self.vector_store:
                    logger.info("Vector DB loaded successfully.")
                else:
                    logger.warning("Vector DB not found during engine init.")
            except Exception as e:
                logger.error(f"Error loading vector store: {e}")
                self.vector_store = None
        except Exception:
            self.pipeline = None
            self.vector_store = None

        # Initialize LLM only if explicitly enabled in settings
        self.llm = None
        if settings.use_llm:
            self.llm = self._initialize_llm()
        
        # Initialize safety filter and language detector
        self.safety_filter = SafetyFilter()
        self.language_detector = LanguageDetector()
        
        # Create retrieval chain
        self.qa_chain = self._create_qa_chain()
        
        logger.success("Multilingual RAG engine initialized successfully")
        logger.info(f"Supported languages: {', '.join(settings.supported_languages)}")
    
    def _load_or_create_vector_store(self) -> FAISS:
        """
        Load existing vector store. This method will NOT create/build a new
        vector store. Building must be performed by `ingest.py` separately.

        Returns:
            FAISS vector store or None if not present
        """
        if not self.pipeline:
            logger.warning("Data ingestion pipeline not available; cannot load vector store.")
            return None

        try:
            vector_store = self.pipeline.load_vector_store()
            if vector_store is None:
                logger.warning("Vector store not found. Please run ingest.py to build the vector DB.")
            else:
                logger.info("Vector DB loaded successfully.")
            return vector_store
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            return None
    
    def _initialize_llm(self):
        """
        Initialize the Language Model based on configuration.
        
        Returns:
            LLM instance (OpenAI or Gemini)
        """
        logger.info(f"Initializing {settings.ai_provider} LLM")
        
        # Perform lazy imports for LLM wrappers so the module can be imported
        # even if langchain/OpenAI libs are not installed. Raise a clear error
        # if LLM mode is enabled but required packages/keys are missing.
        if settings.ai_provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required when use_llm=true and provider=openai")
            try:
                from langchain_openai import ChatOpenAI as _ChatOpenAI
            except Exception as e:
                raise ImportError("langchain_openai is required for OpenAI LLM mode") from e

            llm = _ChatOpenAI(
                model_name=settings.model_name_openai,
                temperature=settings.model_temperature,
                openai_api_key=settings.openai_api_key
            )
        elif settings.ai_provider == "gemini":
            if not settings.google_api_key:
                raise ValueError("GOOGLE_API_KEY is required when use_llm=true and provider=gemini")
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI as _ChatGoogleGenerativeAI
            except Exception as e:
                raise ImportError("langchain_google_genai is required for Gemini LLM mode") from e

            llm = _ChatGoogleGenerativeAI(
                model=settings.model_name_gemini,
                temperature=settings.model_temperature,
                google_api_key=settings.google_api_key
            )
        else:
            raise ValueError(f"Unsupported AI provider: {settings.ai_provider}")

        logger.success(f"{settings.ai_provider} LLM initialized")
        return llm
    
    def _create_prompt_template(self) -> PromptTemplate:
        """
        Create the multilingual prompt template with safety guidelines.
        
        Returns:
            PromptTemplate instance
        """
        template = """
You are a humble, compassionate spiritual guide in the voice of a gentle, divine mentor inspired by Sai Baba's teachings.

GUIDELINES (MUST FOLLOW):
- Speak softly and lovingly; open by addressing the user gently (for example "My child,").
- Use calm, reassuring, devotional language and offer consolation, moral counsel, and spiritual perspective.
- Write a single flowing answer of 1–2 meaningful paragraphs (no bullet lists).
- Do NOT mention AI, models, PDFs, sources, or system internals in the answer; do not describe your process.
- Use the retrieved context strictly as grounding: never contradict the content in the context.
- If the context partially answers the question, blend its meaning with compassionate spiritual guidance.
- If the context does not directly answer, respond with faith-based, reflective guidance rather than refusing.
- NEVER provide medical, legal, or harmful instructions.

LANGUAGE INSTRUCTION:
{language_instruction}

CONTEXT (Grounding Passages):
{context}

QUESTION:
{question}

Produce the final answer now following the guidelines above.
Answer:
"""

        # If LangChain's PromptTemplate isn't available, return the raw template string
        if PromptTemplate is None:
            return template

        return PromptTemplate(
            template=template,
            input_variables=["context", "question", "language_instruction"]
        )
    
    def _generate_answer_from_docs(self, docs: List[Document], detected_language: str) -> str:
        """
        Create a devotional 1-2 paragraph answer by concatenating top document chunks.
        This is used when an LLM is not available (RAG-only mode).
        """
        if not docs:
            return {
                "en": "This guidance is not available in Sai Baba's teachings.",
                "hi": "यह मार्गदर्शन साईं बाबा की शिक्षाओं में उपलब्ध नहीं है।",
                "te": "ఈ మార్గదర్శకత్వం సాయి బాబా బోధలలో అందుబాటులో లేదు।",
                "kn": "ಈ ಮಾರ್ಗದರ್ಶನವು ಸಾಯಿ ಬಾಬಾ ಅವರ ಬೋಧನೆಗಳಲ್ಲಿ ಲಭ್ಯವಿಲ್ಲ."
            }.get(detected_language, "This guidance is not available in Sai Baba's teachings.")

        # Take top 3 chunks as grounding
        texts = [re.sub(r"\s+", " ", getattr(d, 'page_content', '')).strip() for d in docs[:3]]
        # Keep non-empty parts
        parts = [t for t in texts if t]
        if not parts:
            return ""

        # Join into up to two paragraphs
        if len(parts) == 1:
            combined = parts[0]
        else:
            combined = "\n\n".join(parts[:2])

        # Devotional prefix / gentle address per language
        prefixes = {
            'en': "My child,",
            'hi': "मेरे बच्चे,",
            'te': "నా బిడ్డా,",
            'kn': "ನನ್ನ ಮಕ್ಕಳೆ,"
        }
        prefix = prefixes.get(detected_language, prefixes['en'])

        # Compose final answer: prefix + grounded passages + gentle closing if single paragraph
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", combined) if p.strip()]
        if not paragraphs:
            return prefix + " " + combined

        # Prepend prefix to first paragraph
        paragraphs[0] = prefix + " " + paragraphs[0]

        if len(paragraphs) == 1:
            closings = {
                'en': " May you find peace and strength in these teachings.",
                'hi': " इन शिक्षाओं में आपको शांति और शक्ति मिले।",
                'te': " ఈ బోధనలలో మీకో శాంతి మరియు శక్తి లభించాలి.",
                'kn': "ಈ ಬೋಧನೆಗಳಲ್ಲಿ ನಿಮಗೆ ಶಾಂತಿ ಮತ್ತು ಶಕ್ತಿ ದೊರಕಲಿ."
            }
            paragraphs[0] = paragraphs[0].strip() + closings.get(detected_language, closings['en'])

        answer = "\n\n".join(paragraphs)
        # Normalize whitespace
        answer = re.sub(r"\s+", " ", answer).strip()
        return answer

    def _create_qa_chain(self):
        """
        Create a simple retrieval and generation chain using modern LangChain.
        
        Returns:
            Chain function
        """
        # For newer LangChain, we'll use a simple retrieval-based approach
        # This will be called directly in answer_question
        return None
    
    def get_relevant_documents(self, question: str) -> List[Document]:
        """
        Retrieve relevant documents for a question.
        
        Args:
            question: User's question
        
        Returns:
            List of relevant documents
        """
        # If vector store is not available, return empty list (graceful fallback)
        if not getattr(self, 'vector_store', None):
            logger.debug("No vector store available for retrieval; returning empty results.")
            return []

        try:
            docs = self.vector_store.similarity_search(
                question,
                k=settings.top_k_results
            )
            return docs
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []
    
    def answer_question(self, question: str, detected_language: Optional[str] = None) -> Dict[str, any]:
        """
        Answer a question using multilingual RAG with safety checks.
        
        Args:
            question: User's question in any supported language
            detected_language: Pre-detected language (optional)
        
        Returns:
            Dictionary containing answer, language, and metadata
        """
        try:
            logger.info(f"Processing question: {question[:100]}...")
            
            # Detect language if not provided
            if detected_language is None:
                detected_language = self.language_detector.detect_language(question)
            
            logger.info(f"Question language: {self.language_detector.get_language_name(detected_language)}")
            
            # Safety check for prohibited topics
            safety_warning = self.safety_filter.is_prohibited_topic(question)
            if safety_warning:
                logger.warning(f"Prohibited topic detected: {question[:50]}...")
                return {
                    "answer": safety_warning,
                    "language": detected_language,
                    "sources": [],
                    "is_safe": False
                }
            
            # Get language-specific instruction
            language_instruction = get_language_specific_prompt(detected_language)
            
            # Retrieve relevant documents
            source_docs = self.get_relevant_documents(question)
            
            if not source_docs:
                logger.warning("No relevant documents found")
                no_info_responses = {
                    "en": "This guidance is not available in Sai Baba's teachings.",
                    "hi": "यह मार्गदर्शन साईं बाबा की शिक्षाओं में उपलब्ध नहीं है।",
                    "te": "ఈ మార్గదర్శకత్వం సాయి బాబా బోధలలో అందుబాటులో లేదు।",
                    "kn": "ಈ ಮಾರ್ಗದರ್ಶನವು ಸಾಯಿಬಾಬಾ ಅವರ ಬೋಧನೆಗಳಲ್ಲಿ ಲಭ್ಯವಿಲ್ಲ."
                }
                answer = no_info_responses.get(detected_language, no_info_responses["en"])
            else:
                # Format context from retrieved documents
                context = "\n\n".join([doc.page_content for doc in source_docs])
                
                # Create the prompt
                prompt = self._create_prompt_template()
                formatted_prompt = prompt.format(
                    context=context,
                    question=question,
                    language_instruction=language_instruction
                )
                
                # Generate answer using LLM if available; otherwise produce RAG-only answer
                llm_error = None
                if self.llm is None:
                    # RAG-only mode: produce a devotional 1-2 paragraph answer from retrieved docs
                    answer = self._generate_answer_from_docs(source_docs, detected_language)
                else:
                    try:
                        from langchain_core.messages import HumanMessage
                        response = self.llm.invoke([HumanMessage(content=formatted_prompt)])
                        answer = response.content
                    except Exception as e:
                        try:
                            response = self.llm.invoke(formatted_prompt)
                            answer = response.content if hasattr(response, 'content') else str(response)
                        except Exception as e2:
                            llm_error = f"LLM generation failed: {str(e2)}"
                            logger.error(f"LLM generation failed: {e2}. Falling back to retrieved context.")
                            # Fallback to RAG-only generation using retrieved docs
                            answer = self._generate_answer_from_docs(source_docs, detected_language)
            
            # Sanitize response
            answer = self.safety_filter.sanitize_response(answer)
            
            # Format for language
            answer = format_multilingual_response(answer, detected_language)
            
            # Extract source information
            sources = []
            for doc in source_docs:
                source_info = {
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata
                }
                sources.append(source_info)
            
            logger.success(f"Question answered successfully in {detected_language}")
            result = {
                "answer": answer,
                "language": detected_language,
                "sources": sources,
                "is_safe": True
            }
            if 'llm_error' in locals() and llm_error:
                result["error"] = llm_error
            return result
            
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            
            # Error messages in detected language
            error_messages = {
                "en": "I apologize, but I encountered an error while processing your question. Please try rephrasing your question or try again later.",
                "hi": "क्षमा करें, आपके प्रश्न को संसाधित करते समय एक त्रुटि हुई। कृपया अपना प्रश्न दोबारा लिखें या बाद में पुनः प्रयास करें।",
                "te": "క్షమించండి, మీ ప్రశ్నను ప్రాసెస్ చేయడంలో లోపం ఏర్పడింది. దయచేసి మీ ప్రశ్నను తిరిగి వ్రాయండి లేదా తర్వాత మళ్లీ ప్రయత్నించండి।",
                "kn": "ಕ್ಷಮಿಸಿ, ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಪ್ರಕ್ರಿಯೆಗೊಳಿಸುವಲ್ಲಿ ದೋಷ ಎದುರಾಗಿದೆ. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಪುನಃ ಬರೆಯಿರಿ ಅಥವಾ ನಂತರ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ."
            }
            
            lang = detected_language if detected_language else "en"
            
            return {
                "answer": error_messages.get(lang, error_messages["en"]),
                "language": lang,
                "sources": [],
                "is_safe": True,
                "error": str(e)
            }
    
    def validate_system(self) -> Dict[str, any]:
        """
        Validate that the RAG system is working correctly.
        
        Returns:
            Dictionary with validation results
        """
        try:
            # If vector store missing, return degraded status rather than failing
            if not getattr(self, 'vector_store', None):
                logger.warning("Vector store missing during system validation; marking as degraded.")
                return {
                    "vector_store_size": None,
                    "retrieval_working": False,
                    "answer_generation_working": True,  # generation may still work in LLM-only mode
                    "llm_provider": settings.ai_provider if settings.use_llm else None,
                    "status": "degraded"
                }

            # Check vector store
            index_size = self.vector_store.index.ntotal

            # Test retrieval
            test_docs = self.get_relevant_documents("What is devotion?")

            # Test answer generation
            test_result = self.answer_question("What is the importance of faith?")

            validation = {
                "vector_store_size": index_size,
                "retrieval_working": len(test_docs) > 0,
                "answer_generation_working": len(test_result["answer"]) > 0,
                "llm_provider": settings.ai_provider if settings.use_llm else None,
                "status": "healthy"
            }

            logger.success("System validation passed")
            return validation

        except Exception as e:
            logger.error(f"System validation failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }


def main():
    """CLI entry point for testing the multilingual RAG engine."""
    logger.info("Starting Multilingual RAG engine test")
    
    try:
        # Initialize engine
        engine = MultilingualRAGEngine()
        
        # Validate system
        validation = engine.validate_system()
        logger.info(f"System validation: {validation}")
        
        # Interactive Q&A
        print("\n" + "="*60)
        print("Sai Baba Spiritual Guidance Chatbot - Multilingual RAG Test")
        print("Supported Languages: English, Hindi, Telugu, Kannada")
        print("="*60)
        print("Type 'quit' or 'exit' to stop\n")
        
        while True:
            question = input("\nYour question (any language): ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                break
            
            if not question:
                continue
            
            result = engine.answer_question(question)
            print(f"\nLanguage: {result.get('language', 'unknown')}")
            print(f"Answer: {result['answer']}")
            
            if result.get('sources'):
                print(f"\n(Based on {len(result['sources'])} source(s))")
        
        logger.info("Multilingual RAG engine test completed")
        
    except Exception as e:
        logger.error(f"Multilingual RAG engine test failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
