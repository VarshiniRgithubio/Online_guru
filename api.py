from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import threading

app = FastAPI(title="Sai Baba Guidance Chatbot")

rag_engine = None
rag_lock = threading.Lock()


class QuestionRequest(BaseModel):
    question: str

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


@app.post("/ask")
def ask(req: QuestionRequest):
    global rag_engine

    if rag_engine is None:
        with rag_lock:
            if rag_engine is None:
                from rag_engine import MultilingualRAGEngine
                rag_engine = MultilingualRAGEngine()

    try:
        result = rag_engine.answer_question(req.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
