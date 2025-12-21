"""
FastAPI server for Sai Baba multilingual spiritual guidance chatbot.
Supports English, Hindi, Telugu, and Kannada with automatic language detection.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from contextlib import asynccontextmanager
import uvicorn
from loguru import logger
import re

from config import settings
from rag_engine import MultilingualRAGEngine


# Pydantic models for API
class QuestionRequest(BaseModel):
    """Request model for asking questions."""
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="The spiritual question to ask",
        examples=["What is the importance of faith in spiritual life?"]
    )


class SourceInfo(BaseModel):
    """Model for source document information."""
    content: str = Field(description="Excerpt from source document")
    metadata: Dict = Field(description="Document metadata")


class AnswerResponse(BaseModel):
    """Simplified response model required by deployment spec."""
    answer: str = Field(description="The spiritual guidance answer, 1-2 paragraphs")
    sources: List[str] = Field(description="List of source document names or teaching references")
    is_safe: bool = Field(description="Whether the question passed safety checks")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(description="System health status")
    version: str = Field(description="API version")
    vector_store_size: Optional[int] = Field(
        default=None,
        description="Number of vectors in the database"
    )
    llm_provider: Optional[str] = Field(
        default=None,
        description="AI provider being used"
    )


class ErrorResponse(BaseModel):
    """Response model for errors."""
    error: str = Field(description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")


# Global Multilingual RAG engine instance
rag_engine: Optional[MultilingualRAGEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    global rag_engine
    logger.info("Starting Sai Baba Multilingual Guidance API server...")
    
    try:
        # Validate configuration
        settings.validate_config()
        
        # Initialize Multilingual RAG engine
        logger.info("Initializing Multilingual RAG engine...")
        rag_engine = MultilingualRAGEngine()

        # Check whether a persisted vector DB exists (do NOT build here)
        from pathlib import Path
        vec_path = Path(settings.vector_db_path)
        has_vectors = any(vec_path.iterdir()) if vec_path.exists() else False
        if not has_vectors or getattr(rag_engine, 'vector_store', None) is None:
            logger.warning("Vector DB not found. Please run ingest.py to build the vector database before using retrieval features.")
        else:
            logger.info("Vector DB loaded and ready to serve retrieval queries.")

        # Validate system (do not fail startup on degraded status)
        validation = rag_engine.validate_system()
        if validation.get("status") != "healthy":
            logger.warning(f"RAG system validation returned non-healthy status: {validation}")
        else:
            logger.success("RAG system healthy")
            logger.info(f"Vector store size: {validation.get('vector_store_size')} vectors")
            logger.info(f"LLM provider: {validation.get('llm_provider')}")
            logger.info(f"Supported languages: {', '.join(settings.supported_languages)}")
        
    except Exception as e:
        logger.error(f"Failed to start API server: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down API server...")


# Initialize FastAPI app
app = FastAPI(
    title="Sai Baba Multilingual Spiritual Guidance API",
    description=(
        "RESTful API for multilingual spiritual guidance based on Sai Baba's teachings. "
        "Uses Retrieval-Augmented Generation (RAG) to provide authentic, "
        "contextual answers in English, Hindi, Telugu, and Kannada. "
        "Automatically detects question language and responds accordingly."
    ),
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Endpoints

@app.get(
    "/",
    response_model=Dict[str, str],
    summary="Root endpoint",
    description="Welcome message and API information"
)
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "Welcome to Sai Baba Multilingual Spiritual Guidance API",
        "version": "2.0.0",
        "supported_languages": ["English", "Hindi", "Telugu", "Kannada"],
        "documentation": "/docs",
        "health": "/health"
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check the health status of the API and RAG system"
)
async def health_check():
    """
    Health check endpoint to verify system status.
    
    Returns system health information including:
    - Overall status
    - API version
    - Vector store size
    - LLM provider
    """
    try:
        if rag_engine is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="RAG engine not initialized"
            )
        
        validation = rag_engine.validate_system()
        
        return HealthResponse(
            status=validation.get("status", "unknown"),
            version="1.0.0",
            vector_store_size=validation.get("vector_store_size"),
            llm_provider=validation.get("llm_provider")
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Health check failed: {str(e)}"
        )


@app.post(
    "/ask",
    response_model=AnswerResponse,
    summary="Ask a spiritual question in any supported language",
    description="Submit a question in English, Hindi, Telugu, or Kannada and receive guidance based on Sai Baba's teachings",
    responses={
        200: {
            "description": "Successful response with spiritual guidance",
            "content": {
                "application/json": {
                    "example": {
                        "answer": "According to Sai Baba's teachings, faith is the foundation of spiritual life...",
                        "language": "en",
                        "sources": [
                            {
                                "content": "Faith is the foundation upon which spiritual life is built...",
                                "metadata": {"source": "teachings.pdf", "page": 42}
                            }
                        ],
                        "is_safe": True,
                        "disclaimer": "This guidance is based on Sai Baba's teachings. For personal spiritual matters, consider seeking guidance from qualified spiritual teachers."
                    }
                }
            }
        },
        400: {"description": "Invalid request"},
        503: {"description": "Service unavailable"}
    }
)
async def ask_question(request: QuestionRequest):
    """
    Answer a spiritual question using multilingual RAG.
    
    The system will:
    1. Auto-detect the language of your question
    2. Search relevant teachings from Sai Baba's works (all languages)
    3. Generate a contextual answer in the same language
    4. Apply ethical guardrails
    
    **Supported Languages:**
    - English (en)
    - Hindi (hi)
    - Telugu (te)
    - Kannada (kn)
    
    **Important Disclaimers:**
    - This API provides spiritual guidance only
    - Not for medical, legal, or predictive advice
    - Answers are based on available texts
    - Consult qualified teachers for personal matters
    """
    try:
        if rag_engine is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="RAG engine not initialized"
            )
        
        logger.info(f"Received question: {request.question[:100]}...")
        
        # If vector DB is not initialized, return a graceful message (do not attempt ingestion)
        if getattr(rag_engine, 'vector_store', None) is None:
            msg = "Knowledge base is not initialized yet. Please run ingest.py to build the knowledge base."
            return AnswerResponse(answer=msg, sources=["vector_db not initialized"], is_safe=False)

        # Get answer from multilingual RAG engine
        result = rag_engine.answer_question(request.question)
        
        # Build simplified response: extract source names if available
        sources = []
        for s in result.get("sources", []):
            meta = s.get("metadata") if isinstance(s, dict) else None
            if meta and isinstance(meta, dict):
                src = meta.get("source") or meta.get("file") or meta.get("source_name")
            else:
                # fall back to any content hint
                src = s.get("content")[:120] if isinstance(s, dict) and s.get("content") else str(s)
            if src:
                sources.append(src)

        if not sources:
            sources = ["Teachings and guidance"]

        answer = result.get("answer", "")
        answer = re.sub(r"\s+", " ", answer).strip()

        response = AnswerResponse(
            answer=answer,
            sources=sources,
            is_safe=result.get("is_safe", True)
        )

        detected_lang = result.get("language", "en")
        logger.success(f"Question answered successfully in {detected_lang}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )


@app.get(
    "/disclaimer",
    response_model=Dict[str, str],
    summary="Get full disclaimer",
    description="Retrieve complete disclaimer and ethical guidelines"
)
async def get_disclaimer():
    """
    Get the full disclaimer and ethical guidelines for using this API.
    
    Returns detailed information about:
    - Limitations of the service
    - What the API does NOT provide
    - Recommended usage guidelines
    - Safety and ethical considerations
    """
    return {
        "disclaimer": (
            "Sai Baba Spiritual Guidance API Disclaimer:\n\n"
            "1. SPIRITUAL GUIDANCE ONLY: This API provides spiritual guidance based on "
            "Sai Baba's teachings. It is not a substitute for personal spiritual practice "
            "or guidance from qualified teachers.\n\n"
            "2. NO MEDICAL ADVICE: This API does not provide medical advice, diagnosis, "
            "or treatment recommendations. Consult healthcare professionals for health matters.\n\n"
            "3. NO LEGAL ADVICE: This API does not provide legal advice or counsel. "
            "Consult legal professionals for legal matters.\n\n"
            "4. NO PREDICTIONS: This API does not predict the future or provide fortune-telling. "
            "It shares timeless wisdom for present guidance.\n\n"
            "5. NOT DIVINE: This API and its creators do not claim divine authority. "
            "We are humble servants sharing Sai Baba's teachings.\n\n"
            "6. ACCURACY DISCLAIMER: While we strive for accuracy, answers are based on "
            "available texts and AI interpretation. Always refer to original sources.\n\n"
            "7. PERSONAL RESPONSIBILITY: Users are responsible for how they apply this guidance. "
            "Use wisdom and discernment in your spiritual journey.\n\n"
            "By using this API, you acknowledge and accept these terms."
        ),
        "contact": "For concerns or feedback, please contact the system administrator.",
        "last_updated": "2025-12-07"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc) if settings.log_level == "DEBUG" else None
        ).dict()
    )


def main():
    """Main entry point for running the API server."""
    logger.info(f"Starting server on {settings.api_host}:{settings.api_port}")
    
    uvicorn.run(
        "api:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    main()
