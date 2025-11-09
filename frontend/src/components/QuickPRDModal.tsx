/**
 * Quick PRD Modal - Simple single-prompt PRD generation
 */
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Zap, Loader2, ArrowLeft } from 'lucide-react';
import apiClient from '../utils/apiClient';

interface QuickPRDModalProps {
  isOpen: boolean;
  onClose: () => void;
  onComplete: (prdData: any) => void;
}

export const QuickPRDModal: React.FC<QuickPRDModalProps> = ({
  isOpen,
  onClose,
  onComplete,
}) => {
  const [productIdea, setProductIdea] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    if (!productIdea.trim()) return;

    setIsGenerating(true);
    try {
      // Run a lightweight workflow with just the product idea
      const result = await apiClient.runTask(
        'research_and_strategy',
        {
          feature: productIdea,
          quick_mode: true,
        },
        undefined,
        false // Don't use Nemotron for quick mode
      );

      // Generate quick PRD
      const prdResult = await apiClient.generatePRD(result.workflow_id);
      
      onComplete(prdResult.prd);
      setProductIdea('');
      onClose();
    } catch (error) {
      console.error('Error generating quick PRD:', error);
      alert('Failed to generate PRD. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      handleGenerate();
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
          className="relative w-full max-w-2xl bg-dark-card border-2 border-dark-border rounded-xl shadow-2xl"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-dark-border">
            <div className="flex items-center gap-3">
              {!isGenerating && (
                <button
                  onClick={onClose}
                  className="p-2 hover:bg-dark-lighter rounded-lg transition-colors"
                  title="Back to home"
                >
                  <ArrowLeft className="w-5 h-5 text-gray-400" />
                </button>
              )}
              <div>
                <h2 className="text-2xl font-display font-bold text-white flex items-center gap-2">
                  <Zap className="w-6 h-6 text-orange-400" />
                  Quick PRD Generation
                </h2>
                <p className="text-sm text-gray-400 mt-1">
                  Describe your product idea in a few sentences
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
                <textarea
                  value={productIdea}
                  onChange={(e) => setProductIdea(e.target.value)}
                  onKeyDown={handleKeyPress}
                  placeholder="Describe your product idea...&#10;&#10;Example: An AI-powered project management tool that helps teams automate sprint planning, track progress, and generate insights from project data. Target users are product managers at tech startups."
                  className="w-full h-48 px-4 py-3 bg-dark-lighter border border-dark-border rounded-lg text-white placeholder-gray-500 focus:border-orange-400 focus:outline-none resize-none"
                  autoFocus
                />
                
                <div className="mt-4 flex items-center justify-between">
                  <p className="text-xs text-gray-500">
                    Press ⌘+Enter (Ctrl+Enter on Windows) to generate
                  </p>
                  <button
                    onClick={handleGenerate}
                    disabled={!productIdea.trim()}
                    className="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Zap className="w-4 h-4" />
                    Generate Quick PRD
                  </button>
                </div>

                <div className="mt-4 p-4 bg-orange-400/10 border border-orange-400/30 rounded-lg">
                  <p className="text-sm text-gray-300">
                    💡 <span className="font-medium">Quick Mode:</span> AI will generate assumptions
                    and structure based on your description. Great for rapid prototyping!
                  </p>
                </div>
              </>
            ) : (
              <div className="text-center py-12">
                <Loader2 className="w-12 h-12 text-orange-400 mx-auto mb-4 animate-spin" />
                <h3 className="text-xl font-bold text-white mb-2">
                  Generating Quick PRD
                </h3>
                <p className="text-gray-400">
                  This should only take a moment...
                </p>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default QuickPRDModal;

