# Railway Build Timeout Fix

## Problem
Railway builds are timing out because `sentence-transformers` downloads large ML models (several GB) during installation, which exceeds Railway's build timeout.

## Solution
We've created a minimal requirements file that excludes heavy dependencies, making the build much faster.

## Quick Fix Steps

### 1. Use Minimal Requirements File

In Railway dashboard:
1. Go to your service → **Settings** → **Variables**
2. Add environment variable:
   - **Key**: `RAILWAY_ENVIRONMENT`
   - **Value**: `production`

3. Go to **Settings** → **Source**
4. Make sure root directory is set to: `backend`

5. In Railway, the build will use `requirements-minimal.txt` automatically (configured in `railway.json`)

### 2. Alternative: Manual Override

If Railway still uses the full requirements.txt:

1. In Railway dashboard → **Settings** → **Deploy**
2. Add build command:
   ```
   pip install --no-cache-dir -r requirements-minimal.txt
   ```

### 3. Verify Build

After deployment:
- Check Railway logs for successful startup
- Test health endpoint: `https://your-app.railway.app/health`
- The app will work without RAG/embedding features (they're optional)

## What's Excluded

The minimal requirements file excludes:
- `sentence-transformers` (heavy ML library - downloads large models)
- `numpy` (included indirectly if needed)
- `pinecone` (optional - can be added later if needed)

## Adding Features Later

If you need RAG/embedding features:

1. Install dependencies in Railway:
   - Go to Railway → Service → **Shell**
   - Run: `pip install sentence-transformers pinecone numpy`
   
2. Or update `requirements-minimal.txt` and redeploy:
   ```bash
   # Add these lines to requirements-minimal.txt
   sentence-transformers>=2.2.2
   pinecone>=5.0.0
   numpy>=1.24.0
   ```

3. Set environment variables:
   - `PINECONE_API_KEY` (if using Pinecone)
   - `PINECONE_ENVIRONMENT`

## Build Optimization Tips

1. **Use Build Cache**: Railway caches pip packages between builds
2. **Exclude Files**: `.railwayignore` excludes unnecessary files
3. **Minimal Dependencies**: Only install what's needed for core functionality
4. **Lazy Imports**: Heavy dependencies are imported only when needed

## Verification

After deployment, check:

```bash
# Test health endpoint
curl https://your-app.railway.app/health

# Check logs in Railway dashboard
# Should see: "⚠️ Pinecone not available" (if not installed)
# Should see: "✅ ProdigyPM v1.0.0" (app started successfully)
```

## Troubleshooting

### Build Still Times Out

1. Check Railway logs for the exact error
2. Try using Railway's **Build Logs** to see where it's failing
3. Consider using a different platform (Render, Fly.io) if Railway continues to timeout

### App Starts But Features Don't Work

1. Check if optional dependencies are needed
2. Install them via Railway Shell or update requirements
3. Verify environment variables are set correctly

### CORS Errors

1. Make sure `CORS_ORIGINS` includes your Netlify URL
2. Format: `https://your-app.netlify.app` (no trailing slash)
3. Redeploy backend after changing CORS_ORIGINS

## Files Changed

- `backend/requirements-minimal.txt` - Lightweight requirements for deployment
- `backend/.railwayignore` - Excludes unnecessary files from build
- `backend/railway.json` - Updated to use minimal requirements
- `backend/nixpacks.toml` - Optimized build configuration
- `backend/rag/pinecone_rag.py` - Made imports optional (graceful fallback)

## Next Steps

1. Commit and push these changes
2. Redeploy on Railway (it will use the minimal requirements)
3. Verify the build completes successfully
4. Test the deployed backend
5. Configure Netlify with the backend URL

