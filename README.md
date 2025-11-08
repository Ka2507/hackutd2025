# ProdigyPM

**Your AI Co-Pilot for Product Management**

ProdigyPM is an Agentic AI platform that helps Product Managers plan, ideate, research, and automate workflows using multi-agent AI orchestration powered by NVIDIA Nemotron and local LLMs.

![ProdigyPM](https://img.shields.io/badge/Version-1.0.0-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green) ![React](https://img.shields.io/badge/React-18.2-blue) ![TypeScript](https://img.shields.io/badge/TypeScript-5.2-blue)

---

## Features

### Multi-Agent AI System
- **7 Specialized Agents** working in harmony:
  - **StrategyAgent**: Market sizing, idea generation, competitive analysis
  - **ResearchAgent**: User research, trend analysis, sentiment analysis
  - **DevAgent**: User stories, backlog generation, technical specs
  - **PrototypeAgent**: Design mockups, Figma integration
  - **GtmAgent**: Go-to-market strategy, launch planning, pricing
  - **AutomationAgent**: Sprint summaries, workflow automation
  - **RegulationAgent**: Compliance checks, risk assessment (PNC challenge)

### Key Capabilities
- **Multi-Agent Orchestration** with LangGraph
- **NVIDIA Nemotron Integration** for strategic reasoning (budget under $40)
- **Local LLM Support** via Ollama (Llama 3 8B or Mistral)
- **Vector Memory** with FAISS for context-aware agent communication
- **Real-time WebSocket Updates** for live agent status
- **Integration Stubs** for Jira, Slack, Figma, Reddit

### Modern UI
- **Futuristic Design** with clean, modern aesthetic
- **Framer Motion Animations** for smooth transitions
- **TailwindCSS** with custom color palette
- **Real-time Dashboard** with agent panels and activity feed
- **Chat Interface** for natural language interaction
- **Analytics & Insights** page with charts and metrics

---

## Architecture

```
ProdigyPM/
├── backend/                   # FastAPI Backend
│   ├── agents/               # 7 AI Agents
│   │   ├── base_agent.py
│   │   ├── strategy_agent.py
│   │   ├── research_agent.py
│   │   ├── dev_agent.py
│   │   ├── prototype_agent.py
│   │   ├── gtm_agent.py
│   │   ├── automation_agent.py
│   │   └── regulation_agent.py
│   ├── orchestrator/         # Multi-agent coordination
│   │   ├── task_graph.py    # LangGraph workflow
│   │   ├── memory_manager.py # FAISS vector store
│   │   └── nemotron_bridge.py # NVIDIA Nemotron API
│   ├── integrations/         # External APIs (mock for MVP)
│   │   ├── jira_api.py
│   │   ├── slack_api.py
│   │   ├── figma_api.py
│   │   └── reddit_api.py
│   ├── db/                   # SQLite database
│   │   └── context_store.py
│   ├── utils/                # Configuration & logging
│   └── main.py              # FastAPI app with WebSocket
│
└── frontend/                 # React + TypeScript Frontend
    ├── src/
    │   ├── components/      # React components
    │   │   ├── Dashboard.tsx
    │   │   ├── AgentPanel.tsx
    │   │   ├── TaskCard.tsx
    │   │   ├── ChatInterface.tsx
    │   │   └── ReportView.tsx
    │   ├── pages/           # Page components
    │   │   ├── Home.tsx
    │   │   ├── ProjectDashboard.tsx
    │   │   └── Insights.tsx
    │   ├── hooks/           # Custom React hooks
    │   │   └── useAgents.ts
    │   ├── utils/           # API client
    │   │   └── apiClient.ts
    │   └── styles/          # TailwindCSS
    └── package.json
```

---

## Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **Ollama** (optional, for local LLM)
- **NVIDIA API Key** (optional, for Nemotron)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ProdigyPM.git
cd ProdigyPM
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API keys (optional)

# Run the backend
python main.py
```

Backend will start on `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Run development server
npm run dev
```

Frontend will start on `http://localhost:5173`

### 4. Open Your Browser

Navigate to `http://localhost:5173` to see ProdigyPM in action!

---

## Configuration

### Backend Configuration (`backend/.env`)

```bash
# Ollama Settings (for local LLM)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:8b

# NVIDIA Nemotron (for strategic reasoning)
NEMOTRON_API_KEY=your_nvidia_api_key_here
NEMOTRON_MAX_CALLS=3  # Budget control

# Integration APIs (optional - uses mock data if not provided)
JIRA_API_TOKEN=your_token
SLACK_BOT_TOKEN=your_token
FIGMA_ACCESS_TOKEN=your_token
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
```

### Installing Ollama (Optional but Recommended)

For local LLM processing:

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama3:8b
# or
ollama pull mistral
```

---

## Usage

### Running a Workflow

1. **Select a Workflow** from the dropdown:
   - Full Feature Planning (all agents)
   - Research & Strategy
   - Dev Planning
   - Launch Planning
   - Compliance Check

2. **Click "Run Workflow"** to execute

3. **Watch Agents Work** in real-time via WebSocket updates

### Using the Chat Interface

Type natural language queries:
- "Research user pain points for PM tools"
- "Generate user stories for AI dashboard feature"
- "Create a go-to-market plan for B2B SaaS"
- "Check compliance for financial data feature"

### Viewing Insights

Navigate to the Insights page to see:
- Time saved metrics
- Agent performance analytics
- Task completion rates
- Activity charts

---

## Design System

### Color Palette

- **Base**: Charcoal `#0F1117`
- **Accents**: 
  - Neon Cyan `#00FFFF`
  - Soft Orange `#FF7A00`
- **Neutral Grays**: `#1A1D29` to `#3A3E4A`

### Typography

- **Headings**: Orbitron
- **Body**: Inter
- **Code**: Fira Code

---

## Challenge Integration

### PNC Challenge
- **RegulationAgent** specializes in financial compliance
- Checks GDPR, SOC 2, PCI-DSS, SOX, GLBA
- Risk assessment and audit reports
- Privacy review capabilities

### NVIDIA Challenge
- **Nemotron Integration** for multi-step reasoning
- Strategic orchestration of multiple agents
- Budget-controlled API calls (max 3 per session)
- Fallback to local LLM when appropriate
- Caching and smart routing

---

## Deployment

### Backend (Railway/Render)

```bash
# Deploy to Railway
railway init
railway up

# Or deploy to Render
# Connect your GitHub repo to Render
# Set environment variables in Render dashboard
```

### Frontend (Vercel/Netlify)

```bash
# Deploy to Vercel
vercel deploy

# Or deploy to Netlify
netlify deploy
```

### Environment Variables

Make sure to set all required environment variables in your deployment platform.

---

## Cost Management

### Budget: $40 Total

**Strategy:**
- **Nemotron**: Limited to 2-3 calls per major workflow
- **Ollama**: Free local inference for routine tasks
- **Caching**: Response caching to avoid duplicate API calls
- **Smart Routing**: Use Nemotron only for strategic tasks

**Estimated Costs:**
- Nemotron API: $20-30 (50-100 calls)
- Hosting: Free tier (Railway/Render + Vercel)
- Total: Well under $40

---

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

- `POST /api/v1/run_task` - Execute multi-agent workflow
- `POST /api/v1/agents/{agent_name}/execute` - Run single agent
- `GET /api/v1/agents` - Get agent status
- `WS /ws/agents` - WebSocket for real-time updates
- `GET /health` - Health check

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Acknowledgments

- **NVIDIA** for Nemotron API access
- **PNC** for the productivity challenge inspiration
- **Ollama** for local LLM infrastructure
- **LangChain/LangGraph** for agent orchestration patterns
- **FastAPI** and **React** communities

---

## Contact

- **Email**: contact@prodigypm.ai
- **Twitter**: @ProdigyPM
- **Discord**: [Join our community](https://discord.gg/prodigypm)

---

## Roadmap

- [ ] Real Ollama LLM integration
- [ ] Production Nemotron API calls
- [ ] Real FAISS vector embeddings
- [ ] Actual integration APIs (Jira, Slack, etc.)
- [ ] User authentication
- [ ] Team collaboration features
- [ ] Mobile app
- [ ] Chrome extension
- [ ] More specialized agents

---

**Built with care by the ProdigyPM Team**

**#AIforPMs #ProductManagement #NVIDIA #PNC #Hackathon2025**
