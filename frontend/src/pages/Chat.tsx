/**
 * Chat Page - Intelligent chat interface for task-based agent execution
 * Users can describe what they want to do, and the system will automatically
 * select the appropriate workflow and agents
 */
import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Send, Bot, User, Sparkles, ArrowLeft, Loader2, CheckCircle, XCircle } from 'lucide-react';
import { useAgents } from '@/hooks/useAgents';
import BudgetMeter from '@/components/BudgetMeter';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system' | 'agent';
  content: string;
  timestamp: Date;
  workflowType?: string;
  agents?: string[];
  status?: 'running' | 'completed' | 'failed';
}

interface TaskAnalysis {
  workflowType: string;
  confidence: number;
  reasoning: string;
  agents: string[];
  inputData: Record<string, any>;
}

/**
 * Intelligent task parser - determines workflow type from user input
 */
const analyzeTask = (userMessage: string): TaskAnalysis => {
  const message = userMessage.toLowerCase();
  
  // Product Strategy & Planning
  if (
    message.includes('product strategy') ||
    message.includes('strategic plan') ||
    message.includes('go-to-market') ||
    message.includes('market strategy') ||
    message.includes('business strategy') ||
    message.includes('launch strategy')
  ) {
    return {
      workflowType: 'launch_planning',
      confidence: 0.9,
      reasoning: 'Detected product strategy and launch planning task',
      agents: ['strategy', 'research', 'gtm', 'automation'],
      inputData: {
        product: extractProductName(userMessage),
        target_audience: extractTargetAudience(userMessage),
        query: userMessage,
      },
    };
  }
  
  // Full Feature Planning
  if (
    message.includes('create') && (message.includes('feature') || message.includes('product')) ||
    message.includes('build') && (message.includes('feature') || message.includes('product')) ||
    message.includes('design') && message.includes('feature') ||
    message.includes('plan') && (message.includes('feature') || message.includes('product')) ||
    message.includes('new feature') ||
    message.includes('entire thing') ||
    message.includes('complete') && (message.includes('feature') || message.includes('product'))
  ) {
    return {
      workflowType: 'full_feature_planning',
      confidence: 0.95,
      reasoning: 'Detected full feature/product creation task',
      agents: ['strategy', 'research', 'prioritization', 'risk', 'regulation', 'dev', 'prototype', 'gtm', 'automation'],
      inputData: {
        feature: extractFeatureName(userMessage),
        market: extractMarket(userMessage),
        target_audience: extractTargetAudience(userMessage),
        query: userMessage,
      },
    };
  }
  
  // Research & Strategy
  if (
    message.includes('research') ||
    message.includes('analyze') ||
    message.includes('investigate') ||
    message.includes('study') ||
    message.includes('competitor') ||
    message.includes('market research') ||
    message.includes('user research')
  ) {
    return {
      workflowType: 'research_and_strategy',
      confidence: 0.85,
      reasoning: 'Detected research and analysis task',
      agents: ['strategy', 'research'],
      inputData: {
        query: userMessage,
        sources: ['reddit', 'twitter'],
      },
    };
  }
  
  // Development Planning
  if (
    message.includes('develop') ||
    message.includes('build') ||
    message.includes('code') ||
    message.includes('user story') ||
    message.includes('user stories') ||
    message.includes('sprint') ||
    message.includes('backlog') ||
    message.includes('technical') ||
    message.includes('implementation')
  ) {
    return {
      workflowType: 'dev_planning',
      confidence: 0.9,
      reasoning: 'Detected development and implementation task',
      agents: ['dev', 'prototype'],
      inputData: {
        feature: extractFeatureName(userMessage),
        requirements: extractRequirements(userMessage),
        query: userMessage,
      },
    };
  }
  
  // Compliance & Regulation
  if (
    message.includes('compliance') ||
    message.includes('regulation') ||
    message.includes('legal') ||
    message.includes('audit') ||
    message.includes('gdpr') ||
    message.includes('soc2') ||
    message.includes('pci') ||
    message.includes('regulatory')
  ) {
    return {
      workflowType: 'compliance_check',
      confidence: 0.95,
      reasoning: 'Detected compliance and regulatory task',
      agents: ['regulation', 'risk'],
      inputData: {
        feature: extractFeatureName(userMessage),
        jurisdiction: extractJurisdiction(userMessage),
        query: userMessage,
      },
    };
  }
  
  // Prioritization
  if (
    message.includes('prioritize') ||
    message.includes('priority') ||
    message.includes('roadmap') ||
    message.includes('which feature') ||
    message.includes('what should') ||
    message.includes('should we build')
  ) {
    return {
      workflowType: 'adaptive',
      confidence: 0.8,
      reasoning: 'Detected prioritization task - using adaptive workflow',
      agents: ['prioritization', 'strategy', 'research'],
      inputData: {
        query: userMessage,
        task_type: 'prioritization',
      },
    };
  }
  
  // Default: Adaptive workflow for unknown tasks
  return {
    workflowType: 'adaptive',
    confidence: 0.7,
    reasoning: 'Using adaptive workflow to intelligently select agents',
    agents: [],
    inputData: {
      query: userMessage,
      task_description: userMessage,
    },
  };
};

