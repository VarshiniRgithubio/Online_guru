# 🌍 Sai Baba Multilingual Spiritual Guidance Chatbot - Complete Backend

## Project Overview

A **production-ready multilingual Python backend** for a Sai Baba spiritual guidance chatbot using **Retrieval-Augmented Generation (RAG)**. Built to serve **English, Hindi, Telugu, and Kannada** speakers with automatic language detection and cross-lingual semantic search.

---

## ✨ Core Features

### 🌐 Multilingual Support
- **4 Languages**: English, Hindi (हिंदी), Telugu (తెలుగు), Kannada (ಕನ್ನಡ)
- **Auto Language Detection**: Automatically detects question language
- **Cross-Lingual Search**: Search across all 4 languages simultaneously
- **Language-Matched Responses**: Answer in the same language as the question
- **UTF-8 Safe**: Proper handling of Indic scripts (Devanagari, Telugu, Kannada)

### 🎯 Key Capabilities
- ✅ Multilingual Audio Transcription (Whisper)
- ✅ Cross-lingual Semantic Search (Multilingual Embeddings)
- ✅ Intelligent Question Answering (RAG with LangChain)
- ✅ Safety Guardrails (Medical/Legal/Predictive filtering)
- ✅ RESTful API (FastAPI with full multilingual support)
- ✅ Flexible AI Backend (OpenAI GPT-4 or Google Gemini)

---

## 📁 Complete File Structure

```
online guru/
├── Core Application
│   ├── api.py                         # FastAPI server (multilingual)
│   ├── rag_engine.py                  # Multilingual RAG engine
│   ├── ingest.py                      # Vector DB builder
│   ├── speech_to_text.py              # Multilingual audio transcription
│   ├── language_utils.py              # Language detection & handling
│   ├── config.py                      # Configuration management
│   ├── logger_config.py               # Logging setup
│   └── utils.py                       # Utility functions
│
├── Configuration
│   ├── requirements.txt               # Python dependencies
│   ├── .env.example                   # Environment template
│   └── .gitignore                     # Git ignore rules
│
├── Setup & Documentation
│   ├── setup.py                       # Setup verification script
│   ├── README_MULTILINGUAL.md         # Full multilingual documentation
│   ├── QUICKSTART_MULTILINGUAL.md     # Quick start (all languages)
│   ├── API_EXAMPLES.md                # API usage examples
│   └── README.md                      # Original English docs
│
└── Data Directories (created automatically)
    ├── data/                          # Input documents (all languages)
    ├── audio/                         # Input audio files
    └── vector_db/                     # Persistent vector database
```

---
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure
cp .env.example .env

---

## 📋 Complete Workflow

### Step 1: Add Multilingual Data

Place your content in the appropriate folders:
audio/          ← Audio speeches (.mp3, .wav) in any language

### Step 2: Process Audio (Optional)

```powershell
python speech_to_text.py
```

**What it does:**
- Auto-detects language of each audio file
- Transcribes using Whisper in original language
- Cleans transcripts (removes timestamps, fillers)
- Saves UTF-8 encoded .txt files to `data/` folder
- Shows language distribution report

### Step 3: Build Vector Database

```powershell
python ingest.py
```

**What it does:**
- Uses multilingual embeddings (paraphrase-multilingual-MiniLM-L12-v2)
- Chunks documents (500 chars, 50 overlap)
- Creates FAISS vector store for cross-lingual search
- Persists to `vector_db/` folder

**Access:**
---

  -d "{\"question\": \"What is the importance of faith?\"}"

**Response:**
```json
{
  "answer": "According to Sai Baba's teachings, faith is the foundation...",
  "language": "en",
  "sources": [...],
  "is_safe": true,
  "disclaimer": "This guidance is based on Sai Baba's teachings..."
}
```

### Example 2: Hindi Question (हिंदी)

**Request:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"विश्वास का महत्व क्या है?\"}"
```

**Response:**
```json
{
  "answer": "साईं बाबा की शिक्षाओं के अनुसार, विश्वास आधारशिला है...",
  "language": "hi",
  "sources": [...],
  "is_safe": true,
  "disclaimer": "यह मार्गदर्शन साईं बाबा की शिक्षाओं पर आधारित है..."
}
```

### Example 3: Telugu Question (తెలుగు)

**Request:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"విశ్వాసం యొక్క ప్రాముఖ్యత ఏమిటి?\"}"
```
**Response:**
```json
{
  "answer": "సాయి బాబా బోధల ప్రకారం, విశ్వాసం పునాది...",
  "language": "te",
  "sources": [...],
  "is_safe": true,
  "disclaimer": "ఈ మార్గదర్శకత్వం సాయి బాబా బోధలపై ఆధారపడి ఉంది..."
}
```

