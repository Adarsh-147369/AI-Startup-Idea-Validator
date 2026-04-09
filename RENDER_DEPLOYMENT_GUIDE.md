# 🚀 Deploy to Render - Step by Step Guide

## ✅ Your Project is Already Ready!

Good news! Your current project setup works for **BOTH** local development and Render deployment without any changes needed!

---

## 📋 Prerequisites

1. ✅ GitHub account (you already have this)
2. ✅ Render account (free) - Sign up at https://render.com
3. ✅ OpenRouter API key (you already have this in `server/.env`)

---

## 🎯 Step-by-Step Deployment

### Step 1: Sign Up / Login to Render

1. Go to https://render.com
2. Click **"Get Started for Free"** or **"Sign In"**
3. Sign up with your **GitHub account** (recommended)
4. Authorize Render to access your GitHub repositories

---

### Step 2: Create a New Web Service

1. Once logged in, click **"New +"** button (top right)
2. Select **"Web Service"**
3. You'll see a list of your GitHub repositories

---

### Step 3: Connect Your Repository

1. Find **"AI-Startup-Idea-Validator"** in the list
2. Click **"Connect"** button next to it
3. If you don't see it, click **"Configure account"** and grant access to the repository

---

### Step 4: Configure the Web Service

Fill in these details:

#### Basic Settings:
- **Name:** `ai-startup-validator` (or any name you prefer)
- **Region:** Choose closest to you (e.g., Oregon, Frankfurt, Singapore)
- **Branch:** `main`
- **Root Directory:** Leave empty (blank)
- **Runtime:** `Python 3`

#### Build & Deploy Settings:

**Build Command:** (Copy this exactly)
```bash
cd client && npm install && npm run build && cd ../server && pip install -r requirements.txt
```

**Start Command:** (Copy this exactly)
```bash
cd server && uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### Instance Type:
- Select **"Free"** (this gives you 750 hours/month free)

---

### Step 5: Add Environment Variable

This is **CRITICAL** - your app won't work without this!

1. Scroll down to **"Environment Variables"** section
2. Click **"Add Environment Variable"**
3. Add this:
   - **Key:** `OPENROUTER_API_KEY`
   - **Value:** `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`
   
   (This is your API key from `server/.env`)

---

### Step 6: Deploy!

1. Scroll to the bottom
2. Click **"Create Web Service"**
3. Render will start building your application
4. This will take **5-10 minutes** for the first deployment

---

## 📊 Deployment Process

You'll see these stages:

1. **Building** - Installing dependencies and building frontend
   - Installing Node.js packages
   - Building React app with Vite
   - Installing Python packages
   
2. **Deploying** - Starting your application
   - Starting Uvicorn server
   - Application becomes live

3. **Live** - Your app is running! 🎉

---

## 🌐 Access Your Deployed App

Once deployment is complete:

1. You'll see a **green "Live"** status
2. Your app URL will be shown at the top (e.g., `https://ai-startup-validator.onrender.com`)
3. Click the URL to open your app
4. Test it by submitting a startup idea!

---

## ⚠️ Important Notes

### Free Tier Limitations:

1. **Spin Down After Inactivity**
   - Free apps sleep after 15 minutes of inactivity
   - First request after sleep takes 30-60 seconds to wake up
   - Subsequent requests are fast

2. **750 Hours/Month**
   - Free tier gives 750 hours per month
   - More than enough for testing and demos

3. **Automatic Deploys**
   - Every time you push to GitHub, Render auto-deploys
   - You can disable this in settings if needed

---

## 🔧 Your Project Works on Both!

### Why No Changes Needed?

Your project is already configured correctly:

1. **API Routes:** Use `/api` prefix (works locally and on Render)
2. **Static Files:** Served from `client/dist/` (works everywhere)
3. **Port:** Uses `$PORT` environment variable (Render provides this)
4. **Database:** SQLite file (works on Render's persistent disk)

### Local Development:
```bash
cd server
venv\Scripts\activate
python -m uvicorn main:app --reload
# Opens on http://localhost:8000
```

### Render Production:
```bash
# Render automatically runs:
cd server && uvicorn main:app --host 0.0.0.0 --port $PORT
# Opens on https://your-app.onrender.com
```

**Same code, works everywhere!** ✅

---

## 🐛 Troubleshooting

### Build Failed?

**Check Build Logs:**
1. Click on your service
2. Go to **"Logs"** tab
3. Look for error messages

**Common Issues:**
- Missing `package.json` in client folder → Check it exists
- Missing `requirements.txt` in server folder → Check it exists
- Build command typo → Copy exactly from this guide

### App Not Loading?

**Check Runtime Logs:**
1. Go to **"Logs"** tab
2. Look for errors after "Deploy succeeded"

**Common Issues:**
- Missing `OPENROUTER_API_KEY` → Add in Environment Variables
- Wrong API key → Check the key is correct
- Database error → Render creates SQLite file automatically

### "Not Found" Error on Deployed App?

**This shouldn't happen because:**
- Your axios is configured with `/api` (relative path)
- Works on any domain (localhost or Render)

**If it happens:**
1. Check browser console (F12)
2. Check if request goes to `/api/ideas`
3. Check Render logs for incoming requests

---

## 📝 Post-Deployment Checklist

After deployment, test these:

- [ ] Homepage loads (https://your-app.onrender.com)
- [ ] Can submit a startup idea
- [ ] AI analysis works (wait 5-10 seconds)
- [ ] Report page shows full analysis
- [ ] Dashboard shows all ideas
- [ ] Can view individual reports

---

## 🔄 Updating Your Deployed App

### Automatic Updates:
1. Make changes locally
2. Commit to git: `git add . && git commit -m "your message"`
3. Push to GitHub: `git push origin main`
4. Render automatically detects and redeploys!

### Manual Deploy:
1. Go to Render dashboard
2. Click your service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 💰 Cost Breakdown

### Free Tier (What You're Using):
- **Cost:** $0/month
- **Hours:** 750 hours/month
- **Instances:** 1 free web service
- **Bandwidth:** 100 GB/month
- **Build Minutes:** 500 minutes/month

**Perfect for:**
- Personal projects
- Demos
- Portfolio projects
- Testing

---

## 🎯 Quick Reference

### Your Render Configuration:

```yaml
Name: ai-startup-validator
Runtime: Python 3
Branch: main

Build Command:
cd client && npm install && npm run build && cd ../server && pip install -r requirements.txt

Start Command:
cd server && uvicorn main:app --host 0.0.0.0 --port $PORT

Environment Variables:
OPENROUTER_API_KEY=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

Instance Type: Free
```

---

## 📞 Support

### Render Documentation:
- https://render.com/docs

### Common Questions:
- **How to add custom domain?** Settings → Custom Domain
- **How to view logs?** Click service → Logs tab
- **How to redeploy?** Manual Deploy → Deploy latest commit
- **How to delete service?** Settings → Delete Web Service

---

## ✅ Summary

1. Sign up on Render.com
2. Connect your GitHub repository
3. Configure with the commands above
4. Add `OPENROUTER_API_KEY` environment variable
5. Click "Create Web Service"
6. Wait 5-10 minutes
7. Your app is live! 🎉

**No code changes needed - works on both local and Render!**

---

## 🎉 You're Ready!

Follow the steps above and your app will be live on the internet in about 10 minutes!

**Good luck with your deployment!** 🚀