// Helper functions to extract information from user message
const extractProductName = (message: string): string => {
  const patterns = [
    /(?:product|app|tool|platform|system)\s+(?:called|named|for)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)/i,
    /(?:create|build|design)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)/i,
  ];
  for (const pattern of patterns) {
    const match = message.match(pattern);
    if (match) return match[1];
  }
  return 'New Product';
};

const extractFeatureName = (message: string): string => {
  const patterns = [
    /(?:feature|functionality|module)\s+(?:called|named|for)\s+([a-z]+(?:\s+[a-z]+)*)/i,
    /(?:create|build|design)\s+(?:a|an)?\s+([a-z]+(?:\s+[a-z]+)*)\s+(?:feature|functionality)/i,
  ];
  for (const pattern of patterns) {
    const match = message.match(pattern);
    if (match) return match[1];
  }
  return 'New Feature';
};

const extractMarket = (message: string): string => {
  if (message.includes('b2b') || message.includes('enterprise')) return 'B2B Enterprise';
  if (message.includes('b2c') || message.includes('consumer')) return 'B2C Consumer';
  if (message.includes('saas')) return 'B2B SaaS';
  if (message.includes('mobile')) return 'Mobile';
  return 'B2B SaaS';
};

const extractTargetAudience = (message: string): string => {
  if (message.includes('product manager')) return 'Product Managers';
  if (message.includes('developer') || message.includes('engineer')) return 'Developers';
  if (message.includes('designer')) return 'Designers';
  if (message.includes('business') || message.includes('executive')) return 'Business Executives';
  return 'Product Managers';
};

const extractRequirements = (message: string): string[] => {
  const requirements: string[] = [];
  const lines = message.split('\n');
  for (const line of lines) {
    if (line.match(/^[-*•]\s+/) || line.match(/^\d+\.\s+/)) {
      requirements.push(line.replace(/^[-*•]\s+/, '').replace(/^\d+\.\s+/, '').trim());
    }
  }
  return requirements.length > 0 ? requirements : ['User-friendly interface', 'Scalable architecture'];
};

const extractJurisdiction = (message: string): string => {
  if (message.includes('eu') || message.includes('europe')) return 'EU';
  if (message.includes('us') || message.includes('usa') || message.includes('united states')) return 'US';
  if (message.includes('uk')) return 'UK';
  return 'US';
};

