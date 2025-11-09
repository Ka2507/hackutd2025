# How to Start ProdigyPM Services

## Quick Start

### Option 1: Automatic Start (Both Services)

```bash
# Terminal 1 - Backend
cd /Users/frootyloops44/Desktop/hackutd2025/backend
source venv/bin/activate
python main.py

# Terminal 2 - Frontend
cd /Users/frootyloops44/Desktop/hackutd2025/frontend
npm run dev
```

### Option 2: Background Start

```bash
# Start Backend in Background
cd /Users/frootyloops44/Desktop/hackutd2025/backend
source venv/bin/activate
python main.py > /tmp/backend.log 2>&1 &

# Start Frontend in Background
cd /Users/frootyloops44/Desktop/hackutd2025/frontend
npm run dev > /tmp/frontend.log 2>&1 &
```

## Service URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **WebSocket**: ws://localhost:8000/ws/agents

## Verify Services are Running

### Check Frontend
```bash
curl http://localhost:5173
# Should return HTML (status 200)
```

### Check Backend
```bash
curl http://localhost:8000/health
# Should return JSON with status: "healthy"
```

### Check Ports
```bash
# Check if ports are in use
lsof -ti:5173 && echo "Frontend running" || echo "Frontend NOT running"
lsof -ti:8000 && echo "Backend running" || echo "Backend NOT running"
```

## Troubleshooting

### Frontend Not Starting

1. **Check if port 5173 is already in use**
   ```bash
   lsof -ti:5173 | xargs kill -9
   ```

2. **Check Node.js version**
   ```bash
   node --version  # Should be 18+
   ```

3. **Reinstall dependencies**
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Check frontend logs**
   ```bash
   tail -f /tmp/frontend.log
   ```

### Backend Not Starting

1. **Check if port 8000 is already in use**
   ```bash
   lsof -ti:8000 | xargs kill -9
   ```

2. **Check Python version**
   ```bash
   python3 --version  # Should be 3.10+
   ```

3. **Activate virtual environment**
   ```bash
   cd backend
   source venv/bin/activate
   ```

4. **Check backend logs**
   ```bash
   tail -f /tmp/backend.log
   ```

5. **Verify dependencies**
   ```bash
   cd backend
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### WebSocket Connection Issues

1. **Verify backend is running**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check WebSocket endpoint**
   ```bash
   # Should see WebSocket connection in backend logs
   tail -f /tmp/backend.log | grep -i websocket
   ```

3. **Check browser console**
   - Open browser DevTools
   - Look for WebSocket connection messages
   - Check for CORS errors

### Multiple Backend Processes

If you have multiple backend processes:

```bash
# List all Python processes on port 8000
lsof -ti:8000

# Kill all processes on port 8000
lsof -ti:8000 | xargs kill -9

# Restart backend
cd backend
source venv/bin/activate
python main.py
```

## Service Management Scripts

### Start Both Services
```bash
#!/bin/bash
# start_services.sh

# Start Backend
cd backend
source venv/bin/activate
python main.py > /tmp/backend.log 2>&1 &
echo $! > /tmp/backend.pid
echo "Backend started (PID: $(cat /tmp/backend.pid))"

# Start Frontend
cd ../frontend
npm run dev > /tmp/frontend.log 2>&1 &
echo $! > /tmp/frontend.pid
echo "Frontend started (PID: $(cat /tmp/frontend.pid))"

echo "Services started!"
echo "Frontend: http://localhost:5173"
echo "Backend: http://localhost:8000"
```

### Stop Both Services
```bash
#!/bin/bash
# stop_services.sh

# Stop Backend
if [ -f /tmp/backend.pid ]; then
    kill $(cat /tmp/backend.pid) 2>/dev/null
    rm /tmp/backend.pid
    echo "Backend stopped"
fi

# Stop Frontend
if [ -f /tmp/frontend.pid ]; then
    kill $(cat /tmp/frontend.pid) 2>/dev/null
    rm /tmp/frontend.pid
    echo "Frontend stopped"
fi

# Kill any processes on ports
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:5173 | xargs kill -9 2>/dev/null

echo "All services stopped"
```

## Common Issues

### "Connection Refused" Errors

**Cause**: Service is not running or port is blocked

**Solution**:
1. Check if service is running: `lsof -ti:5173` or `lsof -ti:8000`
2. Start the service if not running
3. Check firewall settings
4. Verify port is not blocked by another application

### "Port Already in Use" Errors

**Cause**: Another process is using the port

**Solution**:
```bash
# Find process using port
lsof -ti:5173  # or 8000

# Kill the process
lsof -ti:5173 | xargs kill -9
```

### WebSocket Connection Fails

**Cause**: Backend not running or CORS issue

**Solution**:
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check backend logs for WebSocket errors
3. Verify CORS is configured in backend
4. Check browser console for specific errors

### Frontend Can't Connect to Backend

**Cause**: Backend not running or wrong URL

**Solution**:
1. Verify backend is running
2. Check `VITE_API_URL` in frontend `.env` file
3. Default should be: `http://localhost:8000`
4. Check browser Network tab for API calls

## Logs

### View Backend Logs
```bash
tail -f /tmp/backend.log
```

### View Frontend Logs
```bash
tail -f /tmp/frontend.log
```

### View Both Logs
```bash
tail -f /tmp/backend.log /tmp/frontend.log
```

## Next Steps

1. **Verify Services**: Check both frontend and backend are running
2. **Open Browser**: Navigate to http://localhost:5173
3. **Check Console**: Open browser DevTools and check for errors
4. **Test WebSocket**: Run a workflow and verify real-time updates
5. **Check Logs**: Monitor logs for any errors

## Quick Commands

```bash
# Start backend
cd backend && source venv/bin/activate && python main.py

# Start frontend
cd frontend && npm run dev

# Check status
curl http://localhost:8000/health && curl http://localhost:5173

# Kill services
lsof -ti:8000 | xargs kill -9 && lsof -ti:5173 | xargs kill -9
```

Happy coding! 🚀

