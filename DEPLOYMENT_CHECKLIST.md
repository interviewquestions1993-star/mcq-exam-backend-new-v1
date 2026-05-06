# 🚀 MCQ Exam Preparer - Deployment Checklist

## Quick Start to Get Your App Online

### ✅ Pre-Deployment Setup (Do this first!)

- [ ] Create GitHub account (free at github.com)
- [ ] Create Render account (free at render.com)
- [ ] Create Vercel account (free at vercel.com)
- [ ] Have your Hugging Face token ready: `YOUR_HF_TOKEN`

### ✅ GitHub Setup (5 minutes)

- [ ] Create repository: `mcq-exam-backend`
- [ ] Create repository: `mcq-exam-frontend`
- [ ] Push backend code to mcq-exam-backend repo
- [ ] Push frontend code to mcq-exam-frontend repo

**VS Code has built-in Git support - you can use Source Control panel (Ctrl+Shift+G)**

### ✅ Backend Deployment on Render (10 minutes)

1. [ ] Go to render.com → New Web Service
2. [ ] Connect `mcq-exam-backend` repository
3. [ ] Set Build Command: `pip install -r requirements.txt`
4. [ ] Set Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. [ ] Add Environment Variables:
   - `HF_TOKEN` = `YOUR_HF_TOKEN`
   - `HF_MODEL` = `deepseek-ai/DeepSeek-V4-Flash`
6. [ ] Click Deploy
7. [ ] **Copy your backend URL** (looks like: `https://mcq-exam-backend.onrender.com`)

### ✅ Frontend Deployment on Vercel (10 minutes)

1. [ ] Go to vercel.com → Add Project → Import
2. [ ] Select `mcq-exam-frontend` repository
3. [ ] Framework: Angular
4. [ ] Build Command: `ng build --configuration production`
5. [ ] Output Directory: `dist/mcq-exam-preparer`
6. [ ] Add Environment Variable:
   - `API_URL` = (paste your backend URL from above)
7. [ ] Click Deploy
8. [ ] **Your frontend URL** will be shown (looks like: `https://mcq-exam-frontend.vercel.app`)

### ✅ Testing Your Live App (2 minutes)

1. [ ] Open your frontend URL in browser
2. [ ] Click on a topic (e.g., Angular)
3. [ ] Verify questions load correctly
4. [ ] Answer a few questions
5. [ ] Check the results page

---

## 🎯 What You'll Get

```
Your Live MCQ App:
├── Frontend: https://mcq-exam-frontend.vercel.app
├── Backend API: https://mcq-exam-backend.onrender.com
├── Status: Available 24/7 on the internet
└── Shareable: Send the frontend link to anyone!
```

---

## 📖 Detailed Instructions

See `DEPLOYMENT_GUIDE.md` for step-by-step instructions with screenshots.

---

## ⚠️ Important Notes

1. **Render Free Tier Sleep**:
   - Your backend sleeps after 15 minutes of inactivity
   - First request after sleep takes ~30 seconds (this is normal)
   - To keep it always-on, upgrade to paid ($7/month)

2. **First Deployment**:
   - Render backend: 5-10 minutes to deploy
   - Vercel frontend: 2-5 minutes to deploy
   - Total: ~15 minutes

3. **Automatic Updates**:
   - When you push code to GitHub, both platforms automatically redeploy
   - No manual redeployment needed!

---

## 🔗 Quick Links

- [Render Dashboard](https://dashboard.render.com)
- [Vercel Dashboard](https://vercel.com/dashboard)
- [GitHub](https://github.com)
- [Hugging Face Tokens](https://huggingface.co/settings/tokens)

---

**Ready to make your app live? Follow the checklist above! 🎉**
