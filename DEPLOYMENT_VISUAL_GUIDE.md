# 🚀 VISUAL DEPLOYMENT GUIDE - Using VS Code GUI

## ✨ Good News: You Don't Need Command Line!

VS Code has an excellent built-in Git interface. Follow these visual steps to deploy your app.

---

## 📋 PART 1: Push Code to GitHub (Using VS Code)

### Step 1.1: Create GitHub Account (if needed)

1. Go to https://github.com/signup
2. Enter your email
3. Create password
4. Verify email
5. **COPY YOUR USERNAME** - you'll need it later

### Step 1.2: Create Two GitHub Repositories

**Repository 1: Backend**
1. Go to https://github.com/new
2. Repository name: `mcq-exam-backend`
3. Description: "AI-powered MCQ generator with FastAPI"
4. **Public** (easier for deployment)
5. ☐ Don't initialize with README
6. Click **Create repository**
7. **COPY THE REPOSITORY URL** (looks like: `https://github.com/YOUR_USERNAME/mcq-exam-backend.git`)

**Repository 2: Frontend**
1. Go to https://github.com/new
2. Repository name: `mcq-exam-frontend`
3. Description: "Angular Material MCQ exam frontend"
4. **Public**
5. ☐ Don't initialize with README
6. Click **Create repository**
7. **COPY THE REPOSITORY URL** (looks like: `https://github.com/YOUR_USERNAME/mcq-exam-frontend.git`)

### Step 1.3: Publish Backend to GitHub (Using VS Code)

1. **Open VS Code**
2. Go to **File** → **Open Folder**
3. Select: `d:\AI-Exam-Preparer`
4. On the left sidebar, click **Source Control** (looks like a branch icon)
   - Or press: **Ctrl+Shift+G**

5. Click **Initialize Repository**

6. In the Source Control panel, you'll see all files are "untracked"
   - Type a commit message: `Initial commit: MCQ backend with FastAPI`
   - Click the **+** button next to "Changes" to stage all files
   - Click **Commit** (or press Ctrl+Enter)

7. At the bottom left of VS Code, click the **Branch** button (shows "main")
8. Click **Publish Branch**
9. VS Code will ask for your GitHub credentials:
   - Select: "Sign in with your browser"
   - Complete the authentication
   - Return to VS Code

10. In the "Publish to GitHub" dialog:
    - Paste your backend repository URL: `https://github.com/YOUR_USERNAME/mcq-exam-backend.git`
    - **Wait for upload to complete** (might take 1-2 minutes)

✅ **Backend code is now on GitHub!**

### Step 1.4: Publish Frontend to GitHub (Using VS Code)

1. In VS Code, go to **File** → **Open Folder**
2. Select: `d:\AI-Exam-Preparer\Frontend`
3. Go to **Source Control** (Ctrl+Shift+G)

4. Click **Initialize Repository**

5. Stage and commit:
   - Type message: `Initial commit: Angular Material MCQ frontend`
   - Click **+** to stage all files
   - Click **Commit**

6. Click **Publish Branch**
   - Authenticate if prompted
   - Paste frontend repository URL: `https://github.com/YOUR_USERNAME/mcq-exam-frontend.git`

✅ **Frontend code is now on GitHub!**

---

## 🔧 PART 2: Deploy Backend on Render

### Step 2.1: Create Render Account

1. Go to https://render.com
2. Click **Sign Up**
3. Click **Continue with GitHub**
4. Authorize Render to access your GitHub account
5. Complete your profile

### Step 2.2: Deploy Backend

1. In Render dashboard, click **New +**
2. Click **Web Service**
3. Click **Connect a repository** (or "Connect repository")
4. Find and select: `mcq-exam-backend`
5. Click **Connect**

6. **Fill in the form:**
   ```
   Name: mcq-exam-backend
   Environment: Python 3
   Region: (choose closest to you)
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

7. Scroll down to **Environment**
8. Add these environment variables:
   ```
   HF_TOKEN = YOUR_HF_TOKEN
   HF_MODEL = deepseek-ai/DeepSeek-V4-Flash
   ```

9. Click **Create Web Service**

10. **Wait for deployment** (5-10 minutes)
    - Watch the logs scroll
    - Look for: `Uvicorn running on http://0.0.0.0:8000`
    - When it says **"Live"**, your backend is deployed! ✅

