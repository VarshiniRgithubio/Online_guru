# Sai Baba Multilingual Spiritual Guidance Chatbot - Backend

A production-ready **multilingual** Python backend for a Sai Baba spiritual guidance chatbot using Retrieval-Augmented Generation (RAG). This system provides API-based spiritual guidance in **English, Hindi, Telugu, and Kannada** with automatic language detection.

## 🌐 Multilingual Features

### Supported Languages
- **English (en)** - Full support
- **Hindi (hi)** - हिंदी में पूर्ण समर्थन
- **Telugu (te)** - తెలుగులో పూర్తి మద్దతు
- **Kannada (kn)** - ಕನ್ನಡದಲ್ಲಿ ಸಂಪೂರ್ಣ ಬೆಂಬಲ

### Key Capabilities
- ✅ **Automatic Language Detection** - Detects question language automatically
- ✅ **Cross-Lingual Search** - Search across all 4 languages simultaneously
- ✅ **Language-Matched Responses** - Answer in the same language as the question
- ✅ **Multilingual Audio Transcription** - Whisper-based transcription for all languages
- ✅ **UTF-8 Safe** - Proper handling of Indic scripts
- ✅ **Multilingual Embeddings** - Semantic search across languages

## Features

- **Multilingual RAG-Based QA**: LangChain + FAISS for cross-lingual retrieval
- **Multi-Format Input**: PDF books, TXT files, Audio (mp3, wav) in all 4 languages
- **Intelligent Speech-to-Text**: Whisper with auto language detection
- **Safety Guardrails**: Medical, legal, predictive advice filtering
- **API-First Design**: RESTful API with FastAPI
- **Flexible AI Backend**: OpenAI GPT-4 or Google Gemini
- **Production Ready**: Complete error handling, logging, monitoring

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- (Optional) CUDA GPU for faster processing

### Quick Setup

```powershell
# 1. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API key

# 4. Verify setup
python setup.py
```

### Environment Configuration

Edit `.env`:

```env
# Choose AI provider
AI_PROVIDER=openai

# Add your API key
OPENAI_API_KEY=sk-your-key-here

# Multilingual settings (default values work well)
SUPPORTED_LANGUAGES=["en", "hi", "te", "kn"]
MULTILINGUAL_EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
DEFAULT_LANGUAGE=en
```

## Usage

### 1. Prepare Multilingual Data

Create folder structure:

```
online guru/
├── data/           # PDF and TXT files (any language)
├── audio/          # MP3/WAV audio files (any language)
└── vector_db/      # Auto-generated vector database
```

**Add your multilingual content:**
- Place English, Hindi, Telugu, Kannada PDFs in `data/`
- Place audio speeches in any of the 4 languages in `audio/`

### 2. Convert Audio to Text (Multilingual)

```powershell
python speech_to_text.py
```

**Features:**
- Auto-detects language of each audio file
- Transcribes in original language
- Cleans transcripts
- Saves UTF-8 encoded .txt files to `data/` folder
- Shows language distribution

**Process single file:**
```powershell
python speech_to_text.py path/to/audio.mp3
```

### 3. Build Multilingual Vector Database

```powershell
python ingest.py
```

**What it does:**
- Loads all documents from `data/` (all languages)
- Uses multilingual embeddings
- Creates cross-lingual searchable vector DB
- Enables semantic search across all 4 languages

**Force rebuild:**
```powershell
python ingest.py --rebuild
```

### 4. Test Multilingual RAG

```powershell
python rag_engine.py
```

**Try questions in any language:**
```
Your question (any language): What is faith?
Your question (any language): विश्वास क्या है?
Your question (any language): విశ్వాసం అంటే ఏమిటి?
Your question (any language): ನಂಬಿಕೆ ಎಂದರೇನು?
```

### 5. Start API Server

```powershell
python api.py
```

Access at:
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

## API Endpoints

### POST /ask

Ask a question in any supported language.

**Request:**
```json
{
  "question": "विश्वास का महत्व क्या है?"
}
```

**Response:**
```json
{
  "answer": "साईं बाबा की शिक्षाओं के अनुसार, विश्वास आध्यात्मिक जीवन की नींव है...",
  "language": "hi",
  "sources": [...],
  "is_safe": true,
  "disclaimer": "यह मार्गदर्शन साईं बाबा की शिक्षाओं पर आधारित है..."
}
```

### Language Detection Examples

**English:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is devotion?\"}"
```

**Hindi:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"भक्ति क्या है?\"}"
```

**Telugu:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"భక్తి అంటే ఏమిటి?\"}"
```

**Kannada:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"ಭಕ್ತಿ ಎಂದರೇನು?\"}"
```

