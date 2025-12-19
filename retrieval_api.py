#!/usr/bin/env python3
"""
Minimal retrieval-only API that answers questions by returning relevant
passages from the existing FAISS vector DB (no LLM). Designed to be
lightweight and safe for local deployment.
"""

from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from loguru import logger

from config import settings
from ingest import DataIngestionPipeline
from ask import SimpleChatbot


app = FastAPI(title="Sai Baba — Retrieval Chatbot", version="0.1")


# Lazy-loaded pipeline and vector store
_pipeline: Optional[DataIngestionPipeline] = None
_vector_store = None
_rag_engine = None
_chatbot = None


def get_simple_chatbot() -> SimpleChatbot:
    global _chatbot
    if _chatbot is None:
        _chatbot = SimpleChatbot()
    return _chatbot


def get_pipeline() -> DataIngestionPipeline:
    global _pipeline
    if _pipeline is None:
        logger.info("Initializing data pipeline (embeddings will load)...")
        _pipeline = DataIngestionPipeline()
        logger.success("Pipeline initialized")
    return _pipeline


def get_vector_store():
    global _vector_store
    if _vector_store is None:
        pipeline = get_pipeline()
        _vector_store = pipeline.load_vector_store()
    return _vector_store


def get_rag_engine():
    """Lazily initialize the MultilingualRAGEngine if LLM mode is enabled."""
    global _rag_engine
    if not settings.use_llm:
        return None
    if _rag_engine is None:
        try:
            # Import here to avoid heavy imports at module import time
            from rag_engine import MultilingualRAGEngine
            logger.info("Initializing RAG engine (LLM)...")
            _rag_engine = MultilingualRAGEngine()
            logger.success("RAG engine initialized")
        except Exception as e:
            logger.error(f"Failed to initialize RAG engine: {e}")
            _rag_engine = None
    return _rag_engine


class QuestionRequest(BaseModel):
    question: str
    language: Optional[str] = None


class SourceItem(BaseModel):
    excerpt: str
    metadata: Dict[str, object]


class AnswerResponse(BaseModel):
    answer: str
    language: str
    sources: List[SourceItem]


@app.get("/health")
def health():
    vs = get_vector_store()
    return {
        "status": "healthy" if vs is not None else "vector_db_missing",
        "engine": "retrieval-only",
        "vector_db_present": vs is not None,
        "vector_db_path": settings.vector_db_path,
    }


@app.post("/ask", response_model=AnswerResponse)
def ask(request: QuestionRequest):
    q = (request.question or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    vs = get_vector_store()
    if settings.use_llm:
        # Try RAG+LLM path first when enabled
        rag = get_rag_engine()
        if rag is not None:
            try:
                result = rag.answer_question(q, request.language)
                answer = result.get("answer", "")
                language = result.get("language", request.language or settings.default_language)
                sources_raw = result.get("sources", [])
                sources = []
                for s in sources_raw:
                    content = s.get("content") or s.get("excerpt") or ""
                    excerpt = (content[:400] + "...") if len(content) > 400 else content
                    meta = s.get("metadata") or {}
                    safe_meta = {k: str(v) for k, v in meta.items()}
                    sources.append(SourceItem(excerpt=excerpt, metadata=safe_meta))
                return AnswerResponse(answer=answer, language=language, sources=sources)
            except Exception as e:
                logger.error(f"RAG engine failed to answer: {e}. Falling back to retrieval-only.")
                # fall through to retrieval-only

    if vs is None:
        raise HTTPException(
            status_code=500,
            detail=(
                "Vector DB not found. Run `python ingest.py --rebuild` to build it "
                "from your data in the `data/` folder."
            ),
        )

    try:
        docs = vs.similarity_search(q, k=settings.top_k_results)
    except Exception as e:
        logger.error(f"Error during similarity search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    if not docs:
        no_info = {
            "en": "This guidance is not available in the provided documents.",
            "hi": "यह मार्गदर्शन दिए गए दस्तावेज़ों में उपलब्ध नहीं है।",
        }
        answer = no_info.get(request.language or settings.default_language, no_info["en"])
        return AnswerResponse(answer=answer, language=request.language or settings.default_language, sources=[])

    # Compose answer as concatenation of retrieved passages (you can change formatting)
    passages = [d.page_content.strip() for d in docs]
    answer_text = "\n\n---\n\n".join(passages)

    sources = []
    for d in docs:
        excerpt = (d.page_content[:400] + "...") if len(d.page_content) > 400 else d.page_content
        # Coerce metadata values to simple types (strings) for JSON/Pydantic safety
        raw_meta = d.metadata or {}
        safe_meta = {k: str(v) for k, v in raw_meta.items()}
        sources.append(SourceItem(excerpt=excerpt, metadata=safe_meta))

    return AnswerResponse(answer=answer_text, language=request.language or settings.default_language, sources=sources)


@app.post("/ask_simple", response_model=AnswerResponse)
def ask_simple(request: QuestionRequest):
    """Return a concise multilingual answer using the simple chatbot (no vector DB / LLM)."""
    q = (request.question or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    chatbot = get_simple_chatbot()
    try:
        result = chatbot.ask(q, request.language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Map SimpleChatbot result into AnswerResponse
    sources = []
    for s in result.get("sources", []):
        content = s.get("content") if isinstance(s, dict) else str(s)
        excerpt = content if len(content) <= 400 else content[:400] + "..."
        sources.append(SourceItem(excerpt=excerpt, metadata={}))

    return AnswerResponse(answer=result.get("answer", ""), language=result.get("language", settings.default_language), sources=sources)


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", settings.api_port))
    uvicorn.run(app, host=settings.api_host, port=port)
