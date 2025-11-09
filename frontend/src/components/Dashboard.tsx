/**
 * Dashboard - Main dashboard layout with agents and activity
 */
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Play, Layers, History, Network, TrendingUp, Rocket, Target } from 'lucide-react';
import { useAgents } from '@/hooks/useAgents';
import apiClient from '../utils/apiClient';
import AgentPanel from './AgentPanel';
import TaskCard from './TaskCard';
import ChatInterface from './ChatInterface';
import BudgetMeter from './BudgetMeter';
import WorkflowTemplates from './WorkflowTemplates';
import WorkflowVisualization from './WorkflowVisualization';
import BeforeAfter from './BeforeAfter';
import AgentChatModal from './AgentChatModal';
import JiraIntegration from './JiraIntegration';
import IntegrationStatus from './IntegrationStatus';
import PRDSelectionModal from './PRDSelectionModal';
import WorkflowTemplateModal from './WorkflowTemplateModal';
import { FileText, X, CheckCircle, AlertTriangle, Sparkles } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { agents, wsMessages, runWorkflow } = useAgents();
  const [activeTab, setActiveTab] = useState<'agents' | 'visualization' | 'impact' | 'history' | 'templates'>('agents');
  const [demoScenarios, setDemoScenarios] = useState<any[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<{key: string, name: string, description: string} | null>(null);
  const [showJiraIntegration, setShowJiraIntegration] = useState(false);
  const [showPRDSelection, setShowPRDSelection] = useState(false);
  const [selectedDemo, setSelectedDemo] = useState<any>(null);
  const [demoResults, setDemoResults] = useState<any>(null);
  const [loadingDemo, setLoadingDemo] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState<any>(null);
  const [showTemplateModal, setShowTemplateModal] = useState(false);

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
  }, []);


  const handleRunDemo = async (scenario: any) => {
    setSelectedDemo(scenario);
    setLoadingDemo(true);
    setDemoResults(null);
    
    try {
      console.log(`🎬 Running demo: ${scenario.name}`);
      const response = await apiClient.runDemoScenario(scenario.key);
      console.log('✅ Demo response:', response);
      
      if (response.success && response.result) {
        // Transform steps array into outputs object for easier rendering
        const transformedResult = {
          ...response.result,
          outputs: response.result.steps?.reduce((acc: any, step: any) => {
            acc[step.agent.replace('Agent', '').toLowerCase()] = {
              status: step.status,
              data: step.result
            };
            return acc;
          }, {}) || {}
        };
        console.log('✅ Transformed result:', transformedResult);
        setDemoResults(transformedResult);
      } else {
        alert('Demo failed to run. Check console for details.');
      }
    } catch (error) {
      console.error('❌ Error running demo:', error);
      alert('Demo failed to run. Please check the console.');
    } finally {
      setLoadingDemo(false);
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
    <div className="min-h-screen bg-dark p-6">
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-2 hover:opacity-80 transition-opacity mb-2"
        >
          <Sparkles className="w-8 h-8 text-white" />
          <h1 className="text-4xl font-display font-bold gradient-text">
            ProdPlex
          </h1>
        </button>
        <p className="text-silver/70">Your AI Co-Pilot for Product Management</p>
      </div>

      {/* Budget Status & System Status */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <BudgetMeter />
        <div className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs text-silver/70 mb-1">System Status</p>
              <h4 className="text-sm font-semibold text-silver">All Systems Operational</h4>
            </div>
            <div className="flex flex-col items-end gap-1">
              <span className="text-xs text-silver/70">9 Agents</span>
              <span className="text-xs text-white">Active</span>
            </div>
          </div>
          <div className="mt-3 pt-3 border-t border-dark-border">
            <p className="text-xs text-silver/70">
              ✨ Adaptive Workflows • Risk Assessment • Smart Prioritization • Agent Collaboration
            </p>
          </div>
        </div>
        <IntegrationStatus />
      </div>

      {/* Quick Actions */}
      <div className="mb-8 card">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Rocket className="w-5 h-5 text-white" />
          Product Management Tools
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            onClick={() => setShowPRDSelection(true)}
            className="bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 hover:border-purple-400/50 rounded-lg text-white text-left h-auto py-4 px-4 flex items-start gap-3 transition-all"
          >
            <FileText className="w-6 h-6 mt-1 flex-shrink-0 text-purple-400" />
            <div>
              <div className="font-semibold text-base mb-1">Generate PRD</div>
              <div className="text-xs text-silver/70 font-normal">
                Create detailed or quick Product Requirements Documents using our 9-agent AI system
              </div>
            </div>
          </button>
          <button
            onClick={() => setShowJiraIntegration(true)}
            className="bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/30 hover:border-blue-400/50 rounded-lg text-white text-left h-auto py-4 px-4 flex items-start gap-3 transition-all"
          >
            <Target className="w-6 h-6 mt-1 flex-shrink-0 text-blue-400" />
            <div>
              <div className="font-semibold text-base mb-1">Jira Integration</div>
              <div className="text-xs text-silver/70 font-normal">
                Create user stories, manage sprints, and export to Jira with PNC templates
              </div>
            </div>
          </button>
        </div>
      </div>

      {/* Demo Scenarios */}
      {demoScenarios.length > 0 && (
        <div className="mb-8 card">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h2 className="text-lg font-semibold mb-1 flex items-center gap-2">
                <Play className="w-5 h-5 text-purple-400" />
                Live Demo Scenarios
              </h2>
              <p className="text-xs text-silver/70">
                See real-world examples of how our 9-agent AI system handles complex product management scenarios
              </p>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {demoScenarios.map((scenario) => (
              <button
                key={scenario.key}
                onClick={() => handleRunDemo(scenario)}
                className="p-5 bg-gradient-to-br from-purple-500/10 to-blue-500/10 hover:from-purple-500/20 hover:to-blue-500/20 rounded-lg border border-purple-500/30 hover:border-purple-400 transition-all text-left group"
              >
                <div className="font-semibold text-white mb-2 text-base group-hover:text-purple-300 transition-colors">
                  {scenario.name}
                </div>
                <div className="text-xs text-silver/80 mb-4 leading-relaxed">
                  {scenario.description}
                </div>
                <div className="flex items-center gap-2 text-xs font-medium text-purple-400 group-hover:text-purple-300">
                  <Play className="w-4 h-4" />
                  <span>Run Demo</span>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="mb-6">
        <div className="flex gap-2 border-b border-dark-border">
          {[
            { id: 'agents', label: 'Agents', icon: Layers },
            { id: 'visualization', label: 'Workflow', icon: Network },
            { id: 'impact', label: 'Impact', icon: TrendingUp },
            { id: 'templates', label: 'Templates', icon: Rocket },
            { id: 'history', label: 'History', icon: History },
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`px-6 py-3 font-medium transition-colors relative ${
                  activeTab === tab.id
                    ? 'text-white'
                    : 'text-silver/70 hover:text-silver'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </div>
                {activeTab === tab.id && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-white"
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
              <div
                key={key}
                onClick={() => setSelectedAgent({
                  key: key,
                  name: agent.name,
                  description: agent.goal || `Specialized agent for ${key}`
                })}
                className="cursor-pointer"
              >
                <AgentPanel agent={agent} agentKey={key} />
              </div>
            ))}
          </div>
        )}

        {activeTab === 'templates' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <WorkflowTemplates
                onSelectTemplate={(templateName) => {
                  // Map template name to workflow type for interactive modal
                  const templateMap: Record<string, string> = {
                    'new_feature_launch': 'full_feature_planning',
                    'competitive_response': 'research_and_strategy',
                    'compliance_audit': 'compliance_check',
                    'sprint_planning': 'dev_planning',
                    'market_research': 'research_and_strategy',
                    'adaptive': 'full_feature_planning',
                  };
                  
                  const workflowType = templateMap[templateName] || 'full_feature_planning';
                  setSelectedTemplate({ name: workflowType, displayName: templateName });
                  setShowTemplateModal(true);
                }}
              />
            </div>
            <div className="space-y-4">
              <div className="card p-4">
                <h4 className="text-sm font-semibold text-silver mb-2">How Templates Work</h4>
                <p className="text-xs text-silver/70 leading-relaxed">
                  Templates are pre-configured workflows optimized for specific PM tasks. 
                  Select a template to automatically configure the best agent sequence.
                </p>
              </div>
              <div className="card p-4">
                <h4 className="text-sm font-semibold text-silver mb-2">Adaptive Workflow</h4>
                <p className="text-xs text-silver/70 leading-relaxed">
                  The adaptive workflow uses AI to dynamically select agents based on your task. 
                  It learns from similar past projects to optimize execution.
                </p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'visualization' && (
          <div className="space-y-4">
            <WorkflowVisualization
              agents={Object.entries(agents).map(([key, agent]) => {
                // Dynamically calculate relevance based on agent activity
                const defaultRelevance: Record<string, number> = {
                  'Strategy': 0.95,
                  'Research': 0.90,
                  'Risk': 0.75,
                  'Development': 0.88,
                  'Prioritization': 0.82,
                  'Prototype': 0.78,
                  'GTM': 0.80,
                  'Automation': 0.70,
                  'Regulation': 0.72,
                };
                
                // Use actual quality score if available, otherwise use relevance
                const relevanceScore = defaultRelevance[agent.name] || 0.75;
                const actualScore = (agent as any).quality_score || relevanceScore;
                
                return {
                  name: agent.name,
                  status: agent.status === 'running' ? 'working' : 
                         agent.status === 'completed' ? 'done' : 'idle',
                  quality_score: actualScore,
                };
              })}
              contextFlow={[]}
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

        {activeTab === 'history' && (
          <div className="space-y-4">
            {wsMessages.length > 0 ? (
              <div className="card p-6">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <History className="w-5 h-5" />
                  Agent Interaction History
                </h3>
                <div className="space-y-3">
                  {wsMessages.slice().reverse().filter(msg => msg.type !== 'connected').map((msg, idx) => (
                    <div
                      key={idx}
                      className="bg-dark-lighter border border-dark-border rounded-lg p-4"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full bg-purple-400"></div>
                          <span className="text-sm font-medium text-white">
                            {msg.data?.agent || 'System'}
                          </span>
                        </div>
                        <span className="text-xs text-silver/50">
                          {new Date(msg.data?.timestamp || Date.now()).toLocaleTimeString()}
                        </span>
                      </div>
                      <p className="text-sm text-silver/80 line-clamp-2">
                        {msg.data?.query || msg.data?.message || 'Agent interaction'}
                      </p>
                      {msg.data?.status && (
                        <div className="mt-2 flex items-center gap-2">
                          <span className={`text-xs px-2 py-0.5 rounded ${
                            msg.data.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                            msg.data.status === 'failed' ? 'bg-red-500/20 text-red-400' :
                            'bg-yellow-500/20 text-yellow-400'
                          }`}>
                            {msg.data.status}
                          </span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="card text-center py-12">
                <History className="w-12 h-12 text-silver/70 mx-auto mb-4" />
                <p className="text-silver/70">No history yet. Start chatting with agents to see your interaction history!</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Agent Chat Modal */}
      {selectedAgent && (
        <AgentChatModal
          isOpen={!!selectedAgent}
          onClose={() => setSelectedAgent(null)}
          agentName={selectedAgent.name}
          agentDescription={selectedAgent.description}
          agentKey={selectedAgent.key}
        />
      )}
      
      {/* Jira Integration Modal */}
      <JiraIntegration
        isOpen={showJiraIntegration}
        onClose={() => setShowJiraIntegration(false)}
      />

      {/* PRD Selection Modal */}
      <PRDSelectionModal
        isOpen={showPRDSelection}
        onClose={() => setShowPRDSelection(false)}
      />

      {/* Workflow Template Modal */}
      <WorkflowTemplateModal
        isOpen={showTemplateModal}
        onClose={() => {
          setShowTemplateModal(false);
          setSelectedTemplate(null);
        }}
        template={selectedTemplate}
      />

      {/* Demo Results Modal */}
      {selectedDemo && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4"
          onClick={() => {
            setSelectedDemo(null);
            setDemoResults(null);
          }}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="bg-dark-lighter border border-dark-border rounded-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="p-6 border-b border-dark-border flex items-start justify-between">
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">{selectedDemo.name}</h2>
                <p className="text-sm text-silver/70">{selectedDemo.description}</p>
              </div>
              <button
                onClick={() => {
                  setSelectedDemo(null);
                  setDemoResults(null);
                }}
                className="text-silver/70 hover:text-white transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-6">
              {loadingDemo ? (
                <div className="text-center py-12">
                  <div className="w-16 h-16 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin mx-auto mb-4"></div>
                  <p className="text-silver/70 text-lg mb-2">Running demo scenario...</p>
                  <p className="text-xs text-silver/50">Our 9-agent AI system is processing this scenario</p>
                </div>
              ) : demoResults ? (
                <div className="space-y-6">
                  {/* Success Message */}
                  <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4 flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
                    <div>
                      <h3 className="font-semibold text-green-400 mb-1">Demo Completed Successfully</h3>
                      <p className="text-sm text-silver/70">
                        The multi-agent system has processed this scenario and generated comprehensive outputs.
                      </p>
                    </div>
                  </div>

                  {/* Agent Outputs */}
                  {demoResults.outputs && Object.keys(demoResults.outputs).length > 0 ? (
                    <div>
                      <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                        <Network className="w-5 h-5 text-purple-400" />
                        Agent Outputs
                      </h3>
                      <div className="space-y-4">
                        {Object.entries(demoResults.outputs).map(([agentName, output]: [string, any]) => (
                          <div
                            key={agentName}
                            className="bg-dark-lighter border border-dark-border rounded-lg p-4"
                          >
                            <div className="flex items-center gap-3 mb-3">
                              <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center">
                                <span className="text-purple-400 text-sm font-bold">
                                  {agentName[0].toUpperCase()}
                                </span>
                              </div>
                              <div>
                                <h4 className="font-semibold text-white capitalize">{agentName} Agent</h4>
                                <p className="text-xs text-silver/50">Status: {output.status || 'completed'}</p>
                              </div>
                            </div>
                            <div className="bg-dark rounded p-3 max-h-64 overflow-y-auto">
                              <div className="text-sm text-silver/90 leading-relaxed">
                                {(() => {
                                  // Extract the most relevant content based on agent type
                                  const data = output.data;
                                  
                                  // Try to find natural language content
                                  if (data.refined_concept) {
                                    return data.refined_concept.replace(/<think>[\s\S]*?<\/think>/g, '').trim();
                                  } else if (data.analysis) {
                                    return data.analysis.replace(/<think>[\s\S]*?<\/think>/g, '').trim();
                                  } else if (data.report) {
                                    return data.report.replace(/<think>[\s\S]*?<\/think>/g, '').trim();
                                  } else if (data.summary) {
                                    return data.summary;
                                  } else if (data.recommendations) {
                                    return Array.isArray(data.recommendations) 
                                      ? data.recommendations.join('\n\n')
                                      : data.recommendations;
                                  } else if (typeof data === 'string') {
                                    return data.replace(/<think>[\s\S]*?<\/think>/g, '').trim();
                                  }
                                  
                                  // Fallback: Extract key-value pairs in readable format
                                  return Object.entries(data)
                                    .filter(([key]) => !key.includes('_id') && key !== 'timestamp')
                                    .map(([key, value]) => {
                                      const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                                      if (typeof value === 'string' && value.length < 200) {
                                        return `${label}: ${value}`;
                                      } else if (Array.isArray(value) && value.length <= 5) {
                                        return `${label}:\n  • ${value.join('\n  • ')}`;
                                      }
                                      return null;
                                    })
                                    .filter(Boolean)
                                    .join('\n\n') || 'Agent completed successfully. See console for detailed output.';
                                })()}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ) : (
                    <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4 flex items-start gap-3">
                      <AlertTriangle className="w-5 h-5 text-yellow-400 mt-0.5 flex-shrink-0" />
                      <div>
                        <h3 className="font-semibold text-yellow-400 mb-1">No Agent Outputs</h3>
                        <p className="text-sm text-silver/70">
                          The demo completed but no agent outputs were generated. Check console for details.
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Workflow Metadata */}
                  {demoResults.workflow && (
                    <div className="border-t border-dark-border pt-6">
                      <h3 className="text-sm font-semibold text-white/50 mb-3">Workflow Metadata</h3>
                      <div className="grid grid-cols-2 gap-3 text-xs">
                        <div>
                          <span className="text-silver/50">Workflow Type:</span>
                          <span className="ml-2 text-white">{demoResults.workflow}</span>
                        </div>
                        {demoResults.timestamp && (
                          <div>
                            <span className="text-silver/50">Completed:</span>
                            <span className="ml-2 text-white">{new Date(demoResults.timestamp).toLocaleString()}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-12">
                  <Play className="w-16 h-16 text-purple-400 mx-auto mb-4" />
                  <p className="text-silver/70">Click "Run Demo" to see how our agents handle this scenario</p>
                </div>
              )}
            </div>
          </motion.div>
        </motion.div>
      )}
    </div>
  );
};

export default Dashboard;

