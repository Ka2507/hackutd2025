# Starting ProdigyPM Locally

## Current Status

**Frontend**: Running on http://localhost:5173
**Backend**: Needs dependencies installed

## Quick Fix for Backend

Open a new terminal and run:

```bash
cd /Users/kaustubhannavarapu/ProdigyPM/backend

# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend
python main.py
```

Backend should start on http://localhost:8000

## Current Frontend Status

The frontend is already running! Open your browser to:

**http://localhost:5173**

You should see:
- ProdigyPM landing page
- "Get Started" button
- Agent showcase
- Clean, professional design

## What's Working Now

- Frontend React application (running)
- UI components and pages
- Navigation
- Design system with TailwindCSS

## What Needs Backend

- API calls
- Agent execution
- WebSocket real-time updates
- Data persistence

## Quick Test Without Backend

The frontend will load and display the UI, but:
- API calls will fail (expected)
- Agent workflows won't execute
- Chat won't work
- But you can see the design and layout!

## GitHub Repository

Your code is successfully pushed to:
**https://github.com/Ka2507/hackutd2025**

All 57 files committed and available online.

