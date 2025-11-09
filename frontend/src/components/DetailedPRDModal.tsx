/**
 * Detailed PRD Modal - Multi-step wizard through all 9 agents
 */
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, ChevronRight, ChevronLeft, Check, Loader2, ArrowLeft, Brain, Sparkles } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import apiClient from '../utils/apiClient';

interface DetailedPRDModalProps {
  isOpen: boolean;
  onClose: () => void;
  onComplete: (prdData: any) => void;
}

const AGENT_STEPS = [
  {
    key: 'strategy',
    name: 'Strategy',
    title: 'Strategic Planning',
    prompt: 'Tell me about your product idea',
    aiPrompt: 'Based on this product idea, provide strategic analysis including: market opportunity, competitive landscape, positioning strategy, and key success metrics.',
    placeholder: 'e.g., AI-powered analytics dashboard for B2B SaaS companies...',
  },
  {
    key: 'research',
    name: 'Research',
    title: 'User Research',
    prompt: 'Who are your target users?',
    aiPrompt: 'Analyze the target users and provide: user personas, pain points, user needs analysis, and market validation insights.',
    placeholder: 'e.g., Product managers at mid-size tech companies...',
  },
  {
    key: 'risk',
    name: 'Risk Assessment',
    title: 'Risk Analysis',
    prompt: 'What challenges do you anticipate?',
    aiPrompt: 'Assess potential risks including: technical risks, market risks, timeline risks, resource constraints, and mitigation strategies for each.',
    placeholder: 'e.g., Technical complexity, market competition...',
  },
  {
    key: 'dev',
    name: 'Development',
    title: 'Technical Requirements',
    prompt: 'What are the key features and capabilities needed?',
    aiPrompt: 'Generate technical specifications including: user stories, acceptance criteria, technical architecture, API requirements, and sprint planning.',
    placeholder: 'e.g., Real-time data visualization, API integrations...',
  },
  {
    key: 'prioritization',
    name: 'Prioritization',
    title: 'Feature Prioritization',
    prompt: 'Which features are most important?',
    aiPrompt: 'Prioritize features using RICE framework (Reach, Impact, Confidence, Effort) and provide: MVP scope, roadmap phases, and feature rankings.',
    placeholder: 'e.g., MVP features: dashboard, analytics. Phase 2: AI...',
  },
  {
    key: 'prototype',
    name: 'Design',
    title: 'Design & UX',
    prompt: 'Describe your design vision',
    aiPrompt: 'Define design requirements including: UI/UX specifications, wireframe concepts, design system elements, and user flow recommendations.',
    placeholder: 'e.g., Clean, modern interface with data visualizations...',
  },
  {
    key: 'gtm',
    name: 'Go-to-Market',
    title: 'Launch Strategy',
    prompt: 'How do you plan to launch?',
    aiPrompt: 'Create go-to-market strategy including: launch plan, pricing strategy, marketing channels, positioning, and success metrics.',
    placeholder: 'e.g., Target early adopters, LinkedIn campaigns...',
  },
  {
    key: 'automation',
    name: 'Automation',
    title: 'Workflow Automation',
    prompt: 'What processes should be automated?',
    aiPrompt: 'Identify automation opportunities including: workflow automation, reporting automation, integration points, and efficiency gains.',
    placeholder: 'e.g., Daily reports, sprint planning...',
  },
  {
    key: 'regulation',
    name: 'Compliance',
    title: 'Compliance & Regulations',
    prompt: 'What compliance requirements apply?',
    aiPrompt: 'Review compliance needs including: regulatory requirements (GDPR, SOC2, etc), security standards, privacy considerations, and compliance roadmap.',
    placeholder: 'e.g., GDPR for EU users, SOC 2 for enterprise...',
  },
];

