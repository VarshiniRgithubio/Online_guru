# 🤖 How to Ask Questions - Complete Guide

Your chatbot is now ready to answer questions! Here are **ALL the ways** you can ask:

---

## ✅ **Method 1: Command Line (Simplest - No Server Needed)**

Run this command to ask a question instantly:

```powershell
python ask.py "What is devotion?"
```

**Works immediately - no setup required!**

### Examples:

```powershell
python ask.py "What is faith?"
python ask.py "What is the purpose of life?"
python ask.py "भक्ति क्या है?"          # Hindi
python ask.py "భక్తి అంటే ఏమిటి?"     # Telugu
```

### Output:
```
✨ Answer:
Devotion is the path of love and surrender to the divine...
```

**Best for:** Quick questions, scripts, automation

---

## ✅ **Method 2: Interactive CLI (Like ChatGPT)**

Keep asking questions in an interactive chat:

```powershell
python ask.py
```

Then type your questions one by one:

```
👉 Ask a question: What is devotion?
✨ Answer: Devotion is the path of love...

👉 Ask a question: What is faith?
✨ Answer: Faith is trust in God...

👉 Ask a question: quit
✨ Thank you...
```

**Best for:** Conversational exploration

---

## ✅ **Method 3: Web Browser (Interactive API Docs)**

### Step 1: Start the API server
```powershell
python simple_api.py
```

You'll see:
```
✨ Starting server...
📡 API running on: http://localhost:8000
📖 Interactive docs: http://localhost:8000/docs
```

### Step 2: Open in browser
```
http://localhost:8000/docs
```

### Step 3: Ask a question
- Click on the **`POST /ask`** endpoint
- Click **"Try it out"**
- Enter your question:
```json
{
  "question": "What is devotion?",
  "language": "en"
}
```
- Click **"Execute"**
- See the answer!

**Best for:** User-friendly, no coding needed

---

## ✅ **Method 4: PowerShell/Command Line**

### Using PowerShell:

```powershell
# Start server in one PowerShell window
python simple_api.py

# In another PowerShell window, ask questions
$body = @{
    question = "What is devotion?"
    language = "en"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/ask" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body | Select-Object -ExpandProperty Content
```

**Best for:** System administrators, automation

---

## ✅ **Method 5: Simple Browser URL**

### Using GET request in address bar:

```
http://localhost:8000/ask?question=What+is+devotion?
```

Or encoded properly:
```
http://localhost:8000/ask?question=What%20is%20devotion?&language=en
```

Click **Enter** and see the JSON response!

**Best for:** Quick testing, bookmarkable

---

## ✅ **Method 6: Python Script**

### Simple Python code:

```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={
        "question": "What is devotion?",
        "language": "en"
    }
)

data = response.json()
print(f"Answer: {data['answer']}")
print(f"Language: {data['language']}")
```

**Best for:** Integration with Python apps

---

## ✅ **Method 7: cURL (Command Line)**

### Using cURL:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is devotion?\"}"
```

Or with a language parameter:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is devotion?\", \"language\": \"en\"}"
```

**Best for:** Linux/Mac users, shell scripting

---

## ✅ **Method 8: JavaScript/Frontend**

### Using Fetch API:

```javascript
// From your web application
fetch('http://localhost:8000/ask', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        question: "What is devotion?",
        language: "en"
    })
})
.then(response => response.json())
.then(data => {
    console.log("Answer:", data.answer);
    console.log("Language:", data.language);
})
.catch(error => console.error('Error:', error));
```

**Best for:** Web applications, frontend integration

---

## 🌍 **Multilingual Examples**

### English:
```powershell
python ask.py "What is the purpose of life?"
```

### Hindi (हिंदी):
```powershell
python ask.py "भक्ति क्या है?"
```

### Telugu (తెలుగు):
```powershell
python ask.py "భక్తి అంటే ఏమిటి?"
```

### Kannada (ಕನ್ನಡ):
```powershell
python ask.py "ಭಕ್ತಿ ಎಂದರೆ ಏನು?"
```

**System auto-detects the language and responds in the same language!**

---

## 📊 **Quick Comparison**

| Method | Setup | Speed | Ease | Best For |
|--------|-------|-------|------|----------|
| CLI (`ask.py`) | ✅ None | ⚡ Instant | ⭐⭐⭐ | Quick questions |
| Interactive CLI | ✅ None | ⚡ Instant | ⭐⭐⭐ | Conversations |
| Browser /docs | ✅ Start server | ⚡ Fast | ⭐⭐⭐ | User-friendly |
| Browser URL | ✅ Start server | ⚡ Fast | ⭐⭐⭐ | Testing |
| PowerShell | ✅ Start server | ⚡ Fast | ⭐⭐ | Automation |
| Python Script | ✅ Start server | ⚡ Fast | ⭐⭐ | Integration |
| cURL | ✅ Start server | ⚡ Fast | ⭐⭐ | Scripts |
| JavaScript | ✅ Start server | ⚡ Fast | ⭐⭐⭐ | Web apps |

---

## 🚀 **Getting Started NOW**

### Option A: Fastest (Right Now!)
```powershell
# Just ask a question - no setup needed
python ask.py "What is devotion?"
```

### Option B: Interactive (Like ChatGPT)
```powershell
# Start interactive chat
python ask.py

# Then type questions...
```

### Option C: Web Interface (Most User-Friendly)
```powershell
# Terminal 1: Start server
python simple_api.py

# Terminal 2 / Browser: 
# Open http://localhost:8000/docs and ask questions there
```

---

## ✨ **Try These Questions**

```powershell
python ask.py "What is faith?"
python ask.py "What is service?"
python ask.py "What is karma?"
python ask.py "What is meditation?"
python ask.py "What is truth?"
python ask.py "What is love?"
python ask.py "What is peace?"
python ask.py "What is wisdom?"
```

---

## 📝 **API Response Format**

All methods return the same format:

```json
{
  "answer": "Devotion is the path of love and surrender...",
  "language": "en",
  "sources": [
    {
      "content": "Sample teachings from data/sample_teachings.txt"
    }
  ],
  "is_safe": true
}
```

---

## 🎯 **My Recommendation**

**For you right now:**

1. **To ask immediately (no setup):**
   ```powershell
   python ask.py "What is your question?"
   ```

2. **For a web interface (best UX):**
   ```powershell
   # Terminal 1:
   python simple_api.py
   
   # Browser: http://localhost:8000/docs
   ```

3. **For continuous conversation:**
   ```powershell
   python ask.py
   # Then keep typing questions
   ```

**Choose the one that feels most natural to you!** 🚀

---

## ❓ **Questions About Questions?**

- **"Can I ask in different languages?"** ✅ Yes! Auto-detected
- **"Can I ask multiple questions?"** ✅ Yes! As many as you want
- **"Do I need API keys?"** ✅ For now, this uses sample data (no keys needed)
- **"What if I want more answers?"** ✅ Add more teachings to `data/` folder and run `python ingest.py`
- **"Can I use this in my app?"** ✅ Yes! Use the API methods (Python, JavaScript, cURL, etc.)

---

**Ready to start?** Pick a method above and ask your first question! 🎉