export const Chat: React.FC = () => {
  const navigate = useNavigate();
  const { agents, wsMessages, runWorkflow } = useAgents();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: "👋 Hi! I'm your AI PM Co-Pilot. Tell me what you'd like to work on:\n\n• Create a new product or feature\n• Research competitors or market trends\n• Plan a product launch\n• Check compliance requirements\n• Prioritize features\n• Develop user stories\n\nJust describe your task and I'll coordinate the right agents to help!",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [activeAgents, setActiveAgents] = useState<Set<string>>(new Set());
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [workflowStatus, setWorkflowStatus] = useState<'idle' | 'running' | 'completed' | 'failed'>('idle');

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Listen to WebSocket messages for agent updates
  useEffect(() => {
    const latestMessage = wsMessages[wsMessages.length - 1];
    if (!latestMessage) return;

    const { type, data } = latestMessage;

    // Update active agents
    if (type === 'agent_started') {
      const agentName = data.agent;
      setActiveAgents(prev => new Set(prev).add(agentName));
      
      // Add agent status message
      setMessages(prev => [...prev, {
        id: `agent-${agentName}-${Date.now()}`,
        role: 'agent',
        content: `🤖 ${agentName} started working...`,
        timestamp: new Date(),
        agents: [agentName],
        status: 'running',
      }]);
    }

    if (type === 'agent_completed') {
      const agentName = data.agent;
      setActiveAgents(prev => {
        const newSet = new Set(prev);
        newSet.delete(agentName);
        return newSet;
      });

      // Add completion message
      setMessages(prev => [...prev, {
        id: `agent-${agentName}-completed-${Date.now()}`,
        role: 'agent',
        content: `✅ ${agentName} completed their task`,
        timestamp: new Date(),
        agents: [agentName],
        status: 'completed',
      }]);
    }

    if (type === 'task_completed') {
      setWorkflowStatus('completed');
      setActiveAgents(new Set());
      
      // Add completion message with results
      const result = data.result || {};
      setMessages(prev => [...prev, {
        id: `workflow-completed-${Date.now()}`,
        role: 'assistant',
        content: `🎉 Workflow completed!\n\n${formatWorkflowResults(result)}`,
        timestamp: new Date(),
        status: 'completed',
      }]);
    }

    if (type === 'task_failed') {
      setWorkflowStatus('failed');
      setActiveAgents(new Set());
      
      setMessages(prev => [...prev, {
        id: `workflow-failed-${Date.now()}`,
        role: 'assistant',
        content: `❌ Workflow failed: ${data.error || 'Unknown error'}`,
        timestamp: new Date(),
        status: 'failed',
      }]);
    }
  }, [wsMessages]);

  const formatWorkflowResults = (result: any): string => {
    if (!result || Object.keys(result).length === 0) {
      return 'Workflow completed successfully, but no detailed results were returned.';
    }
    
    const parts: string[] = [];
    
    // Workflow info
    if (result.workflow) {
      parts.push(`**Workflow Type:** ${result.workflow.replace(/_/g, ' ').replace(/\b\w/g, (l: string) => l.toUpperCase())}`);
    }
    
    // Summary first (if available)
    if (result.summary) {
      if (typeof result.summary === 'object') {
        const summary = result.summary;
        
        // Show summary text if available
        if (summary.summary_text) {
          parts.push(`**${summary.summary_text}**`);
        }
        
        // Show agents used from summary
        if (summary.agents_used && summary.agents_used.length > 0) {
          parts.push(`**Agents Used:** ${summary.agents_used.join(', ')}`);
        }
        
        // Show key outputs from summary
        if (summary.key_outputs && Array.isArray(summary.key_outputs) && summary.key_outputs.length > 0) {
          parts.push(`\n**Agent Outputs:**`);
          summary.key_outputs.forEach((output: any, index: number) => {
            const agentName = output.agent || `Agent ${index + 1}`;
            const summaryText = output.summary || output.content || JSON.stringify(output.full_result || output, null, 2);
            parts.push(`\n${index + 1}. **${agentName}**:\n${summaryText.substring(0, 1500)}${summaryText.length > 1500 ? '\n... (truncated)' : ''}`);
          });
        }
      } else {
        parts.push(`\n**Summary:**\n${String(result.summary).substring(0, 1000)}${String(result.summary).length > 1000 ? '\n... (truncated)' : ''}`);
      }
    }
    
    // Agents used (if not in summary)
    if (!result.summary?.agents_used && result.agents_used && result.agents_used.length > 0) {
      parts.push(`**Agents Used:** ${result.agents_used.join(', ')}`);
    }
    
    // Steps/Results from agents (for full_feature_planning and other workflows)
    if (result.steps && Array.isArray(result.steps) && result.steps.length > 0) {
      // Only show steps if we don't have summary key_outputs
      if (!result.summary?.key_outputs || result.summary.key_outputs.length === 0) {
        parts.push(`\n**Agent Outputs:**`);
        result.steps.forEach((step: any, index: number) => {
          const agentName = step.agent || step.agent_name || `Agent ${index + 1}`;
          const stepResult = step.result || {};
          
          // Extract meaningful content from step result
          let content = '';
          if (typeof stepResult === 'object' && stepResult !== null) {
            // Try various keys that might contain the actual AI response
            content = stepResult.launch_plan || 
                     stepResult.marketing_strategy || 
                     stepResult.pricing_strategy ||
                     stepResult.messaging_framework ||
                     stepResult.strategic_analysis ||
                     stepResult.market_analysis ||
                     stepResult.research_synthesis ||
                     stepResult.output ||
                     stepResult.raw_response ||
                     (stepResult.result && typeof stepResult.result === 'string' ? stepResult.result : '') ||
                     JSON.stringify(stepResult, null, 2);
          } else {
            content = String(stepResult);
          }
          
          if (content) {
            parts.push(`\n${index + 1}. **${agentName}**:\n${content.substring(0, 1500)}${content.length > 1500 ? '\n... (truncated)' : ''}`);
          }
        });
      }
    }
    
    // Nodes (for adaptive workflow)
    if (result.nodes && Array.isArray(result.nodes) && result.nodes.length > 0) {
      parts.push(`\n**Agent Outputs:**`);
      result.nodes.forEach((node: any, index: number) => {
        const agentName = node.agent || node.agent_name || `Agent ${index + 1}`;
        const nodeResult = node.result || {};
        
        if (nodeResult) {
          let formattedResult = '';
          if (typeof nodeResult === 'object') {
            formattedResult = JSON.stringify(nodeResult, null, 2);
          } else {
            formattedResult = String(nodeResult);
          }
          parts.push(`\n${index + 1}. **${agentName}**:\n${formattedResult.substring(0, 1500)}${formattedResult.length > 1500 ? '\n... (truncated)' : ''}`);
        }
      });
    }
    
    // Adaptations (for adaptive workflow)
    if (result.adaptations && Array.isArray(result.adaptations) && result.adaptations.length > 0) {
      parts.push(`\n**Adaptations Made:**\n${result.adaptations.map((a: any, i: number) => `${i + 1}. ${JSON.stringify(a)}`).join('\n')}`);
    }
    
    // General results
    if (result.results && typeof result.results === 'object') {
      const resultsStr = JSON.stringify(result.results, null, 2);
      parts.push(`\n**Key Results:**\n${resultsStr.substring(0, 1000)}${resultsStr.length > 1000 ? '\n... (truncated)' : ''}`);
    }
    
    // If we have the full result object but no formatted output, show it
    if (parts.length <= 2 && result.workflow) {
      // Try to extract any meaningful data
      const steps = result.steps || [];
      if (steps.length > 0) {
        const firstStep = steps[0];
        const firstResult = firstStep?.result || {};
        if (firstResult && Object.keys(firstResult).length > 0) {
          const resultStr = JSON.stringify(firstResult, null, 2);
          parts.push(`\n**Workflow Results:**\n${resultStr.substring(0, 2000)}${resultStr.length > 2000 ? '\n... (truncated)' : ''}`);
        }
      }
    }
    
    return parts.join('\n\n') || 'Workflow completed successfully. Check the Activity tab for detailed results.';
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setIsLoading(true);
    setWorkflowStatus('running');

    // Add user message
    const userMsg: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: userMessage,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMsg]);

    try {
      // Analyze task and determine workflow
      const analysis = analyzeTask(userMessage);
      
      // Add analysis message
      const analysisMsg: Message = {
        id: `analysis-${Date.now()}`,
        role: 'assistant',
        content: `🔍 Analyzing your request...\n\n**Detected Task:** ${analysis.workflowType.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}\n**Confidence:** ${Math.round(analysis.confidence * 100)}%\n**Reasoning:** ${analysis.reasoning}\n\n🚀 Starting workflow with agents: ${analysis.agents.join(', ') || 'Adaptive selection'}...`,
        timestamp: new Date(),
        workflowType: analysis.workflowType,
        agents: analysis.agents,
        status: 'running',
      };
      setMessages(prev => [...prev, analysisMsg]);

      // Run the workflow
      await runWorkflow(analysis.workflowType, analysis.inputData, undefined, true);
      
    } catch (error: any) {
      console.error('Error running workflow:', error);
      setMessages(prev => [...prev, {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: `❌ Error: ${error.message || 'Failed to execute workflow'}`,
        timestamp: new Date(),
        status: 'failed',
      }]);
      setWorkflowStatus('failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-charcoal flex flex-col">
      {/* Header */}
      <div className="bg-dark-card border-b border-dark-border px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/')}
              className="p-2 hover:bg-dark-lighter rounded-lg transition-colors"
            >
              <ArrowLeft className="w-5 h-5 text-gray-400" />
            </button>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-nvidia-green/20 to-pnc-blue/20 border border-nvidia-green/30 rounded-xl flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-nvidia-green" />
              </div>
              <div>
                <h1 className="text-xl font-display font-bold text-white">AI PM Co-Pilot</h1>
                <p className="text-xs text-gray-400">Intelligent task-based agent orchestration</p>
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <BudgetMeter />
            <div className="text-right">
              <p className="text-xs text-gray-400">Active Agents</p>
              <p className="text-sm font-semibold text-white">
                {activeAgents.size > 0 ? `${activeAgents.size} working` : 'Idle'}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Chat Area */}
        <div className="flex-1 flex flex-col">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-6 py-6 space-y-4 scrollbar-hide">
            <AnimatePresence>
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className={`flex gap-3 ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  {message.role !== 'user' && (
                    <div className="flex-shrink-0">
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                        message.role === 'agent' 
                          ? 'bg-pnc-blue/20 border border-pnc-blue/30' 
                          : 'bg-neon-cyan/20 border border-neon-cyan'
                      }`}>
                        {message.role === 'agent' ? (
                          <Loader2 className="w-5 h-5 text-pnc-blue-light animate-spin" />
                        ) : message.status === 'completed' ? (
                          <CheckCircle className="w-5 h-5 text-green-400" />
                        ) : message.status === 'failed' ? (
                          <XCircle className="w-5 h-5 text-red-400" />
                        ) : (
                          <Bot className="w-5 h-5 text-neon-cyan" />
                        )}
                      </div>
                    </div>
                  )}
                  
                  <div
                    className={`max-w-[75%] rounded-2xl px-5 py-4 ${
                      message.role === 'user'
                        ? 'bg-gradient-to-r from-nvidia-green to-pnc-blue text-white'
                        : message.role === 'agent'
                        ? 'bg-pnc-blue/10 border border-pnc-blue/20 text-gray-200'
                        : 'bg-dark-card border border-dark-border text-gray-200'
                    }`}
                  >
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">
                      {message.content}
                    </p>
                    
                    {message.agents && message.agents.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-dark-border">
                        <p className="text-xs text-gray-400 mb-2">Agents:</p>
                        <div className="flex flex-wrap gap-2">
                          {message.agents.map((agent) => (
                            <span
                              key={agent}
                              className="text-xs px-2 py-1 bg-nvidia-green/20 text-nvidia-green rounded"
                            >
                              {agent}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    <span className={`text-xs mt-3 block ${
                      message.role === 'user' ? 'text-white/70' : 'text-gray-400'
                    }`}>
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                  
                  {message.role === 'user' && (
                    <div className="flex-shrink-0">
                      <div className="w-10 h-10 rounded-full bg-gray-300 border border-gray-400 flex items-center justify-center">
                        <User className="w-5 h-5 text-charcoal" />
                      </div>
                    </div>
                  )}
                </motion.div>
              ))}
            </AnimatePresence>
            
            {isLoading && workflowStatus === 'running' && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex gap-3"
              >
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 rounded-full bg-neon-cyan/20 border border-neon-cyan flex items-center justify-center">
                    <Loader2 className="w-5 h-5 text-neon-cyan animate-spin" />
                  </div>
                </div>
                <div className="bg-dark-card rounded-2xl px-5 py-4 border border-dark-border">
                  <div className="flex items-center gap-2">
                    <Loader2 className="w-4 h-4 text-neon-cyan animate-spin" />
                    <p className="text-sm text-gray-300">Agents are working on your task...</p>
                  </div>
                  {activeAgents.size > 0 && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      {Array.from(activeAgents).map((agent) => (
                        <span
                          key={agent}
                          className="text-xs px-2 py-1 bg-pnc-blue/20 text-pnc-blue-light rounded animate-pulse"
                        >
                          {agent}...
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t border-dark-border bg-dark-card px-6 py-4">
            <form onSubmit={handleSendMessage} className="max-w-4xl mx-auto">
              <div className="flex gap-3">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Describe what you want to create, research, or plan... (e.g., 'Create a new AI-powered dashboard feature')"
                  disabled={isLoading}
                  className="flex-1 input bg-dark-lighter border-dark-border focus:border-nvidia-green"
                />
                <button
                  type="submit"
                  disabled={isLoading || !input.trim()}
                  className="btn btn-primary px-6 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <Send className="w-5 h-5" />
                  )}
                </button>
              </div>
              <p className="text-xs text-gray-400 mt-2 text-center">
                💡 Try: "Create a product strategy for a B2B SaaS tool" or "Research competitors in the AI PM space"
              </p>
            </form>
          </div>
        </div>

        {/* Sidebar - Active Agents */}
        {activeAgents.size > 0 && (
          <div className="w-80 border-l border-dark-border bg-dark-card p-4 overflow-y-auto">
            <h3 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
              <Loader2 className="w-4 h-4 text-neon-cyan animate-spin" />
              Active Agents
            </h3>
            <div className="space-y-3">
              {Object.entries(agents).map(([key, agent]) => {
                const isActive = activeAgents.has(key);
                if (!isActive) return null;
                
                return (
                  <motion.div
                    key={key}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="p-3 bg-dark-lighter rounded-lg border border-pnc-blue/20"
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <Loader2 className="w-4 h-4 text-pnc-blue-light animate-spin" />
                      <span className="text-sm font-medium text-white">{agent.name}</span>
                    </div>
                    <p className="text-xs text-gray-400">{agent.goal}</p>
                    <p className="text-xs text-pnc-blue-light mt-2">Status: Running...</p>
                  </motion.div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Chat;

