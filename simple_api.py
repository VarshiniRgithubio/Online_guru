#!/usr/bin/env python3
"""
Simple REST API for asking questions - runs on http://localhost:8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from loguru import logger
from ask import SimpleChatbot

# Initialize FastAPI app
app = FastAPI(
    title="Sai Baba Guidance Chatbot",
    description="Ask questions about Sai Baba's spiritual teachings",
    version="1.0.0"
)

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in production use specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot
chatbot = SimpleChatbot()

# Configure logging to be minimal
logger.remove()


class QuestionRequest(BaseModel):
    """Request model for asking questions"""
    question: str
    language: Optional[str] = None


class AnswerResponse(BaseModel):
    """Response model for answers"""
    answer: str
    language: str
    sources: List[Dict[str, str]]
    is_safe: bool


@app.get("/", tags=["Info"])
def root():
    """Welcome message"""
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


@app.get("/health", tags=["Info"])
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Sai Baba Guidance Chatbot",
        "version": "1.0.0"
    }


@app.post("/ask", response_model=AnswerResponse, tags=["Chat"])
def ask_question(request: QuestionRequest):
    """
    Ask a question about Sai Baba's teachings
    
    **Parameters:**
    - `question` (required): Your question
    - `language` (optional): Language code (en, hi, te, kn). Auto-detected if not provided.
    
    **Response:**
    - `answer`: The answer to your question
    - `language`: Language of the response
    - `sources`: Source references
    - `is_safe`: Whether the response passed safety checks
    """
    try:
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        result = chatbot.ask(request.question, request.language)
        return AnswerResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ask", response_model=AnswerResponse, tags=["Chat"])
def ask_question_get(question: str, language: Optional[str] = None):
    """
    Ask a question via GET request
    
    **Parameters:**
    - `question` (required): Your question
    - `language` (optional): Language code (en, hi, te, kn). Auto-detected if not provided.
    
    **Examples:**
    - `/ask?question=What%20is%20devotion?`
    - `/ask?question=What%20is%20faith?&language=en`
    """
    try:
        if not question or not question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        result = chatbot.ask(question, language)
        return AnswerResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/languages", tags=["Info"])
def get_supported_languages():
    """Get list of supported languages"""
    return {
        "supported_languages": [
            {"code": "en", "name": "English"},
            {"code": "hi", "name": "Hindi (हिंदी)"},
            {"code": "te", "name": "Telugu (తెలుగు)"},
            {"code": "kn", "name": "Kannada (ಕನ್ನಡ)"}
        ],
        "auto_detection": "If language is not specified, it will be automatically detected"
    }


# API Examples
"""
USAGE EXAMPLES:

1. **Via Browser (Simplest):**
   - Start server: python simple_api.py
   - Open: http://localhost:8000/docs
   - Click on /ask endpoint
   - Enter question and click Execute

2. **Via PowerShell:**
   $body = @{
       question = "What is devotion?"
       language = "en"
   } | ConvertTo-Json
   
   Invoke-WebRequest -Uri "http://localhost:8000/ask" `
     -Method POST `
     -Headers @{"Content-Type"="application/json"} `
     -Body $body

3. **Via Python:**
   import requests
   
   response = requests.post(
       "http://localhost:8000/ask",
       json={"question": "What is devotion?", "language": "en"}
   )
   print(response.json())

4. **Via cURL:**
   curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What is devotion?"}'

5. **Via GET URL:**
   http://localhost:8000/ask?question=What+is+devotion?

6. **Via CLI (No server needed):**
   python ask.py "What is devotion?"
"""


if __name__ == "__main__":
    import uvicorn
    import os
    
    print("\n" + "="*60)
    print("  Sai Baba Guidance Chatbot API")
    print("="*60)
    print("\nStarting server...")
    print("API running on: http://localhost:8000")
    print("Interactive docs: http://localhost:8000/docs")
    print("API examples: http://localhost:8000/")
    print("\n" + "="*60 + "\n")
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
