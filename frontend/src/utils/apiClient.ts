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
    const wsUrl = API_BASE_URL.replace('http', 'ws') + '/ws/agents';
    
    this.ws = new WebSocket(wsUrl);
    
    this.ws.onopen = () => {
      console.log('WebSocket connected');
    };
    
    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.wsCallbacks.forEach(callback => callback(data));
        onMessage(data);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };
    
    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      // Auto-reconnect after 3 seconds
      setTimeout(() => {
        if (this.wsCallbacks.size > 0) {
          this.connectWebSocket(onMessage);
        }
      }, 3000);
    };
    
    this.wsCallbacks.add(onMessage);
    
    return () => {
      this.wsCallbacks.delete(onMessage);
      if (this.wsCallbacks.size === 0 && this.ws) {
        this.ws.close();
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

