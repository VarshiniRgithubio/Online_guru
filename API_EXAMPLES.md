# API Examples

## Python Examples

### Basic Question
```python
import requests

url = "http://localhost:8000/ask"
data = {"question": "What is the meaning of faith?"}

response = requests.post(url, json=data)
result = response.json()

print(f"Answer: {result['answer']}")
print(f"Based on {len(result['sources'])} sources")
```

### With Error Handling
```python
import requests

def ask_spiritual_question(question: str) -> dict:
    """Ask a question to the Sai Baba API."""
    try:
        response = requests.post(
            "http://localhost:8000/ask",
            json={"question": question},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Usage
result = ask_spiritual_question("What is devotion?")
if "error" not in result:
    print(result["answer"])
else:
    print(f"Error: {result['error']}")
```

### Batch Questions
```python
import requests

questions = [
    "What is faith?",
    "How to practice devotion?",
    "What is the path to peace?"
]

url = "http://localhost:8000/ask"

for question in questions:
    response = requests.post(url, json={"question": question})
    result = response.json()
    print(f"\nQ: {question}")
    print(f"A: {result['answer'][:200]}...")
```

## JavaScript Examples

### Fetch API
```javascript
async function askQuestion(question) {
    const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question })
    });
    
    const data = await response.json();
    return data;
}

// Usage
askQuestion("What is devotion?")
    .then(result => {
        console.log("Answer:", result.answer);
        console.log("Sources:", result.sources.length);
    })
    .catch(error => console.error("Error:", error));
```

### Axios
```javascript
const axios = require('axios');

async function askSaiBaba(question) {
    try {
        const response = await axios.post('http://localhost:8000/ask', {
            question: question
        });
        return response.data;
    } catch (error) {
        console.error('Error:', error.message);
        return null;
    }
}

// Usage
askSaiBaba("What is the importance of faith?")
    .then(result => {
        if (result) {
            console.log(result.answer);
        }
    });
```

### React Component
```jsx
import React, { useState } from 'react';
import axios from 'axios';

function SaiBabaChat() {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [loading, setLoading] = useState(false);

    const handleAsk = async () => {
        setLoading(true);
        try {
            const response = await axios.post('http://localhost:8000/ask', {
                question: question
            });
            setAnswer(response.data.answer);
        } catch (error) {
            setAnswer('Error: ' + error.message);
        }
        setLoading(false);
    };

    return (
        <div>
            <h2>Sai Baba Guidance</h2>
            <input
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask a spiritual question..."
            />
            <button onClick={handleAsk} disabled={loading}>
                {loading ? 'Asking...' : 'Ask'}
            </button>
            {answer && (
                <div>
                    <h3>Answer:</h3>
                    <p>{answer}</p>
                </div>
            )}
        </div>
    );
}

export default SaiBabaChat;
```

## cURL Examples

### Basic Request
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is devotion?\"}"
```

### Pretty Print Response (with jq)
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is faith?\"}" \
  | jq '.answer'
```

### Health Check
```bash
curl http://localhost:8000/health | jq
```

### Get Disclaimer
```bash
curl http://localhost:8000/disclaimer | jq '.disclaimer'
```

## PowerShell Examples

### Basic Request
```powershell
$body = @{
    question = "What is the meaning of devotion?"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/ask" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"

Write-Host $response.answer
```

### With Error Handling
```powershell
function Ask-SaiBaba {
    param([string]$Question)
    
    try {
        $body = @{ question = $Question } | ConvertTo-Json
        $response = Invoke-RestMethod `
            -Uri "http://localhost:8000/ask" `
            -Method Post `
            -Body $body `
            -ContentType "application/json"
        
        return $response.answer
    }
    catch {
        Write-Error "Failed to get answer: $_"
        return $null
    }
}

# Usage
$answer = Ask-SaiBaba "What is faith?"
Write-Host $answer
```

## Response Structure

All `/ask` responses follow this structure:

```json
{
    "answer": "The spiritual guidance answer...",
    "sources": [
        {
            "content": "Excerpt from source document...",
            "metadata": {
                "source": "teachings.pdf",
                "page": 42
            }
        }
    ],
    "is_safe": true,
    "disclaimer": "This guidance is based on Sai Baba's teachings..."
}
```

## Error Handling

API returns standard HTTP status codes:

- **200**: Success
- **400**: Bad request (invalid question)
- **503**: Service unavailable (system not ready)
- **500**: Internal server error

Error response format:
```json
{
    "error": "Error message",
    "detail": "Detailed error information"
}
```

## Rate Limiting (Production)

For production deployment, consider implementing rate limiting:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/ask")
@limiter.limit("10/minute")
async def ask_question(request: Request, question: QuestionRequest):
    # ... existing code
```

## WebSocket Example (Future Enhancement)

For real-time streaming responses:

```python
# Server side (future implementation)
@app.websocket("/ws/ask")
async def websocket_ask(websocket: WebSocket):
    await websocket.accept()
    while True:
        question = await websocket.receive_text()
        # Stream response chunks
        for chunk in generate_streaming_answer(question):
            await websocket.send_text(chunk)
```

```javascript
// Client side
const ws = new WebSocket('ws://localhost:8000/ws/ask');

ws.onmessage = (event) => {
    console.log('Chunk:', event.data);
};

ws.send('What is devotion?');
```
