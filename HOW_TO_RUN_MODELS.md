# How to Run Models Through the Website Experience

## Quick Start Guide

### 1. Access the Dashboard

1. **Open your browser** and navigate to: `http://localhost:5173`
2. **Click "Get Started"** or navigate to `/dashboard`
3. You'll see the **ProdigyPM Dashboard** with:
   - Budget meter showing Nemotron usage
   - Quick Actions section
   - Agent panels
   - Activity feed

---

## Method 1: Quick Actions (Recommended)

### Step-by-Step:

1. **Select a Workflow** from the dropdown in the "Quick Actions" section:
   - 🤖 **Adaptive Workflow (AI-Powered)** - Intelligently selects agents based on task
   - **Full Feature Planning** - Complete workflow with risk & prioritization
   - **Research & Strategy** - Market research and strategic analysis
   - **Dev Planning** - User stories and prototyping
   - **Launch Planning** - Go-to-market and automation
   - **Compliance Check** - Regulatory compliance review

2. **Click "Run Workflow"** button

3. **Watch the agents work** in real-time via:
   - **Agents Tab**: See each agent's status change as they execute
   - **Activity Tab**: View detailed workflow execution logs
   - **WebSocket updates**: Real-time status updates

### Example Workflows:

#### Full Feature Planning
- Runs all agents in lifecycle order:
  1. Strategy Agent (340B model)
  2. Research Agent (70B model)
  3. Prioritization Agent (340B model)
  4. Risk Assessment Agent (340B model)
  5. Regulation Agent (340B model)
  6. Dev Agent (70B model)
  7. Prototype Agent (70B model)
  8. GTM Agent (340B model)
  9. Automation Agent (70B model)

#### Research & Strategy
- Runs: Strategy Agent → Research Agent
- Uses: 340B for strategy, 70B for research

#### Dev Planning
- Runs: Dev Agent → Prototype Agent
- Uses: 70B models for faster development tasks

---

## Method 2: Workflow Templates

1. **Click the "Templates" tab** in the dashboard

2. **Select a template**:
   - **New Feature Launch** → Full Feature Planning
   - **Competitive Response** → Research & Strategy
   - **Compliance Audit** → Compliance Check
   - **Sprint Planning** → Dev Planning
   - **Market Research** → Research & Strategy
   - **Adaptive** → AI-powered adaptive workflow

3. **The workflow automatically starts** with optimized agent configuration

---

## Method 3: Chat Interface

1. **Click the "Chat" tab** in the dashboard

2. **Type natural language queries** such as:
   - "Research user pain points for PM tools"
   - "Generate user stories for AI dashboard feature"
   - "Create a go-to-market plan for B2B SaaS"
   - "Check compliance for financial data feature"
   - "Develop a prototype for mobile app"

3. **The system automatically**:
   - Analyzes your message
   - Selects the appropriate workflow
   - Runs the relevant agents
   - Returns results in the chat

### Chat Examples:

| User Message | Workflow Triggered | Agents Used |
|-------------|-------------------|-------------|
| "Research competitors" | Research & Strategy | Strategy, Research |
| "Develop new feature" | Dev Planning | Dev, Prototype |
| "Launch product" | Launch Planning | GTM, Automation |
| "Check compliance" | Compliance Check | Regulation, Risk |
| "Plan full feature" | Full Feature Planning | All 9 agents |

---

## Method 4: Individual Agent Execution

### Via API (Advanced):

You can also trigger individual agents via the API:

```bash
# Execute Strategy Agent
curl -X POST http://localhost:8000/api/v1/agents/strategy/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "market_sizing",
    "input_data": {
      "target_market": "B2B SaaS",
      "product_idea": "AI-powered PM tool"
    }
  }'
```

---

## Understanding the Agent Execution

### Lifecycle Order

Agents execute in the **Product Management Lifecycle order**:

1. **Strategy** (340B) - Ideation & Strategy
2. **Research** (70B) - Research & Validation
3. **Prioritization** (340B) - Feature Prioritization
4. **Risk Assessment** (340B) - Risk Assessment
5. **Regulation** (340B) - Compliance & Regulation
6. **Development** (70B) - Development Planning
7. **Prototype** (70B) - Design & Prototyping
8. **GTM** (340B) - Go-to-Market
9. **Automation** (70B) - Automation & Monitoring

