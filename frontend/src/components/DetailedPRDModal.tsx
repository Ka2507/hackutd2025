/**
 * Detailed PRD Modal - Multi-step wizard through all 9 agents
 */
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, ChevronRight, ChevronLeft, Check, Loader2 } from 'lucide-react';
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
    prompt: 'Describe your product idea and target market',
    placeholder: 'e.g., AI-powered analytics dashboard for B2B SaaS companies...',
  },
  {
    key: 'research',
    name: 'Research',
    title: 'User Research',
    prompt: 'Who are your target users and what problems do they face?',
    placeholder: 'e.g., Product managers at mid-size tech companies struggling with...',
  },
  {
    key: 'risk',
    name: 'Risk Assessment',
    title: 'Risk Analysis',
    prompt: 'What are the potential risks and challenges?',
    placeholder: 'e.g., Technical complexity, market competition, timeline constraints...',
  },
  {
    key: 'dev',
    name: 'Development',
    title: 'Technical Requirements',
    prompt: 'Describe key features and technical requirements',
    placeholder: 'e.g., Real-time data visualization, API integrations, authentication...',
  },
  {
    key: 'prioritization',
    name: 'Prioritization',
    title: 'Feature Prioritization',
    prompt: 'What features are must-haves vs nice-to-haves?',
    placeholder: 'e.g., MVP features: dashboard, analytics. Phase 2: integrations, AI...',
  },
  {
    key: 'prototype',
    name: 'Design',
    title: 'Design & UX',
    prompt: 'Describe your design vision and user experience goals',
    placeholder: 'e.g., Clean, modern interface with data visualizations and...',
  },
  {
    key: 'gtm',
    name: 'Go-to-Market',
    title: 'Launch Strategy',
    prompt: 'How will you launch and position this product?',
    placeholder: 'e.g., Target early adopters in PM community, LinkedIn campaigns...',
  },
  {
    key: 'automation',
    name: 'Automation',
    title: 'Workflow Automation',
    prompt: 'What workflows should be automated?',
    placeholder: 'e.g., Daily reports, sprint planning, user feedback analysis...',
  },
  {
    key: 'regulation',
    name: 'Compliance',
    title: 'Compliance & Regulations',
    prompt: 'What compliance or regulatory requirements apply?',
    placeholder: 'e.g., GDPR for EU users, SOC 2 for enterprise, data privacy...',
  },
];

export const DetailedPRDModal: React.FC<DetailedPRDModalProps> = ({
  isOpen,
  onClose,
  onComplete,
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [responses, setResponses] = useState<Record<string, string>>({});
  const [currentInput, setCurrentInput] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const currentAgent = AGENT_STEPS[currentStep];
  const progress = ((currentStep + 1) / AGENT_STEPS.length) * 100;

  const handleNext = () => {
    if (currentInput.trim()) {
      setResponses({ ...responses, [currentAgent.key]: currentInput });
      setCurrentInput('');
      
      if (currentStep < AGENT_STEPS.length - 1) {
        setCurrentStep(currentStep + 1);
      } else {
        handleGeneratePRD();
      }
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      const prevAgent = AGENT_STEPS[currentStep - 1];
      setCurrentInput(responses[prevAgent.key] || '');
      setCurrentStep(currentStep - 1);
    }
  };

  const handleGeneratePRD = async () => {
    setIsGenerating(true);
    try {
      // Run full feature planning workflow with all context
      const workflowResult = await apiClient.runTask(
        'full_feature_planning',
        {
          ...responses,
          feature: responses.strategy || 'New Product',
          market: responses.research || 'Target Market',
        },
        undefined,
        true
      );

      // Generate PRD
      const prdResult = await apiClient.generatePRD(workflowResult.workflow_id);
      
      onComplete(prdResult.prd);
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
    setResponses({});
    setCurrentInput('');
    setIsGenerating(false);
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
            <div>
              <h2 className="text-xl font-display font-bold text-white flex items-center gap-2">
                <Brain className="w-5 h-5 text-neon-cyan" />
                {currentAgent.title}
              </h2>
              <p className="text-sm text-gray-400 mt-1">
                Step {currentStep + 1} of {AGENT_STEPS.length} • {currentAgent.name} Agent
              </p>
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
                <label className="block text-sm font-medium text-gray-300 mb-3">
                  {currentAgent.prompt}
                </label>
                <textarea
                  value={currentInput}
                  onChange={(e) => setCurrentInput(e.target.value)}
                  placeholder={currentAgent.placeholder}
                  className="w-full h-40 px-4 py-3 bg-dark-lighter border border-dark-border rounded-lg text-white placeholder-gray-500 focus:border-neon-cyan focus:outline-none resize-none"
                  autoFocus
                />
                
                {/* Navigation */}
                <div className="flex items-center justify-between mt-6">
                  <button
                    onClick={handleBack}
                    disabled={currentStep === 0}
                    className="flex items-center gap-2 px-4 py-2 text-gray-400 hover:text-white transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
                  >
                    <ChevronLeft className="w-4 h-4" />
                    Back
                  </button>
                  
                  <div className="flex items-center gap-3">
                    <button
                      onClick={handleSkip}
                      className="px-4 py-2 text-gray-400 hover:text-white transition-colors text-sm"
                    >
                      Skip
                    </button>
                    <button
                      onClick={handleNext}
                      disabled={!currentInput.trim()}
                      className="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {currentStep === AGENT_STEPS.length - 1 ? (
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
                  Generating Your Detailed PRD
                </h3>
                <p className="text-gray-400">
                  Our 9 AI agents are working together to create your comprehensive PRD...
                </p>
                <div className="mt-6 flex flex-wrap justify-center gap-2">
                  {AGENT_STEPS.map((agent, idx) => (
                    <span
                      key={agent.key}
                      className={`text-xs px-2 py-1 rounded ${
                        idx <= currentStep
                          ? 'bg-neon-cyan/20 text-neon-cyan'
                          : 'bg-dark-lighter text-gray-500'
                      }`}
                    >
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

