# QUICK START GUIDE - Hugging Face Inference Backend

## ✅ Setup Complete!

Your Hugging Face Inference Backend is ready to use. Follow these steps:

### Step 1: Backend is Running ✓

The backend is currently running on:
```
http://localhost:8000
```

### Step 2: View API Documentation

Open in your browser:
```
http://localhost:8000/docs
```

This opens **Swagger UI** where you can:
- View all endpoints
- Test API calls directly
- See request/response examples

### Step 3: Test the API

#### Option A: Using Swagger UI (Easiest)
1. Go to http://localhost:8000/docs
2. Click on "/generate" endpoint
3. Click "Try it out"
4. Enter your prompt
5. Click "Execute"

#### Option B: Using the Test Script
Open a new terminal and run:
```bash
python test_api.py
```

#### Option C: Using the Interactive Client
```bash
python example_client.py
```

#### Option D: Using curl (Windows PowerShell)
```powershell
$body = @{
    prompt = "What is machine learning?"
    max_new_tokens = 100
    temperature = 0.7
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/generate" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

### Step 4: Use in Your Application

**Python Example:**
```python
import requests

response = requests.post(
    "http://localhost:8000/generate",
    json={
        "prompt": "What is artificial intelligence?",
        "max_new_tokens": 100,
        "temperature": 0.7
    }
)

print(response.json()["generated_text"])
```

**JavaScript Example:**
```javascript
const response = await fetch('http://localhost:8000/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: "What is artificial intelligence?",
    max_new_tokens: 100,
    temperature: 0.7
  })
});

const data = await response.json();
console.log(data.generated_text);
```

---

## 📌 Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/generate` | POST | Generate text from prompt |
| `/summarize` | POST | Summarize text |
| `/chat` | POST | Chat interface |

---

## ⚙️ Configuration

Edit `.env` to change settings:

```
HF_TOKEN=your_token_here              # Your Hugging Face API token
HF_MODEL=google/gemma-2-2b-it         # Model to use
API_PORT=8000                         # Port (change if needed)
API_HOST=0.0.0.0                      # Host
```

### Available Models

- `google/gemma-2-2b-it` - 2B params (fast, CPU-friendly) ✨ Default
- `meta-llama/Llama-3.1-8B-Instruct` - 8B params (more capable)
- `mistralai/Mistral-7B-Instruct-v0.1` - 7B params (balanced)

---

## 🧪 First API Call

**Simple Example - Text Generation:**

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing in simple terms",
    "max_new_tokens": 100,
    "temperature": 0.7
  }'
```

**Expected Response:**
```json
{
  "prompt": "Explain quantum computing in simple terms",
  "generated_text": "Quantum computing uses quantum bits (qubits)...",
  "status": "success"
}
```

---

## ⚠️ Important Notes

### First Request Takes Longer
- First API call may take 30-60 seconds (model loading)
- Subsequent requests are faster (cached)
- Backend automatically handles retries

### Token Security
- Your HF token is in `.env`
- Add `.env` to `.gitignore` (already done)
- Never share your token!

### Rate Limits
- Free tier has rate limits
- Backend automatically handles 429 errors
- Upgrade to HF Pro for higher limits

---

## 📝 Project Files

```
d:\AI-Exam-Preparer\
├── main.py              ← Main FastAPI application
├── hf_inference.py      ← Hugging Face API wrapper
├── config.py            ← Configuration
├── example_client.py    ← Client examples
├── test_api.py          ← Test script
├── .env                 ← Your token (DO NOT COMMIT)
├── requirements.txt     ← Dependencies
└── README.md            ← Full documentation
```

---

## 🔧 Troubleshooting

### Backend Won't Start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Use different port in .env
HF_PORT=8001
```

### Token Error
```
Error: HF_TOKEN not found
```
→ Check `.env` file has your token

### Timeout Error
```
RequestException: Request timeout
```
→ Normal on first call. Increase timeout or wait longer.

### Rate Limited
```
Error: 429 - Too Many Requests
```
→ Backend retries automatically. Space out requests.

---

## 🚀 Next Steps

1. ✅ Backend is running
2. ✅ Dependencies installed
3. 👉 **Next:** Test an endpoint (Swagger UI or test script)
4. 👉 **Then:** Integrate into your application

---

## 📚 Documentation

- Full guide: See `README.md`
- API Docs: http://localhost:8000/docs (Swagger)
- HF Docs: https://huggingface.co/docs/api-inference

---

## 💡 Example Use Cases

### Use Case 1: Q&A System
```python
response = requests.post("http://localhost:8000/generate", json={
    "prompt": "Q: What is Python? A:",
    "max_new_tokens": 100
})
```

### Use Case 2: Content Summarization
```python
response = requests.post("http://localhost:8000/summarize", json={
    "text": "Long article text here..."
})
```

### Use Case 3: Code Generation
```python
response = requests.post("http://localhost:8000/generate", json={
    "prompt": "Write a Python function to reverse a string:",
    "max_new_tokens": 150,
    "temperature": 0.3  # Lower for more deterministic code
})
```

---

**You're all set! 🎉**

Start testing with the Swagger UI: http://localhost:8000/docs
