# 🎓 AI-Powered MCQ Exam Preparer

**Status:** ✅ Ready to Deploy | **Frontend + Backend Complete** | **Free Cloud Ready**

A full-stack application for generating AI-powered multiple choice questions using Hugging Face models. Includes Angular Material frontend and FastAPI backend.

## Features

- ✅ **AI-Powered MCQs**: Hugging Face (DeepSeek-V4-Flash) generates questions
- ✅ **5 Questions per Quiz**: Customizable difficulty levels
- ✅ **Instant Explanations**: AI-generated explanations for each answer
- ✅ **Beautiful UI**: HackerRank-style Material Design
- ✅ **Responsive Design**: Works on mobile, tablet, desktop
- ✅ **Zero Database**: Session storage only (zero setup!)
- ✅ **Deploy Free**: Render (backend) + Vercel (frontend)
- ✅ **CORS Enabled**: Frontend-backend communication

## Quick Start

### 1. Prerequisites

- Python 3.9+
- Hugging Face Account (free)
- API Token from Hugging Face

### 2. Create Hugging Face Token

1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Create a new token with "Read" permissions
3. Copy your token

### 3. Setup Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Update .env file with your token
# Edit the HF_TOKEN value in .env
```

**File: `.env`**
```
HF_TOKEN=your_token_here
HF_MODEL=google/gemma-2-2b-it
API_PORT=8000
API_HOST=0.0.0.0
```

### 4. Run the Backend

```bash
python main.py
```

The API will be available at: `http://localhost:8000`

### 5. Test the API

In another terminal:

```bash
python test_api.py
```

Or use the Swagger UI: `http://localhost:8000/docs`

## API Endpoints

### 1. Health Check
```
GET /
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Hugging Face Inference Backend is running"
}
```

### 2. Generate Text
```
POST /generate
```

**Request Body:**
```json
{
  "prompt": "What is artificial intelligence?",
  "max_new_tokens": 100,
  "temperature": 0.7,
  "top_p": 0.9
}
```

**Response:**
```json
{
  "prompt": "What is artificial intelligence?",
  "generated_text": "Artificial intelligence (AI) is the simulation of human intelligence...",
  "status": "success"
}
```

### 3. Summarize Text
```
POST /summarize
```

**Request Body:**
```json
{
  "text": "Hugging Face is a company that develops tools for building machine learning applications. The company is most notable for its Transformers library..."
}
```

**Response:**
```json
{
  "original_text": "Hugging Face is a company...",
  "summary": "Hugging Face develops ML tools with a focus on Transformers library.",
  "status": "success"
}
```

### 4. Chat
```
POST /chat
```

**Request Body:**
```json
{
  "prompt": "Explain neural networks in simple terms",
  "max_new_tokens": 150,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "prompt": "Explain neural networks in simple terms",
  "generated_text": "Neural networks are computer systems inspired by biological neurons...",
  "status": "success"
}
```

## Parameters Explained

### Text Generation Parameters

- **prompt** (string, required): Input text to generate from
- **max_new_tokens** (integer, default: 100): Maximum tokens to generate
- **temperature** (float, default: 0.7): Controls randomness
  - 0.0 = deterministic (same output every time)
  - 0.7 = balanced (creative but coherent)
  - 1.0+ = very random
- **top_p** (float, default: 0.9): Nucleus sampling - filters to top p% of tokens

## Models Available

You can change the model by updating `HF_MODEL` in `.env`:

- `google/gemma-2-2b-it` (2B, fast, CPU-friendly) - Default
- `meta-llama/Llama-3.1-8B-Instruct` (8B, more capable)
- `mistralai/Mistral-7B-Instruct-v0.1` (7B, balanced)

For summarization:
- `facebook/bart-large-cnn` (default)

## Error Handling

The backend automatically handles:

1. **503 - Model Loading (Cold Start)**
   - Automatically retries with exponential backoff
   - First request may take 30-60 seconds

2. **429 - Rate Limited**
   - Automatically adds delay between requests

3. **Connection Errors**
   - Retries up to 3 times with exponential backoff

## Example Usage with Python

```python
import requests

url = "http://localhost:8000/generate"
payload = {
    "prompt": "What is machine learning?",
    "max_new_tokens": 100,
    "temperature": 0.7
}

response = requests.post(url, json=payload)
result = response.json()
print(result['generated_text'])
```

## Example Usage with JavaScript

```javascript
const response = await fetch('http://localhost:8000/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: "What is machine learning?",
    max_new_tokens: 100,
    temperature: 0.7
  })
});

const data = await response.json();
console.log(data.generated_text);
```

## Project Structure

```
.
├── main.py              # FastAPI application and routes
├── hf_inference.py      # Hugging Face API wrapper
├── config.py            # Configuration and environment variables
├── test_api.py          # API test script
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (with your token)
└── README.md            # This file
```

## Troubleshooting

### 1. "HF_TOKEN not found" Error
- Check `.env` file has your token
- Make sure file is in the same directory as `config.py`

### 2. "Model is loading" (503 Error)
- This is normal on first request
- Backend automatically waits and retries
- Subsequent requests will be faster

### 3. Connection Refused
- Make sure backend is running: `python main.py`
- Check port 8000 is not in use
- Change `API_PORT` in `.env` if needed

### 4. Timeout Errors
- First request may take 30-60 seconds (model loading)
- Increase timeout in test script if needed
- Use simpler models for faster responses

### 5. Rate Limited (429 Error)
- Free tier has rate limits
- Backend automatically handles retries
- Space out requests or use HF Pro tier

## Performance Tips

1. **Reduce max_new_tokens** for faster responses
2. **Use smaller models** (2B vs 7B) for CPU-friendly deployment
3. **Batch multiple prompts** into one request
4. **Cache results** if asking similar questions
5. **Use lower temperature** (0.1-0.3) for deterministic output

## Security Notes

⚠️ **Important:**
- Never commit `.env` file to version control
- Add `.env` to `.gitignore`
- Rotate your token if it's exposed
- Use environment variables in production instead of `.env`

## Supported Tasks

- Text Generation
- Summarization
- Question Answering
- Text Classification
- Translation (with appropriate model)

## Cost Information

- **Free Tier**: Limited API calls
- **Pro Plan**: $9/month (more calls)
- **Dedicated Endpoints**: Starting at $0.06/hour (CPU)

## References

- [Hugging Face Inference API Docs](https://huggingface.co/docs/api-inference)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Hugging Face Model Hub](https://huggingface.co/models)

## License

MIT

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Hugging Face API documentation
3. Check FastAPI documentation