export const DetailedPRDModal: React.FC<DetailedPRDModalProps> = ({
  isOpen,
  onClose,
  onComplete,
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [userInputs, setUserInputs] = useState<Record<string, string>>({});
  const [agentResponses, setAgentResponses] = useState<Record<string, string>>({});
  const [currentInput, setCurrentInput] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isProcessingAgent, setIsProcessingAgent] = useState(false);

  const currentAgent = AGENT_STEPS[currentStep];
  const progress = ((currentStep + 1) / AGENT_STEPS.length) * 100;

  const handleNext = async () => {
    if (!currentInput.trim()) return;
    
    setIsProcessingAgent(true);
    
    try {
      // Store user's input
      const newUserInputs = { ...userInputs, [currentAgent.key]: currentInput };
      setUserInputs(newUserInputs);
      
      // Build context from all previous interactions
      const contextMessages = Object.entries(newUserInputs).map(([key, value]) => {
        const step = AGENT_STEPS.find(s => s.key === key);
        return `${step?.title || key}: ${value}`;
      }).join('\n\n');
      
      // Call the agent with full context
      const fullPrompt = `${currentAgent.aiPrompt}\n\nProduct Context:\n${contextMessages}`;
      
      const response = await apiClient.executeAgent(
        currentAgent.key,
        'chat',
        {
          message: fullPrompt,
          conversation_history: []
        }
      );
      
      // Extract agent's response
      const resultData = response.result?.result || {};
      let aiResponse = resultData.response || 'Analysis complete.';
      
      // Remove thinking tags from displayed response
      aiResponse = aiResponse.replace(/<think>[\s\S]*?<\/think>\s*/g, '').trim();
      
      // Store agent's response
      setAgentResponses({ ...agentResponses, [currentAgent.key]: aiResponse });
      setCurrentInput('');
      
      // Move to next step or generate PRD
      if (currentStep < AGENT_STEPS.length - 1) {
        setCurrentStep(currentStep + 1);
      } else {
        await handleGeneratePRD(newUserInputs, { ...agentResponses, [currentAgent.key]: aiResponse });
      }
    } catch (error) {
      console.error('Error processing agent:', error);
      alert('Failed to process with agent. Please try again.');
    } finally {
      setIsProcessingAgent(false);
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      const prevAgent = AGENT_STEPS[currentStep - 1];
      setCurrentInput(userInputs[prevAgent.key] || '');
      setCurrentStep(currentStep - 1);
    }
  };

  const handleGeneratePRD = async (inputs: Record<string, string>, responses: Record<string, string>) => {
    setIsGenerating(true);
    try {
      // Compile all agent analyses into a comprehensive PRD
      const prdSections = AGENT_STEPS.map(agent => ({
        title: agent.title,
        userInput: inputs[agent.key] || '',
        agentAnalysis: responses[agent.key] || ''
      }));
      
      const compiledPRD = {
        title: inputs.strategy ? `PRD: ${inputs.strategy.split('\n')[0].substring(0, 100)}` : 'Product Requirements Document',
        generatedAt: new Date().toISOString(),
        sections: prdSections,
        fullContent: prdSections.map(section => 
          `## ${section.title}\n\n### Your Input:\n${section.userInput}\n\n### Analysis:\n${section.agentAnalysis}`
        ).join('\n\n---\n\n')
      };
      
      onComplete(compiledPRD);
      handleReset();
      onClose();
    } catch (error) {
      console.error('Error generating detailed PRD:', error);
      alert('Failed to generate PRD. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleReset = () => {
    setCurrentStep(0);
    setUserInputs({});
    setAgentResponses({});
    setCurrentInput('');
    setIsGenerating(false);
    setIsProcessingAgent(false);
  };

  const handleSkip = () => {
    if (currentStep < AGENT_STEPS.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={isGenerating ? undefined : onClose}
          className="absolute inset-0 bg-black/80 backdrop-blur-sm"
        />

        {/* Modal */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="relative w-full max-w-3xl bg-dark-card border-2 border-dark-border rounded-xl shadow-2xl"
        >
          {/* Progress Bar */}
          <div className="h-2 bg-dark-lighter rounded-t-xl overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              className="h-full bg-gradient-to-r from-neon-cyan to-orange-400"
              transition={{ duration: 0.3 }}
            />
          </div>

          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-dark-border">
            <div className="flex items-center gap-3">
              {!isGenerating && currentStep === 0 && (
                <button
                  onClick={onClose}
                  className="p-2 hover:bg-dark-lighter rounded-lg transition-colors"
                  title="Back to home"
                >
                  <ArrowLeft className="w-5 h-5 text-gray-400" />
                </button>
              )}
              <div>
                <h2 className="text-xl font-display font-bold text-white flex items-center gap-2">
                  <Brain className="w-5 h-5 text-neon-cyan" />
                  {currentAgent.title}
                </h2>
                <p className="text-sm text-gray-400 mt-1">
                  Step {currentStep + 1} of {AGENT_STEPS.length} • {currentAgent.name} Agent
                </p>
              </div>
            </div>
            {!isGenerating && (
              <button
                onClick={onClose}
                className="p-2 hover:bg-dark-lighter rounded-lg transition-colors"
              >
                <X className="w-6 h-6 text-gray-400" />
              </button>
            )}
          </div>

          {/* Content */}
          <div className="p-6">
            {!isGenerating ? (
              <>
                {/* Show previous agent's response if available */}
                {currentStep > 0 && agentResponses[AGENT_STEPS[currentStep - 1].key] && (
                  <div className="mb-6 p-4 bg-dark-lighter border border-dark-border rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Sparkles className="w-4 h-4 text-neon-cyan" />
                      <span className="text-sm font-semibold text-neon-cyan">
                        {AGENT_STEPS[currentStep - 1].name} Agent Analysis
                      </span>
                    </div>
                    <div className="text-sm text-gray-300 max-h-40 overflow-y-auto prose prose-invert prose-sm">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {agentResponses[AGENT_STEPS[currentStep - 1].key].substring(0, 500) + '...'}
                      </ReactMarkdown>
                    </div>
                  </div>
                )}
                
                <label className="block text-sm font-medium text-gray-300 mb-3">
                  {currentAgent.prompt}
                </label>
                <textarea
                  value={currentInput}
                  onChange={(e) => setCurrentInput(e.target.value)}
                  placeholder={currentAgent.placeholder}
                  className="w-full h-40 px-4 py-3 bg-dark-lighter border border-dark-border rounded-lg text-white placeholder-gray-500 focus:border-neon-cyan focus:outline-none resize-none"
                  autoFocus
                  disabled={isProcessingAgent}
                />
                
                {/* Loading state while processing agent */}
                {isProcessingAgent && (
                  <div className="mt-4 flex items-center gap-2 text-neon-cyan">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="text-sm">{currentAgent.name} Agent is analyzing...</span>
                  </div>
                )}
                
                {/* Navigation */}
                <div className="flex items-center justify-between mt-6">
                  <button
                    onClick={handleBack}
                    disabled={currentStep === 0 || isProcessingAgent}
                    className="flex items-center gap-2 px-4 py-2 text-gray-400 hover:text-white transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
                  >
                    <ChevronLeft className="w-4 h-4" />
                    Back
                  </button>
                  
                  <div className="flex items-center gap-3">
                    <button
                      onClick={handleSkip}
                      disabled={isProcessingAgent}
                      className="px-4 py-2 text-gray-400 hover:text-white transition-colors text-sm disabled:opacity-30"
                    >
                      Skip
                    </button>
                    <button
                      onClick={handleNext}
                      disabled={!currentInput.trim() || isProcessingAgent}
                      className="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isProcessingAgent ? (
                        <>
                          <Loader2 className="w-4 h-4 animate-spin" />
                          Processing...
                        </>
                      ) : currentStep === AGENT_STEPS.length - 1 ? (
                        <>
                          <Check className="w-4 h-4" />
                          Generate PRD
                        </>
                      ) : (
                        <>
                          Next
                          <ChevronRight className="w-4 h-4" />
                        </>
                      )}
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <div className="text-center py-12">
                <Loader2 className="w-12 h-12 text-neon-cyan mx-auto mb-4 animate-spin" />
                <h3 className="text-xl font-bold text-white mb-2">
                  Compiling Your Comprehensive PRD
                </h3>
                <p className="text-gray-400">
                  Combining insights from all 9 specialized AI agents...
                </p>
                <div className="mt-6 flex flex-wrap justify-center gap-2">
                  {AGENT_STEPS.map((agent) => (
                    <span
                      key={agent.key}
                      className="text-xs px-2 py-1 rounded bg-neon-cyan/20 text-neon-cyan flex items-center gap-1"
                    >
                      <Check className="w-3 h-3" />
                      {agent.name}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default DetailedPRDModal;

