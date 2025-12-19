# 🚀 LLM MODE - Enable for Your Books

## Current Status
✅ **Vector DB ready**: 8,781 chunks from your Sai Baba + Buddha books  
✅ **Multilingual**: English, Hindi, Telugu, Kannada language detection works  
✅ **Simple mode**: Currently answers from hardcoded dataset  
⏳ **LLM mode**: Ready to enable once you have API key  

---

## Step 1: Get an API Key

### Option A: OpenAI (Recommended)
1. Go to https://platform.openai.com/api-keys
2. Create a new secret key
3. Copy it (looks like: `sk-proj-xxxxx...`)
4. Keep it secret! Don't commit to git.

### Option B: Google Gemini
1. Go to https://makersuite.google.com/app/apikey
2. Create an API key
3. Copy it

---

## Step 2: Update .env

Edit `F:\online guru\.env` and update:

```env
# Enable LLM mode to use your trained books + AI model
USE_LLM=true

# Choose AI provider
AI_PROVIDER=openai  # or 'gemini'

# Add your API key
OPENAI_API_KEY=sk-proj-xxxxx...your-key-here
# OR for Gemini:
# GOOGLE_API_KEY=xxxxx...your-key-here

# Choose model (make sure your account has access)
MODEL_NAME_OPENAI=gpt-4o
# MODEL_NAME_OPENAI=GPT-5.1-Codex-Max  # Try if available
# MODEL_NAME_GEMINI=gemini-1.5-pro

# Fine-tune LLM behavior
MODEL_TEMPERATURE=0.3  # Lower = more consistent, Higher = more creative
```

---

## Step 3: Restart API

```powershell
cd "F:\online guru"
python simple_api.py
```

Expected output:
```
============================================================
  Sai Baba Guidance Chatbot API
============================================================

Starting server...
API running on: http://localhost:8000
Interactive docs: http://localhost:8000/docs

============================================================

INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Step 4: Verify LLM Mode is Active

### Check Health Endpoint
Open browser or curl:
```
http://localhost:8000/health
```

Should show:
```json
{
  "status": "healthy",
  "service": "Sai Baba Guidance Chatbot",
  "version": "1.0.0",
  "engine_mode": "llm",
  "ai_provider": "openai",
  "model_name": "gpt-4o"
}
```

### Check Config Endpoint
```
http://localhost:8000/config
```

Should show full configuration including your model and provider.

---

## Step 5: Test Q&A Using Your Books

The API now:
1. **Retrieves** matching passages from your Sai Baba + Buddha books
2. **Sends** them to your LLM (OpenAI/Gemini)
3. **Generates** answer grounded in your texts
4. **Returns** response in detected language

### Test in Browser (Interactive)
1. Go to http://localhost:8000/docs
2. Click **POST /ask**
3. Click **Try it out**
4. Enter question, e.g.: `What is the Eightfold Path?`
5. Click **Execute**
6. See answer grounded in your Buddha books!

### Test via PowerShell

**English:**
```powershell
curl -X POST "http://localhost:8000/ask" `
  -H "Content-Type: application/json" `
  -d '{"question":"What does Sai Baba teach about devotion?"}'
```

**Hindi:**
```powershell
curl -X POST "http://localhost:8000/ask" `
  -H "Content-Type: application/json" `
  -d '{"question":"भक्ति के बारे में साईं बाबा क्या सिखाते हैं?"}'
```

**Telugu:**
```powershell
curl -X POST "http://localhost:8000/ask" `
  -H "Content-Type: application/json" `
  -d '{"question":"తెలుగులో విష్వాసం ఎంటో చెప్పు"}'
```

**Kannada:**
```powershell
curl -X POST "http://localhost:8000/ask" `
  -H "Content-Type: application/json" `
  -d '{"question":"ಧರ್ಮ ಎಂದರೆ ಏನು?"}'
```

---

## Expected Answer Flow (LLM Mode)

When you ask: **"What is devotion?"**

1. **Detect language**: English
2. **Retrieve**: Find 4 relevant chunks from your books
   - Sri-Sai-Satcharitra on devotion
   - Teachings of Shirdi Sai Baba
   - Buddha's teachings on attachment (if relevant)
3. **Build context**: 
   ```
   Based on Sai Baba's teachings:
   "Devotion is not merely performing rituals..."
   "True devotion means surrender to the divine..."
   ```
4. **LLM generates**:
   ```
   Devotion, according to Sai Baba, is a path of love and 
   surrender to the divine. It is not merely following rituals 
   but developing a genuine relationship with God...
   ```
5. **Return**: Answer in English with sources cited

---

## Troubleshooting

### "LLM initialization failed" → Falls back to simple mode
- Check .env has valid API key
- Check USE_LLM=true
- Check AI_PROVIDER is 'openai' or 'gemini'
- Check model name is correct (gpt-4o, not gpt-99-fake)

### "Invalid API key"
- Generate new key from OpenAI/Google
- Paste full key (including sk-proj- prefix)
- Don't add quotes around the key in .env

### "Rate limit exceeded"
- Wait a few minutes
- OpenAI free trial has limits
- Consider upgrading account

### Model not found (e.g., GPT-5.1-Codex-Max)
- Try a known model: gpt-4o, gpt-4-turbo, gpt-3.5-turbo
- Or gemini-1.5-pro for Google
- Once you have access to future models, update MODEL_NAME_OPENAI

---

## What Your Books Provide

**Sai Baba books** (6,500+ chunks):
- Sri-Sai-Satcharitra
- Teachings of Shirdi Sai Baba
- Sai Baba teachings

**Buddha books** (2,000+ chunks):
- Dhammapada (teachings)
- What the Buddha Taught (Rahula)
- The Heart of Buddha's Teaching (Thich Nhat Hanh)
- Life of the Buddha
- The Basic Teachings of Buddha

**Topics covered**:
- Devotion, Faith, Service, Karma
- Meditation, Truth, Love, Peace
- Dharma, Wisdom, Purpose
- Eightfold Path, Four Noble Truths
- Compassion, Enlightenment, Suffering

---

## Next Steps (Optional)

### Deploy to Production
```powershell
# Push to GitHub
git add .
git commit -m "Enable LLM with trained vector DB"
git push origin main

# Deploy on Render/Railway
# Your friend gets public URL to call
```

### Add Citations to Responses
Edit `rag_engine.py` to include source passages in answers.

### Blend Teachings
Add routing logic to balance Sai Baba + Buddha teachings in responses.

### Add Audio Support
Use Whisper (already in `speech_to_text.py`) to transcribe questions in Hindi/Telugu/Kannada, then answer.

---

## Summary

- ✅ Vector DB trained with your books
- ✅ Language detection ready for 4 languages
- ✅ API scaffolding complete
- ⏳ Just need API key to enable LLM mode
- 🚀 Once enabled: answers come from your texts!

**Ready?** Grab an API key and update .env, then share it or I can help you test!