## System Architecture

```
┌─────────────────────────┐
│  Multilingual Data      │
│  (EN/HI/TE/KN)         │
│  PDF/TXT/Audio         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Whisper (Auto-detect)  │ ◄── Language Detection
│  Speech-to-Text         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  UTF-8 Text Files       │
│  (data/ folder)         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Multilingual           │
│  Embeddings Model       │
│  (paraphrase-multi)     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  FAISS Vector DB        │ ◄── Cross-lingual Search
│  (All 4 languages)      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Language Detector      │ ◄── Detect Question Lang
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  RAG Engine + LLM       │ ◄── Generate Answer
│  (OpenAI/Gemini)        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Answer in Same Lang    │
│  + Safety Checks        │
└─────────────────────────┘
```

## Project Structure

```
online guru/
├── api.py                     # FastAPI server (multilingual)
├── rag_engine.py              # Multilingual RAG engine
├── ingest.py                  # Multilingual vector DB builder
├── speech_to_text.py          # Multilingual audio transcription
├── language_utils.py          # Language detection & handling
├── config.py                  # Configuration management
├── logger_config.py           # Logging setup
├── utils.py                   # Utility functions
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── README_MULTILINGUAL.md    # This file
└── data/                     # Multilingual input documents
```

## Multilingual Configuration

### Embedding Model

Default: `paraphrase-multilingual-MiniLM-L12-v2`

This model supports 50+ languages and works excellently for:
- English, Hindi, Telugu, Kannada
- Semantic similarity across languages
- Cross-lingual information retrieval

### Language Detection

Uses `langdetect` library:
- Fast and accurate
- Automatically detects input language
- Falls back to default language if uncertain

### Supported Language Codes

| Language | Code | Script |
|----------|------|--------|
| English  | en   | Latin  |
| Hindi    | hi   | Devanagari |
| Telugu   | te   | Telugu |
| Kannada  | kn   | Kannada |

## Safety Features (Multilingual)

All safety guardrails work across all languages:

### 1. Topic Filtering
- Medical, legal, predictive advice blocked
- Language-aware error messages

### 2. Response Validation
- Removes divine claims in any language
- Ensures humble, devotional tone

### 3. Multilingual Disclaimers
- Disclaimers provided in response language
- Clear safety guidelines

## Example Workflows

### Workflow 1: Process Hindi Audio

```powershell
# 1. Place Hindi audio in audio/
# 2. Run transcription
python speech_to_text.py audio/hindi_speech.mp3

# Output: data/hindi_speech.txt (UTF-8)

# 3. Build/update vector DB
python ingest.py

# 4. Ask questions in Hindi
python rag_engine.py
# > भक्ति का महत्व क्या है?
```

### Workflow 2: Mixed Language Dataset

```powershell
# data/ folder contains:
# - english_teachings.pdf
# - hindi_teachings.txt
# - telugu_audio.mp3 (transcribed)
# - kannada_book.pdf

# Build unified multilingual DB
python ingest.py

# Ask in any language, get relevant results from all documents
```

### Workflow 3: API Integration

```python
import requests

# Ask in different languages
questions = [
    "What is faith?",                      # English
    "विश्वास क्या है?",                      # Hindi
    "విశ్వాసం అంటే ఏమిటి?",                  # Telugu
    "ನಂಬಿಕೆ ಎಂದರೇನು?"                        # Kannada
]

for q in questions:
    response = requests.post(
        "http://localhost:8000/ask",
        json={"question": q}
    )
    result = response.json()
    print(f"Q ({result['language']}): {q}")
    print(f"A: {result['answer']}\n")
```

## Troubleshooting

### Unicode/Encoding Issues

**Problem:** Garbled text for Hindi/Telugu/Kannada

**Solution:**
- Ensure all text files are UTF-8 encoded
- Check console/terminal supports UTF-8
- In PowerShell: `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`

### Language Detection Issues

**Problem:** Wrong language detected

**Solution:**
- Ensure question has sufficient text (10+ characters)
- Avoid mixing languages in single question
- Manually specify language if needed

### Audio Transcription

**Problem:** Poor transcription quality

**Solution:**
- Use larger Whisper model: `medium` or `large`
- Ensure clear audio quality
- Check if language is in audio file metadata

## Performance Tips

1. **Whisper Model Selection:**
   - `tiny`: Fastest, lowest accuracy
   - `base`: Good balance (default)
   - `small`: Better accuracy
   - `medium`: High accuracy
   - `large`: Best accuracy, slowest

2. **Embedding Model:**
   - Default model is optimized for speed & quality
   - For better accuracy: `paraphrase-multilingual-mpnet-base-v2`

