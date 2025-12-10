# 🚀 API for Your Frontend - Quick Guide

## Base URL
```
http://localhost:8000
```

## How to Use

### 1. POST Request (Recommended)
```javascript
fetch('http://localhost:8000/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: 'What is devotion?' })
})
.then(r => r.json())
.then(data => console.log(data))
```

### 2. GET Request
```
http://localhost:8000/ask?question=What%20is%20devotion?
```

## Response Example
```json
{
  "answer": "Devotion is the path of love and surrender to the divine...",
  "language": "en"
}
```

## Supported Languages
Ask in any language, get answer in same language:
- English: "What is devotion?"
- Hindi: "भक्ति क्या है?"
- Telugu: "విశ్వాసం ఎంటో చెప్పు"
- Kannada: "ಭಕ್ತಿ ಎಂದರೆ ಏನು?"

## Quick React Example
```jsx
const [answer, setAnswer] = useState('');

const askQuestion = async (question) => {
  const res = await fetch('http://localhost:8000/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  const data = await res.json();
  setAnswer(data.answer);
};
```

## Topics Available
Devotion, Faith, Service, Karma, Meditation, Truth, Love, Peace, Purpose, God, Dharma, Wisdom

## That's it! 🎉
- ✅ Simple JSON response
- ✅ Auto language detection
- ✅ CORS enabled
- ✅ Works with any frontend framework

Start using it now!
