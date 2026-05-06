# 🚀 Deployment Instructions

**Your app is ready!** Follow these steps to deploy to the internet.

---

## ⏱️ Total Time: ~30 minutes

---

## Step 1: Create GitHub Repositories (2 min)

### Backend Repository:
1. Go to https://github.com/new
2. **Repository name:** `mcq-exam-backend`
3. **Visibility:** Public
4. **Do NOT** initialize with README
5. Click **Create repository**

### Frontend Repository:
1. Go to https://github.com/new
2. **Repository name:** `mcq-exam-frontend`
3. **Visibility:** Public
4. **Do NOT** initialize with README
5. Click **Create repository**

---

## Step 2: Push Code to GitHub (5 min)

### Create Personal Access Token:
1. Go to https://github.com/settings/tokens
2. Click **Generate new token (classic)**
3. **Token name:** `deploy-token`
4. **Expiration:** 90 days
5. ✅ Check `repo` permission
6. Click **Generate token**
7. **Copy the token** (save it!)

### Push Backend:
```powershell
cd d:\AI-Exam-Preparer
& "C:\Program Files\Git\cmd\git.exe" push -u origin main
```
When prompted:
- **Username:** Your GitHub username (`Architect-Ameer`)
- **Password:** Paste the Personal Access Token

### Push Frontend:
```powershell
cd d:\AI-Exam-Preparer\Frontend
& "C:\Program Files\Git\cmd\git.exe" push -u origin main
```
Use the same token.

---

## Step 3: Deploy Backend on Render (10 min)

1. Go to https://render.com
2. Sign up with GitHub
3. Click **New +**
4. Select **Web Service**
5. Click **Connect Repository**
6. Select `mcq-exam-backend`
7. Fill in the form:
   - **Name:** `mcq-exam-backend`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
8. Scroll to **Environment Variables**
9. Add these:
   ```
   HF_TOKEN = YOUR_HF_TOKEN
   HF_MODEL = deepseek-ai/DeepSeek-V4-Flash
   ```
10. Click **Create Web Service**
11. Wait for status to turn **"Live"** (5-10 minutes)
12. **Copy your backend URL** from the top (example: `https://mcq-exam-backend.onrender.com`)

---

## Step 4: Deploy Frontend on Vercel (5 min)

1. Go to https://vercel.com
2. Sign up with GitHub
3. Click **Add New**
4. Select **Project**
5. Click **Import Project**
6. Select `mcq-exam-frontend`
7. Settings should auto-fill:
   - **Framework Preset:** Angular
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist/mcq-exam-preparer`
8. Click **Environment Variables**
9. Add one variable:
   ```
   API_URL = (paste the Render backend URL from Step 3)
   ```
   Example: `https://mcq-exam-backend.onrender.com`

10. Click **Deploy**
11. Wait for status to turn **"Ready"** (2-5 minutes)
12. Click the **blue domain link** to open your app 🎉

---

## Step 5: Test Your Live App (2 min)

1. Open the Vercel frontend URL
2. Click on a topic (e.g., "Angular")
3. Wait for 5 questions to load
4. Answer all questions
5. Click **Submit**
6. See your results with AI explanations
7. ✅ Success!

---

## Your Live URLs

| Component | URL |
|-----------|-----|
| **Frontend** | `https://mcq-exam-frontend.vercel.app` |
| **Backend API** | `https://mcq-exam-backend.onrender.com` |
| **Backend Docs** | `https://mcq-exam-backend.onrender.com/docs` |

---

## Troubleshooting

### "Push rejected" on GitHub
- Make sure Personal Access Token is correct
- Verify repositories are Public
- Check repository names match

### Backend takes 30 seconds first time
- **This is normal!** Render free tier spins up on first request
- Subsequent requests are faster
- First quiz load may take 30-60 seconds

### Frontend can't connect to backend
- Verify `API_URL` is set in Vercel
- Make sure backend URL is correct
- Check backend is "Live" status
- Wait 5 minutes and refresh

### CORS errors
- CORS is enabled in backend
- Check browser console for exact error
- Verify API_URL has no trailing slash

---

## Advanced Options

### Update Code After Deployment
1. Make changes locally
2. Commit in VS Code (Ctrl+Shift+G)
3. Push to GitHub
4. Platforms auto-redeploy (5-10 minutes)

### Upgrade from Free Tier
- **Render:** $7/month (no spin-down)
- **Vercel:** Free (Pro $20/month for priority)

### Monitor Your App
- Render dashboard: https://render.com/dashboard
- Vercel dashboard: https://vercel.com/dashboard
- Check logs for errors

---

## File Structure

**Backend** (`d:\AI-Exam-Preparer`)
```
├── main.py (FastAPI server)
├── config.py (Config)
├── hf_inference.py (HF wrapper)
├── requirements.txt (Dependencies)
├── Procfile (Render config)
├── render.yaml (Render setup)
└── .env (Your HF token)
```

**Frontend** (`d:\AI-Exam-Preparer\Frontend`)
```
├── src/
│   ├── main.ts (Bootstrap)
│   ├── app/ (Components)
│   └── styles.scss (Global styles)
├── package.json (NPM deps)
├── angular.json (Angular config)
├── vercel.json (Vercel config)
└── tsconfig.json (TypeScript config)
```

---

## Support Resources

- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **GitHub Docs:** https://docs.github.com
- **Angular Docs:** https://angular.io/docs

---

**Your app is production-ready! 🚀 You've got this!**