3. **Chunk Size:**
   - Default 500 chars works well for all languages
   - Increase for longer context needs

## Production Deployment
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "api.py"]
```

### Environment Variables

Ensure UTF-8 support:
```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf-8
```

## Testing Multilingual Support

### Unit Tests

Test language detection:
```python
from language_utils import LanguageDetector

detector = LanguageDetector()

assert detector.detect_language("What is faith?") == "en"
assert detector.detect_language("विश्वास क्या है?") == "hi"
assert detector.detect_language("విశ్వాసం అంటే ఏమిటి?") == "te"
assert detector.detect_language("ನಂಬಿಕೆ ಎಂದರೇನು?") == "kn"
```

### Integration Tests

Test full pipeline:
```powershell
# Test with sample questions
python -c "
from rag_engine import MultilingualRAGEngine

engine = MultilingualRAGEngine()
result = engine.answer_question('విశ్వాసం అంటే ఏమిటి?')
print(f'Language: {result[\"language\"]}')
print(f'Answer: {result[\"answer\"]}')
"
```

## Ethical Guidelines

This multilingual system maintains the same ethical principles across all languages:

1. **Humility** - Never claims divine authority
2. **Safety** - Refuses harmful advice in all languages
3. **Authenticity** - Only shares from available teachings
4. **Respect** - Honors all language communities equally
5. **Transparency** - Clear about limitations

## Support & Resources

### Language-Specific Help

- **English:** Full documentation in this README
- **Hindi:** हिंदी सहायता के लिए API docs देखें
- **Telugu:** తెలుగు సహాయం కోసం API docs చూడండి
- **Kannada:** ಕನ್ನಡ ಸಹಾಯಕ್ಕಾಗಿ API docs ನೋಡಿ

### Common Issues

1. Check `app.log` for detailed errors
2. Verify UTF-8 encoding for all text files
3. Ensure API key is configured correctly
4. Test individual modules before full integration

## License

This project is for educational and spiritual guidance purposes. Please use responsibly and ethically across all language communities.

## Acknowledgments

- Sai Baba's multilingual teachings and global devotee community
- OpenAI Whisper for multilingual speech recognition
- Sentence Transformers for multilingual embeddings
- LangChain for RAG framework
- FastAPI for API framework

---

**Multilingual Disclaimer / बहुभाषी अस्वीकरण / బహుభాష నిరాకరణ / ಬಹುಭಾಷಾ ನಿರಾಕರಣೆ:**

This system provides spiritual guidance in multiple languages based on available teachings. It is not a substitute for personal spiritual practice, qualified teachers, or professional advice in medical, legal, or other specialized domains.

यह प्रणाली उपलब्ध शिक्षाओं के आधार पर कई भाषाओं में आध्यात्मिक मार्गदर्शन प्रदान करती है। यह व्यक्तिगत आध्यात्मिक अभ्यास, योग्य शिक्षकों या चिकित्सा, कानूनी या अन्य विशेष डोमेन में पेशेवर सलाह का विकल्प नहीं है।

ఈ వ్యవస్థ అందుబాటులో ఉన్న బోధల ఆధారంగా బహుళ భాషలలో ఆధ్యాత్మిక మార్గదర్శకత్వాన్ని అందిస్తుంది। ఇది వ్యక్తిగత ఆధ్యాత్మిక అభ్యాసం, అర్హత కలిగిన గురువులు లేదా వైద్య, న్యాయ లేదా ఇతర ప్రత్యేక డొమైన్‌లలో వృత్తిపరమైన సలహాకు ప్రత్యామ్నాయం కాదు।

ಈ ವ್ಯವಸ್ಥೆಯು ಲಭ್ಯವಿರುವ ಬೋಧನೆಗಳ ಆಧಾರದ ಮೇಲೆ ಬಹು ಭಾಷೆಗಳಲ್ಲಿ ಆಧ್ಯಾತ್ಮಿಕ ಮಾರ್ಗದರ್ಶನವನ್ನು ಒದಗಿಸುತ್ತದೆ। ಇದು ವೈಯಕ್ತಿಕ ಆಧ್ಯಾತ್ಮಿಕ ಅಭ್ಯಾಸ, ಅರ್ಹ ಗುರುಗಳು ಅಥವಾ ವೈದ್ಯಕೀಯ, ಕಾನೂನು ಅಥವಾ ಇತರ ವಿಶೇಷ ಡೊಮೇನ್‌ಗಳಲ್ಲಿ ವೃತ್ತಿಪರ ಸಲಹೆಗೆ ಪರ್ಯಾಯವಲ್ಲ।
