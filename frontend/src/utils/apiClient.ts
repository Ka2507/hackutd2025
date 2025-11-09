/**
 * API Client for ProdigyPM Backend
 * Handles all HTTP requests and WebSocket connections
 */
import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class APIClient {
  private client: AxiosInstance;
  private ws: WebSocket | null = null;
  private wsCallbacks: Set<(data: any) => void> = new Set();
  private reconnectTimeout: ReturnType<typeof setTimeout> | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Projects
  async createProject(name: string, description?: string) {
    const response = await this.client.post('/api/v1/projects', { name, description });
    return response.data;
  }

  async listProjects() {
    const response = await this.client.get('/api/v1/projects');
    return response.data;
  }

  async getProject(projectId: number) {
    const response = await this.client.get(`/api/v1/projects/${projectId}`);
    return response.data;
  }

  // Workflows
  async runTask(workflowType: string, inputData: any, projectId?: number, useNemotron = true) {
    const response = await this.client.post('/api/v1/run_task', {
      workflow_type: workflowType,
      input_data: inputData,
      project_id: projectId,
      use_nemotron: useNemotron,
    });
    return response.data;
  }

  async listWorkflows() {
    const response = await this.client.get('/api/v1/workflows');
    return response.data;
  }

  async getWorkflowHistory(limit = 10) {
    const response = await this.client.get(`/api/v1/workflows/history?limit=${limit}`);
    return response.data;
  }

  // Agents
  async executeAgent(agentName: string, taskType: string, inputData: any, projectId?: number) {
    const response = await this.client.post(`/api/v1/agents/${agentName}/execute`, {
      agent_name: agentName,
      task_type: taskType,
      input_data: inputData,
      project_id: projectId,
    });
    return response.data;
  }

  async getAgentsStatus() {
    const response = await this.client.get('/api/v1/agents');
    return response.data;
  }

  // Conversations
  async addConversation(projectId: number, message: string, metadata?: any) {
    const response = await this.client.post('/api/v1/conversations', {
      project_id: projectId,
      message,
      metadata,
    });
    return response.data;
  }

  async getConversations(projectId: number, limit = 50) {
    const response = await this.client.get(`/api/v1/conversations/${projectId}?limit=${limit}`);
    return response.data;
  }

  // Health
  async healthCheck() {
    const response = await this.client.get('/health');
    return response.data;
  }

  // Budget
  async getBudgetStatus() {
    const response = await this.client.get('/api/v1/budget/status');
    return response.data;
  }

  // Risk Assessment
  async assessRisk(workflowState: any, projectId?: number, riskFactors?: string[]) {
    const response = await this.client.post('/api/v1/risk/assess', {
      workflow_state: workflowState,
      project_id: projectId,
      risk_factors: riskFactors,
    });
    return response.data;
  }

  // Prioritization
  async prioritizeFeatures(features: any[], context: any, method = 'multi_factor') {
    const response = await this.client.post('/api/v1/prioritize', {
      features,
      context,
      method,
    });
    return response.data;
  }

  // Workflow Templates
  async listWorkflowTemplates() {
    const response = await this.client.get('/api/v1/workflows/templates');
    return response.data;
  }

  async recommendTemplate(projectDescription: string) {
    const response = await this.client.get('/api/v1/workflows/templates/recommend', {
      params: { project_description: projectDescription },
    });
    return response.data;
  }

  // Integrations
  async getJiraSprint(sprintId: string) {
    const response = await this.client.get(`/api/v1/integrations/jira/sprint/${sprintId}`);
    return response.data;
  }

  async searchReddit(subreddit: string, query: string, limit = 10) {
    const response = await this.client.get('/api/v1/integrations/reddit/search', {
      params: { subreddit, query, limit },
    });
    return response.data;
  }

  async getFigmaFile(fileKey: string) {
    const response = await this.client.get(`/api/v1/integrations/figma/file/${fileKey}`);
    return response.data;
  }

  // WebSocket
  connectWebSocket(onMessage: (data: any) => void) {
    // If already connected and callback not registered, just add callback
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.wsCallbacks.add(onMessage);
      return () => {
        this.wsCallbacks.delete(onMessage);
      };
    }

    // If connection exists but not open, wait for it
    if (this.ws && this.ws.readyState === WebSocket.CONNECTING) {
      // Wait for connection to open, then add callback
      this.wsCallbacks.add(onMessage);
      // Store original onopen if it exists
      const originalOnOpen = this.ws.onopen;
      this.ws.onopen = (event: Event) => {
        if (originalOnOpen) {
          try {
            originalOnOpen.call(this.ws!, event);
          } catch (e) {
            // Ignore errors from original handler
          }
        }
        console.log('WebSocket connected (existing connection)');
      };
      return () => {
        this.wsCallbacks.delete(onMessage);
      };
    }

    // If connection is closing, wait and create new one
    if (this.ws && this.ws.readyState === WebSocket.CLOSING) {
      this.wsCallbacks.add(onMessage);
      // Wait for close, then create new connection
      const checkClose = setInterval(() => {
        if (!this.ws || this.ws.readyState === WebSocket.CLOSED) {
          clearInterval(checkClose);
          this.ws = null;
          this.connectWebSocket(onMessage);
        }
      }, 100);
      return () => {
        clearInterval(checkClose);
        this.wsCallbacks.delete(onMessage);
      };
    }

    // Create new connection
    const wsUrl = API_BASE_URL.replace('http', 'ws') + '/ws/agents';
    console.log('Connecting to WebSocket:', wsUrl);
    
    try {
      this.ws = new WebSocket(wsUrl);
      this.wsCallbacks.add(onMessage);
      
      this.ws.onopen = () => {
        console.log('WebSocket connected successfully');
        // Send a ping to keep connection alive
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(JSON.stringify({ type: 'ping' }));
        }
      };
      
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          // Don't process ping/pong messages
          if (data.type === 'pong') {
            return;
          }
          // Call all registered callbacks
          this.wsCallbacks.forEach(callback => {
            try {
              callback(data);
            } catch (err) {
              console.error('Error in WebSocket callback:', err);
            }
          });
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };
      
      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        // Don't log as error if it's just a connection issue
        if (this.ws?.readyState === WebSocket.CONNECTING) {
          console.warn('WebSocket connection in progress, this error may be expected');
        }
      };
      
      this.ws.onclose = (event) => {
        console.log('WebSocket disconnected', {
          code: event.code,
          reason: event.reason,
          wasClean: event.wasClean,
          callbacks: this.wsCallbacks.size
        });
        
        // Clear the connection reference
        this.ws = null;
        
        // Only auto-reconnect if we have callbacks registered and it wasn't a clean close (1000)
        if (this.wsCallbacks.size > 0 && event.code !== 1000) {
          console.log(`Attempting to reconnect WebSocket in 3 seconds... (code: ${event.code})`);
          
          // Clear any existing reconnect timeout
          if (this.reconnectTimeout) {
            clearTimeout(this.reconnectTimeout);
          }
          
          this.reconnectTimeout = setTimeout(() => {
            // Only reconnect if still have callbacks and no active connection
            if (this.wsCallbacks.size > 0 && (!this.ws || this.ws.readyState === WebSocket.CLOSED)) {
              console.log('Reconnecting WebSocket...');
              // Create a new connection for the first callback
              const firstCallback = Array.from(this.wsCallbacks)[0];
              if (firstCallback) {
                this.ws = null; // Ensure old connection is cleared
                this.connectWebSocket(firstCallback);
              }
            }
            this.reconnectTimeout = null;
          }, 3000);
        } else {
          console.log('WebSocket closed cleanly or no callbacks, not reconnecting');
          if (this.reconnectTimeout) {
            clearTimeout(this.reconnectTimeout);
            this.reconnectTimeout = null;
          }
        }
      };
    } catch (error) {
      console.error('Error creating WebSocket:', error);
      this.wsCallbacks.delete(onMessage);
    }
    
    return () => {
      this.wsCallbacks.delete(onMessage);
      // Only close if no more callbacks and connection is open
      if (this.wsCallbacks.size === 0 && this.ws && this.ws.readyState === WebSocket.OPEN) {
        console.log('Closing WebSocket (no more callbacks)');
        this.ws.close(1000, 'No more callbacks');
        this.ws = null;
      }
    };
  }

  sendWebSocketMessage(message: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }
}

export const apiClient = new APIClient();
export default apiClient;

