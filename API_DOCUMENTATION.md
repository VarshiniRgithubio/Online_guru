# 🔌 Sai Baba Chatbot - API Documentation

**Version:** 1.0  
**Date:** December 10, 2025  
**For:** UI Designer Team

---

## 📍 Base URL

```
http://localhost:8000
```

---

## 🚀 Getting Started

### Step 1: Start the API Server
```powershell
python simple_api.py
```

Output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Step 2: Access Interactive API Docs
```
http://localhost:8000/docs
```

---

## 📝 API Endpoints

### 1️⃣ POST /ask - Ask a Question

**Purpose:** Send a question and get an answer in the same language

**Endpoint:** `POST /ask`

**Request Body:**
```json
{
  "question": "What is devotion?"
}
```

**Example with cURL:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is devotion?"}'
```

**Example with Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "What is devotion?"}
)

print(response.json())
```

**Example with JavaScript/Fetch:**
```javascript
fetch('http://localhost:8000/ask', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: 'What is devotion?'
  })
})
.then(response => response.json())
.then(data => console.log(data))
```

**Response (Success - 200):**
```json
{
  "question": "What is devotion?",
  "answer": "Devotion is the path of love and surrender to the divine. Through devotion, we connect with the higher consciousness and experience unconditional love.",
  "language": "en",
  "sources": [
    "Sai Baba Teachings",
    "Spiritual Wisdom"
  ],
  "is_safe": true
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `question` | string | The question that was asked |
| `answer` | string | The answer from Sai Baba teachings |
| `language` | string | Detected language (en, hi, te, kn) |
| `sources` | array | Sources of the teaching |
| `is_safe` | boolean | True if safe, false if blocked |

---

### 2️⃣ GET /ask - Ask via Query Parameter

**Purpose:** Ask a question using URL parameter (simpler for some use cases)

**Endpoint:** `GET /ask`

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `question` | string | Yes | The question to ask |

**Example:**
```
GET /ask?question=What+is+devotion?
```

**cURL Example:**
```bash
curl "http://localhost:8000/ask?question=What%20is%20devotion?"
```

**Response:**
```json
{
  "question": "What is devotion?",
  "answer": "Devotion is the path of love and surrender...",
  "language": "en",
  "sources": ["Sai Baba Teachings"],
  "is_safe": true
}
```

---

### 3️⃣ GET /health - Health Check

**Purpose:** Check if API is running

**Endpoint:** `GET /health`

**Response (200):**
```json
{
  "status": "healthy",
  "service": "Sai Baba Guidance Chatbot",
  "version": "1.0.0",
  "engine_mode": "simple | llm",
  "ai_provider": "openai | gemini | null",
  "model_name": "gpt-4-turbo-preview | gemini-pro | null"
}
```

**cURL Example:**
```bash
curl "http://localhost:8000/health"
```

---

### 4️⃣ GET /languages - Supported Languages

**Purpose:** Get list of supported languages

**Endpoint:** `GET /languages`

**Response:**
```json
{
  "supported_languages": [
    {
      "code": "en",
      "name": "English"
    },
    {
      "code": "hi",
      "name": "Hindi (हिंदी)"
    },
    {
      "code": "te",
      "name": "Telugu (తెలుగు)"
    },
    {
      "code": "kn",
      "name": "Kannada (ಕನ್ನಡ)"
    }
  ]
}
```

**cURL Example:**
```bash
curl "http://localhost:8000/languages"
```

---

### 5️⃣ GET /docs - Interactive API Docs
### 6️⃣ GET /config - Current AI Config

**Purpose:** Show which model/provider the API is using

**Endpoint:** `GET /config`

**Response:**
```json
{
  "engine_mode": "simple | llm",
  "ai_provider": "openai",
  "model_name_openai": "gpt-4-turbo-preview",
  "model_name_gemini": "gemini-pro",
  "temperature": 0.3,
  "use_llm": true,
  "supported_languages": ["en", "hi", "te", "kn"]
}
```

**Purpose:** Swagger UI for interactive API testing

**URL:** `http://localhost:8000/docs`

**Features:**
- Try out endpoints directly in browser
- See real-time responses
- View request/response schemas
- Download OpenAPI specification

---

## 🌍 Multilingual Support

