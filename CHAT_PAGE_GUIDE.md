# Chat Page Guide - Intelligent Task-Based Agent Execution

## Overview

The Chat page (`/chat`) is an intelligent interface where users can describe what they want to do in natural language, and the system automatically selects the appropriate workflow and agents to accomplish the task.

## Accessing the Chat Page

**URL**: `http://localhost:5173/chat`

### From Home Page
1. Navigate to `http://localhost:5173`
2. Click **"Start Chat with AI Co-Pilot"** button
3. You'll be taken to the chat interface

### Direct Access
- Type `http://localhost:5173/chat` in your browser

## How It Works

### 1. Intelligent Task Analysis

The system analyzes your message and automatically determines:
- **Workflow Type**: Which workflow to use (full_feature_planning, research_and_strategy, etc.)
- **Confidence Score**: How confident the system is in its analysis
- **Agents Needed**: Which agents should be involved
- **Input Data**: Extracts relevant information (product name, market, requirements, etc.)

### 2. Workflow Selection

Based on keywords and context, the system selects:

| User Input Keywords | Workflow Type | Agents Used |
|-------------------|---------------|-------------|
| "create", "build", "entire thing", "new feature" | Full Feature Planning | All 9 agents (Strategy → Research → Prioritization → Risk → Regulation → Dev → Prototype → GTM → Automation) |
| "product strategy", "go-to-market", "launch strategy" | Launch Planning | Strategy, Research, GTM, Automation |
| "research", "analyze", "competitor", "market research" | Research & Strategy | Strategy, Research |
| "develop", "build", "user story", "sprint", "backlog" | Dev Planning | Dev, Prototype |
| "compliance", "regulation", "legal", "audit", "gdpr" | Compliance Check | Regulation, Risk |
| "prioritize", "roadmap", "which feature" | Adaptive | Prioritization, Strategy, Research |
| Other/Unknown | Adaptive | AI-selected agents based on task |

### 3. Agent Execution

Agents execute in the **Product Management Lifecycle order**:

1. **Strategy Agent** (340B) - Ideation & Strategy
2. **Research Agent** (70B) - Research & Validation
3. **Prioritization Agent** (340B) - Feature Prioritization
4. **Risk Assessment Agent** (340B) - Risk Assessment
5. **Regulation Agent** (340B) - Compliance & Regulation
6. **Development Agent** (70B) - Development Planning
7. **Prototype Agent** (70B) - Design & Prototyping
8. **GTM Agent** (340B) - Go-to-Market
9. **Automation Agent** (70B) - Automation & Monitoring

## Example Tasks

### Full Feature Creation
**User Input**: 
```
"Create a new AI-powered analytics dashboard feature for product managers"
```

**System Response**:
- Detects: Full Feature Planning workflow
- Confidence: 95%
- Agents: All 9 agents
- Extracts: Feature name, target audience, market

### Product Strategy
**User Input**:
```
"Create a product strategy for a B2B SaaS tool for product managers"
```

**System Response**:
- Detects: Launch Planning workflow
- Confidence: 90%
- Agents: Strategy, Research, GTM, Automation
- Extracts: Product name, target market, audience

### Research Task
**User Input**:
```
"Research competitors in the AI product management space"
```

**System Response**:
- Detects: Research & Strategy workflow
- Confidence: 85%
- Agents: Strategy, Research
- Extracts: Research query, sources

### Development Task
**User Input**:
```
"Develop user stories for a real-time collaboration feature"
```

**System Response**:
- Detects: Dev Planning workflow
- Confidence: 90%
- Agents: Dev, Prototype
- Extracts: Feature name, requirements

### Compliance Check
**User Input**:
```
"Check compliance requirements for a financial data feature in the US"
```

**System Response**:
- Detects: Compliance Check workflow
- Confidence: 95%
- Agents: Regulation, Risk
- Extracts: Feature name, jurisdiction

## Features

### Real-Time Updates
- See agents start and complete in real-time
- Watch workflow execution progress
- View agent status and results

### Active Agents Sidebar
- Shows which agents are currently working
- Displays agent goals and status
- Updates automatically as agents complete

### Budget Monitoring
- Budget meter shows Nemotron API usage
- Tracks remaining budget and calls
- Helps manage API costs

### Message History
- All messages are saved in the conversation
- See workflow analysis and reasoning
- Review agent outputs and results

## UI Components

