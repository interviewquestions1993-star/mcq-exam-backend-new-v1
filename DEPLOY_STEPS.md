# 🚀 Deploy Your MCQ App - 5 Simple Steps

## Your Repositories Are Ready!

✅ **Backend:** `d:\AI-Exam-Preparer` (git initialized, committed, ready to push)
✅ **Frontend:** `d:\AI-Exam-Preparer\Frontend` (git initialized, committed, ready to push)
✅ **GitHub Username:** `Architect-Ameer`

---

## Step 1: Create GitHub Repositories (2 min)

### Create Backend Repo:
1. Go to https://github.com/new
2. **Repository name:** `mcq-exam-backend`
3. Make it **Public** ✓
4. **Do NOT** initialize with README
5. Click **Create repository**
6. Copy the HTTPS URL (looks like: `https://github.com/Architect-Ameer/mcq-exam-backend.git`)

### Create Frontend Repo:
1. Go to https://github.com/new
2. **Repository name:** `mcq-exam-frontend`
3. Make it **Public** ✓
4. **Do NOT** initialize with README
5. Click **Create repository**
6. Copy the HTTPS URL

---

## Step 2: Push Code to GitHub (5 min)

### Push Backend:
Open Terminal/PowerShell:
```powershell
cd d:\AI-Exam-Preparer
& "C:\Program Files\Git\cmd\git.exe" push -u origin main
```
When prompted for password, use a **Personal Access Token** (not your password):
1. Go to https://github.com/settings/tokens
2. Click **Generate new token (classic)**
3. Give it a name like "Deploy Token"
4. Check ✓ `repo` permission
5. Click **Generate token**
6. **Copy the token** (you won't see it again!)
7. Paste it when Git asks for password

### Push Frontend:
```powershell
cd d:\AI-Exam-Preparer\Frontend
& "C:\Program Files\Git\cmd\git.exe" push -u origin main
```
Use the same token as above.

---

## Step 3: Deploy Backend on Render (10 min)

1. Go to https://render.com
2. Sign up with GitHub (recommended)
3. Click **New +** → **Web Service**
4. Click **Connect a repository**
5. Select `mcq-exam-backend`
6. Fill in:
   ```
   Name:  mcq-exam-backend
   Build: pip install -r requirements.txt
   Start: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
7. Scroll to **Environment**
8. Add these variables:
   ```
   HF_TOKEN = YOUR_HF_TOKEN
   HF_MODEL = deepseek-ai/DeepSeek-V4-Flash
   ```
9. Click **Create Web Service**
10. Wait for it to say **"Live"** (5-10 minutes)
11. **Copy your backend URL** from the top (e.g., `https://mcq-exam-backend.onrender.com`)

---

## Step 4: Deploy Frontend on Vercel (5 min)

1. Go to https://vercel.com
2. Sign up with GitHub (recommended)
3. Click **Add New** → **Project**
4. Click **Import** next to `mcq-exam-frontend`
5. Framework should auto-select **Angular** ✓
6. Click **Environment Variables**
7. Add one variable:
   ```
   API_URL = (paste your Render backend URL from Step 3)
   Example: https://mcq-exam-backend.onrender.com
   ```
8. Click **Deploy**
9. Wait for it to say **"Ready"** (2-5 minutes)
10. Click the blue domain link - **That's your live app!** 🎉

---

## Step 5: Test Your Live App (2 min)

1. Open the Vercel frontend URL in your browser
2. Click a topic (e.g., "Angular")
3. Answer the 5 questions
4. Click "Submit"
5. See your results with explanations
6. **Success!** 🎊

---

## Your Live URLs

```
Frontend: https://mcq-exam-frontend.vercel.app
Backend:  https://mcq-exam-backend.onrender.com
```

---

## Troubleshooting

### "Push rejected"
- Make sure GitHub repo is created and is PUBLIC
- Use Personal Access Token, not password

### "Build failed on Render"
- Check the build logs in Render dashboard
- Make sure `requirements.txt` is correct
- Verify `HF_TOKEN` is set

### "Frontend can't connect to backend"
- Make sure `API_URL` is set in Vercel
- Check the backend URL is correct in Vercel settings
- Wait 5 minutes - Vercel needs to rebuild after env change

### Questions?
- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- GitHub Docs: https://docs.github.com

---

**You've got this! 🚀 Good luck with your deployment!**
