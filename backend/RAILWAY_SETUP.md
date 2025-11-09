# Railway Deployment Setup

## Current Configuration

Railway will automatically:
1. Detect Python project (via `requirements.txt`)
2. Install dependencies from `requirements.txt`
3. Use `Procfile` or `railway.json` start command
4. Run the application

## Requirements File Strategy

- **`requirements.txt`** - Currently set to minimal (for fast builds)
- **`requirements-full.txt`** - Full requirements with all dependencies
- **`requirements-minimal.txt`** - Minimal requirements (lightweight)

## Switching Requirements

### Use Minimal (Current - Fast Builds)
```bash
cp requirements-minimal.txt requirements.txt
git add requirements.txt
git commit -m "Use minimal requirements for Railway"
git push
```

### Use Full (If you need RAG features)
```bash
cp requirements-full.txt requirements.txt
git add requirements.txt
git commit -m "Use full requirements"
git push
```

## Railway Dashboard Settings

In Railway dashboard, you can also:
1. Go to **Settings** → **Build**
2. Set **Build Command** (optional): `pip install --no-cache-dir -r requirements.txt`
3. Set **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Environment Variables

Set in Railway dashboard → **Variables**:
- `CORS_ORIGINS` = `https://your-netlify-app.netlify.app`
- `PORT` = (auto-set by Railway)
- `NEMOTRON_API_KEY` = (optional)
- Other API keys as needed

## Troubleshooting

### Build Fails
- Check Railway logs for errors
- Verify `requirements.txt` is valid
- Make sure root directory is set to `backend` in Railway settings

### App Won't Start
- Check start command in `Procfile` or `railway.json`
- Verify `main.py` exists in root directory
- Check logs for import errors

### Timeout Issues
- Use `requirements-minimal.txt` (current setup)
- Check Railway logs for slow operations
- Consider upgrading Railway plan if needed

