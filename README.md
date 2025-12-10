# Sai Baba Spiritual Guidance Chatbot - Backend

A production-ready Python backend for a Sai Baba spiritual guidance chatbot using Retrieval-Augmented Generation (RAG). This system provides API-based spiritual guidance derived from authentic teachings, with built-in safety and ethical guardrails.

## Features

- **RAG-Based Question Answering**: Uses LangChain and FAISS for intelligent retrieval
- **Multi-Format Input**: Supports PDF books, TXT files, and audio speeches
- **Audio Transcription**: Automatic speech-to-text using Whisper
- **Safety Guardrails**: Built-in filters for medical, legal, and predictive questions
- **API-First Design**: RESTful API built with FastAPI
- **Flexible AI Backend**: Supports both OpenAI and Google Gemini
- **Production Ready**: Complete error handling, logging, and monitoring

## System Architecture

```
┌─────────────────┐
│   Data Sources  │
│  (PDF/TXT/Audio)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Speech-to-Text  │ ◄── Whisper Model
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Ingestion │
│   (ingest.py)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Vector Store   │ ◄── FAISS + Embeddings
│   (Persistent)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   RAG Engine    │ ◄── LangChain + LLM
│ (rag_engine.py) │     (OpenAI/Gemini)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │
│   (api.py)      │
└────────┬────────┘
         │
         ▼
    Frontend/Client
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- (Optional) CUDA-capable GPU for faster audio processing

### Setup

1. **Clone or create the project directory:**
```bash
cd "f:\online guru"
```

2. **Create a virtual environment:**
```bash
python -m venv venv
```

3. **Activate the virtual environment:**
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows Command Prompt
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Configure environment variables:**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys
```

### Environment Configuration

Edit `.env` file with your settings:

```env
# Choose AI provider: openai or gemini
AI_PROVIDER=openai

# Add your API key
OPENAI_API_KEY=your_openai_api_key_here
# OR
GOOGLE_API_KEY=your_google_api_key_here

# Model settings (default values are production-ready)
MODEL_TEMPERATURE=0.3
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

## Usage

### 1. Prepare Your Data

Create the following folder structure:

```
online guru/
├── data/           # Place PDF and TXT files here
├── audio/          # Place MP3/WAV audio files here
├── transcripts/    # Auto-generated transcripts will be saved here
└── vector_db/      # Auto-generated vector database
```

### 2. Convert Audio to Text (Optional)

If you have audio speeches:

```bash
python speech_to_text.py
```

This will:
- Process all audio files in the `audio/` folder
- Transcribe using Whisper
- Clean the transcripts
- Save to `transcripts/` folder

**Process a single file:**
```bash
python speech_to_text.py path/to/audio.mp3
```

### 3. Build the Vector Database

```bash
python ingest.py
```

This will:
- Load all PDF and TXT files from `data/` folder
- Load all transcripts from `transcripts/` folder
- Chunk the documents (500 chars, 50 overlap)
- Create embeddings using sentence-transformers
- Build and persist FAISS vector database

**Force rebuild:**
```bash
python ingest.py --rebuild
```

### 4. Test the RAG Engine

```bash
python rag_engine.py
```

Interactive CLI for testing questions and answers.

### 5. Start the API Server

```bash
python api.py
```

The API will be available at:
- Main API: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## API Endpoints

### POST /ask

Ask a spiritual question.

**Request:**
```json
{
  "question": "What is the importance of faith?"
}
```

**Response:**
```json
{
  "answer": "According to Sai Baba's teachings, faith is...",
  "sources": [
    {
      "content": "Excerpt from source document...",
      "metadata": {"source": "teachings.pdf", "page": 42}
    }
  ],
  "is_safe": true,
  "disclaimer": "This guidance is based on Sai Baba's teachings..."
}
```

### GET /health

Check system health.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "vector_store_size": 1523,
  "llm_provider": "openai"
}
```

### GET /disclaimer

Get full disclaimer and ethical guidelines.

## Safety Features

The system implements multiple safety layers:

