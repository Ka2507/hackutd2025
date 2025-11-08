# ProdigyPM - API Keys and Requirements

## Overview
This document lists all API keys, integrations, and external services needed for ProdigyPM to function fully.

---

## REQUIRED APIs (For Full Functionality)

### 1. NVIDIA Nemotron API (Strategic Planning)
**Purpose**: High-level multi-agent orchestration and strategic reasoning  
**Cost**: ~$20-30 for MVP testing (50-100 calls)  
**Priority**: HIGH  

**What You Need**:
- API Key from https://build.nvidia.com/
- Add to `backend/.env`:
  ```
  NEMOTRON_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```

**Usage**:
- Multi-agent workflow coordination
- Strategic planning decisions
- Complex reasoning tasks
- Limited to 2-3 calls per major workflow (budget control)

---

### 2. Local LLM (Ollama) - RECOMMENDED
**Purpose**: Local inference for routine tasks, privacy, cost savings  
**Cost**: FREE (runs on your machine)  
**Priority**: HIGH (alternative to expensive API calls)

**What You Need**:
1. Install Ollama:
   ```bash
   curl https://ollama.ai/install.sh | sh
   ```

2. Pull a model:
   ```bash
   ollama pull llama3:8b  # ~4.7GB, recommended
   # OR
   ollama pull mistral    # ~4.1GB, alternative
   ```

3. Verify it's running:
   ```bash
   ollama list
   ```

**Usage**:
- Agent responses (Strategy, Research, Dev, etc.)
- Chat interface
- Document generation
- 90% of AI tasks (only use Nemotron for strategic decisions)

---

## OPTIONAL INTEGRATIONS (Mock Data Available)

### 3. Jira API (Development Tracking)
**Purpose**: Sprint data, issue creation, backlog management  
**Cost**: FREE (with Jira account)  
**Priority**: MEDIUM (has mock fallback)

**What You Need**:
- Jira account with API access
- API Token from: https://id.atlassian.com/manage-profile/security/api-tokens
- Base URL: Your Jira instance (e.g., `https://yourcompany.atlassian.net`)
- Add to `backend/.env`:
  ```
  JIRA_API_TOKEN=your_jira_api_token_here
  JIRA_BASE_URL=https://yourcompany.atlassian.net
  ```

**Current Status**: Uses mock data if not configured

---

### 4. Slack API (Notifications & Reporting)
**Purpose**: Send sprint summaries, agent updates, notifications  
**Cost**: FREE (with Slack workspace)  
**Priority**: MEDIUM (has mock fallback)

**What You Need**:
- Slack workspace admin access
- Create Slack App: https://api.slack.com/apps
- Bot Token Scopes needed:
  - `chat:write`
  - `files:write`
  - `channels:read`
- Add to `backend/.env`:
  ```
  SLACK_BOT_TOKEN=xoxb-your-bot-token-here
  ```

**Current Status**: Uses mock data if not configured

---

### 5. Figma API (Design Integration)
**Purpose**: Fetch design mockups, prototypes, design system  
**Cost**: FREE (with Figma account)  
**Priority**: LOW (has mock fallback)

**What You Need**:
- Figma account
- Personal Access Token from: https://www.figma.com/developers/api#access-tokens
- Add to `backend/.env`:
  ```
  FIGMA_ACCESS_TOKEN=your_figma_token_here
  ```

**Current Status**: Uses mock data if not configured

---

### 6. Reddit API (User Research)
**Purpose**: Market research, sentiment analysis, trend detection  
**Cost**: FREE  
**Priority**: LOW (has mock fallback)

**What You Need**:
- Reddit account
- Create app: https://www.reddit.com/prefs/apps
- Add to `backend/.env`:
  ```
  REDDIT_CLIENT_ID=your_client_id
  REDDIT_CLIENT_SECRET=your_client_secret
  ```

**Current Status**: Uses mock data if not configured

---

## OPTIONAL (Advanced Features)

### 7. Pinecone (Vector Database)
**Purpose**: Production-grade vector storage (alternative to FAISS)  
**Cost**: FREE tier available  
**Priority**: LOW (FAISS works fine for MVP)

**What You Need**:
- Pinecone account: https://www.pinecone.io/
- Create index
- Add to `backend/.env`:
  ```
  VECTOR_STORE_TYPE=pinecone
  PINECONE_API_KEY=your_api_key
  PINECONE_ENVIRONMENT=us-west1-gcp
  PINECONE_INDEX_NAME=prodigypm
  ```

**Current Status**: Using FAISS (local, free)

