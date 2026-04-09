# ✅ Render Deployment Checklist

## Quick Deployment Steps

### Before You Start:
- [ ] GitHub repository is up to date
- [ ] You have your OpenRouter API key ready
- [ ] You have a Render account (or ready to sign up)

---

## 🚀 Deployment Steps:

### 1. Render Setup
- [ ] Go to https://render.com
- [ ] Sign up / Login with GitHub
- [ ] Authorize Render to access your repositories

### 2. Create Web Service
- [ ] Click "New +" → "Web Service"
- [ ] Find "AI-Startup-Idea-Validator"
- [ ] Click "Connect"

### 3. Configure Service

**Basic Settings:**
- [ ] Name: `ai-startup-validator` (or your choice)
- [ ] Region: Choose closest to you
- [ ] Branch: `main`
- [ ] Runtime: `Python 3`

**Build Command:** (Copy exactly)
```bash
cd client && npm install && npm run build && cd ../server && pip install -r requirements.txt
```
- [ ] Paste build command

**Start Command:** (Copy exactly)
```bash
cd server && uvicorn main:app --host 0.0.0.0 --port $PORT
```
- [ ] Paste start command

**Instance Type:**
- [ ] Select "Free"

### 4. Environment Variable
- [ ] Click "Add Environment Variable"
- [ ] Key: `OPENROUTER_API_KEY`
- [ ] Value: `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`

### 5. Deploy
- [ ] Click "Create Web Service"
- [ ] Wait 5-10 minutes for build
- [ ] Check logs for any errors

### 6. Test Your App
- [ ] Click the app URL (e.g., https://your-app.onrender.com)
- [ ] Homepage loads correctly
- [ ] Submit a test idea
- [ ] AI analysis works
- [ ] Report page displays
- [ ] Dashboard works

---

## 🎯 Configuration Summary

Copy these exactly when deploying:

**Build Command:**
```
cd client && npm install && npm run build && cd ../server && pip install -r requirements.txt
```

**Start Command:**
```
cd server && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Environment Variable:**
- Key: `OPENROUTER_API_KEY`
- Value: Your API key from `server/.env`

---

## ✅ Success Indicators

You'll know it's working when:
- [ ] Build completes without errors
- [ ] Status shows "Live" (green)
- [ ] App URL opens your application
- [ ] Can submit and analyze ideas
- [ ] AI generates full reports

---

## 🐛 If Something Goes Wrong

### Build Failed:
1. Check "Logs" tab
2. Look for error messages
3. Verify build command is correct
4. Check all files are in GitHub

### App Not Working:
1. Check "Logs" tab for runtime errors
2. Verify environment variable is set
3. Check API key is correct
4. Try manual redeploy

---

## 📞 Need Help?

- **Full Guide:** See `RENDER_DEPLOYMENT_GUIDE.md`
- **Render Docs:** https://render.com/docs
- **Render Support:** https://render.com/support

---

**Estimated Time:** 10-15 minutes  
**Cost:** FREE (750 hours/month)  
**Difficulty:** Easy ⭐⭐☆☆☆

**You got this!** 🚀