### 1. Topic Filtering
- **Medical**: Rejects health/medical advice questions
- **Legal**: Rejects legal advice questions  
- **Predictive**: Rejects fortune-telling/future prediction

### 2. Response Sanitization
- Removes divine claims from responses
- Ensures humble, devotional tone
- Adds disclaimers where appropriate

### 3. Context Validation
- Only answers from available teachings
- Acknowledges when information is unavailable
- Maintains authenticity to source material

### 4. Rate Limiting (Production)
Consider adding rate limiting middleware for production deployment.

## Project Structure

```
online guru/
├── api.py                  # FastAPI server
├── rag_engine.py          # RAG question-answering engine
├── ingest.py              # Vector database builder
├── speech_to_text.py      # Audio transcription module
├── config.py              # Configuration management
├── logger_config.py       # Logging setup
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── data/                 # Input documents (create this)
├── audio/                # Input audio files (create this)
├── transcripts/          # Generated transcripts
└── vector_db/            # FAISS vector database
```

## Configuration Options

All settings can be configured via `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `AI_PROVIDER` | `openai` | AI provider: `openai` or `gemini` |
| `OPENAI_API_KEY` | - | OpenAI API key |
| `GOOGLE_API_KEY` | - | Google API key |
| `MODEL_TEMPERATURE` | `0.3` | LLM temperature (0.0-1.0) |
| `CHUNK_SIZE` | `500` | Document chunk size |
| `CHUNK_OVERLAP` | `50` | Chunk overlap size |
| `TOP_K_RESULTS` | `4` | Number of documents to retrieve |
| `API_HOST` | `0.0.0.0` | API server host |
| `API_PORT` | `8000` | API server port |
| `LOG_LEVEL` | `INFO` | Logging level |

## Troubleshooting

### Error: "No documents found"
- Ensure PDF/TXT files are in the `data/` folder
- Check file permissions
- Run `python ingest.py` to rebuild

### Error: "API key not configured"
- Check `.env` file exists
- Verify API key is set correctly
- Restart the API server

### Error: "Vector store not found"
- Run `python ingest.py` to build the database
- Check `vector_db/` folder exists

### Slow audio transcription
- Use smaller Whisper model: `tiny` or `base`
- Consider using GPU if available
- Process fewer files at once

## Development

### Adding New Features

1. **Custom Embeddings**: Modify `_load_embeddings()` in `ingest.py`
2. **Different LLM**: Add provider in `_initialize_llm()` in `rag_engine.py`
3. **New Endpoints**: Add routes in `api.py`

### Testing

```bash
# Test individual modules
python speech_to_text.py
python ingest.py
python rag_engine.py

# Test API
python api.py
# Visit http://localhost:8000/docs for interactive testing
```

## Production Deployment

### Docker (Recommended)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "api.py"]
```

Build and run:
```bash
docker build -t sai-baba-api .
docker run -p 8000:8000 --env-file .env sai-baba-api
```

### Security Considerations

1. **API Keys**: Use environment variables, never commit to git
2. **CORS**: Configure specific origins in production
3. **Rate Limiting**: Add rate limiting middleware
4. **HTTPS**: Use reverse proxy (nginx) with SSL
5. **Authentication**: Consider adding API authentication

## Ethical Guidelines

This system is designed with strict ethical principles:

1. **Humility**: Never claims divine authority
2. **Safety**: Refuses harmful advice categories
3. **Authenticity**: Only shares from available teachings
4. **Responsibility**: Includes clear disclaimers
5. **Transparency**: Open about limitations

## License

This project is for educational and spiritual guidance purposes. Please use responsibly and ethically.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs in `app.log`
3. Test individual modules
4. Contact system administrator

## Acknowledgments

- Sai Baba's teachings and devotees
- OpenAI Whisper for speech recognition
- LangChain for RAG framework
- FastAPI for API framework
- Sentence Transformers for embeddings

---

**Disclaimer**: This system provides spiritual guidance based on available teachings. It is not a substitute for personal spiritual practice, qualified teachers, or professional advice in medical, legal, or other specialized domains.
