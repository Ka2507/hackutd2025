# Backend Deployment Guide

This guide will help you deploy the ProdigyPM backend to a cloud platform so it can connect to your Netlify frontend.

## Quick Overview

- **Frontend**: Deployed on Netlify (static site)
- **Backend**: Needs to be deployed separately (Railway, Render, or similar)
- **Connection**: Frontend connects to backend via `VITE_API_URL` environment variable

## Option 1: Deploy to Railway (Recommended)

Railway is easy to use and has a generous free tier.

### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Create a new project

### Step 2: Deploy Backend

1. Click "New Project" → "Deploy from GitHub repo"
2. Select your `hackutd2025` repository
3. Railway will auto-detect the Python backend
4. Set the root directory to `backend`:
   - Go to Settings → Source
   - Set Root Directory to `backend`

### Step 3: Configure Environment Variables

In Railway dashboard, go to your service → Variables and add:

```bash
# Required: Set CORS to allow your Netlify domain
CORS_ORIGINS=https://your-netlify-app.netlify.app,https://your-custom-domain.com

# Optional: NVIDIA Nemotron API (if you have it)
NEMOTRON_API_KEY=your_api_key_here

# Optional: Integration API keys
JIRA_API_TOKEN=your_token
SLACK_BOT_TOKEN=your_token
FIGMA_ACCESS_TOKEN=your_token
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret

# Optional: Pinecone for vector store
PINECONE_API_KEY=your_key
PINECONE_ENVIRONMENT=your_env
```

### Step 4: Get Backend URL

1. Railway will automatically assign a URL like: `https://your-app.railway.app`
2. Copy this URL (you'll need it for Netlify)

### Step 5: Configure Netlify

1. Go to your Netlify site dashboard
2. Navigate to: **Site settings** → **Build & deploy** → **Environment**
3. Add environment variable:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-app.railway.app` (your Railway backend URL)
4. Redeploy your site (or push a new commit)

---

## Option 2: Deploy to Render

Render is another good option with a free tier.

### Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub

### Step 2: Deploy Backend

1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `prodigypm-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Configure Environment Variables

In Render dashboard, go to Environment and add:

```bash
CORS_ORIGINS=https://your-netlify-app.netlify.app
NEMOTRON_API_KEY=your_api_key_here
# ... other optional variables
```

### Step 4: Get Backend URL

Render will provide a URL like: `https://prodigypm-backend.onrender.com`

### Step 5: Configure Netlify

Same as Railway - add `VITE_API_URL` environment variable in Netlify dashboard.

---

## Option 3: Deploy to Fly.io

Fly.io is another option with good performance.

### Step 1: Install Fly CLI

```bash
curl -L https://fly.io/install.sh | sh
```

### Step 2: Create Fly App

```bash
cd backend
fly launch
```

### Step 3: Configure

Follow the prompts and set environment variables in Fly dashboard.

---

## Testing the Connection

After deploying:

1. **Test Backend Health**:
   ```bash
   curl https://your-backend-url.com/health
   ```

2. **Test from Frontend**:
   - Open your Netlify site
   - Open browser console (F12)
   - Check for API calls - they should go to your backend URL
   - If you see CORS errors, make sure `CORS_ORIGINS` includes your Netlify URL

3. **Check Backend Logs**:
   - Railway/Render/Fly dashboards show real-time logs
   - Check for any startup errors

---

## Troubleshooting

### CORS Errors

**Symptom**: Browser console shows CORS errors when calling backend API.

**Solution**: 
- Make sure `CORS_ORIGINS` environment variable in backend includes your Netlify URL
- Format: `https://your-app.netlify.app` (no trailing slash)
- For multiple origins: `https://app1.netlify.app,https://app2.netlify.app`

### Backend Not Starting

**Symptom**: Backend deployment fails or crashes.

**Solution**:
- Check logs in your platform's dashboard
- Verify `requirements.txt` is correct
- Make sure Python version matches (3.11+)
- Check that all environment variables are set correctly

### Frontend Can't Connect

**Symptom**: Frontend shows network errors or "Failed to fetch".

**Solution**:
- Verify `VITE_API_URL` is set in Netlify environment variables
- Make sure backend URL is correct (no trailing slash)
- Check backend is running (visit backend URL in browser)
- Verify CORS is configured correctly

### WebSocket Connection Issues

**Symptom**: WebSocket connections fail.

**Solution**:
- Some platforms require WebSocket support (Railway and Render support it)
- Check that your backend URL uses `https://` (not `http://`)
- Verify WebSocket endpoint: `wss://your-backend-url.com/ws/agents`

---

## Environment Variables Reference

### Backend (Railway/Render/Fly)

| Variable | Required | Description |
|----------|----------|-------------|
| `CORS_ORIGINS` | Yes | Comma-separated list of allowed origins (your Netlify URL) |
| `PORT` | Auto | Port number (automatically set by platform) |
| `NEMOTRON_API_KEY` | No | NVIDIA Nemotron API key for advanced AI |
| `JIRA_API_TOKEN` | No | Jira integration token |
| `SLACK_BOT_TOKEN` | No | Slack bot token |
| `FIGMA_ACCESS_TOKEN` | No | Figma API token |
| `REDDIT_CLIENT_ID` | No | Reddit API client ID |
| `REDDIT_CLIENT_SECRET` | No | Reddit API client secret |
| `PINECONE_API_KEY` | No | Pinecone vector database key |

### Frontend (Netlify)

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_URL` | Yes | Your backend URL (e.g., `https://your-app.railway.app`) |

---

## Quick Start Checklist

- [ ] Deploy backend to Railway/Render/Fly
- [ ] Set `CORS_ORIGINS` environment variable in backend (include Netlify URL)
- [ ] Get backend URL from deployment platform
- [ ] Set `VITE_API_URL` environment variable in Netlify
- [ ] Redeploy Netlify site
- [ ] Test backend health endpoint
- [ ] Test frontend connection
- [ ] Verify WebSocket connection works

---

## Need Help?

- Check backend logs in your platform's dashboard
- Check browser console for frontend errors
- Verify all environment variables are set correctly
- Test backend endpoints directly with curl or Postman