---

## DEPENDENCIES (Python Packages)

Already in `requirements.txt`, install with:
```bash
cd backend
pip install -r requirements.txt
```

**Required Packages**:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `pydantic-settings` - Settings management
- `aiohttp` - Async HTTP client
- `websockets` - Real-time updates
- `python-dateutil` - Date handling

**Optional Packages** (uncomment in requirements.txt):
- `faiss-cpu` - Vector similarity search
- `sentence-transformers` - Text embeddings
- `atlassian-python-api` - Jira integration
- `slack-sdk` - Slack integration
- `praw` - Reddit integration

---

## COST BREAKDOWN

### Minimum to Start (FREE):
- Ollama (local LLM) - FREE
- FAISS (vector store) - FREE
- Mock integrations - FREE
- **Total: $0**

### Recommended Setup ($20-30):
- Ollama (local) - FREE
- NVIDIA Nemotron - $20-30 for testing
- Mock integrations - FREE
- **Total: $20-30**

### Full Production ($40-50/month):
- Ollama (local) - FREE
- NVIDIA Nemotron - $20-30/month
- Jira - Included in existing subscription
- Slack - FREE
- Figma - FREE
- Reddit - FREE
- Hosting (Railway/Vercel) - FREE tier
- **Total: $20-30/month**

---

## QUICK START PRIORITIES

### To Get Running Immediately (REQUIRED):
1. ✅ None! Uses mock data by default
2. ✅ All integrations have fallbacks

### To Get AI Working (RECOMMENDED):
1. **Install Ollama** - 15 minutes
   - Download and install
   - Pull llama3:8b model
   - Start Ollama service

### To Get Full Features (OPTIONAL):
1. **NVIDIA Nemotron** - For strategic planning
2. **Jira API** - For real sprint data
3. **Slack API** - For real notifications

---

## ENVIRONMENT VARIABLES TEMPLATE

Copy this to `backend/.env`:

```bash
# App Settings
APP_NAME=ProdigyPM
DEBUG=true

# Ollama (LOCAL LLM - RECOMMENDED)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:8b

# NVIDIA Nemotron (STRATEGIC PLANNING - OPTIONAL)
NEMOTRON_API_KEY=
NEMOTRON_MAX_CALLS=3

# Jira (OPTIONAL - has mock fallback)
JIRA_API_TOKEN=
JIRA_BASE_URL=

# Slack (OPTIONAL - has mock fallback)
SLACK_BOT_TOKEN=

# Figma (OPTIONAL - has mock fallback)
FIGMA_ACCESS_TOKEN=

# Reddit (OPTIONAL - has mock fallback)
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=

# Vector Store (FAISS is default, free)
VECTOR_STORE_TYPE=faiss
```

---

## WHAT WORKS WITHOUT ANY SETUP

### Currently Working (No APIs needed):
- ✅ Frontend UI (all pages, components)
- ✅ Backend API structure
- ✅ Agent system architecture
- ✅ WebSocket real-time updates
- ✅ Database (SQLite)
- ✅ Mock data for all integrations

### Needs Ollama for AI:
- ⏳ Actual LLM responses
- ⏳ Agent reasoning
- ⏳ Chat interface responses

### Needs Nemotron for Strategy:
- ⏳ Advanced multi-agent coordination
- ⏳ Strategic decision making
- ⏳ Complex reasoning workflows

---

## RECOMMENDATIONS

### For Hackathon Demo:
1. **Install Ollama** (15 min) - Essential for AI features
2. **Skip Nemotron** - Use local LLM fallback (saves money)
3. **Skip other integrations** - Mock data looks real enough

### For Production:
1. **Ollama** - Primary inference
2. **Nemotron** - Strategic tasks only
3. **Real integrations** - Jira, Slack as needed

### Budget Allocation:
- Ollama: $0 (local)
- Nemotron: $20-30 (strategic only, 2-3 calls per workflow)
- Hosting: $0 (free tiers)
- **Total: Under $40 easily**

---

## NEED HELP?

**Ollama Installation**:
```bash
# macOS/Linux
curl https://ollama.ai/install.sh | sh
ollama pull llama3:8b
ollama serve  # starts on localhost:11434
```

**NVIDIA Nemotron**:
- Sign up: https://build.nvidia.com/
- Get API key from dashboard
- Free credits available for testing

**Testing Without APIs**:
- Application works with mock data
- Install Ollama for full AI experience
- Nemotron optional for demo

---

**Questions?** Check `backend/.env.example` for all configuration options.

