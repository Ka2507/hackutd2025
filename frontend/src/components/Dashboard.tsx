/**
 * Dashboard - Main dashboard layout with agents and activity
 */
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Play, Layers, History, Network, TrendingUp, Rocket } from 'lucide-react';
import { useAgents } from '@/hooks/useAgents';
import AgentPanel from './AgentPanel';
import TaskCard from './TaskCard';
import ChatInterface from './ChatInterface';
import BudgetMeter from './BudgetMeter';
import WorkflowTemplates from './WorkflowTemplates';
import WorkflowVisualization from './WorkflowVisualization';
import BeforeAfter from './BeforeAfter';
import RefinementModal from './RefinementModal';
import apiClient from '@/utils/apiClient';

export const Dashboard: React.FC = () => {
  const { agents, wsMessages, runWorkflow } = useAgents();
  const [activeTab, setActiveTab] = useState<'agents' | 'visualization' | 'chat' | 'activity' | 'templates' | 'impact'>('agents');
  const [selectedWorkflow, setSelectedWorkflow] = useState('');
  const [demoScenarios, setDemoScenarios] = useState<any[]>([]);
  const [refinementModal, setRefinementModal] = useState<{open: boolean, agentName: string, output: any}>({open: false, agentName: '', output: null});
  const [workflowState, setWorkflowState] = useState<any>(null);

  const workflows = [
    { value: 'adaptive', label: '🤖 Adaptive Workflow (AI-Powered)', description: 'Intelligently selects agents based on task' },
    { value: 'full_feature_planning', label: 'Full Feature Planning', description: 'Complete workflow with risk & prioritization' },
    { value: 'research_and_strategy', label: 'Research & Strategy', description: 'Market research and strategic analysis' },
    { value: 'dev_planning', label: 'Dev Planning', description: 'User stories and prototyping' },
    { value: 'launch_planning', label: 'Launch Planning', description: 'Go-to-market and automation' },
    { value: 'compliance_check', label: 'Compliance Check', description: 'Regulatory compliance review' },
  ];

  useEffect(() => {
    // Load demo scenarios
    apiClient.listDemoScenarios().then(res => {
      if (res.scenarios) {
        setDemoScenarios(Object.entries(res.scenarios).map(([key, value]: [string, any]) => ({
          key,
          ...value
        })));
      }
    }).catch(console.error);

    // Parse workflow state from WebSocket messages
    const latestWorkflow = wsMessages
      .filter(msg => msg.type === 'agent_status' || msg.type === 'task_completed')
      .slice(-1)[0];
    
    if (latestWorkflow) {
      setWorkflowState(latestWorkflow.data);
    }
  }, [wsMessages]);

  const handleRunDemo = async (scenarioKey: string) => {
    try {
      await apiClient.runDemoScenario(scenarioKey);
    } catch (error) {
      console.error('Error running demo:', error);
    }
  };

  const handleRunWorkflow = async () => {
    if (!selectedWorkflow) return;
    
    try {
      await runWorkflow(selectedWorkflow, {
        feature: 'AI Agent Dashboard',
        market: 'B2B SaaS',
      });
    } catch (error) {
      console.error('Error running workflow:', error);
    }
  };

  const handleSendMessage = async (message: string) => {
    // For demo, we'll simulate running a workflow based on the message
    const lowerMessage = message.toLowerCase();
    let workflowType = 'research_and_strategy';
    
    if (lowerMessage.includes('develop') || lowerMessage.includes('build')) {
      workflowType = 'dev_planning';
    } else if (lowerMessage.includes('launch') || lowerMessage.includes('market')) {
      workflowType = 'launch_planning';
    } else if (lowerMessage.includes('compliance') || lowerMessage.includes('regulation')) {
      workflowType = 'compliance_check';
    }
    
    await runWorkflow(workflowType, {
      query: message,
      feature: message,
    });
  };

  // Convert WebSocket messages to chat messages
  const chatMessages = wsMessages
    .filter(msg => msg.type !== 'connected')
    .map((msg, idx) => ({
      id: `msg-${idx}`,
      role: 'assistant' as const,
      content: JSON.stringify(msg.data, null, 2),
      timestamp: new Date(msg.data.timestamp || Date.now()),
    }));

  return (
    <div className="min-h-screen bg-charcoal p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-display font-bold gradient-text mb-2">
          ProdigyPM
        </h1>
        <p className="text-gray-400">Your AI Co-Pilot for Product Management</p>
      </div>

      {/* Budget Status & System Status */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <BudgetMeter />
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs text-gray-400 mb-1">System Status</p>
              <h4 className="text-sm font-semibold text-white">All Systems Operational</h4>
            </div>
            <div className="flex flex-col items-end gap-1">
              <span className="text-xs text-gray-400">9 Agents</span>
              <span className="text-xs text-green-400">Active</span>
            </div>
          </div>
          <div className="mt-3 pt-3 border-t border-dark-border">
            <p className="text-xs text-gray-400">
              ✨ Adaptive Workflows • Risk Assessment • Smart Prioritization • Agent Collaboration
            </p>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mb-8 space-y-4">
        <div className="card">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Play className="w-5 h-5 text-neon-cyan" />
            Quick Actions
          </h2>
          <div className="flex gap-4">
            <div className="flex-1">
              <select
                value={selectedWorkflow}
                onChange={(e) => setSelectedWorkflow(e.target.value)}
                className="w-full input"
              >
                <option value="">Select Workflow...</option>
                {workflows.map((wf) => (
                  <option key={wf.value} value={wf.value}>
                    {wf.label}
                  </option>
                ))}
              </select>
              {selectedWorkflow && (
                <p className="text-xs text-gray-400 mt-1">
                  {workflows.find(w => w.value === selectedWorkflow)?.description}
                </p>
              )}
            </div>
            <button
              onClick={handleRunWorkflow}
              disabled={!selectedWorkflow}
              className="btn btn-primary disabled:opacity-50"
            >
              <Play className="w-5 h-5 mr-2" />
              Run Workflow
            </button>
          </div>
        </div>

        {/* Demo Scenarios */}
        {demoScenarios.length > 0 && (
          <div className="card">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Rocket className="w-5 h-5 text-neon-cyan" />
              Demo Scenarios
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {demoScenarios.map((scenario) => (
                <button
                  key={scenario.key}
                  onClick={() => handleRunDemo(scenario.key)}
                  className="p-3 bg-dark-lighter hover:bg-dark-border rounded border border-dark-border transition-colors text-left"
                >
                  <div className="font-medium text-white mb-1">{scenario.name}</div>
                  <div className="text-xs text-gray-400">{scenario.description}</div>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="mb-6">
        <div className="flex gap-2 border-b border-gray-300">
          {[
            { id: 'agents', label: 'Agents', icon: Layers },
            { id: 'visualization', label: 'Workflow', icon: Network },
            { id: 'impact', label: 'Impact', icon: TrendingUp },
            { id: 'templates', label: 'Templates', icon: Layers },
            { id: 'chat', label: 'Chat', icon: History },
            { id: 'activity', label: 'Activity', icon: History },
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`px-6 py-3 font-medium transition-colors relative ${
                  activeTab === tab.id
                    ? 'text-neon-cyan'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </div>
                {activeTab === tab.id && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-neon-cyan"
                  />
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Content */}
      <div>
        {activeTab === 'agents' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(agents).map(([key, agent]) => (
              <AgentPanel 
                key={key} 
                agent={agent} 
                agentKey={key}
                onClick={() => {
                  // Show refinement modal if agent has output
                  if (agent.last_output) {
                    setRefinementModal({
                      open: true,
                      agentName: agent.name,
                      output: agent.last_output
                    });
                  }
                }}
              />
            ))}
          </div>
        )}

        {activeTab === 'visualization' && (
          <div className="space-y-4">
            <WorkflowVisualization
              agents={Object.entries(agents).map(([key, agent]) => ({
                name: agent.name,
                status: agent.status === 'running' ? 'working' : 
                       agent.status === 'completed' ? 'done' : 'idle',
                quality_score: agent.quality_score,
                reasoning: agent.reasoning,
                collaborating_with: agent.collaborating_with,
              }))}
              contextFlow={workflowState?.context_flow || []}
              onNodeClick={(agentName) => {
                const agent = Object.values(agents).find(a => a.name === agentName);
                if (agent?.last_output) {
                  setRefinementModal({
                    open: true,
                    agentName: agent.name,
                    output: agent.last_output
                  });
                }
              }}
            />
          </div>
        )}

        {activeTab === 'impact' && (
          <div className="space-y-6">
            <BeforeAfter
              timeSaved={8.5}
              qualityImprovement={35}
              itemsGenerated={23}
              traditionalCount={8}
              automatedCount={23}
            />
          </div>
        )}

        {activeTab === 'templates' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <WorkflowTemplates
                onSelectTemplate={(templateName) => {
                  // Map template name to workflow type
                  const templateMap: Record<string, string> = {
                    'new_feature_launch': 'full_feature_planning',
                    'competitive_response': 'research_and_strategy',
                    'compliance_audit': 'compliance_check',
                    'sprint_planning': 'dev_planning',
                    'market_research': 'research_and_strategy',
                    'adaptive': 'adaptive',
                  };
                  const workflowType = templateMap[templateName] || templateName;
                  setSelectedWorkflow(workflowType);
                  setActiveTab('agents');
                }}
              />
            </div>
            <div className="space-y-4">
              <div className="card p-4">
                <h4 className="text-sm font-semibold text-white mb-2">How Templates Work</h4>
                <p className="text-xs text-gray-400 leading-relaxed">
                  Templates are pre-configured workflows optimized for specific PM tasks. 
                  Select a template to automatically configure the best agent sequence.
                </p>
              </div>
              <div className="card p-4">
                <h4 className="text-sm font-semibold text-white mb-2">Adaptive Workflow</h4>
                <p className="text-xs text-gray-400 leading-relaxed">
                  The adaptive workflow uses AI to dynamically select agents based on your task. 
                  It learns from similar past projects to optimize execution.
                </p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'chat' && (
          <div className="card h-[600px]">
            <ChatInterface
              onSendMessage={handleSendMessage}
              messages={chatMessages}
            />
          </div>
        )}

        {activeTab === 'activity' && (
          <div className="space-y-4">
            {wsMessages.length > 0 ? (
              wsMessages.slice().reverse().map((msg, idx) => {
                // Check if this is a workflow completion message with full result
                const isWorkflowComplete = msg.type === 'task_completed' && msg.data?.result;
                const workflowResult = isWorkflowComplete ? msg.data.result : null;
                
                return (
                  <TaskCard
                    key={idx}
                    task={{
                      ...msg.data,
                      workflow_type: msg.data?.workflow_type || workflowResult?.workflow,
                      status: msg.type.includes('completed') ? 'completed' :
                             msg.type.includes('failed') ? 'failed' : 'running',
                      result: workflowResult || msg.data,
                    }}
                    index={idx}
                  />
                );
              })
            ) : (
              <div className="card text-center py-12">
                <History className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-400">No activity yet. Run a workflow to get started!</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Refinement Modal */}
      <RefinementModal
        isOpen={refinementModal.open}
        onClose={() => setRefinementModal({open: false, agentName: '', output: null})}
        agentName={refinementModal.agentName}
        originalOutput={refinementModal.output}
        onRefined={(refined) => {
          console.log('Refined output:', refined);
          // Could update agent state here
        }}
      />
    </div>
  );
};

export default Dashboard;