### Example 4: Kannada Question (ಕನ್ನಡ)

**Request:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"ನಂಬಿಕೆಯ ಮಹತ್ವ ಏನು?\"}"
```

**Response:**
```json
{
  "answer": "ಸಾಯಿಬಾಬಾ ಅವರ ಬೋಧನೆಗಳ ಪ್ರಕಾರ, ನಂಬಿಕೆ ಅಡಿಪಾಯ...",
  "language": "kn",
  "sources": [...],
  "is_safe": true,
  "disclaimer": "ಈ ಮಾರ್ಗದರ್ಶನವು ಸಾಯಿಬಾಬಾ ಅವರ ಬೋಧನೆಗಳ ಮೇಲೆ ಆಧಾರಿತವಾಗಿದೆ..."
}
```


## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────┐
│            Multilingual Input Layer                │
│  PDF (EN/HI/TE/KN) + TXT + Audio (4 languages)    │
└──────────────────┬─────────────────────────────────┘
                   │
                   ▼
│         Speech-to-Text Layer (Whisper)            │
│  • Auto language detection                         │
│  • Multilingual transcription                      │
│  • UTF-8 encoding                                  │
└──────────────────┬─────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────┐
│            Data Processing Layer                   │
│  • Clean transcripts                               │
│  • Chunk documents (500/50)                        │
│  • UTF-8 safe loading                              │
└──────────────────┬─────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────┐
│         Multilingual Embedding Layer               │
│  Model: paraphrase-multilingual-MiniLM-L12-v2     │
│  • Supports 50+ languages                          │
│  • Semantic similarity across languages            │
└──────────────────┬─────────────────────────────────┘
                   │
                   ▼
│          Vector Database (FAISS)                   │
│  • Cross-lingual semantic search                   │
│  • Persistent storage                              │
│  • Fast retrieval                                  │
└──────────────────┬─────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────┐
│        Language Detection Layer                    │
│  • Auto-detect question language                   │
│  • Fallback to default                             │
└──────────────────┬─────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────┐
│          RAG Engine with Safety                    │
│  • Retrieve relevant documents (all languages)     │
│  • Generate answer with LLM                        │
│  • Apply safety filters                            │
│  • Format in question language                     │
                   │
                   ▼
┌────────────────────────────────────────────────────┐
│            FastAPI Server                          │
│  • RESTful endpoints                               │
│  • Multilingual responses                          │
│  • Error handling                                  │
│  • Interactive documentation                       │
└────────────────────────────────────────────────────┘
```

---

## 🛡️ Safety & Ethics

### Implemented Across All Languages:

1. **Topic Filtering**
   - ❌ Legal advice blocked
   - ❌ Predictive/fortune-telling blocked
   - ✅ Language-aware error messages

2. **Response Validation**
   - Removes divine claims in any language
   - Ensures humble, devotional tone
   - Adds appropriate disclaimers

3. **Multilingual Disclaimers**
   - Provided in response language
   - Clear safety guidelines
   - Ethical boundaries maintained

---

## 📊 Technology Stack

### Core Technologies
- **FastAPI** - Web framework
- **LangChain** - RAG framework
- **FAISS** - Vector database
- **OpenAI Whisper** - Speech-to-text
- **Sentence Transformers** - Multilingual embeddings

### AI Models
- **LLM**: OpenAI GPT-4 or Google Gemini
- **Embeddings**: paraphrase-multilingual-MiniLM-L12-v2
- **Language Detection**: langdetect

### Key Libraries
- `langchain` - RAG pipeline
- `faiss-cpu` - Vector search
- `sentence-transformers` - Embeddings
- `langdetect` - Language detection
- `pypdf` - PDF processing


