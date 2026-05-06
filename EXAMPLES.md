# API Examples - Copy & Paste Ready

## Windows PowerShell Examples

### 1. Health Check
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/" -Method GET
```

### 2. Generate Text
```powershell
$body = @{
    prompt = "What is artificial intelligence?"
    max_new_tokens = 100
    temperature = 0.7
    top_p = 0.9
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/generate" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

### 3. Summarize Text
```powershell
$body = @{
    text = "Hugging Face is a company that develops tools for building machine learning applications. The company is most notable for its Transformers library, which provides thousands of pretrained models. Founded in 2016, Hugging Face has grown into one of the most important platforms in the AI ecosystem."
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/summarize" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

### 4. Chat
```powershell
$body = @{
    prompt = "Explain quantum computing"
    max_new_tokens = 150
    temperature = 0.7
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/chat" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

---

## Python Examples

### 1. Simple Request
```python
import requests

response = requests.post(
    "http://localhost:8000/generate",
    json={
        "prompt": "What is machine learning?",
        "max_new_tokens": 100
    }
)

print(response.json()["generated_text"])
```

### 2. With Error Handling
```python
import requests

try:
    response = requests.post(
        "http://localhost:8000/generate",
        json={
            "prompt": "Explain neural networks",
            "max_new_tokens": 100,
            "temperature": 0.7
        },
        timeout=120
    )
    response.raise_for_status()
    result = response.json()
    print(f"Generated: {result['generated_text']}")
    
except requests.exceptions.Timeout:
    print("Request timed out - first request may take 30-60s")
except requests.exceptions.ConnectionError:
    print("Connection error - is backend running?")
except Exception as e:
    print(f"Error: {e}")
```

### 3. Batch Processing
```python
import requests

prompts = [
    "What is Python?",
    "Explain JavaScript",
    "What is React?"
]

for prompt in prompts:
    response = requests.post(
        "http://localhost:8000/generate",
        json={"prompt": prompt, "max_new_tokens": 50}
    )
    result = response.json()["generated_text"]
    print(f"Q: {prompt}\nA: {result}\n")
```

---

## JavaScript/Fetch Examples

### 1. Basic Request
```javascript
const response = await fetch('http://localhost:8000/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: "What is AI?",
    max_new_tokens: 100
  })
});

const data = await response.json();
console.log(data.generated_text);
```

### 2. With Error Handling
```javascript
async function generateText(prompt) {
  try {
    const response = await fetch('http://localhost:8000/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: prompt,
        max_new_tokens: 100,
        temperature: 0.7
      })
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data.generated_text;
    
  } catch (error) {
    console.error('Error:', error.message);
    return null;
  }
}

// Usage
const result = await generateText("Explain machine learning");
console.log(result);
```

### 3. React Component
```jsx
import { useState } from 'react';

function AIChat() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: prompt,
          max_new_tokens: 100
        })
      });
      const data = await res.json();
      setResponse(data.generated_text);
    } catch (error) {
      setResponse('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <textarea 
        value={prompt} 
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter your prompt..."
      />
      <button onClick={handleGenerate} disabled={loading}>
        {loading ? 'Generating...' : 'Generate'}
      </button>
      {response && <div>{response}</div>}
    </div>
  );
}

export default AIChat;
```

---

## cURL Examples (Git Bash / Linux)

### 1. Health Check
```bash
curl -X GET http://localhost:8000/
```

### 2. Generate Text
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is machine learning?",
    "max_new_tokens": 100,
    "temperature": 0.7
  }'
```

### 3. Summarize
```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your text to summarize here..."
  }'
```

### 4. Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing",
    "max_new_tokens": 150
  }'
```

---

## Testing with Swagger UI

**Best for beginners!**

1. Open browser: http://localhost:8000/docs
2. Click on any endpoint (e.g., `/generate`)
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"
6. See response

---

## Parameter Reference

### Common Parameters

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `prompt` | string | - | - | Your input text |
| `max_new_tokens` | int | 100 | 1-2048 | Max output length |
| `temperature` | float | 0.7 | 0.0-2.0 | 0=deterministic, 1+=creative |
| `top_p` | float | 0.9 | 0.0-1.0 | Nucleus sampling |

### Examples with Different Parameters

**Deterministic (Q&A):**
```python
{
    "prompt": "Q: What is Python? A:",
    "max_new_tokens": 50,
    "temperature": 0.1,
    "top_p": 0.5
}
```

**Balanced (Default):**
```python
{
    "prompt": "What is AI?",
    "max_new_tokens": 100,
    "temperature": 0.7,
    "top_p": 0.9
}
```

**Creative (Brainstorming):**
```python
{
    "prompt": "Write a creative story about:",
    "max_new_tokens": 300,
    "temperature": 1.0,
    "top_p": 0.95
}
```

---

## Response Format

### Success Response (200)
```json
{
  "prompt": "What is AI?",
  "generated_text": "Artificial intelligence is...",
  "status": "success"
}
```

### Error Response (500)
```json
{
  "detail": "Error message here"
}
```

---

## Rate Limit Handling

The backend automatically handles:
- ✅ 503 (model loading) - retries with backoff
- ✅ 429 (rate limited) - retries with delay
- ✅ Connection errors - retries 3 times

You don't need to handle these yourself!

---

## Pro Tips

1. **First request is slower** - Model needs to load (30-60s)
2. **Subsequent requests are fast** - Uses cache
3. **Lower temperature for facts** - Use 0.1-0.3
4. **Higher temperature for creativity** - Use 0.8-1.0+
5. **Test in Swagger UI first** - Then integrate to code

---

## Frontend Integration

### Option 1: Call Backend from Frontend
```
Frontend (React/Vue/Angular) 
  ↓
Your Backend (localhost:8000) 
  ↓
Hugging Face API
```

### Option 2: Call HF API Directly (CORS issue!)
```
Frontend 
  ↓
Hugging Face API (may have CORS issues)
```

**Recommendation:** Use Option 1 (call your backend)

---

**Need help?** Check README.md or QUICK_START.md
