# Quick Deployment Setup

## Summary

Your frontend is deployed on Netlify, but the backend needs to be deployed separately. Follow these steps:

## Step 1: Deploy Backend (Choose One Platform)

### Option A: Railway (Easiest - Recommended)

1. Go to [railway.app](https://railway.app) and sign up
2. Create new project → Deploy from GitHub
3. Select your repository
4. Set root directory to `backend` in project settings
5. Add environment variable:
   - `CORS_ORIGINS` = `https://your-netlify-site.netlify.app`
6. Copy the Railway URL (e.g., `https://your-app.railway.app`)

### Option B: Render

1. Go to [render.com](https://render.com) and sign up
2. New → Web Service → Connect GitHub repo
3. Set:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variable:
   - `CORS_ORIGINS` = `https://your-netlify-site.netlify.app`
5. Copy the Render URL

## Step 2: Configure Netlify

1. Go to your Netlify site dashboard
2. Site settings → Build & deploy → Environment variables
3. Add new variable:
   - **Key**: `VITE_API_URL`
   - **Value**: Your backend URL (from Step 1)
4. Trigger a new deployment (or push a commit)

## Step 3: Test

1. Visit your Netlify site
2. Open browser console (F12)
3. Try using the app - API calls should go to your backend
4. If you see CORS errors, double-check `CORS_ORIGINS` includes your Netlify URL

## Files Created

- `backend/Procfile` - For Railway/Heroku deployment
- `backend/runtime.txt` - Python version specification
- `backend/railway.json` - Railway configuration
- `backend/render.yaml` - Render configuration
- `BACKEND_DEPLOYMENT.md` - Detailed deployment guide

## Important Notes

- Backend URL must use `https://` (not `http://`)
- CORS_ORIGINS must include your exact Netlify URL (no trailing slash)
- After setting VITE_API_URL in Netlify, you must redeploy for it to take effect
- WebSocket connections require `wss://` (secure WebSocket)

## Need Help?

See `BACKEND_DEPLOYMENT.md` for detailed instructions and troubleshooting.