```env
# AI Provider
AI_PROVIDER=openai

# API Keys
OPENAI_API_KEY=sk-your-key-here
GOOGLE_API_KEY=your-google-key-here

# Model Settings
MODEL_TEMPERATURE=0.3

# Multilingual Settings
SUPPORTED_LANGUAGES=["en", "hi", "te", "kn"]
MULTILINGUAL_EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
DEFAULT_LANGUAGE=en

# RAG Settings
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_RESULTS=4

# Paths
DATA_FOLDER=./data
AUDIO_FOLDER=./audio
VECTOR_DB_PATH=./vector_db

# API Settings
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

---

## 🧪 Testing

### Test CLI
```powershell
python rag_engine.py
```

Try questions in all 4 languages interactively.

### Test API
```python
import requests

questions = [
    "What is devotion?",           # English
    "भक्ति क्या है?",               # Hindi
    "భక్తి అంటే ఏమిటి?",            # Telugu
    "ಭಕ್ತಿ ಎಂದರೇನು?"               # Kannada
]

for question in questions:
    response = requests.post(
        "http://localhost:8000/ask",
        json={"question": question}
    )
    result = response.json()
    print(f"Q: {question}")
    print(f"A ({result['language']}): {result['answer'][:100]}...\n")
```

---

## 📚 Documentation Files

| File | Description |
|------|-------------|
| `README_MULTILINGUAL.md` | Complete multilingual documentation |
| `QUICKSTART_MULTILINGUAL.md` | Quick start guide (all 4 languages) |
| `API_EXAMPLES.md` | API usage examples |
| `README.md` | Original English documentation |

---

## 🎯 Use Cases

1. **Spiritual Guidance Platform**
   - Serve global devotee community
   - Support regional languages
   - 24/7 availability

2. **Educational Tool**
   - Learn Sai Baba's teachings
   - Access in native language
   - Interactive Q&A

3. **Research Assistant**
   - Search across multilingual texts
   - Find relevant passages
   - Cross-reference teachings

4. **Mobile App Backend**
   - Connect any frontend
   - Multilingual support built-in
   - RESTful API ready

---

## 🚀 Production Deployment
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "api.py"]
```

### Environment Setup
```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf-8
```

---

## 🐛 Troubleshooting

### Unicode Issues
**Solution:** Set encoding in PowerShell
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### Language Detection Fails
**Solution:** Ensure sufficient text (10+ characters)

### Audio Transcription Poor
**Solution:** Use larger Whisper model (`medium` or `large`)

### Check Logs
```powershell
Get-Content app.log -Tail 50
```

---

## 📈 Performance Tips

1. **Whisper Model Selection:**
   - `tiny`: Fastest, lowest accuracy
   - `base`: Recommended (good balance)
   - `medium`: High accuracy
   - `large`: Best accuracy (slower)

2. **Embedding Model:**
   - Default: Good for most use cases
   - For better accuracy: `paraphrase-multilingual-mpnet-base-v2`

3. **Optimization:**
   - Use GPU if available
   - Adjust `CHUNK_SIZE` based on content
   - Tune `TOP_K_RESULTS` for retrieval

---

## 🌟 Key Highlights

✨ **Fully Multilingual** - Not just translation, native language support

✨ **Production Ready** - Error handling, logging, monitoring

✨ **API-First** - Connect any frontend easily

✨ **Safety Built-In** - Ethical guardrails enforced

✨ **Cross-Lingual Search** - Find answers across all languages

✨ **Auto Language Detection** - Seamless user experience

✨ **UTF-8 Safe** - Proper Indic script handling

✨ **Modular Design** - Easy to extend and maintain

---

## 📞 Support

For issues or questions:
1. Check documentation files
2. Review `app.log` for errors
3. Test individual modules
4. Verify UTF-8 encoding

---

## 📜 License

For educational and spiritual guidance purposes. Use responsibly across all language communities.

---

## 🙏 Acknowledgments

- Sai Baba's multilingual teachings and global devotee community
- OpenAI Whisper for multilingual speech recognition
- Sentence Transformers for multilingual embeddings
- LangChain for RAG framework
- FastAPI for web framework
- All open-source contributors

---

**Built with ❤️ for the global Sai Baba devotee community**

**वैश्विक साईं बाबा भक्त समुदाय के लिए ❤️ के साथ बनाया गया**

**ప్రపంచ సాయి బాబా భక్త సమాజం కోసం ❤️తో నిర్మించబడింది**

**ಜಾಗತಿಕ ಸಾಯಿಬಾಬಾ ಭಕ್ತ ಸಮುದಾಯಕ್ಕಾಗಿ ❤️ ಅಂಚೆಯೊಂದಿಗೆ ನಿರ್ಮಿಸಲಾಗಿದೆ**
