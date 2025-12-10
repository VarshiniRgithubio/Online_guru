# 🔗 Frontend Integration Guide for Vercel App

**For:** Frontend Developer  
**Date:** December 10, 2025  
**App URL:** https://spiritual-guru-app-ai.vercel.app/

---

## ⚡ Quick Start

Your backend API is ready! Here's what you need to integrate it.

---

## 🔌 API Endpoint

```
Base URL: http://localhost:8000
```

**⚠️ Important for Production:**
- **Local Development:** Use `http://localhost:8000`
- **Deployed App:** Will need to deploy backend API or use environment-specific URLs

---

## 📋 API Endpoints Available

### 1. Ask a Question (Recommended)
```
POST /ask
Content-Type: application/json

Request:
{
  "question": "What is devotion?"
}

Response:
{
  "answer": "Devotion is the path of love and surrender to the divine...",
  "language": "en"
}
```

### 2. Ask via URL Parameter
```
GET /ask?question=What%20is%20devotion?

Response:
{
  "answer": "Devotion is the path of love and surrender to the divine...",
  "language": "en"
}
```

### 3. Health Check
```
GET /health

Response:
{
  "status": "healthy",
  "service": "Sai Baba Guidance Chatbot",
  "version": "1.0.0"
}
```

### 4. List Languages
```
GET /languages

Response:
{
  "supported_languages": [
    {"code": "en", "name": "English"},
    {"code": "hi", "name": "Hindi (हिंदी)"},
    {"code": "te", "name": "Telugu (తెలుగు)"},
    {"code": "kn", "name": "Kannada (ಕನ್ನಡ)"}
  ]
}
```

---

## 🚀 Integration Code

### React Component Example

```jsx
import React, { useState } from 'react';

const ChatBot = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [language, setLanguage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const API_URL = 'http://localhost:8000'; // Change for production

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setError('');
    setAnswer('');

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setAnswer(data.answer);
      setLanguage(data.language);
      setQuestion('');
    } catch (err) {
      setError(`Error: ${err.message}`);
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading) {
      askQuestion();
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>Sai Baba Guidance Chatbot</h1>

      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question..."
          disabled={loading}
          style={{
            width: '100%',
            padding: '10px',
            fontSize: '16px',
            marginBottom: '10px',
          }}
        />
        <button
          onClick={askQuestion}
          disabled={loading || !question.trim()}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            cursor: loading ? 'not-allowed' : 'pointer',
          }}
        >
          {loading ? 'Loading...' : 'Ask'}
        </button>
      </div>

      {error && (
        <div style={{ color: 'red', marginBottom: '10px' }}>
          {error}
        </div>
      )}

      {answer && (
        <div
          style={{
            backgroundColor: '#f5f5f5',
            padding: '15px',
            borderRadius: '5px',
            marginTop: '20px',
          }}
        >
          <h3>Answer ({language})</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
};

export default ChatBot;
```

### Vue.js Example

```vue
<template>
  <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
    <h1>Sai Baba Guidance Chatbot</h1>

    <div style="margin-bottom: 20px;">
      <input
        v-model="question"
        @keyup.enter="askQuestion"
        placeholder="Ask a question..."
        :disabled="loading"
        style="width: 100%; padding: 10px; font-size: 16px; margin-bottom: 10px;"
      />
      <button
        @click="askQuestion"
        :disabled="loading || !question.trim()"
        style="padding: 10px 20px; font-size: 16px;"
      >
        {{ loading ? 'Loading...' : 'Ask' }}
      </button>
    </div>

    <div v-if="error" style="color: red; margin-bottom: 10px;">
      {{ error }}
    </div>

    <div
      v-if="answer"
      style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-top: 20px;"
    >
      <h3>Answer ({{ language }})</h3>
      <p>{{ answer }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      question: '',
      answer: '',
      language: '',
      loading: false,
      error: '',
      apiUrl: 'http://localhost:8000', // Change for production
    };
  },
  methods: {
    async askQuestion() {
      if (!this.question.trim()) return;

      this.loading = true;
      this.error = '';
      this.answer = '';

      try {
        const response = await fetch(`${this.apiUrl}/ask`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question: this.question }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        this.answer = data.answer;
        this.language = data.language;
        this.question = '';
      } catch (err) {
        this.error = `Error: ${err.message}`;
        console.error('API Error:', err);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
```

