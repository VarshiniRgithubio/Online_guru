# Multilingual Quick Start Guide
# बहुभाषी त्वरित आरंभ गाइड
# బహుభాష త్వరిత ప్రారంభ మార్గదర్శి
# ಬಹುಭಾಷಾ ತ್ವರಿತ ಪ್ರಾರಂಭ ಮಾರ್ಗದರ್ಶಿ

## English Quick Start

### 1. Installation (5 minutes)
```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install packages
pip install -r requirements.txt

# Configure environment
cp .env.example .env
notepad .env  # Add your API key
```

### 2. Add Multilingual Data
```
Place your files here:
├── data/           ← PDFs/TXTs (English/Hindi/Telugu/Kannada)
└── audio/          ← Audio files (any language)
```

### 3. Process Audio (if you have audio files)
```powershell
python speech_to_text.py
# Auto-detects language of each file
# Transcribes in original language
# Saves to data/ folder with UTF-8 encoding
```

### 4. Build Vector Database
```powershell
python ingest.py
# Processes all languages
# Creates multilingual searchable index
```

### 5. Start API
```powershell
python api.py
# Access at: http://localhost:8000
# Docs at: http://localhost:8000/docs
```

### 6. Test Questions
```powershell
# English
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"question\": \"What is faith?\"}"

# Hindi
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"question\": \"विश्वास क्या है?\"}"

# Telugu
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"question\": \"విశ్వాసం అంటే ఏమిటి?\"}"

# Kannada
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"question\": \"ನಂಬಿಕೆ ಎಂದರೇನು?\"}"
```

---

## हिंदी त्वरित आरंभ (Hindi Quick Start)

### 1. इंस्टॉलेशन
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. अपना API कुंजी जोड़ें
`.env` फ़ाइल में अपना OpenAI या Gemini API कुंजी जोड़ें

### 3. डेटा जोड़ें
- `data/` फ़ोल्डर में PDF और TXT फाइलें रखें (किसी भी भाषा में)
- `audio/` फ़ोल्डर में ऑडियो फाइलें रखें

### 4. ऑडियो प्रोसेस करें
```powershell
python speech_to_text.py
# स्वचालित रूप से भाषा का पता लगाता है
# मूल भाषा में ट्रांसक्राइब करता है
```

### 5. वेक्टर डेटाबेस बनाएं
```powershell
python ingest.py
# सभी भाषाओं को प्रोसेस करता है
```

### 6. API शुरू करें
```powershell
python api.py
# http://localhost:8000 पर उपलब्ध
```

### 7. हिंदी में प्रश्न पूछें
```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "भक्ति का महत्व क्या है?"}
)

print(response.json()["answer"])
```

---

## తెలుగు త్వరిత ప్రారంభం (Telugu Quick Start)

### 1. ఇన్‌స్టాలేషన్
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. మీ API కీని జోడించండి
`.env` ఫైల్‌లో మీ OpenAI లేదా Gemini API కీని జోడించండి

### 3. డేటాను జోడించండి
- `data/` ఫోల్డర్‌లో PDF మరియు TXT ఫైల్‌లను ఉంచండి (ఏదైనా భాషలో)
- `audio/` ఫోల్డర్‌లో ఆడియో ఫైల్‌లను ఉంచండి

### 4. ఆడియోను ప్రాసెస్ చేయండి
```powershell
python speech_to_text.py
# స్వయంచాలకంగా భాషను గుర్తిస్తుంది
# అసలు భాషలో ట్రాన్స్‌క్రైబ్ చేస్తుంది
```

### 5. వెక్టర్ డేటాబేస్ నిర్మించండి
```powershell
python ingest.py
# అన్ని భాషలను ప్రాసెస్ చేస్తుంది
```

### 6. APIని ప్రారంభించండి
```powershell
python api.py
# http://localhost:8000 వద్ద అందుబాటులో ఉంది
```

### 7. తెలుగులో ప్రశ్నలు అడగండి
```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "భక్తి యొక్క ప్రాముఖ్యత ఏమిటి?"}
)

print(response.json()["answer"])
```

---

## ಕನ್ನಡ ತ್ವರಿತ ಪ್ರಾರಂಭ (Kannada Quick Start)

### 1. ಅನುಸ್ಥಾಪನೆ
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. ನಿಮ್ಮ API ಕೀಲಿಯನ್ನು ಸೇರಿಸಿ
`.env` ಫೈಲ್‌ನಲ್ಲಿ ನಿಮ್ಮ OpenAI ಅಥವಾ Gemini API ಕೀಲಿಯನ್ನು ಸೇರಿಸಿ

