# Quick Start Guide

## Installation (5 minutes)

### 1. Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy and edit .env file
cp .env.example .env
notepad .env
```

**Add your API key:**
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Run Setup Verification
```bash
python setup.py
```

## Usage (3 steps)

### Step 1: Add Your Data
```
Place files in these folders:
├── data/           ← PDF and TXT files
└── audio/          ← MP3 or WAV files (optional)
```

### Step 2: Build Vector Database
```bash
# Process audio (if you have audio files)
python speech_to_text.py

# Build vector database
python ingest.py
```

### Step 3: Start API Server
```bash
python api.py
```

API is now running at: **http://localhost:8000**

## Testing

### Interactive API Documentation
Open in browser: http://localhost:8000/docs

### Test with CLI
```bash
python rag_engine.py
```

### Test with cURL
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is the importance of faith?\"}"
```

### Test with Python
```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "What is devotion?"}
)

print(response.json()["answer"])
```

## Common Issues

**Error: "No documents found"**
→ Add PDF/TXT files to `data/` folder

**Error: "API key not configured"**
→ Check `.env` file has correct API key

**Error: "Vector store not found"**
→ Run `python ingest.py` to build database

## File Descriptions

| File | Purpose |
|------|---------|
| `api.py` | FastAPI server (main entry point) |
| `rag_engine.py` | Question answering logic |
| `ingest.py` | Build vector database |
| `speech_to_text.py` | Convert audio to text |
| `config.py` | Configuration management |
| `setup.py` | Setup verification script |

## Next Steps

1. **Add more data**: The more content, the better the answers
2. **Tune settings**: Adjust `CHUNK_SIZE` and `TOP_K_RESULTS` in `.env`
3. **Deploy**: Use a cloud platform for production
4. **Build frontend**: Connect your UI to the API

## Support

- 📖 Full documentation: `README.md`
- 🔍 API docs: http://localhost:8000/docs
- 📝 Logs: Check `app.log` file