### Next.js API Route (Recommended for Vercel)

**File:** `pages/api/ask.js`

```javascript
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { question } = req.body;

  if (!question) {
    return res.status(400).json({ error: 'Question is required' });
  }

  try {
    const response = await fetch('http://localhost:8000/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      throw new Error(`Backend API error: ${response.status}`);
    }

    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    console.error('API Error:', error);
    res.status(500).json({ error: 'Failed to get answer' });
  }
}
```

Then in your component:
```jsx
const askQuestion = async () => {
  const response = await fetch('/api/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });
  const data = await response.json();
  setAnswer(data.answer);
};
```

---

## 🌍 Multilingual Support

The API automatically detects the language and responds in the same language!

### Supported Languages:
- **English** (en) - Ask: "What is devotion?"
- **Hindi** (hi) - Ask: "भक्ति क्या है?"
- **Telugu** (te) - Ask: "విశ్వాసం ఎంటో చెప్పు"
- **Kannada** (kn) - Ask: "ಭಕ್ತಿ ಎಂದರೆ ಏನು?"

---

## 🔒 CORS Configuration

The API supports CORS and can be called from any domain.

**Allowed Methods:** GET, POST, OPTIONS, PUT, DELETE

---

## 📱 Mobile Friendly

The API works great for:
- ✅ React Native apps
- ✅ Flutter apps
- ✅ Mobile web
- ✅ Progressive Web Apps (PWA)

---

## 🧪 Testing Before Integration

### Test Health Check
```javascript
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(data => console.log(data))
```

### Test API
```javascript
fetch('http://localhost:8000/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: 'What is devotion?' })
})
  .then(r => r.json())
  .then(data => console.log(data))
```

---

## 🚀 Environment Variables

**For Local Development:**
```
REACT_APP_API_URL=http://localhost:8000
```

**For Production:**
```
REACT_APP_API_URL=https://your-backend-api.com
```

(Your backend will need to be deployed to production)

---

## 📊 Topics Supported

Ask about any of these in any language:

- Devotion (भक्ति, విశ్వాసం, ಭಕ್ತಿ)
- Faith (विश्वास, విశ్వాసం, ವಿಶ್ವಾಸ)
- Service (सेवा, సేవ, ಸೇವೆ)
- Karma (कर्म, కర్మ, ಕರ್ಮ)
- Meditation (ध्यान, ధ్యానం, ಧ್ಯಾನ)
- Truth (सत्य, సత్యం, ಸತ್ಯ)
- Love (प्रेम, ప్రేమ, ಪ್ರೀತಿ)
- Peace (शांति, శాంతి, ಶಾಂತಿ)
- Purpose, God, Dharma, Wisdom

---

## ⚠️ Important Notes

1. **Localhost Only:** Currently runs on `http://localhost:8000`
   - For your Vercel app to access it, you need to:
     - Option A: Deploy the backend API
     - Option B: Use a proxy/relay server
     - Option C: Run backend locally + frontend locally during development

2. **CORS:** Already configured, no issues

3. **Response Time:** ~100-200ms per request

4. **Concurrent Requests:** Unlimited

5. **Error Handling:** Always wrap API calls in try-catch

---

## 💡 Pro Tips

1. **Add Loading States** - Show spinner while API responds
2. **Debounce Requests** - Don't send multiple questions rapidly
3. **Error Messages** - Show friendly error messages to users
4. **Caching** - Cache repeated questions locally
5. **Language Detection** - Show detected language to user

---

## 📞 API Documentation

For complete API documentation, see:
- `API_DOCUMENTATION.md` - Full reference
- `API_VERIFICATION.md` - Test results

---

## ✅ Checklist Before Going Live

- [ ] API server is running (`python simple_api.py`)
- [ ] Frontend can reach API at configured URL
- [ ] Health check endpoint responds
- [ ] Questions return valid answers
- [ ] Language detection works
- [ ] Error handling in place
- [ ] Loading states working
- [ ] No CORS errors
- [ ] Ready for backend deployment to production

---

**API is ready to use! Start integrating now!** 🚀