### Supported Languages:
1. **English** - Code: `en`
2. **Hindi** - Code: `hi` (हिंदी)
3. **Telugu** - Code: `te` (తెలుగు)
4. **Kannada** - Code: `kn` (ಕನ್ನಡ)

### Auto-Detection:
The API automatically detects the language of the question and responds in the **same language**.

**Examples:**

#### English Question → English Answer
```json
POST /ask
{
  "question": "What is karma?"
}
```
Response:
```json
{
  "question": "What is karma?",
  "answer": "Karma is the law of action and consequence...",
  "language": "en",
  "is_safe": true
}
```

#### Hindi Question → Hindi Answer
```json
POST /ask
{
  "question": "कर्म क्या है?"
}
```
Response:
```json
{
  "question": "कर्म क्या है?",
  "answer": "कर्म कर्म और परिणाम का नियम है...",
  "language": "hi",
  "is_safe": true
}
```

#### Telugu Question → Telugu Answer
```json
POST /ask
{
  "question": "కర్మ ఎంటో చెప్పు"
}
```
Response:
```json
{
  "question": "కర్మ ఎంటో చెప్పు",
  "answer": "కర్మ క్రియ మరియు ఫలితాల చట్టం...",
  "language": "te",
  "is_safe": true
}
```

#### Kannada Question → Kannada Answer
```json
POST /ask
{
  "question": "ಕರ್ಮ ಎಂದರೆ ಏನು?"
}
```
Response:
```json
{
  "question": "ಕರ್ಮ ಎಂದರೆ ಏನು?",
  "answer": "ಕರ್ಮವು ಕ್ರಿಯೆ ಮತ್ತು ಪರಿಣಾಮದ ನಿಯಮ...",
  "language": "kn",
  "is_safe": true
}
```

---

## 💾 Response Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| **200** | Success | Question answered |
| **400** | Bad Request | Missing question parameter |
| **422** | Validation Error | Invalid request format |
| **500** | Server Error | Unexpected error |

---

## 🛡️ Safety Features

### Blocked Topics:
The API blocks questions about:
- ❌ Medical advice
- ❌ Legal advice
- ❌ Dangerous activities
- ❌ Unethical content

### Response on Blocked Question:
```json
{
  "question": "Can you diagnose my symptoms?",
  "answer": "I cannot provide medical advice. Please consult a healthcare professional.",
  "language": "en",
  "sources": ["Safety Guidelines"],
  "is_safe": false
}
```

---

## 📦 Topics Supported

The chatbot has answers for these topics in **all 4 languages**:

| Topic | Examples |
|-------|----------|
| **Devotion** | "What is devotion?", "भक्ति क्या है?" |
| **Faith** | "What is faith?", "విశ్వాసం ఎంటో చెప్పు" |
| **Service** | "What is service?", "सेवा क्या है?" |
| **Karma** | "What is karma?", "ಕರ್ಮ ಎಂದರೆ ಏನು?" |
| **Meditation** | "What is meditation?", "ধ্যান কি?" |
| **Truth** | "What is truth?", "सत्य क्या है?" |
| **Love** | "What is love?", "ప్రేమ ఎంటో చెప్పు" |
| **Peace** | "What is peace?", "शांति क्या है?" |
| **Purpose** | "What is life's purpose?" |
| **God** | "What is God?" |
| **Dharma** | "What is dharma?" |
| **Wisdom** | "What is wisdom?" |

---

## 🔐 CORS (Cross-Origin Resource Sharing)

The API allows requests from any origin. Your frontend can make requests from any domain.

**Allowed Methods:** GET, POST, PUT, DELETE, OPTIONS

---

## 📱 Frontend Integration Examples

### React Example:
```javascript
import React, { useState } from 'react';

function ChatBot() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div>
      <input 
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question..."
      />
      <button onClick={askQuestion}>Ask</button>
      
      {loading && <p>Loading...</p>}
      {response && (
        <div>
          <p><strong>Answer:</strong> {response.answer}</p>
          <p><strong>Language:</strong> {response.language}</p>
          <p><strong>Safe:</strong> {response.is_safe ? 'Yes' : 'No'}</p>
        </div>
      )}
    </div>
  );
}

export default ChatBot;
```