### Model Selection

- **340B Model**: Used for complex reasoning (Strategy, Prioritization, Risk, Regulation, GTM)
- **70B Model**: Used for faster tasks (Research, Dev, Prototype, Automation)

### Real-time Monitoring

Watch agents execute in real-time:
- **Agent Panels**: See status changes (idle → running → completed)
- **Activity Feed**: View detailed execution logs
- **Budget Meter**: Track Nemotron API usage
- **WebSocket**: Real-time updates without page refresh

---

## Workflow Input Data

### Custom Input Data

When running workflows, you can provide custom input:

```javascript
// Example: Research & Strategy
{
  "feature": "AI Agent Dashboard",
  "market": "B2B SaaS",
  "target_audience": "Product Managers",
  "query": "User pain points for PM tools"
}

// Example: Dev Planning
{
  "feature": "Real-time Collaboration",
  "requirements": [
    "Multi-user editing",
    "Real-time sync",
    "Conflict resolution"
  ]
}

// Example: Launch Planning
{
  "product": "ProdigyPM",
  "target_audience": "Product Managers",
  "launch_date": "2025-Q1"
}
```

---

## Viewing Results

### Activity Tab

1. **Click "Activity" tab** after running a workflow
2. **View detailed results**:
   - Agent execution logs
   - Workflow completion status
   - Results from each agent
   - Error messages (if any)

### Agent Panels

1. **Click "Agents" tab**
2. **See individual agent status**:
   - Current status (idle/running/completed/failed)
   - Last execution time
   - Model being used
   - Lifecycle stage

### Budget Meter

- **Track Nemotron usage**:
  - Calls made / remaining
  - Budget used / remaining
  - Cost per workflow
  - Recommendations

---

## Tips for Best Results

### 1. Start with Adaptive Workflow
- Let AI select the best agents for your task
- Optimal for new users

### 2. Use Specific Workflows
- **Research & Strategy**: For market research
- **Dev Planning**: For development tasks
- **Compliance Check**: For regulatory review
- **Launch Planning**: For go-to-market

### 3. Provide Clear Input
- Be specific about your feature/product
- Include target market information
- Add relevant context

### 4. Monitor Budget
- Check budget meter before running workflows
- 340B model uses more budget than 70B
- Adaptive workflow optimizes budget usage

### 5. Review Results
- Check Activity tab for detailed logs
- Review agent outputs
- Use results to inform decisions

---

## Troubleshooting

### Workflow Not Starting
- Check backend is running: `http://localhost:8000/health`
- Check frontend is running: `http://localhost:5173`
- Check browser console for errors

### No Results Showing
- Check Activity tab for error messages
- Verify WebSocket connection (check browser console)
- Check backend logs: `/tmp/backend.log`

### Agents Stuck
- Refresh the page
- Check backend status
- Review agent logs in Activity tab

### Budget Exceeded
- Check Budget Meter for remaining budget
- Use 70B model workflows (faster, cheaper)
- Wait for budget reset (if configured)

---

## API Endpoints

### Run Workflow
```bash
POST http://localhost:8000/api/v1/run_task
{
  "workflow_type": "full_feature_planning",
  "input_data": {
    "feature": "AI Dashboard",
    "market": "B2B SaaS"
  },
  "use_nemotron": true
}
```

### Execute Single Agent
```bash
POST http://localhost:8000/api/v1/agents/{agent_name}/execute
{
  "task_type": "market_sizing",
  "input_data": {
    "target_market": "B2B SaaS"
  }
}
```

### Get Agent Status
```bash
GET http://localhost:8000/api/v1/agents
```

### Get Budget Status
```bash
GET http://localhost:8000/api/v1/budget/status
```

---

## Next Steps

1. **Try Adaptive Workflow**: Start with AI-powered workflow selection
2. **Experiment with Chat**: Use natural language to trigger workflows
3. **Review Templates**: Explore pre-configured workflow templates
4. **Monitor Activity**: Watch agents execute in real-time
5. **Check Results**: Review outputs in Activity tab

---

## Support

- **Backend API Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`
- **Frontend**: `http://localhost:5173`
- **Backend Logs**: Check `/tmp/backend.log`

Happy workflow execution! 🚀

