# MCQ Exam Preparer - Architecture & Deployment Diagram

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          DEPLOYED ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────────────┘

                                   INTERNET
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
              ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
              │  End Users   │  │  Browsers    │  │  Mobile      │
              │ (Students)   │  │  (Chrome,    │  │  Users       │
              │              │  │   Safari)    │  │              │
              └──────────────┘  └──────────────┘  └──────────────┘
                    │                 │                 │
                    └─────────────────┼─────────────────┘
                                      │
                         https://mcq-exam-frontend.vercel.app
                                      │
                    ┌─────────────────▼─────────────────┐
                    │                                   │
                    │      VERCEL (Frontend Hosting)    │
                    │      ✅ Angular Application       │
                    │      ✅ Material Design UI        │
                    │      ✅ Automatic HTTPS           │
                    │      ✅ Global CDN Distribution   │
                    │                                   │
                    └─────────────────┬─────────────────┘
                                      │
                         API Request: /api/mcq/generate
                                      │
                    ┌─────────────────▼─────────────────┐
                    │                                   │
                    │      RENDER (Backend Hosting)     │
                    │      ✅ FastAPI Server            │
                    │      ✅ Python 3.11              │
                    │      ✅ Automatic HTTPS           │
                    │      ✅ Environment Variables     │
                    │                                   │
        https://mcq-exam-backend.onrender.com           │
                    │                                   │
                    └─────────────────┬─────────────────┘
                                      │
                         API Call: Generate MCQ
                                      │
                    ┌─────────────────▼─────────────────┐
                    │                                   │
                    │   HUGGING FACE INFERENCE API      │
                    │   ✅ DeepSeek-V4-Flash Model      │
                    │   ✅ OpenAI-compatible endpoint   │
                    │   ✅ Free tier via Groq provider  │
                    │   ✅ HF Token: hf_zSb...          │
                    │                                   │
                    └─────────────────┬─────────────────┘
                                      │
                         AI Response: MCQ Questions
                                      │
                    ┌─────────────────▼─────────────────┐
                    │   Response to Frontend            │
                    │   - Questions                     │
                    │   - Options                       │
                    │   - Difficulty Levels             │
                    │   - Explanations                  │
                    └─────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagram

```
┌───────────────────────────────────────────────────────────────┐
│                      USER JOURNEY                             │
└───────────────────────────────────────────────────────────────┘

1. BROWSE
   └─→ Open: https://mcq-exam-frontend.vercel.app
   └─→ Home Page: Select Topic (Angular, React, Python, etc.)

2. QUIZ REQUEST
   └─→ Frontend sends: POST /api/mcq/generate
   └─→ Backend receives request
   └─→ Backend sends request to Hugging Face API
   └─→ AI generates questions
   └─→ Backend returns JSON response

3. DISPLAY QUESTIONS
   └─→ Frontend receives questions
   └─→ Shows Question 1/5 with options
   └─→ User selects answer

4. NAVIGATION
   └─→ User clicks Next → Show next question
   └─→ Progress bar updates
   └─→ All answers stored in browser

5. SUBMIT
   └─→ User clicks Submit Quiz
   └─→ Frontend calculates score
   └─→ Results page shows: Score, Breakdown, Explanations

6. REVIEW
   └─→ See all questions with correct/incorrect marks
   └─→ Read AI explanations for each answer
   └─→ Retake or go home
```

---

## 📊 Technology Stack

### Frontend (Vercel)
```
Angular 19.0.0           - Framework
Material Design 19.0.0   - UI Components
TypeScript 5.6           - Language
RxJS 7.8.0              - Reactive Programming
Node.js                 - Build toolchain
```

### Backend (Render)
```
FastAPI 0.104.1         - Web Framework
Python 3.11             - Runtime
Uvicorn 0.24.0          - ASGI Server
Pydantic 2.5.0          - Data Validation
OpenAI SDK 1.3.5        - Hugging Face Integration
```

