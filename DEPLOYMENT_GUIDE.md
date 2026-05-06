# MCQ Exam Preparer - Deployment Guide

## 🚀 Deployment Overview

This guide walks you through deploying the MCQ Exam Preparer application to the internet using:
- **Backend**: Render.com (Free tier)
- **Frontend**: Vercel.com (Free tier)

## 📋 Prerequisites

Before starting, you need:
1. **GitHub Account** - For version control ([Sign up free](https://github.com/signup))
2. **Render Account** - For backend hosting ([Sign up free](https://render.com))
3. **Vercel Account** - For frontend hosting ([Sign up free](https://vercel.com))
4. **Hugging Face API Token** - You already have this (YOUR_HF_TOKEN)

---

## 📤 Part 1: Push Code to GitHub

### Step 1.1: Create Two GitHub Repositories

1. Go to [github.com/new](https://github.com/new)
2. **Create first repository**: `mcq-exam-backend`
   - Description: "AI-powered MCQ generator backend with FastAPI"
   - Public (easier for deployment)
   - Click "Create repository"

3. Repeat and create second repository: `mcq-exam-frontend`
   - Description: "Angular + Material Design MCQ exam frontend"
   - Public
   - Click "Create repository"

### Step 1.2: Push Backend Code

Open VS Code Terminal (Frontend folder):

```powershell
# Navigate to backend folder
cd d:\AI-Exam-Preparer

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: MCQ backend with FastAPI and Hugging Face integration"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/mcq-exam-backend.git
git push -u origin main
```

### Step 1.3: Push Frontend Code

```powershell
# Navigate to frontend folder
cd d:\AI-Exam-Preparer\Frontend

# Initialize git
git init
git add .
git commit -m "Initial commit: Angular Material MCQ frontend"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/mcq-exam-frontend.git
git push -u origin main
```

---

## 🔧 Part 2: Deploy Backend to Render

### Step 2.1: Connect Render to Backend Repository

1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect a repository"**
4. Search for `mcq-exam-backend` and connect it
5. Fill in the form:
   - **Name**: `mcq-exam-backend` (or your preference)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 2.2: Add Environment Variables

Under **"Environment"** section, add these variables:

```
HF_TOKEN = YOUR_HF_TOKEN
HF_MODEL = deepseek-ai/DeepSeek-V4-Flash
API_PORT = 8000
API_HOST = 0.0.0.0
```

### Step 2.3: Deploy

1. Scroll down and click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Deploy the application
3. Wait for deployment to complete (5-10 minutes)
4. You'll get a URL like: `https://mcq-exam-backend.onrender.com`

**Save this URL!** You'll need it for the frontend.

---

## 🎨 Part 3: Deploy Frontend to Vercel

### Step 3.1: Import Frontend Repository

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New"** → **"Project"**
3. Click **"Import"** next to your GitHub repository
4. Search for `mcq-exam-frontend` and select it
5. Click **"Import"**

### Step 3.2: Configure Build Settings

When prompted, modify these settings:

- **Framework Preset**: Angular
- **Build Command**: `ng build --configuration production`
- **Output Directory**: `dist/mcq-exam-preparer`
- **Install Command**: `npm install`

### Step 3.3: Add Environment Variables

In the "Environment Variables" section, add:

```
API_URL = https://mcq-exam-backend.onrender.com
```

(Replace with your actual Render backend URL from Step 2.4)

### Step 3.4: Deploy

1. Click **"Deploy"**
2. Vercel will:
   - Build your Angular application
   - Deploy to their CDN
   - Provide you with a live URL
3. Wait for deployment (2-5 minutes)
4. You'll get a URL like: `https://mcq-exam-frontend.vercel.app`

---

## ✅ Verification

### Test Your Deployment

1. Open your frontend URL: `https://mcq-exam-frontend.vercel.app`
2. Select a topic (e.g., "Angular")
3. Start a quiz
4. Verify that questions load (from your backend)
5. Complete the quiz and check results

### If Questions Don't Load

**Issue**: "Failed to load questions"

**Solution**: Check if backend API URL is correct
```powershell
# Test your backend API directly
curl https://mcq-exam-backend.onrender.com/health
```

If this fails, redeploy frontend with correct `API_URL` environment variable.

---

## 📝 Troubleshooting

### Backend Issues

| Problem | Solution |
|---------|----------|
| Deployment fails | Check that `requirements.txt` exists and has all dependencies |
| Build is slow | Render free tier is slower; this is normal (5-10 min) |
| API returns 403 | Check that `HF_TOKEN` environment variable is set correctly |
| API returns 500 | Check backend logs in Render dashboard |

### Frontend Issues

| Problem | Solution |
|---------|----------|
| Blank page on load | Check browser console for errors |
| Questions don't load | Verify `API_URL` environment variable is correct |
| CORS errors | Backend CORS is already enabled in `main.py` |

---

## 🔄 Making Updates

### To update your deployed application:

1. **Make changes locally** in VS Code
2. **Push to GitHub**:
   ```powershell
   git add .
   git commit -m "Description of changes"
   git push
   ```
3. **Automatic redeployment**:
   - Render watches your GitHub repo (backend)
   - Vercel watches your GitHub repo (frontend)
   - Both will automatically redeploy on new commits

---

## 🎯 Final URLs

Once deployed, you'll have:

- **Frontend**: `https://mcq-exam-frontend.vercel.app` ✅
- **Backend API**: `https://mcq-exam-backend.onrender.com` ✅
- **Backend Health Check**: `https://mcq-exam-backend.onrender.com/health`
- **Backend MCQ API**: `https://mcq-exam-backend.onrender.com/api/mcq/generate`

**Share your frontend URL with anyone to let them use your MCQ app!** 🎓

---

## 💡 Pro Tips

1. **Free tier limitations**:
   - Render free tier sleeps after 15 minutes of inactivity
   - First request after sleep takes 30 seconds (normal)
   - Vercel has no sleep timeout

2. **Upgrade if needed**:
   - Render paid plan: $7/month for always-on backend
   - Vercel paid plan: Pay as you go (usually free for small apps)

3. **Custom domain**:
   - Render allows custom domain on paid plans
   - Vercel allows free custom domain setup

---

## 📞 Support Resources

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Angular Build Optimization**: https://angular.io/guide/build
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/

---

**Your MCQ Exam Preparer is now live on the internet! 🚀**
