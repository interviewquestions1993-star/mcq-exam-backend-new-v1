# 🚀 Hugging Face Official InferenceClient - Working Solution

This project uses the **official Hugging Face `InferenceClient`** library for online inference. This is the recommended approach from Hugging Face documentation.

## ✅ What Works

- ✅ Text Generation with any Hugging Face model
- ✅ Chat Completion with instruction-tuned models
- ✅ Automatic error handling and retries
- ✅ Cold start handling (503 errors)
- ✅ FastAPI backend with Swagger documentation
- ✅ CORS support for frontend integration

## 📋 Setup Instructions

### Step 1: Get Your Hugging Face Token

1. Go to: https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Choose **"Read"** permission (free account is fine)
4. Copy your token (starts with `hf_`)

### Step 2: Create .env File

Create a file named `.env` in the project root:

```env
HF_TOKEN=hf_YOUR_TOKEN_HERE
HF_MODEL=google/gemma-2-2b-it
API_PORT=8000
API_HOST=0.0.0.0
```

Replace `hf_YOUR_TOKEN_HERE` with your actual token.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `huggingface-hub` - Official library for inference
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `python-dotenv` - Environment variables

## 🎯 Quick Start - Three Ways to Use It

### Option 1: Direct Python Example (Simplest)

Run the working example:

```bash
python hf_online_working.py
```

This demonstrates all official InferenceClient methods:
- Simple text generation
- Text generation with Gemma 2B
- Chat completion
- API connection test

### Option 2: FastAPI Backend

Start the API server:

```bash
python main_official.py
```

Then visit:
- **Swagger UI**: http://localhost:8000/docs
- **Interactive docs**: http://localhost:8000/redoc

### Option 3: Manual Testing

Test individual examples:

```bash
python test_official_client.py
```

## 📚 Official InferenceClient Methods

### 1. Text Generation

```python
from huggingface_hub import InferenceClient

client = InferenceClient(api_key="hf_YOUR_TOKEN")

# Simple text generation
response = client.text_generation(
    prompt="The capital of France is",
    model="gpt2",
    max_new_tokens=20
)
print(response)  # Returns string directly
```

**Response:** Returns a string directly (not a JSON object)

**Available Models:**
- `gpt2` - Fast, lightweight
- `google/gemma-2-2b-it` - Powerful, instruction-tuned
- `mistralai/Mistral-7B-Instruct-v0.2` - Great for chat
- Any other Hugging Face model

### 2. Chat Completion

```python
# Chat-style interaction
response = client.chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is machine learning?"}
    ],
    model="mistralai/Mistral-7B-Instruct-v0.2",
    max_tokens=200
)

# Extract message
message = response.choices[0].message.content
print(message)
```

**Response:** ChatCompletionOutput object with structured response

**Best Models for Chat:**
- `mistralai/Mistral-7B-Instruct-v0.2` - Recommended
- `meta-llama/Llama-2-7b-chat-hf` - Alternative
- `google/gemma-2-2b-it` - Lightweight

### 3. Summarization (via Text Generation)

```python
# Summarize text
prompt = """Summarize the following text:
[Long text here]

Summary:"""

response = client.text_generation(
    prompt=prompt,
    model="google/gemma-2-2b-it",
    max_new_tokens=100
)
print(response)
```

## 🔧 API Endpoints (FastAPI Backend)

### GET `/`
Health check

**Response:**
```json
{
  "status": "healthy",
  "message": "Hugging Face Inference Backend (Official InferenceClient) is running"
}
```

### POST `/generate`
Generate text

**Request:**
```json
{
  "prompt": "Explain quantum computing:",
  "max_new_tokens": 100,
  "temperature": 0.7,
  "top_p": 0.9,
  "model": "google/gemma-2-2b-it"
}
```

**Response:**
```json
{
  "prompt": "Explain quantum computing:",
  "model": "google/gemma-2-2b-it",
  "generated_text": "Quantum computing is...",
  "tokens_used": 45
}
```

### POST `/chat`
Chat completion

**Request:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "What is machine learning?"
    }
  ],
  "max_tokens": 200,
  "model": "mistralai/Mistral-7B-Instruct-v0.2"
}
```

**Response:**
```json
{
  "model": "mistralai/Mistral-7B-Instruct-v0.2",
  "message": "Machine learning is a subset of artificial intelligence...",
  "tokens_used": 52
}
```

### POST `/summarize`
Summarize text

**Request:**
```json
{
  "prompt": "Long text to summarize...",
  "max_new_tokens": 100,
  "model": "google/gemma-2-2b-it"
}
```

## 🛠️ Files Overview

| File | Purpose |
|------|---------|
| `main_official.py` | FastAPI backend with official InferenceClient |
| `hf_online_working.py` | Working examples showing all methods |
| `test_official_client.py` | Test suite to verify setup |
| `config.py` | Configuration management |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for environment variables |

## 🐛 Troubleshooting

### "HF_TOKEN not found"
- Create a `.env` file with your token
- Check that you copied the token correctly from https://huggingface.co/settings/tokens

### "Model Loading" (503 errors)
- This is normal! The model takes time to load on first use
- The code automatically waits and retries
- Wait 30-60 seconds for model to load

### "Unauthorized" (401 errors)
- Token is invalid or expired
- Generate a new token from https://huggingface.co/settings/tokens

### "Rate Limited" (429 errors)
- You're making too many requests
- The code implements exponential backoff automatically

### Model Not Available
- Not all models support the free API
- Use `text_generation` for most models
- Use `chat_completion` only with chat-specific models

## 📖 Official Documentation

- **Hugging Face Hub**: https://huggingface.co/docs/hub/
- **InferenceClient API**: https://huggingface.co/docs/huggingface_hub/main/en/package_reference/inference_client
- **Models**: https://huggingface.co/models

## 🎓 Example Use Cases

### 1. Exam Preparation
```python
response = client.text_generation(
    prompt="List 5 key concepts for studying machine learning",
    model="google/gemma-2-2b-it",
    max_new_tokens=150
)
print(response)
```

### 2. Question Answering
```python
response = client.chat_completion(
    messages=[
        {
            "role": "system",
            "content": "You are an expert educator."
        },
        {
            "role": "user",
            "content": "Explain photosynthesis in simple terms"
        }
    ],
    model="mistralai/Mistral-7B-Instruct-v0.2",
    max_tokens=300
)
print(response.choices[0].message.content)
```

### 3. Text Summarization
```python
article = "Long article text here..."
response = client.text_generation(
    prompt=f"Summarize this:\n{article}\n\nSummary:",
    model="google/gemma-2-2b-it",
    max_new_tokens=100
)
print(response)
```

## ✨ Key Features

✅ **Official Library**: Uses `huggingface_hub` - the recommended library  
✅ **No Local GPU Needed**: Runs on Hugging Face servers  
✅ **Free API**: Use free tier for development  
✅ **Multiple Models**: Choose from 100,000+ models  
✅ **Automatic Retries**: Handles errors gracefully  
✅ **Chat Support**: Full conversation support  
✅ **Easy Integration**: Simple Python API  

## 🚀 Next Steps

1. Copy `.env.example` to `.env` and add your token
2. Run `python test_official_client.py` to verify setup
3. Run `python main_official.py` to start the API
4. Visit http://localhost:8000/docs to test endpoints

---

**Need Help?**  
Check the official Hugging Face documentation or create an issue!
