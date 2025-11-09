# ProdPlex Quick Start Guide

Get ProdPlex up and running in 5 minutes!

## Option 1: Automated Setup (Recommended)

```bash
cd ProdPlex
./setup.sh
```

This will automatically:
- Set up Python virtual environment
- Install all backend dependencies
- Install all frontend dependencies
- Create .env files from templates

## Option 2: Manual Setup

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
```

## Running the Application

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```
Backend runs on: `http://localhost:8000`

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```
Frontend runs on: `http://localhost:5173`

## First Steps

1. **Open Browser**: Navigate to `http://localhost:5173`
2. **Explore Home Page**: See the agent showcase
3. **Go to Dashboard**: Click "Get Started"
4. **Run a Workflow**:
   - Select "Research & Strategy" from dropdown
   - Click "Run Workflow"
   - Watch agents work in real-time
5. **Try Chat Interface**: Click "Chat" tab and ask questions
6. **View Insights**: Check analytics and metrics

## Optional: Local LLM Setup

For the full experience with local AI:

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull Llama 3 (8B model, ~4.7GB)
ollama pull llama3:8b

# Or pull Mistral (7B model, ~4.1GB)
ollama pull mistral
```

Then update `backend/.env`:
```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:8b
```

## Optional: NVIDIA Nemotron API

For strategic planning with Nemotron:

1. Get API key from: https://build.nvidia.com/
2. Update `backend/.env`:
```bash
NEMOTRON_API_KEY=your_nvidia_api_key_here
```

## Testing the System

### Test Backend
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "agents": 7,
  ...
}
```

### Test WebSocket
Open browser console at `http://localhost:5173/dashboard` and you should see:
```
WebSocket connected
```

## Troubleshooting

### Port already in use
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173 (frontend)
lsof -ti:5173 | xargs kill -9
```

### Python dependencies fail
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Node modules issues
```bash
rm -rf node_modules package-lock.json
npm install
```

### Import errors in Python
Make sure virtual environment is activated:
```bash
which python  # Should show venv/bin/python
```

## What's Next?

- **Explore Agents**: Try each workflow type
- **Check Integrations**: View mock data from Jira, Slack, Figma, Reddit
- **Customize**: Edit agent behaviors in `backend/agents/`
- **Add Features**: Extend with your own agents

## Need Help?

- Full Documentation: See `README.md`
- Issues: Check logs in `backend/logs/`
- API Docs: Visit `http://localhost:8000/docs`
- Config: Edit `.env` files

**Happy building!**
