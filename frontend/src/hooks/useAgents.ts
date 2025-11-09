/**
 * Custom React hook for managing agents state
 */
import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '@/utils/apiClient';

export interface AgentStatus {
  name: string;
  status: string;
  goal: string;
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
    let isMounted = true;
    
    const handleWebSocketMessage = (data: WebSocketMessage) => {
      if (!isMounted) return;
      
      setWsMessages(prev => [...prev.slice(-50), data]); // Keep last 50 messages
      
      // Update agent status based on WebSocket messages
      if (data.type === 'agent_started' || data.type === 'agent_completed') {
        const agentName = data.data.agent;
        setAgents(prev => ({
          ...prev,
          [agentName]: {
            ...prev[agentName],
            status: data.type === 'agent_started' ? 'running' : 'completed',
          },
        }));
      }
    };

    // Only connect WebSocket once when component mounts
    const cleanup = apiClient.connectWebSocket(handleWebSocketMessage);
    
    // Initial fetch
    fetchAgents();

    return () => {
      isMounted = false;
      cleanup();
    };
  }, []); // Empty dependency array - only run once on mount

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

