from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import threading

app = FastAPI(title="Sai Baba Guidance Chatbot")

rag_engine = None
rag_lock = threading.Lock()


class QuestionRequest(BaseModel):
    question: str


class Source(BaseModel):
    content: str
    metadata: Optional[dict] = None


class AnswerResponse(BaseModel):
    answer: str
    language: str
    sources: List[Source]
    is_safe: bool


@app.get("/")
def root():
    return {
        "message": "Welcome to Sai Baba Guidance Chatbot",
        "endpoints": {
            "ask": "/ask (POST)",
            "ask_get": "/ask?question=... (GET)",
            "docs": "/docs (Interactive API docs)",
            "health": "/health"
        },
        "example": {
            "question": "What is devotion?",
            "language": "en"
        }
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
def ask(req: QuestionRequest):
    global rag_engine

    # Preserve existing lazy-loading and thread-safety behavior
    if rag_engine is None:
        with rag_lock:
            if rag_engine is None:
                from rag_engine import MultilingualRAGEngine
                rag_engine = MultilingualRAGEngine()

    try:
        result = rag_engine.answer_question(req.question)
        # FastAPI will validate/serialize the response according to AnswerResponse
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