11. **COPY YOUR BACKEND URL** from the top of the page
    - Looks like: `https://mcq-exam-backend.onrender.com`
    - **SAVE THIS - you need it for frontend!**

---

## 🎨 PART 3: Deploy Frontend on Vercel

### Step 3.1: Create Vercel Account

1. Go to https://vercel.com
2. Click **Sign Up**
3. Click **Continue with GitHub**
4. Authorize Vercel to access your GitHub account

### Step 3.2: Deploy Frontend

1. In Vercel dashboard, click **Add New**
2. Click **Project**
3. Click **Import** next to your `mcq-exam-frontend` repository
4. If you don't see it, click **Select a Git Namespace** and choose your username

5. **Framework Settings:**
   - Framework: **Angular**
   - Build Command: `ng build --configuration production`
   - Output Directory: `dist/mcq-exam-preparer`
   - Install Command: `npm install`

6. **Environment Variables:**
   - Click **Environment Variables** (or **Add Environment Variable**)
   - Name: `API_URL`
   - Value: (paste your Render backend URL from Step 2.11)
   - Example: `https://mcq-exam-backend.onrender.com`

7. Click **Deploy**

8. **Wait for deployment** (2-5 minutes)
    - Watch the build progress
    - When it says **"Ready"**, your frontend is live! ✅

9. **GET YOUR FRONTEND URL**
    - Click on the blue domain link at the top
    - Looks like: `https://mcq-exam-frontend.vercel.app`

---

## ✅ Testing Your Live Application

### Test Backend API

1. Open browser tab
2. Go to: `https://mcq-exam-backend.onrender.com/health`
3. Should see: `{"status":"ok"}`
4. ✅ Backend is working!

### Test Frontend

1. Open your frontend URL: `https://mcq-exam-frontend.vercel.app`
2. Click on any topic (e.g., "Angular")
3. Questions should load in 3-8 seconds
4. Select answers and click "Next"
5. Submit quiz and view results
6. ✅ **Your app is live!**

---

## 🎉 Success! Your App is Online

### Your Live URLs:
```
Frontend:  https://mcq-exam-frontend.vercel.app
Backend:   https://mcq-exam-backend.onrender.com
```

### Share with Others:
Send this link to anyone: `https://mcq-exam-frontend.vercel.app`

They can use your MCQ quiz app without any installation!

---

## 🔄 Making Updates

### If you want to change something:

1. Edit your code in VS Code locally
2. Go to **Source Control** (Ctrl+Shift+G)
3. Stage files (click **+**)
4. Type commit message
5. Click **Commit**
6. Click **Sync Changes** (or **Push**)

**Automatic redeployment:**
- Render detects the push to GitHub
- Frontend redeploys automatically in 2-5 minutes
- Backend redeploys automatically in 5-10 minutes

No manual steps needed!

---

## ❓ Troubleshooting

### Questions don't load (Blank page)
- Check API_URL environment variable in Vercel
- Should be exactly: `https://mcq-exam-backend.onrender.com`
- Redeploy if you fixed it

### Backend shows error
- Check Render deployment logs
- Verify HF_TOKEN is correct
- Verify requirements.txt has all dependencies

### Deployment stuck
- Wait longer (Render free tier is slow, 5-10 min normal)
- Check the logs for error messages
- Try redeploying from Render/Vercel dashboard

### First request is slow
- This is normal! Render free tier "wakes up" on first request
- Upgrade to paid ($7/month) for always-on backend

---

## 📞 Help Resources

- **Render Help**: https://render.com/docs
- **Vercel Help**: https://vercel.com/docs
- **GitHub Help**: https://docs.github.com

---

## 🎯 You're All Set!

Your MCQ Exam Preparer app is now:
- ✅ On the internet
- ✅ Accessible 24/7
- ✅ Shareable with anyone
- ✅ Auto-updating when you push code

**Enjoy your live app! 🚀**