### Header
- **Back Button**: Return to home page
- **Title**: "AI PM Co-Pilot"
- **Budget Meter**: Shows Nemotron usage
- **Active Agents Counter**: Number of agents currently working

### Chat Area
- **Messages**: User messages and agent responses
- **Agent Status**: Real-time agent execution updates
- **Workflow Results**: Formatted results from agents

### Input Area
- **Text Input**: Describe your task
- **Send Button**: Submit your request
- **Placeholder**: Example prompts and suggestions

### Sidebar (When Agents Active)
- **Active Agents Panel**: Shows agents currently working
- **Agent Status**: Real-time status updates
- **Agent Goals**: What each agent is working on

## Tips for Best Results

### 1. Be Specific
- Include product/feature names
- Mention target market or audience
- Add relevant requirements or constraints

### 2. Use Natural Language
- Write as you would to a colleague
- Don't worry about technical jargon
- The system understands context

### 3. Provide Context
- Include business goals
- Mention competitors if relevant
- Specify target audience or market

### 4. Examples of Good Prompts

✅ **Good**:
- "Create a product strategy for a B2B SaaS tool for product managers"
- "Research competitors in the AI product management space"
- "Develop user stories for a real-time collaboration feature with multi-user editing"
- "Check compliance for a financial data feature in the EU"

❌ **Less Effective**:
- "Help me" (too vague)
- "Do something" (no specific task)
- "Work" (unclear what to do)

## Workflow Details

### Full Feature Planning
**When to use**: Creating a complete new feature or product

**Agents Used**: All 9 agents in lifecycle order
1. Strategy - Market analysis
2. Research - User research
3. Prioritization - Feature prioritization
4. Risk - Risk assessment
5. Regulation - Compliance check
6. Dev - User stories
7. Prototype - Design mockups
8. GTM - Launch strategy
9. Automation - Workflow setup

### Launch Planning
**When to use**: Planning a product launch or go-to-market strategy

**Agents Used**: Strategy, Research, GTM, Automation
- Strategic planning
- Market research
- Launch strategy
- Automation setup

### Research & Strategy
**When to use**: Market research, competitor analysis

**Agents Used**: Strategy, Research
- Market analysis
- Competitor research
- Strategic insights

### Dev Planning
**When to use**: Development planning, user stories, technical specs

**Agents Used**: Dev, Prototype
- User stories
- Technical specifications
- Design mockups

### Compliance Check
**When to use**: Regulatory compliance, audit preparation

**Agents Used**: Regulation, Risk
- Compliance checks
- Risk assessment
- Audit reports

### Adaptive Workflow
**When to use**: Unknown tasks or when you want AI to decide

**Agents Used**: AI-selected based on task
- Intelligent agent selection
- Dynamic workflow planning
- Context-aware execution

## Monitoring Execution

### Real-Time Updates
- **Agent Started**: See when agents begin working
- **Agent Completed**: See when agents finish
- **Workflow Completed**: See final results

### Status Indicators
- 🟢 **Running**: Agent is actively working
- ✅ **Completed**: Agent finished successfully
- ❌ **Failed**: Agent encountered an error
- ⚪ **Idle**: Agent is waiting

### Results Display
- **Formatted Output**: Easy-to-read results
- **Agent Contributions**: What each agent produced
- **Workflow Summary**: Overall workflow results

## Troubleshooting

### Workflow Not Starting
- Check backend is running: `http://localhost:8000/health`
- Check browser console for errors
- Verify WebSocket connection

### Agents Not Appearing
- Check WebSocket connection status
- Verify agents are initialized in backend
- Check browser console for WebSocket errors

### Results Not Showing
- Wait for workflow to complete
- Check Activity tab for detailed logs
- Review browser console for errors

### Wrong Workflow Selected
- Be more specific in your prompt
- Use keywords that match desired workflow
- Try adaptive workflow for AI selection

## Next Steps

1. **Try It Out**: Navigate to `/chat` and start a conversation
2. **Experiment**: Try different types of tasks
3. **Monitor**: Watch agents work in real-time
4. **Review**: Check results and agent outputs

## Examples to Try

1. **"Create a product strategy for a B2B SaaS AI tool"**
2. **"Research competitors in the product management software market"**
3. **"Develop user stories for a real-time collaboration feature"**
4. **"Create the entire thing for a new mobile app for task management"**
5. **"Check compliance for a financial data processing feature"**
6. **"Prioritize features for a project management tool"**

Happy chatting! 🚀

