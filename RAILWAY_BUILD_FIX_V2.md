# Railway Build Fix - Nixpacks Error Resolved

## Problem
Railway build was failing with Nixpacks error:
```
error: undefined variable 'pip'
at /app/.nixpacks/nixpkgs-bc8f8d1be58e8c8383e683a06e1e1e57893fff87.nix:19:9
```

## Root Cause
The `nixpacks.toml` file had incorrect syntax that conflicted with Railway's Nixpacks builder.

## Solution
1. ✅ **Removed `nixpacks.toml`** - Let Railway auto-detect Python
2. ✅ **Simplified `railway.json`** - Removed custom build command
3. ✅ **Replaced `requirements.txt`** - Now uses minimal requirements (fast builds)
4. ✅ **Backed up full requirements** - Saved as `requirements-full.txt`

## Current Setup

### Files
- `requirements.txt` - **Minimal requirements** (used by Railway)
- `requirements-full.txt` - Full requirements (backup)
- `requirements-minimal.txt` - Source of minimal requirements
- `railway.json` - Simplified configuration
- `Procfile` - Start command for Railway
- `.railwayignore` - Excludes unnecessary files

### Railway Configuration
- **Builder**: Nixpacks (auto-detected)
- **Root Directory**: `backend` (set in Railway dashboard)
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Health Check**: `/health`

## How It Works Now

1. Railway detects `requirements.txt` (Python project)
2. Nixpacks automatically installs Python and pip
3. Runs `pip install -r requirements.txt` (minimal requirements)
4. Starts app using `Procfile` or `railway.json` start command

## Next Steps

1. **Commit and push** these changes:
   ```bash
   git add backend/requirements.txt backend/railway.json
   git commit -m "Fix Railway build: remove nixpacks.toml, use minimal requirements"
   git push
   ```

2. **Verify in Railway**:
   - Build should complete successfully
   - App should start on port $PORT
   - Health check should pass

3. **Test deployment**:
   ```bash
   curl https://your-app.railway.app/health
   ```

## Switching Requirements (If Needed)

### Use Minimal (Current - Fast Builds)
```bash
cp requirements-minimal.txt requirements.txt
git add requirements.txt
git commit -m "Use minimal requirements"
git push
```

### Use Full (If you need RAG features)
```bash
cp requirements-full.txt requirements.txt
git add requirements.txt
git commit -m "Use full requirements"
git push
```

## Environment Variables

Make sure these are set in Railway dashboard:
- `CORS_ORIGINS` = `https://your-netlify-app.netlify.app`
- `PORT` = (auto-set by Railway)
- Optional: `NEMOTRON_API_KEY`, `JIRA_API_TOKEN`, etc.

## Troubleshooting

### Build Still Fails
- Check Railway logs for specific errors
- Verify `requirements.txt` syntax is correct
- Make sure root directory is set to `backend` in Railway settings

### App Won't Start
- Check Railway logs for startup errors
- Verify `main.py` exists in backend directory
- Check that all required environment variables are set

### Timeout Issues
- Current setup uses minimal requirements (should be fast)
- If still timing out, check Railway logs for slow operations
- Consider Railway plan upgrade if needed

## Files Changed

- ❌ **Deleted**: `backend/nixpacks.toml` (was causing errors)
- ✅ **Updated**: `backend/railway.json` (simplified)
- ✅ **Updated**: `backend/requirements.txt` (now minimal)
- ✅ **Created**: `backend/requirements-full.txt` (backup)

---

**The build should now work!** Railway will auto-detect Python and use the minimal requirements for fast builds.

