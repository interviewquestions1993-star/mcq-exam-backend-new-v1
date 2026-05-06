# 🚀 START HERE - Deploy Your App in 3 Easy Steps

## ⏱️ Time Required: ~30 minutes
## 💰 Cost: $0 (free tier)
## 🎯 Goal: Get your app live on the internet

---

## 🎬 Watch This First (Optional)

If you're new to GitHub/Render/Vercel, watch these 2-minute videos:
- GitHub basics: https://www.youtube.com/watch?v=0fKg7e37bQE
- Deploying to Vercel: https://www.youtube.com/watch?v=ZjAqacIm9bQ

---

## 📋 QUICK STEP-BY-STEP

### **Step 1: Create GitHub Account & Repositories (5 min)**

1. Go to https://github.com/signup
   - Create account (it's free!)
   - Verify your email
   - **REMEMBER YOUR USERNAME**

2. Create two repositories:
   - Go to https://github.com/new
   
   **Repository 1:**
   - Name: `mcq-exam-backend`
   - Make it Public
   - Create repo
   - **Copy the URL** (github.com/YOUR_USERNAME/mcq-exam-backend.git)
   
   **Repository 2:**
   - Go to https://github.com/new
   - Name: `mcq-exam-frontend`
   - Make it Public
   - Create repo
   - **Copy the URL** (github.com/YOUR_USERNAME/mcq-exam-frontend.git)

### **Step 2: Push Your Code to GitHub (Using VS Code) (10 min)**

#### Push Backend:

1. Open VS Code
2. Click **File** → **Open Folder**
3. Choose: `d:\AI-Exam-Preparer`
4. Press **Ctrl+Shift+G** (Source Control)
5. Click **Initialize Repository**
6. In the message box, type: `Initial commit: MCQ backend`
7. Click **+** to stage all files
8. Click **Commit**
9. Click **Publish Branch**
10. Sign in with GitHub (if needed)
11. Paste your backend URL and confirm

#### Push Frontend:

1. File → Open Folder → `d:\AI-Exam-Preparer\Frontend`
2. Press Ctrl+Shift+G
3. Initialize, commit, publish (same steps as above)
4. Paste frontend URL and confirm

✅ **Both repos are now on GitHub!**

### **Step 3: Deploy Backend on Render (10 min)**

1. Go to https://render.com
2. Sign up with GitHub
3. Click **New +** → **Web Service**
4. Click **Connect a repository**
5. Select `mcq-exam-backend`
6. Fill in:
   ```
   Name: mcq-exam-backend
   Build: pip install -r requirements.txt
   Start: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
7. Scroll to **Environment** and add:
   ```
   HF_TOKEN = YOUR_HF_TOKEN
   HF_MODEL = deepseek-ai/DeepSeek-V4-Flash
   ```
8. Click **Create Web Service**
9. Wait for it to say **"Live"** (5-10 minutes)
10. **Copy your backend URL** from the top
    - Looks like: `https://mcq-exam-backend.onrender.com`

### **Step 4: Deploy Frontend on Vercel (5 min)**

1. Go to https://vercel.com
2. Sign up with GitHub
3. Click **Add New** → **Project**
4. Click **Import** next to `mcq-exam-frontend`
5. Settings should auto-fill:
   - Framework: Angular ✅
   - Build: ng build --configuration production ✅
   - Output: dist/mcq-exam-preparer ✅
6. Click **Environment Variables**
7. Add:
   ```
   API_URL = (paste your Render URL from Step 3)
   Example: https://mcq-exam-backend.onrender.com
   ```
8. Click **Deploy**
9. Wait for it to say **"Ready"** (2-5 minutes)
10. Click the blue domain link - **That's your app!** 🎉

---

## 🎯 Done! Your App is Live!

### Your URLs:
```
Frontend: https://mcq-exam-frontend.vercel.app
Backend:  https://mcq-exam-backend.onrender.com
```

### Test it:
- Open your frontend URL
- Click a topic
- Answer quiz questions
- See results

### Share it:
- Send the frontend URL to anyone
- They can use it in their browser
- No installation needed!

---

## 📖 Need More Details?

- **Visual step-by-step guide**: See `DEPLOYMENT_VISUAL_GUIDE.md`
- **Complete guide with pictures**: See `DEPLOYMENT_GUIDE.md`
- **Architecture diagram**: See `ARCHITECTURE.md`

---

## ⚡ Pro Tips

1. **Render free tier sleeps after 15 min**
   - First request takes 30 sec (normal)
   - Upgrade to $7/month to fix

2. **Push updates automatically redeploy**
   - Change code locally
   - Commit & push in VS Code (Ctrl+Shift+G)
   - Platforms auto-redeploy in 5-10 min
   - No manual action needed!

3. **Need help?**
   - Check browser console (F12)
   - Check Render logs in dashboard
   - Check Vercel logs in dashboard

---

## ✨ That's It!

Your app is production-ready and online. Anyone in the world can now use it! 🌍

**Any questions? Refer to the detailed guides in this folder.**

---

**Let's get your app live! 🚀**
