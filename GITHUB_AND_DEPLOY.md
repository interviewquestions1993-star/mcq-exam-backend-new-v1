# 🚀 Deploy Your App - Step by Step

## Current Status ✅
- **Backend**: Git repo initialized, code committed, remote configured
  - Remote: `https://github.com/Architect-Ameer/mcq-exam-backend.git`
  - Commit: `381963a - Initial commit: MCQ backend with FastAPI`
  
- **Frontend**: Git repo initialized, code committed, remote configured
  - Remote: `https://github.com/Architect-Ameer/mcq-exam-frontend.git`
  - Commit: Angular Material MCQ frontend

---

## Step 1: Create GitHub Repositories (5 minutes)

### Backend Repository:
1. Go to https://github.com/new
2. **Repository name**: `mcq-exam-backend`
3. **Description**: MCQ exam backend with FastAPI and Hugging Face AI
4. **Public** ✓ (important - must be public for Render)
5. **DO NOT** initialize with README, gitignore, or license
6. Click **Create repository**
7. **COPY THIS URL**: `https://github.com/Architect-Ameer/mcq-exam-backend.git`

### Frontend Repository:
1. Go to https://github.com/new
2. **Repository name**: `mcq-exam-frontend`
3. **Description**: MCQ exam Angular Material frontend
4. **Public** ✓ (important - must be public for Vercel)
5. **DO NOT** initialize with anything
6. Click **Create repository**
7. **COPY THIS URL**: `https://github.com/Architect-Ameer/mcq-exam-frontend.git`

✅ **Once both repos are created, say "repos created" and I'll push the code**

---

## Step 2: Push Code to GitHub (automated when you say "repos created")

```powershell
# Backend push
cd d:\AI-Exam-Preparer
git push -u origin main

# Frontend push  
cd d:\AI-Exam-Preparer\Frontend
git push -u origin main
```

---

## Step 3: Deploy to Render (Backend) - 10 minutes

1. Go to https://render.com
2. Click **Sign up** → **Continue with GitHub**
3. Authorize Render to access your GitHub
4. Click **New +** → **Web Service**
5. Click **Connect a repository**
6. Select `mcq-exam-backend`
7. Fill in the form:
   ```
   Name: mcq-exam-backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
8. Scroll down to **Environment Variables** and add:
   ```
   HF_TOKEN = YOUR_HF_TOKEN
   HF_MODEL = deepseek-ai/DeepSeek-V4-Flash
   ```
9. Click **Create Web Service**
10. **Wait 5-10 minutes** until status shows **Live** ✅
11. **COPY YOUR BACKEND URL** from the top (looks like `https://mcq-exam-backend.onrender.com`)

---

## Step 4: Deploy to Vercel (Frontend) - 5 minutes

1. Go to https://vercel.com
2. Click **Sign up** → **Continue with GitHub**  
3. Authorize Vercel
4. Click **Add New** → **Project**
5. Find and click **Import** on `mcq-exam-frontend`
6. Settings will auto-fill (Framework: Angular, Build: `ng build --configuration production`)
7. Scroll to **Environment Variables**
8. Add one variable:
   ```
   Key: API_URL
   Value: (paste your Render URL from Step 3)
   Example: https://mcq-exam-backend.onrender.com
   ```
9. Click **Deploy**
10. **Wait 2-5 minutes** for deployment to complete
11. Click the **blue domain link** when ready

---

## Your Live URLs 🌍

Once deployed, you'll have:
```
Frontend: https://mcq-exam-frontend.vercel.app (or similar)
Backend:  https://mcq-exam-backend.onrender.com (or similar)
```

**Share the frontend URL with anyone! They can use your app in their browser.**

---

## ⚡ Important Notes

1. **Free tier Render limitation**: App sleeps after 15 minutes of inactivity
   - First request after sleep takes 30 seconds (normal)
   - To avoid this, upgrade to paid tier ($7/month)

2. **Auto-redeploy**: Future updates are automatic!
   - Make code changes locally
   - `git commit` and `git push`
   - Render/Vercel auto-redeploy in 5-10 minutes

3. **Custom domain**: You can add your own domain later in platform settings

4. **Environment secrets**: Keep your HF_TOKEN secure - never commit it to git

---

## 📋 Next Actions

1. ✅ Create 2 GitHub repositories (public)
2. ✅ Push code (I'll do this when repos are ready)
3. ✅ Deploy to Render (backend)
4. ✅ Deploy to Vercel (frontend)
5. ✅ Test the live app

---

**Ready? Go create those GitHub repos and let me know when they're ready!**
