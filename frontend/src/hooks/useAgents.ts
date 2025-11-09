/**
 * Custom React hook for managing agents state
 */
import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '@/utils/apiClient';

export interface AgentStatus {
  name: string;
  status: string;
  goal: string;
  quality_score?: number;
  reasoning?: string[];
  collaborating_with?: string[];
  last_output?: any;
}

export interface AgentsState {
  [key: string]: AgentStatus;
}

export interface WebSocketMessage {
  type: string;
  data: any;
}

export const useAgents = () => {
  const [agents, setAgents] = useState<AgentsState>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [wsMessages, setWsMessages] = useState<WebSocketMessage[]>([]);

  // Fetch initial agents status
  const fetchAgents = useCallback(async () => {
    try {
      setLoading(true);
      const response = await apiClient.getAgentsStatus();
      if (response.success) {
        setAgents(response.agents);
      }
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch agents');
      console.error('Error fetching agents:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Execute a specific agent task
  const executeAgent = useCallback(async (
    agentName: string,
    taskType: string,
    inputData: any,
    projectId?: number
  ) => {
    try {
      const response = await apiClient.executeAgent(agentName, taskType, inputData, projectId);
      return response;
    } catch (err: any) {
      console.error(`Error executing agent ${agentName}:`, err);
      throw err;
    }
  }, []);

  // Run a full workflow
  const runWorkflow = useCallback(async (
    workflowType: string,
    inputData: any,
    projectId?: number,
    useNemotron = true
  ) => {
    try {
      const response = await apiClient.runTask(workflowType, inputData, projectId, useNemotron);
      return response;
    } catch (err: any) {
      console.error('Error running workflow:', err);
      throw err;
    }
  }, []);

  // WebSocket connection
  useEffect(() => {
    const handleWebSocketMessage = (data: WebSocketMessage) => {
      setWsMessages(prev => [...prev.slice(-50), data]); // Keep last 50 messages
      
      // Update agent status based on WebSocket messages
      if (data.type === 'agent_started' || data.type === 'agent_completed' || data.type === 'agent_status') {
        const agentName = data.data.agent || data.data.agent_name;
        const agentData = data.data;
        
        setAgents(prev => ({
          ...prev,
          [agentName]: {
            ...prev[agentName],
            status: data.type === 'agent_started' ? 'running' : 
                   data.type === 'agent_completed' ? 'completed' :
                   agentData.status || prev[agentName]?.status || 'idle',
            quality_score: agentData.quality_score || prev[agentName]?.quality_score,
            reasoning: agentData.reasoning || prev[agentName]?.reasoning,
            collaborating_with: agentData.collaborating_with || prev[agentName]?.collaborating_with,
            last_output: agentData.output || agentData.result || prev[agentName]?.last_output,
          },
        }));
      }
    };

    const cleanup = apiClient.connectWebSocket(handleWebSocketMessage);
    
    // Initial fetch
    fetchAgents();

    return () => {
      cleanup();
    };
  }, [fetchAgents]);

  return {
    agents,
    loading,
    error,
    wsMessages,
    fetchAgents,
    executeAgent,
    runWorkflow,
  };
};

export default useAgents;

