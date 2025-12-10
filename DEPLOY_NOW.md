# 🚀 DEPLOYMENT GUIDE

## Quick Deploy to Render.com (FREE)

### Step 1: Create GitHub Repository
```powershell
cd "F:\online guru"
git init
git add .
git commit -m "Initial commit - Sai Baba API"
```

Then create a new repository on GitHub and push:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/saibaba-api.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to https://render.com
2. Sign up/Login with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - **Name:** saibaba-api
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn simple_api:app --host 0.0.0.0 --port $PORT`
6. Click **"Create Web Service"**

### Step 3: Get Your API URL
After deployment (takes ~5 min), you'll get a URL like:
```
https://saibaba-api.onrender.com
```

### Step 4: Send This to Your Frontend Developer
```
API Base URL: https://saibaba-api.onrender.com

POST /ask
{
  "question": "What is devotion?"
}

Test it:
https://saibaba-api.onrender.com/docs
```

---

## Alternative: Deploy to Railway (Also FREE)

### Step 1: Push to GitHub (same as above)

### Step 2: Deploy on Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Railway auto-detects Python and deploys!

### Step 3: Get Your URL
Railway gives you a URL like:
```
https://saibaba-api.up.railway.app
```

---

## Alternative: Deploy to Heroku

### Step 1: Install Heroku CLI
```powershell
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Deploy
```powershell
cd "F:\online guru"
heroku login
heroku create saibaba-api
git push heroku main
```

Your API will be at:
```
https://saibaba-api.herokuapp.com
```

---

## What Files I Created for Deployment:

✅ **Procfile** - Tells deployment how to run your app
✅ **runtime.txt** - Specifies Python version
✅ **requirements.txt** - Already exists
✅ **simple_api.py** - Updated with CORS and PORT support

---

## After Deployment - Send to Frontend Developer:

```
✅ Deployed API URL: https://your-app.onrender.com

POST https://your-app.onrender.com/ask
{
  "question": "What is devotion?"
}

Response:
{
  "answer": "Devotion is the path...",
  "language": "en"
}

Interactive Docs:
https://your-app.onrender.com/docs
```

---

## Quick Test After Deployment:

```javascript
fetch('https://your-app.onrender.com/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: 'What is devotion?' })
})
.then(r => r.json())
.then(data => console.log(data))
```

---

## ⚡ FASTEST METHOD - Use Render (Recommended)

1. Push code to GitHub (5 min)
2. Connect to Render.com (2 min)
3. Deploy automatically (5 min)
4. **Total: ~12 minutes to live API!**

Then send your friend the deployed URL! 🎉
