# WebSocket Connection Troubleshooting

## Understanding the WebSocket Error

The error message you're seeing:
```
WebSocket connection to 'ws://localhost:8000/ws/agents' failed: 
WebSocket is closed before the connection is established.
```

This indicates that the WebSocket connection is being attempted but closed before it fully establishes.

## What Was Fixed

### 1. Improved Connection Handling
- Added better state checking before creating new connections
- Prevented multiple simultaneous connection attempts
- Added proper handling for CONNECTING, OPEN, CLOSING, and CLOSED states

### 2. Better Error Handling
- More descriptive error messages
- Proper cleanup of connection attempts
- Prevention of connection leaks

### 3. Ping/Pong Keepalive
- Added ping/pong mechanism to keep connection alive
- Backend responds to ping messages with pong
- Helps detect dead connections

### 4. Improved Reconnection Logic
- Only reconnects when necessary
- Avoids immediate reconnection on connection failures
- Cleans up old connections before creating new ones

## Common Causes

### 1. Backend Not Running
**Solution**: Ensure backend is running on port 8000
```bash
curl http://localhost:8000/health
```

### 2. CORS Issues
**Solution**: Backend CORS is configured, but check browser console for CORS errors

### 3. Multiple Connection Attempts
**Solution**: Fixed in the code - now prevents multiple simultaneous connections

### 4. Component Re-rendering
**Solution**: Fixed useEffect dependency to only run once on mount

### 5. Network Issues
**Solution**: Check network connectivity and firewall settings

## How to Verify It's Working

### 1. Check Browser Console
Look for:
- ✅ "Connecting to WebSocket: ws://localhost:8000/ws/agents"
- ✅ "WebSocket connected successfully"
- ❌ Should NOT see multiple "WebSocket disconnected" messages immediately

### 2. Check Backend Logs
```bash
tail -f /tmp/backend.log | grep -i websocket
```

You should see:
- "WebSocket connected. Total connections: X"
- No immediate disconnections

### 3. Test Connection
Open browser DevTools → Network → WS tab
- Should see connection to `ws://localhost:8000/ws/agents`
- Status should be "101 Switching Protocols"
- Connection should stay open

## If Issues Persist

### 1. Clear Browser Cache
- Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
- Clear browser cache and cookies

### 2. Check Backend Status
```bash
# Check if backend is running
ps aux | grep "python main.py"

# Check backend logs
tail -50 /tmp/backend.log

# Test WebSocket endpoint
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: test" \
  http://localhost:8000/ws/agents
```

### 3. Restart Backend
```bash
# Kill existing backend
lsof -ti:8000 | xargs kill -9

# Restart backend
cd backend
source venv/bin/activate
python main.py
```

### 4. Check Frontend
```bash
# Check if frontend is running
curl http://localhost:5173

# Restart frontend if needed
cd frontend
npm run dev
```

## Expected Behavior

### On Page Load
1. Frontend connects to WebSocket
2. Backend accepts connection
3. Backend sends initial "connected" message
4. Connection stays open
5. Real-time updates flow through WebSocket

### During Workflow Execution
1. Backend sends "agent_started" messages
2. Frontend updates agent status in real-time
3. Backend sends "agent_completed" messages
4. Frontend displays results

### On Disconnect
1. Frontend detects disconnect
2. Waits 3 seconds
3. Automatically reconnects if callbacks exist
4. Resumes receiving updates

## Debugging Tips

### Enable Debug Logging
In browser console:
```javascript
localStorage.setItem('debug', 'websocket');
```

### Monitor WebSocket Messages
In browser console:
```javascript
// Intercept WebSocket messages
const originalSend = WebSocket.prototype.send;
WebSocket.prototype.send = function(data) {
  console.log('WS Send:', data);
  return originalSend.call(this, data);
};
```

### Check Connection State
In browser console:
```javascript
// Check WebSocket state
console.log('WS State:', apiClient.ws?.readyState);
// 0 = CONNECTING
// 1 = OPEN
// 2 = CLOSING
// 3 = CLOSED
```

## Solutions Applied

1. ✅ Fixed multiple connection attempts
2. ✅ Improved connection state handling
3. ✅ Added ping/pong keepalive
4. ✅ Better error messages
5. ✅ Proper cleanup on unmount
6. ✅ Smart reconnection logic

## Next Steps

If you're still experiencing issues:
1. Check browser console for specific error messages
2. Check backend logs for WebSocket errors
3. Verify both frontend and backend are running
4. Try refreshing the page
5. Check network tab in DevTools for WebSocket connection status

The WebSocket should now connect successfully and stay connected for real-time updates!

