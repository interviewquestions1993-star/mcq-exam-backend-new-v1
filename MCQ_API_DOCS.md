# AI Exam Preparer - MCQ API Documentation

## 🎯 Overview
The MCQ API generates multiple-choice questions for any topic using AI. Perfect for building study/exam websites.

## 📍 Base URL
```
http://localhost:8000
```

## 🔌 Endpoints

### 1. Generate MCQ Questions
**Endpoint**: `POST /api/mcq/generate`

**Request**:
```json
{
  "topic": "Angular",
  "num_questions": 5,
  "difficulty": null
}
```

**Parameters**:
- `topic` (string, required): Topic to generate questions about (e.g., "Angular", "React", "Python")
- `num_questions` (integer, optional): Number of questions to generate. Default: 5
- `difficulty` (string, optional): Filter by difficulty ("easy", "medium", "hard"). If null, generates mixed difficulty

**Response** (200 OK):
```json
{
  "topic": "Angular",
  "num_questions": 2,
  "questions": [
    {
      "id": 1,
      "question": "What is the correct way to inject a service into an Angular component?",
      "options": [
        "A) Use the @Inject decorator on the component class",
        "B) Declare the service in the component's providers array and add a constructor parameter",
        "C) Create a new instance using `new ServiceName()`",
        "D) Use the @Service decorator"
      ],
      "correct_answer": "B",
      "explanation": "Angular's dependency injection system requires services to be registered...",
      "difficulty": "medium"
    },
    {
      "id": 2,
      "question": "Which change detection strategy does NOT check the entire component tree?",
      "options": [
        "A) Default",
        "B) OnPush",
        "C) NoCheck",
        "D) ChangeDetectorRef"
      ],
      "correct_answer": "B",
      "explanation": "OnPush strategy marks the component to be checked only when...",
      "difficulty": "hard"
    }
  ],
  "status": "success"
}
```

---

### 2. Text Generation (General)
**Endpoint**: `POST /generate`

**Request**:
```json
{
  "prompt": "What is machine learning?",
  "max_new_tokens": 100,
  "temperature": 0.7,
  "top_p": 0.9
}
```

**Response** (200 OK):
```json
{
  "prompt": "What is machine learning?",
  "generated_text": "Machine learning is a subset of artificial intelligence...",
  "status": "success"
}
```

---

### 3. Chat Completions
**Endpoint**: `POST /chat`

**Request**:
```json
{
  "prompt": "Hello, how are you?",
  "max_new_tokens": 50
}
```

**Response** (200 OK):
```json
{
  "prompt": "Hello, how are you?",
  "generated_text": "Hello! I'm doing well, thank you for asking...",
  "status": "success"
}
```

---

### 4. Health Check
**Endpoint**: `GET /health`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "message": "Hugging Face Inference Backend is running"
}
```

---

## 🧪 Example Usage

### cURL
```bash
# Generate 5 Angular MCQ questions
curl -X POST http://localhost:8000/api/mcq/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Angular",
    "num_questions": 5
  }'
```

### Python
```python
import requests

response = requests.post('http://localhost:8000/api/mcq/generate', json={
    'topic': 'Angular',
    'num_questions': 5,
    'difficulty': 'medium'
})

data = response.json()
for question in data['questions']:
    print(f"Q{question['id']}: {question['question']}")
    for option in question['options']:
        print(f"  {option}")
    print(f"Answer: {question['correct_answer']}")
    print()
```

### JavaScript/TypeScript
```javascript
async function generateMCQs(topic, numQuestions = 5) {
  const response = await fetch('http://localhost:8000/api/mcq/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      topic: topic,
      num_questions: numQuestions
    })
  });
  
  const data = await response.json();
  return data.questions;
}

// Usage
const questions = await generateMCQs('React', 5);
questions.forEach(q => {
  console.log(q.question);
  console.log(q.options);
  console.log('Answer: ' + q.correct_answer);
});
```

---

## 📋 Supported Topics
Any educational topic works! Examples:
- Programming: Angular, React, Vue.js, Python, JavaScript, Java, C++
- Data Science: Machine Learning, Deep Learning, Statistics, Data Analysis
- Web: HTML, CSS, Node.js, Express, Django, Flask
- Cloud: AWS, Azure, Google Cloud, Docker, Kubernetes
- And many more!

---

## ⚙️ Configuration

**Environment Variables** (in `.env`):
```
HF_TOKEN=your_hugging_face_token
HF_MODEL=deepseek-ai/DeepSeek-V4-Flash
API_PORT=8000
API_HOST=0.0.0.0
```

---

## 📊 API Limits & Notes
- **Max Questions per Request**: 20 (recommended: 5-10)
- **Timeout**: 120 seconds per request
- **Generation Time**: ~5-15 seconds per question (varies by complexity)
- **Temperature**: Controls randomness (0.0 = deterministic, 1.0+ = random)
- **Model**: DeepSeek-V4-Flash (fast, free tier available)

---

## 🚀 Next Steps
1. **Frontend Integration**: Use the API in your React/Vue/Angular app
2. **Database**: Store generated questions for caching
3. **User Tracking**: Track which questions users answered
4. **Scoring**: Calculate scores based on answers
5. **Analytics**: Track performance by topic/difficulty

---

## 🐛 Error Handling
```json
{
  "detail": "MCQ generation failed: error message"
}
```

Common errors:
- **400**: Invalid request parameters
- **500**: Generation failed (check backend logs)
- **503**: Hugging Face service temporarily unavailable

---

## 📞 Support
- Check backend logs: `python main.py 2>&1`
- Test endpoint: `curl http://localhost:8000/health`
- Verify token: Check `.env` file for valid HF_TOKEN