### 3. ಡೇಟಾವನ್ನು ಸೇರಿಸಿ
- `data/` ಫೋಲ್ಡರ್‌ನಲ್ಲಿ PDF ಮತ್ತು TXT ಫೈಲ್‌ಗಳನ್ನು ಇರಿಸಿ (ಯಾವುದೇ ಭಾಷೆಯಲ್ಲಿ)
- `audio/` ಫೋಲ್ಡರ್‌ನಲ್ಲಿ ಆಡಿಯೋ ಫೈಲ್‌ಗಳನ್ನು ಇರಿಸಿ

### 4. ಆಡಿಯೋವನ್ನು ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಿ
```powershell
python speech_to_text.py
# ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಭಾಷೆಯನ್ನು ಪತ್ತೆ ಮಾಡುತ್ತದೆ
# ಮೂಲ ಭಾಷೆಯಲ್ಲಿ ಲಿಪ್ಯಂತರಿಸುತ್ತದೆ
```

### 5. ವೆಕ್ಟರ್ ಡೇಟಾಬೇಸ್ ನಿರ್ಮಿಸಿ
```powershell
python ingest.py
# ಎಲ್ಲಾ ಭಾಷೆಗಳನ್ನು ಪ್ರಕ್ರಿಯೆಗೊಳಿಸುತ್ತದೆ
```

### 6. API ಪ್ರಾರಂಭಿಸಿ
```powershell
python api.py
# http://localhost:8000 ನಲ್ಲಿ ಲಭ್ಯವಿದೆ
```

### 7. ಕನ್ನಡದಲ್ಲಿ ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳಿ
```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "ಭಕ್ತಿಯ ಮಹತ್ವ ಏನು?"}
)

print(response.json()["answer"])
```

---

## Common Commands / सामान्य आदेश / సాధారణ ఆదేశాలు / ಸಾಮಾನ್ಯ ಆದೇಶಗಳು

### Process Audio
```powershell
# All audio files
python speech_to_text.py

# Single file
python speech_to_text.py audio/myfile.mp3
```

### Build Database
```powershell
# Build or use existing
python ingest.py

# Force rebuild
python ingest.py --rebuild
```

### Test RAG
```powershell
# Interactive CLI
python rag_engine.py
```

### Start API
```powershell
python api.py
```

## Troubleshooting / समस्या निवारण / సమస్యా పరిష్కారం / ಸಮಸ್ಯೆ ಪರಿಹಾರ

### Unicode Issues
**PowerShell:**
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### Check Logs
```powershell
Get-Content app.log -Tail 50
```

### Verify Setup
```powershell
python setup.py
```

## Testing Different Languages

### Python Script
```python
import requests

# Test all languages
questions = {
    "en": "What is faith?",
    "hi": "विश्वास क्या है?",
    "te": "విశ్వాసం అంటే ఏమిటి?",
    "kn": "ನಂಬಿಕೆ ಎಂದರೇನು?"
}

for lang, question in questions.items():
    response = requests.post(
        "http://localhost:8000/ask",
        json={"question": question}
    )
    result = response.json()
    print(f"\n{lang.upper()}: {result['answer'][:100]}...")
```

## Next Steps

1. **Add More Data** - The more multilingual content, the better
2. **Tune Settings** - Adjust chunk size and retrieval count in `.env`
3. **Deploy** - Use Docker for production deployment
4. **Build Frontend** - Connect your multilingual UI to the API

## Support Resources

- 📖 Full docs: `README_MULTILINGUAL.md`
- 🔍 API docs: http://localhost:8000/docs
- 📝 Logs: `app.log`
- 🌐 Languages: EN, HI, TE, KN

---

**All features work seamlessly across all 4 languages!**

**सभी सुविधाएँ सभी 4 भाषाओं में निर्बाध रूप से काम करती हैं!**

**అన్ని ఫీచర్లు అన్ని 4 భాషలలో సజావుగా పనిచేస్తాయి!**

**ಎಲ್ಲಾ ವೈಶಿಷ್ಟ್ಯಗಳು ಎಲ್ಲಾ 4 ಭಾಷೆಗಳಲ್ಲಿ ಸರಾಗವಾಗಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತವೆ!**
