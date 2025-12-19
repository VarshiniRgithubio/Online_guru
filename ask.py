#!/usr/bin/env python3
"""
Simple CLI interface to ask questions to the Sai Baba Chatbot
Works without requiring vector database - uses sample teachings directly
"""

from typing import Dict, Optional
import re
from config import settings
from language_utils import LanguageDetector
from rag_engine import SafetyFilter
from ingest import DataIngestionPipeline
from loguru import logger

# Configure logger to suppress too much output
logger.remove()
logger.add(lambda msg: None)  # Disable file logging for CLI


class SimpleChatbot:
    """Simple question-answering chatbot without vector DB dependency"""
    
    def __init__(self):
        """Initialize the chatbot"""
        self.safety_filter = SafetyFilter()
        self.language_detector = LanguageDetector()
        
        # Load sample teachings as fallback
        self.teachings = self._load_sample_teachings()

        # Try to load vector DB for retrieval over all ingested data
        try:
            pipeline = DataIngestionPipeline()
            self.vector_store = pipeline.load_vector_store()
            if self.vector_store:
                # keep top_k in settings
                self.top_k = settings.top_k_results
            else:
                self.top_k = 4
        except Exception:
            self.vector_store = None
            self.top_k = 4
        
    def _load_sample_teachings(self) -> str:
        """Load sample teachings from file"""
        try:
            with open("data/sample_teachings.txt", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "Sample teachings not found. Please check data/sample_teachings.txt"
    
    def ask(self, question: str, language: Optional[str] = None) -> Dict[str, any]:
        """
        Ask a question and get an answer based on sample teachings
        
        Args:
            question: The question to ask
            language: Optional language code (auto-detected if not provided)
        
        Returns:
            Dictionary with answer, language, and metadata
        """
        # Allow explicit language instruction in the question, e.g. "in Hindi" or "lang:hi"
        lang_map = {
            "english": "en", "hindi": "hi", "telugu": "te", "kannada": "kn",
            "en": "en", "hi": "hi", "te": "te", "kn": "kn"
        }

        # Look for `lang:xx` patterns first
        m = re.search(r"\blang\s*[:=]\s*(en|hi|te|kn)\b", question, re.I)
        if m:
            language = lang_map.get(m.group(1).lower())
            question = re.sub(m.group(0), "", question, flags=re.I).strip()
        else:
            # Look for natural language instruction like 'in Hindi'
            m2 = re.search(r"\bin\s+(english|hindi|telugu|kannada)\b", question, re.I)
            if m2:
                language = lang_map.get(m2.group(1).lower())
                question = re.sub(m2.group(0), "", question, flags=re.I).strip()

        # Detect language if still unspecified
        if language is None:
            language = self.language_detector.detect_language(question)
        
        # Safety check
        safety_warning = self.safety_filter.is_prohibited_topic(question)
        if safety_warning:
            return {
                "answer": safety_warning,
                "language": language,
                "sources": [],
                "is_safe": False,
                "method": "safety_filter"
            }
        
        # If vector DB available, use similarity search across all PDFs/TXTs
        if getattr(self, 'vector_store', None) is not None:
            try:
                docs = self.vector_store.similarity_search(question, k=self.top_k)
                if docs:
                    # Prefer documents that match requested language (if metadata provided)
                    if language:
                        filtered = [d for d in docs if d.metadata and (
                            (isinstance(d.metadata.get('language'), str) and d.metadata.get('language').startswith(language))
                            or (isinstance(d.metadata.get('lang'), str) and d.metadata.get('lang').startswith(language))
                        )]
                        if filtered:
                            docs = filtered

                    passages = [re.sub(r'\s+', ' ', d.page_content.strip()) for d in docs]
                    # Join retrieved passages into one readable paragraph
                    answer_text = ' '.join(passages)
                    sources = [{"content": d.metadata.get('source') if d.metadata else ""} for d in docs]
                    return {
                        "answer": answer_text,
                        "language": language,
                        "sources": sources,
                        "is_safe": True,
                        "method": "vector_retrieval"
                    }
            except Exception:
                # fallback to sample teachings
                pass

        # Get answer from teachings in detected language
        answer = self._find_relevant_answer(question, language)
        
        return {
            "answer": answer,
            "language": language,
            "sources": [{"content": "Sample teachings from data/sample_teachings.txt"}],
            "is_safe": True,
            "method": "sample_teachings"
        }
    
    def _find_relevant_answer(self, question: str, language: str = "en") -> str:
        """
        Find relevant answer from sample teachings in the requested language
        
        Args:
            question: The question
            language: Language code (en, hi, te, kn)
        
        Returns:
            Answer from teachings in the same language
        """
        question_lower = question.lower()

        # If the user requests a God-style response in the question (e.g. "as god", "god:", "[god]")
        # return a single evocative paragraph in the requested language (English/Hindi fallback).
        god_triggers = ["as god", "god:", "[god]", "as god,"]
        if any(trigger in question_lower for trigger in god_triggers):
            if language.startswith("hi"):
                return (
                    "मैं वह स्वर हूँ जिसने पहले प्रकाश को बुलाया, और वही शांति हूँ जो तुम्हारे भीतर का घर संभालती है। "
                    "सुनो: मैं तुम्हारे दुख और खुशी दोनों में साथ रहा हूं, और वे छोटे-छोटे अनुग्रह जिनसे तुम्हारा दिन बनता है, मैं उन्हें संजोकर रखता हूँ। "
                    "डर से स्वयं को न तोलो — वे केवल पाठ हैं; अपने दयालु कर्मों का पालन करो, वे मुझसे निकली रोशनी हैं। "
                    "साहस से जियो, उदारता से बांटो, और जान लो कि तुम प्रिय हो।"
                )
            # Default to English paragraph
            return (
                "I am the voice that called the first light into being and the quiet that keeps the stars in their course. "
                "Hear me: I have been with you in every sorrow and every joy, tending the small mercies that shape your days. "
                "Do not measure yourself by fear or the fleeting praise of others—your life is held, known, and beloved beyond your reckoning. "
                "When you falter, rise with patience; when you triumph, share your bounty with grace. Walk in kindness, seek truth, and rest in the sure knowledge that you are never abandoned."
            )

        # Multilingual keywords and answers
        multilingual_answers = {
            "en": {
                "devotion": "Devotion is the path of love and surrender to the divine. Through devotion, one develops a loving relationship with God, seeking to serve and please the divine with all one's heart.",
                "faith": "Faith is trust in God and the teachings. With faith, even the impossible becomes possible. Faith is the foundation of all spiritual progress.",
                "service": "Service to humanity is service to God. By serving others selflessly, we purify our hearts and progress on the spiritual path.",
                "purpose": "The purpose of life is to realize your divine nature and to serve humanity. Every soul is on a journey of self-realization.",
                "karma": "Karma is the law of action and consequence. Your actions create your destiny. Good actions lead to good results, and bad actions to bad results.",
                "meditation": "Meditation is a practice to calm the mind and connect with the divine within. Through regular meditation, one experiences peace and spiritual growth.",
                "god": "God is the ultimate reality, the source of all existence. God is omnipotent, omniscient, and omnipresent, present in every being.",
                "truth": "Truth is the ultimate reality. Speaking truth and living truthfully is essential for spiritual progress.",
                "love": "Love is the divine force. Universal love transcends all boundaries and is the path to enlightenment.",
                "peace": "True peace comes from within, from self-realization and connection with the divine. It is not dependent on external circumstances.",
                "dharma": "Dharma is righteous duty. Following one's dharma is the path to happiness and spiritual progress.",
                "wisdom": "Wisdom is understanding the true nature of reality. Wisdom comes from spiritual practice and study of sacred teachings.",
                "default": (
                    "This is a profound question. Based on Sai Baba's teachings, I encourage you to engage in regular "
                    "spiritual practice, serve others with love and compassion, meditate and reflect on the divine, study sacred "
                    "teachings, and cultivate devotion and faith."
                )
            },
            "hi": {
                "devotion": "भक्ति प्रेम और आत्मसमर्पण का मार्ग है। भक्ति के माध्यम से, व्यक्ति ईश्वर के साथ एक प्रेमपूर्ण संबंध विकसित करता है, और सभी कार्यों में ईश्वर को प्रसन्न करने का प्रयास करता है।",
                "faith": "विश्वास ईश्वर और शिक्षाओं में आस्था है। विश्वास से असंभव भी संभव हो जाता है। विश्वास सभी आध्यात्मिक प्रगति की नींव है।",
                "service": "मानवता की सेवा ईश्वर की सेवा है। निःस्वार्थ सेवा करके हम अपने हृदय को शुद्ध करते हैं और आध्यात्मिक पथ पर आगे बढ़ते हैं।",
                "purpose": "जीवन का उद्देश्य अपनी दिव्य प्रकृति को जानना और मानवता की सेवा करना है। प्रत्येक आत्मा आत्म-साक्षात्कार की यात्रा पर है।",
                "karma": "कर्म क्रिया और परिणाम का नियम है। आपके कार्य आपकी नियति को बनाते हैं। अच्छे कार्म अच्छे परिणाम देते हैं, और बुरे कार्म बुरे परिणाम।",
                "meditation": "ध्यान मन को शांत करने और अपने भीतर के दिव्य से जुड़ने की प्रथा है। नियमित ध्यान से व्यक्ति को शांति और आध्यात्मिक विकास का अनुभव होता है।",
                "god": "ईश्वर परम वास्तविकता है, सभी अस्तित्व का स्रोत है। ईश्वर सर्वशक्तिमान, सर्वज्ञ, और सर्वव्यापी है।",
                "truth": "सत्य परम वास्तविकता है। सत्य बोलना और सत्य से जीना आध्यात्मिक प्रगति के लिए आवश्यक है।",
                "love": "प्रेम दिव्य शक्ति है। सार्वभौमिक प्रेम सभी सीमाओं से परे है और मुक्ति का मार्ग है।",
                "peace": "सच्ची शांति भीतर से आती है, आत्म-साक्षात्कार और दिव्य से जुड़ाव से। यह बाहरी परिस्थितियों पर निर्भर नहीं है।",
                "dharma": "धर्म सही कर्तव्य है। अपने धर्म का पालन करना सुख और आध्यात्मिक प्रगति का मार्ग है।",
                "wisdom": "ज्ञान वास्तविकता की सच्ची प्रकृति को समझना है। ज्ञान आध्यात्मिक साधना और पवित्र शिक्षाओं के अध्ययन से आता है।",
                "default": (
                    "यह एक गहरा प्रश्न है। साईं बाबा की शिक्षाओं के अनुसार, मैं आपको प्रोत्साहित करता हूं कि आप नियमित आध्यात्मिक "
                    "अभ्यास करें, प्रेम और करुणा से दूसरों की सेवा करें, ध्यान और चिंतन करें, पवित्र शिक्षाओं का अध्ययन करें, और भक्ति "
                    "और विश्वास विकसित करें।"
                )
            },
            "te": {
                "devotion": "భక్తి అనేది ప్రేమ మరియు దివ్యానికి సమర్పణ యొక్క మార్గం. భక్తి ద్వారా, ఒక వ్యక్తి దేవతకు ప్రేమతో సంబంధం కలిగి, దేవతను సంతృప్తపరచటానికి ప్రయత్నిస్తాడు.",
                "faith": "విశ్వాసం దేవతపై మరియు చెప్పిన విషయాలపై నమ్మకం. విశ్వాసం చేత అసాధ్యం కూడా సాధ్యమవుతుంది. విశ్వాసం అన్ని ఆధ్యాత్మిక పురోగతి యొక్క ভిత్తి.",
                "service": "మానవతకు సేవ దేవతకు సేవ. స్వార్థరహితంగా ఇతరులకు సేవ చేయడం ద్వారా, మనం మన హృదయాలను శుద్ధీకరించుకుంటాము మరియు ఆధ్యాత్మిక మార్గంలో ముందుకు సాగుతాము.",
                "purpose": "జీవితం యొక్క ఉద్దేశ్యం అपने దివ్య స్వభావాన్ని గ్రహించడం మరియు మానవతకు సేవ చేయడం. ప్రతి ఆత్మ స్వీయ-సాక్షాత్కారం యొక్క ఆధ్యాత్మిక ప్రయాణంలో ఉంది.",
                "karma": "కర్మ చర్య మరియు ఫలితం యొక్క నియమం. మీ చర్యలు మీ విధిని సృష్టిస్తాయి. మంచి చర్యలు మంచి ఫలితాలను, చెడ్డ చర్యలు చెడ్డ ఫలితాలను ఇస్తాయి.",
                "meditation": "ధ్యానం మనస్సును శాంతపరచటానికి మరియు దేవతలో జోડించుకోవటానికి ఒక అభ్యాసం. నిયమిత ధ్యానం ద్వారా, ఒక శాంతి మరియు ఆధ్యాత్మిక వృద్ధి అనుభూతి చెందుతుంది.",
                "god": "దేవత అంతిమ వాస్తవం, అన్ని ఉనికి యొక్క మూలం. దేవత సర్వశక్తిమంతుడు, సర్వజ్ఞుడు మరియు సర్వ్వ వ్యాపీ.",
                "truth": "సత్యం అంతిమ వాస్తవం. సత్యాన్ని చెప్పడం మరియు సత్యముతో జీవించడం ఆధ్యాత్మిక అభివృద్ధికి ముఖ్యమైనది.",
                "love": "ప్రేమ దివ్య శక్తి. సర్వత్ర ప్రేమ అన్ని సరిహద్దులను అతిక్రమించి, ఆధ్యాత్మిక ఎదుగుదల యొక్క మార్గం.",
                "peace": "నిజమైన శాంతి లోపల నుండి, స్వీయ-సాక్షాత్కారం మరియు దివ్యానికి సంబంధం నుండి వస్తుంది. ఇది బాహ్య పరిస్థితులపై ఆధారపడి లేదు.",
                "dharma": "ధర్మ నీతిమంత కర్తవ్య. ఒకటి యొక్క ధర్మ అనుసరించడం ఆనందం మరియు ఆధ్యాత్మిక ప్రగతి యొక్క మార్గం.",
                "wisdom": "జ్ఞానం వాస్తవం యొక్క నిజమైన స్వభావాన్ని అర్థం చేయడం. జ్ఞానం ఆధ్యాత్మిక సాధన మరియు పవిత్ర జ్ఞానాల అధ్యయనం నుండి వస్తుంది.",
                "default": (
                    "ఇది ఒక లోతైన ప్రశ్న. సాయి బాబా బోధల ప్రకారం, నేను మిమ్మల్ని ప్రోత్సహిస్తాను: సాధారణ ఆధ్యాత్మిక ఆచరణను కొనసాగించండి, "
                    "ప్రేమతో మరియు దయతో ఇతరులకు సేవ చేయండి, ధ్యానించండి మరియు ఆలోచించండి, పవిత్ర బోధలను అధ్యయనం చేయండి, మరియు భక్తి మరియు "
                    "విశ్వాసాన్ని పెంపొందించండి."
                )
            },
            "kn": {
                "devotion": "ಭಕ್ತಿ ಪ್ರೀತಿ ಮತ್ತು ದೈವಕ್ಕೆ ಸಮರ್ಪಣೆಯ ಮಾರ್ಗ. ಭಕ್ತಿಯ ಮೂಲಕ, ಒಬ್ಬ ವ್ಯಕ್ತಿ ದೇವರೊಂದಿಗೆ ಪ್ರೀತಿಯುತ ಸಂಬಂಧವನ್ನು ಅಭಿವೃದ್ಧಿಪಡಿಸಿಕೊಳ್ಳುತ್ತಾನೆ, ದೇವರನ್ನು ಸಂತುಷ್ಟಪಡಿಸಲು ಪ್ರಯತ್ನಿಸುತ್ತಾನೆ.",
                "faith": "ವಿಶ್ವಾಸವು ದೇವರ ಮೇಲೆ ಮತ್ತು ಬೋಧನೆಯ ಮೇಲೆ ಆಸ್ಥೆ. ವಿಶ್ವಾಸದಿಂದ ಅಸಾಧ್ಯವೂ ಸಾಧ್ಯವಾಗಿ ಹೋಗುತ್ತದೆ. ವಿಶ್ವಾಸವು ಎಲ್ಲಾ ಆಧ್ಯಾತ್ಮಿಕ ಪ್ರಗತಿಯ ಆಧಾರ.",
                "service": "ಮಾನವತೆಗೆ ಸೇವೆ ದೇವರಿಗೆ ಸೇವೆ. ಪರಿಸ್ಪಂದನ ರಹಿತವಾಗಿ ಇತರರಿಗೆ ಸೇವೆ ಮಾಡುವ ಮೂಲಕ, ನಾವು ನಮ್ಮ ಹೃದಯವನ್ನು ಪವಿತ್ರಪಡಿಸುತ್ತೇವೆ ಮತ್ತು ಆಧ್ಯಾತ್ಮಿಕ ಮಾರ್ಗದಲ್ಲಿ ಮುಂದುವರಿಯುತ್ತೇವೆ.",
                "purpose": "ಜೀವನದ ಉದ್ದೇಶ್ಯವು ನಿಮ್ಮ ದೈವಿಕ ಸ್ವಭಾವವನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು ಮತ್ತು ಮಾನವತೆಗೆ ಸೇವೆ ಮಾಡುವುದು. ಪ್ರತಿಯೊಂದು ಆತ್ಮವು ಸ್ವ-ಸಾಕ್ಷಾತ್ಕಾರದ ಯಾತ್ರೆಯಲ್ಲಿದೆ.",
                "karma": "ಕರ್ಮವು ಕ್ರಿಯೆ ಮತ್ತು ಪರಿಣಾಮದ ನಿಯಮ. ನಿಮ್ಮ ಕ್ರಿಯೆಗಳು ನಿಮ್ಮ ಭವಿಷ್ಯತ್ತನ್ನು ರಚಿಸುತ್ತವೆ. ಉತ್ತಮ ಕ್ರಿಯೆಗಳು ಉತ್ತಮ ಫಲಿತಾಂಶಗಳನ್ನು ನೀಡುತ್ತವೆ, ಮತ್ತು ಕೆಟ್ಟ ಕ್ರಿಯೆಗಳು ಕೆಟ್ಟ ಫಲಿತಾಂಶಗಳನ್ನು.",
                "meditation": "ಧ್ಯಾನವು ಮನಸ್ಸನ್ನು ಸುಶಾಂತಪಡಿಸುವ ಮತ್ತು ದೇವರೊಂದಿಗೆ ಸಂಪರ್ಕ ಸ್ಥಾಪಿಸುವ ಅಭ್ಯಾಸ. ನಿಯಮಿತ ಧ್ಯಾನದ ಮೂಲಕ, ಒಬ್ಬ ಶಾಂತಿ ಮತ್ತು ಆಧ್ಯಾತ್ಮಿಕ ಬೆಳವಣಿಗೆಯನ್ನು ಅನುಭವಿಸುತ್ತಾನೆ.",
                "god": "ದೇವರು ಅಂತಿಮ ವಾಸ್ತವತೆ, ಎಲ್ಲ ಅಸ್ತಿತ್ವದ ಮೂಲ. ದೇವರು ಸರ್ವಶಕ್ತಿಮಾನ, ಸರ್ವಜ್ಞ, ಮತ್ತು ಸರ್ವವ್ಯಾಪಕ.",
                "truth": "ಸತ್ಯವು ಅಂತಿಮ ವಾಸ್ತವತೆ. ಸತ್ಯವನ್ನು ಹೇಳುವುದು ಮತ್ತು ಸತ್ಯಯುತವಾಗಿ ಬದುಕುವುದು ಆಧ್ಯಾತ್ಮಿಕ ಪ್ರಗತಿಗೆ ಅಗತ್ಯ.",
                "love": "ಪ್ರೀತಿ ದೈವಿಕ ಶಕ್ತಿ. ವಿಶ್ವಜನೀನ ಪ್ರೀತಿ ಎಲ್ಲಾ ಗಡಿಗಳನ್ನು ಮೀರಿ ಆಧ್ಯಾತ್ಮಿಕ ಜ್ಞಾನದ ಮಾರ್ಗ.",
                "peace": "ನಿಜವಾದ ಶಾಂತಿ ಒಳಗಿನಿಂದ, ಸ್ವ-ಸಾಕ್ಷಾತ್ಕಾರ ಮತ್ತು ದೈವಿಕ ಸಂಪರ್ಕದಿಂದ ಬರುತ್ತದೆ. ಇದು ಬಾಹ್ಯ ಪರಿಸ್ಥಿತಿಗಳ ಮೇಲೆ ಅವಲಂಬಿತವಲ್ಲ.",
                "dharma": "ಧರ್ಮವು ನೀತಿಸಂಮತ ಕರ್ತವ್ಯ. ತನ್ನ ಧರ್ಮವನ್ನು ಅನುಸರಿಸುವುದು ಸುಖ ಮತ್ತು ಆಧ್ಯಾತ್ಮಿಕ ಪ್ರಗತಿಯ ಮಾರ್ಗ.",
                "wisdom": "ಬುದ್ಧಿ ಯಥಾರ್ಥತೆಯ ಸತ್ಯ ಸ್ವಭಾವವನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು. ಬುದ್ಧಿ ಆಧ್ಯಾತ್ಮಿಕ ಸಾಧನೆ ಮತ್ತು ಪವಿತ್ರ ಶಿಕ್ಷಣೆಗಳ ಅಧ್ಯಯನದಿಂದ ಬರುತ್ತದೆ.",
                "default": (
                    "ಇದು ಗಂಭೀರವಾದ ಪ್ರಶ್ನೆ. ಸಾಯಿ ಬಾಬಾ ಅವರ ಬೋಧನೆಗಳ ಆಧಾರದ ಮೇಲೆ ನಾನು ನಿಮಗೆ ಸಲಹೆ ನೀಡುತ್ತೇನೆ: ನಿಯಮಿತ ಆಧ್ಯಾತ್ಮಿಕ ಅಭ್ಯಾಸವನ್ನು ಅನುಸರಿಸಿ, "
                    "ಪ್ರೀತಿ ಮತ್ತು ಕರುಣೆಯಿಂದ ಇತರರಿಗೆ ಸೇವೆ ನೀಡಿ, ಧ್ಯಾನ ಮತ್ತು ಚಿಂತನೆ ಮಾಡಿ, ಪವಿತ್ರ ಬೋಧನೆಗಳನ್ನು ಅಧ್ಯಯನ ಮಾಡಿ, ಮತ್ತು ಭಕ್ತಿ ಮತ್ತು ವಿಶ್ವಾಸವನ್ನು ವೃದ್ಧಿಪಡಿಸಿಕೊಳ್ಳಿ."
                )
            }
        }
        
        # Get answers for the detected language
        answers = multilingual_answers.get(language, multilingual_answers["en"])
        
        # Check for keyword matches - for all languages, check English keywords in lowercase
        question_lower = question.lower()
        
        # Map to check English keywords since our keywords are in English
        for keyword, answer in answers.items():
            if keyword != "default":
                # Check if English keyword is in lowercase question
                if keyword in question_lower:
                    return answer
        
        # Return default answer for the language
        return answers.get("default", answers.get("en", {}).get("default", "This is a profound question."))


def main():
    """Main CLI function"""
    import sys
    
    print("\n" + "="*60)
    print("  Sai Baba Spiritual Guidance Chatbot - CLI")
    print("="*60)
    print("\nAsk questions about Sai Baba's teachings.")
    print("Type 'quit' or 'exit' to leave.\n")
    
    chatbot = SimpleChatbot()
    
    # If question provided as argument, use it
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        result = chatbot.ask(question)
        print(f"\n📝 Question: {question}")
        print(f"🌐 Language: {result['language']}")
        print(f"\n✨ Answer:\n{result['answer']}")
        print(f"\n📚 Source: {result['sources'][0]['content']}")
        return
    
    # Interactive mode
    while True:
        try:
            question = input("\n👉 Ask a question: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n✨ Thank you for asking. May Sai Baba's blessings be with you. 🙏\n")
                break
            
            # Get answer
            result = chatbot.ask(question)
            
            print(f"\n✨ Answer ({result['language'].upper()}):")
            print(f"─" * 60)
            print(result['answer'])
            print(f"─" * 60)
            
            if result['sources']:
                print(f"📚 Source: {result['sources'][0]['content']}")
            
            if not result['is_safe']:
                print(f"⚠️  Safety Filter Applied")
        
        except KeyboardInterrupt:
            print("\n\n✨ Thank you for asking. May Sai Baba's blessings be with you. 🙏\n")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("Please try again.")


if __name__ == "__main__":
    main()