### AI Engine (Hugging Face)
```
DeepSeek-V4-Flash       - Language Model
Router Endpoint         - Multi-provider routing
Groq Provider           - Free tier inference
```

---

## 🌍 Deployment Infrastructure

### Frontend Deployment (Vercel)
```
Vercel CDN (Global)
  ├─ Automatic HTTPS
  ├─ Auto-scaling
  ├─ 99.9% uptime SLA
  ├─ Git integration (auto-deploy)
  └─ Custom domain support
```

### Backend Deployment (Render)
```
Render Web Service
  ├─ Automatic HTTPS
  ├─ Auto-restart on crash
  ├─ Environment variables
  ├─ Custom domains (paid)
  └─ Auto-deploy from GitHub
```

### API Communication
```
Frontend → Backend: HTTPS REST API
Backend → Hugging Face: HTTPS with Bearer Token
CORS: Enabled on Backend for Frontend domain
```

---

## 📈 Performance Expectations

### Frontend (Vercel)
- Page load: < 2 seconds
- Interactive: < 3 seconds
- Time to First Paint: < 1 second

### Backend (Render)
- API response: 3-8 seconds (first request after sleep)
- Subsequent requests: 2-4 seconds
- Free tier: Sleeps after 15 min inactivity

### AI Model (Hugging Face)
- Generation time: 2-5 seconds per question
- Batch generation: 5-15 seconds for 5 questions

### Total Quiz Loading
- First load: 5-10 seconds
- Subsequent loads: 2-5 seconds

---

## 🔐 Security Measures

✅ **HTTPS**: All connections encrypted
✅ **CORS**: Backend only accepts requests from frontend
✅ **Environment Variables**: Secrets not in code
✅ **API Token**: Hugging Face token stored securely in backend
✅ **No Authentication Needed**: Fully public API (suitable for demo)

---

## 💰 Cost Breakdown

### Free Tier (No cost)
```
Vercel Frontend:        $0/month (unlimited)
Render Backend:         $0/month (free tier)
Hugging Face AI:        $0/month (free tier via Groq)
Total:                  $0/month ✅
```

### Recommended Upgrade (For production)
```
Vercel (if needed):     $20-100/month (Pro plan)
Render Backend:         $7/month (starter plan, always-on)
Hugging Face (if needed): Pay per usage
Total:                  ~$10-15/month for reliable service
```

---

## 📋 Monitoring & Logs

### Vercel Dashboard
- Deployment logs: https://vercel.com/dashboard
- Performance metrics
- Function invocations

### Render Dashboard
- Backend logs: https://dashboard.render.com
- Service health
- Resource usage

### How to Debug
1. Check Vercel logs for frontend issues
2. Check Render logs for API errors
3. Check browser console (F12) for client errors
4. Test API directly: `curl https://mcq-exam-backend.onrender.com/health`

---

## 🚀 Scaling Opportunities

### Phase 2: User Authentication
- Add login/registration
- Track user progress
- Store quiz history
- Personalized recommendations

### Phase 3: Database Integration
- PostgreSQL on Railway
- Store user accounts
- Archive quiz results
- Analytics dashboard

### Phase 4: Advanced Features
- Difficulty level selection
- Timed quizzes
- Leaderboards
- AI explanation generation
- Multiple languages

---

## 📞 Quick Reference

| Component | URL | Status |
|-----------|-----|--------|
| Frontend | https://mcq-exam-frontend.vercel.app | Will be live after deployment |
| Backend API | https://mcq-exam-backend.onrender.com | Will be live after deployment |
| Health Check | https://mcq-exam-backend.onrender.com/health | Verify backend is running |
| MCQ Endpoint | https://mcq-exam-backend.onrender.com/api/mcq/generate | Use for quiz questions |

---

**Your complete cloud infrastructure is ready to deploy! 🎉**
