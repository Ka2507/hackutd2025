# 🎯 Where to See All the New Features in the UI

## Quick Navigation Guide

### 1. **Budget Meter & Cost-Aware Orchestration** 💰
**Location**: Dashboard → Top of page (left side)
- Shows real-time API budget usage ($40 total)
- Color-coded status (green/yellow/red)
- Budget recommendations
- Updates every 10 seconds

**What it shows**:
- Used budget vs remaining
- Budget status (healthy/warning/critical)
- Smart recommendations based on usage

---

### 2. **System Status Card** ✨
**Location**: Dashboard → Top of page (right side)
- Shows "9 Agents Active"
- Lists all new features:
  - ✨ Adaptive Workflows
  - Risk Assessment
  - Smart Prioritization
  - Agent Collaboration

---

### 3. **Adaptive Workflow** 🤖
**Location**: Dashboard → Quick Actions dropdown
- **First option**: "🤖 Adaptive Workflow (AI-Powered)"
- Description: "Intelligently selects agents based on task"

**How to use**:
1. Select "Adaptive Workflow" from dropdown
2. Click "Run Workflow"
3. System dynamically selects optimal agents
4. Check Activity tab to see which agents were selected

**What makes it special**:
- Uses Nemotron to analyze task
- Selects agents dynamically (not fixed sequence)
- Can run agents in parallel
- Self-corrects if quality is low

---

### 4. **Workflow Templates** 📋
**Location**: Dashboard → "Templates" tab (new tab!)
- Click "Templates" tab at the top
- See all pre-built templates:
  - New Feature Launch
  - Competitive Response
  - Compliance Audit
  - Sprint Planning
  - Market Research
  - Adaptive Workflow

**How to use**:
1. Go to Templates tab
2. Click any template
3. It automatically selects the workflow
4. Returns to Agents tab with workflow ready to run

---

### 5. **Risk Assessment** ⚠️
**Location**: Activity tab → After running "Full Feature Planning" workflow

**What you'll see**:
- Risk score badge (0.0-1.0)
- Risk level (Low/Medium/High)
- Predicted bottlenecks list
- Mitigation strategies

**When it appears**:
- Automatically runs during "Full Feature Planning"
- Shows in Activity tab after workflow completes
- Also available via API: `/api/v1/risk/assess`

---

### 6. **Smart Prioritization** 📊
**Location**: Activity tab → After running "Full Feature Planning" workflow

**What you'll see**:
- Prioritized features with scores
- Multi-factor breakdown:
  - Market Impact
  - User Value
  - Effort
  - Risk
  - Strategic Alignment
- AI explanation of ranking

**When it appears**:
- Automatically runs after Dev Agent generates stories
- Shows in Activity tab
- Also available via API: `/api/v1/prioritize`

---

### 7. **Agent Collaboration** 🤝
**Location**: Activity tab → Look for "Agent Collaboration" card

**What you'll see**:
- Indicator when agents validate each other
- Refinement requests
- Cross-agent validation results

**How to trigger**:
- Runs automatically in adaptive workflows
- Agents validate each other's outputs
- Shows in workflow results

---

### 8. **Enhanced Workflow Results** 🎨
**Location**: Activity tab → Click on any completed workflow

**What's new**:
- **Adaptive Workflow Indicator**: Shows when workflow was dynamically planned
- **Risk Assessment Card**: Red card with risk score and mitigations
- **Prioritization Card**: Blue card with prioritized features
- **Agent Collaboration Badge**: Purple indicator for collaboration

**Before**: Just showed JSON dump
**Now**: Beautiful cards showing:
- Risk scores with color coding
- Prioritized features with scores
- Bottleneck predictions
- Mitigation strategies

---

### 9. **9 Agents (Not 7)** 👥
**Location**: Dashboard → Agents tab

**New agents visible**:
- Risk Assessment Agent
- Prioritization Agent

**All 9 agents**:
1. Strategy
2. Research
3. Development
4. Prototype
5. Go-to-Market
6. Automation
7. Regulation
8. **Risk Assessment** (NEW)
9. **Prioritization** (NEW)

---

## 🎬 Demo Flow to See Everything

### Step 1: Check Budget
- Go to Dashboard
- See Budget Meter at top (shows $40 budget)

### Step 2: Try Adaptive Workflow
- Select "🤖 Adaptive Workflow (AI-Powered)" from dropdown
- Click "Run Workflow"
- Watch agents execute dynamically

### Step 3: Try Templates
- Click "Templates" tab
- Browse pre-built templates
- Click one to select it

### Step 4: Run Full Feature Planning
- Select "Full Feature Planning" workflow
- Click "Run Workflow"
- Go to "Activity" tab
- See:
  - Risk Assessment card (red)
  - Prioritization card (blue)
  - All agent results

### Step 5: Check Activity Tab
- See enhanced workflow results
- Risk scores
- Prioritized features
- Agent collaboration indicators

---

## 🔍 API Endpoints (For Testing)

You can also test features directly via API:

1. **Budget Status**: `GET http://localhost:8000/api/v1/budget/status`
2. **Risk Assessment**: `POST http://localhost:8000/api/v1/risk/assess`
3. **Prioritization**: `POST http://localhost:8000/api/v1/prioritize`
4. **Templates**: `GET http://localhost:8000/api/v1/workflows/templates`
5. **Similar Projects**: `GET http://localhost:8000/api/v1/projects/{id}/similar`

---

## 🎯 Key Visual Indicators

- **🤖 Robot icon**: Adaptive/AI-powered features
- **Red cards**: Risk-related content
- **Blue cards**: Prioritization results
- **Purple badges**: Agent collaboration
- **Green badges**: Budget healthy
- **Yellow badges**: Budget warning
- **Red badges**: Budget critical

---

## 💡 Pro Tips

1. **Run "Full Feature Planning"** to see all features at once
2. **Check Activity tab** after workflows complete to see enhanced results
3. **Use Templates tab** to quickly select optimized workflows
4. **Watch Budget Meter** to see cost-aware orchestration in action
5. **Try Adaptive Workflow** to see dynamic agent selection

---

**All features are now visible in the UI!** 🎉