### Vue.js Example:
```javascript
<template>
  <div>
    <input 
      v-model="question"
      placeholder="Ask a question..."
      @keyup.enter="askQuestion"
    />
    <button @click="askQuestion">Ask</button>
    
    <div v-if="loading">Loading...</div>
    <div v-if="response">
      <p><strong>Answer:</strong> {{ response.answer }}</p>
      <p><strong>Language:</strong> {{ response.language }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      question: '',
      response: null,
      loading: false
    };
  },
  methods: {
    async askQuestion() {
      this.loading = true;
      const res = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: this.question })
      });
      this.response = await res.json();
      this.loading = false;
    }
  }
};
</script>
```

### Angular Example:
```typescript
import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-chatbot',
  template: `
    <input [(ngModel)]="question" placeholder="Ask a question..." />
    <button (click)="askQuestion()">Ask</button>
    
    <div *ngIf="loading">Loading...</div>
    <div *ngIf="response">
      <p><strong>Answer:</strong> {{ response.answer }}</p>
      <p><strong>Language:</strong> {{ response.language }}</p>
    </div>
  `
})
export class ChatbotComponent {
  question = '';
  response: any = null;
  loading = false;

  constructor(private http: HttpClient) {}

  askQuestion() {
    this.loading = true;
    this.http.post('http://localhost:8000/ask', { question: this.question })
      .subscribe(data => {
        this.response = data;
        this.loading = false;
      });
  }
}
```

---

## 🧪 Testing the API

### Using Postman:
1. Open Postman
2. Create new POST request
3. URL: `http://localhost:8000/ask`
4. Body (JSON):
```json
{
  "question": "What is devotion?"
}
```
5. Click Send

### Using Thunder Client (VS Code):
1. Install Thunder Client extension
2. Create POST request
3. URL: `http://localhost:8000/ask`
4. Body: Same JSON as above
5. Send

### Using Python:
```python
import requests

# Test English
response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "What is devotion?"}
)
print(response.json())

# Test Hindi
response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "भक्ति क्या है?"}
)
print(response.json())

# Test Telugu
response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "విశ్వాసం ఎంటో చెప్పు"}
)
print(response.json())
```

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Response Time | ~100-500ms |
| Max Request Size | 1MB |
| Timeout | 30 seconds |
| Concurrent Requests | Unlimited |

---

## 🔧 Troubleshooting

### API not responding?
```powershell
# Check if server is running
curl http://localhost:8000/health

# Restart server
python simple_api.py
```

### CORS errors in frontend?
- API supports CORS from any origin
- Make sure to use correct base URL

### Language not detected?
- System auto-detects language from question
- If detection fails, defaults to English
- Check supported languages: `GET /languages`

---

## 📞 Support

### For Questions:
1. Check this documentation
2. Test endpoint in `/docs`
3. Review examples above

### Common Issues:
| Issue | Solution |
|-------|----------|
| 400 Bad Request | Check JSON format |
| Empty answer | Question may not match topics |
| Language not detected | Try clearer text in that language |

---

## 🚀 Deployment

### Local Development:
```powershell
python simple_api.py
# Runs on http://localhost:8000
```

### Production Deployment:
```powershell
# Using uvicorn directly
uvicorn simple_api:app --host 0.0.0.0 --port 8000 --workers 4

# Using Gunicorn (Linux/Mac)
gunicorn simple_api:app -w 4
```

---

## 📚 Full OpenAPI Spec

Visit `http://localhost:8000/openapi.json` to get the complete OpenAPI 3.0 specification for your API documentation tools.

---

**API Documentation v1.0**  
**Last Updated:** December 10, 2025

---

## Quick Reference Card

```
🔌 BASE URL: http://localhost:8000

📝 ENDPOINTS:
  POST /ask              - Ask a question
  GET  /ask?question=... - Ask via URL param
  GET  /health           - Check if running
  GET  /languages        - List languages
  GET  /docs             - Interactive docs

🌍 LANGUAGES: en (English), hi (हिंदी), te (తెలుగు), kn (ಕನ್ನಡ)

📦 RESPONSE:
  {
    "question": "...",
    "answer": "...",
    "language": "en|hi|te|kn",
    "sources": [...],
    "is_safe": true|false
  }

✅ TOPICS: Devotion, Faith, Service, Karma, Meditation, Truth, Love, Peace, Purpose, God, Dharma, Wisdom
```

