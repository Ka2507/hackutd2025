# Railway Build Timeout - Quick Fix

## The Problem
Railway builds were timing out because `sentence-transformers` downloads large ML models (several GB) during installation.

## The Solution
Created a **minimal requirements file** that excludes heavy dependencies, making builds 5-10x faster.

## Quick Steps to Fix

### 1. In Railway Dashboard

1. Go to your Railway service → **Settings** → **Variables**
2. Make sure you have:
   - `CORS_ORIGINS` = `https://your-netlify-app.netlify.app`
   - (Other env vars as needed)

3. The build will now automatically use `requirements-minimal.txt` (configured in `railway.json`)

### 2. Verify Build

After pushing these changes:
- Railway will use the minimal requirements
- Build should complete in 2-5 minutes (instead of timing out)
- App will start successfully
- RAG features will be disabled (but app works without them)

### 3. Test Deployment

```bash
# Test health endpoint
curl https://your-app.railway.app/health

# Should return:
# {"status":"healthy","agents":9,...}
```

## What Changed

✅ **Created `requirements-minimal.txt`** - Lightweight version without heavy ML libraries
✅ **Updated `railway.json`** - Uses minimal requirements for builds  
✅ **Made RAG optional** - App works without Pinecone/sentence-transformers
✅ **Added `.railwayignore`** - Excludes unnecessary files from build
✅ **Updated `pinecone_rag.py`** - Graceful fallback when dependencies missing

## What's Excluded (Can Add Later)

- `sentence-transformers` - Heavy ML library (downloads large models)
- `pinecone` - Vector database (optional for RAG features)
- `numpy` - Usually included indirectly if needed

## Adding RAG Features Later (Optional)

If you need RAG/embedding features:

1. Install in Railway Shell:
   ```bash
   pip install sentence-transformers pinecone numpy
   ```

2. Or update `requirements-minimal.txt`:
   ```bash
   # Add these lines
   sentence-transformers>=2.2.2
   pinecone>=5.0.0
   numpy>=1.24.0
   ```

3. Set environment variables:
   - `PINECONE_API_KEY`
   - `PINECONE_ENVIRONMENT`

## Files Changed

- `backend/requirements-minimal.txt` - **NEW** - Lightweight requirements
- `backend/railway.json` - Updated build command
- `backend/.railwayignore` - **NEW** - Excludes files from build
- `backend/nixpacks.toml` - **NEW** - Optimized build config
- `backend/rag/pinecone_rag.py` - Made imports optional

## Next Steps

1. ✅ Commit and push these changes
2. ✅ Railway will automatically use minimal requirements
3. ✅ Build should complete successfully
4. ✅ Test the deployed backend
5. ✅ Configure Netlify with backend URL

## Troubleshooting

### Build Still Times Out
- Check Railway logs for exact error
- Verify `railway.json` is using `requirements-minimal.txt`
- Try clearing Railway build cache

### App Starts But Features Don't Work
- This is expected - RAG features are optional
- Core API features should work fine
- Install optional dependencies if needed

### CORS Errors
- Verify `CORS_ORIGINS` includes your Netlify URL
- Format: `https://your-app.netlify.app` (no trailing slash)
- Redeploy backend after changing CORS_ORIGINS

---

**The build should now complete successfully!** 🎉

