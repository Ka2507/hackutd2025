/**
 * PRD Selection Modal - Choose between Detailed or Quick PRD generation
 */
import { motion, AnimatePresence } from 'framer-motion';
import { X, Zap, Brain, FileText, ArrowRight, ArrowLeft } from 'lucide-react';

interface PRDSelectionModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectDetailed: () => void;
  onSelectQuick: () => void;
}

export const PRDSelectionModal: React.FC<PRDSelectionModalProps> = ({
  isOpen,
  onClose,
  onSelectDetailed,
  onSelectQuick,
}) => {
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="absolute inset-0 bg-black/80 backdrop-blur-sm"
        />

        {/* Modal */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="relative w-full max-w-4xl bg-dark-card border-2 border-dark-border rounded-xl shadow-2xl"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-dark-border">
            <div className="flex items-center gap-3">
              <button
                onClick={onClose}
                className="p-2 hover:bg-dark-lighter rounded-lg transition-colors"
                title="Back to home"
              >
                <ArrowLeft className="w-5 h-5 text-gray-400" />
              </button>
              <div>
                <h2 className="text-2xl font-display font-bold gradient-text flex items-center gap-2">
                  <FileText className="w-6 h-6" />
                  Generate PRD
                </h2>
                <p className="text-sm text-gray-400 mt-1">
                  Choose your PRD generation method
                </p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-dark-lighter rounded-lg transition-colors"
            >
              <X className="w-6 h-6 text-gray-400" />
            </button>
          </div>

          {/* Content */}
          <div className="p-6">
            <div className="grid md:grid-cols-2 gap-6">
              {/* Detailed PRD Option */}
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={onSelectDetailed}
                className="relative p-6 bg-dark-lighter border-2 border-dark-border hover:border-neon-cyan rounded-xl text-left transition-all group overflow-hidden"
              >
                {/* Glow effect */}
                <div className="absolute inset-0 bg-gradient-to-br from-neon-cyan/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                
                <div className="relative">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-3 bg-neon-cyan/20 rounded-lg">
                      <Brain className="w-8 h-8 text-neon-cyan" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-white">Detailed PRD</h3>
                      <span className="text-xs text-neon-cyan font-medium">Recommended</span>
                    </div>
                  </div>
                  
                  <p className="text-gray-300 mb-4">
                    Comprehensive PRD with all 9 AI agents working together. You'll provide context through each agent for maximum detail and accuracy.
                  </p>
                  
                  <div className="space-y-2 mb-4">
                    <div className="flex items-start gap-2 text-sm text-gray-400">
                      <span className="text-neon-cyan mt-0.5">✓</span>
                      <span>Full agent orchestration (Strategy, Research, Dev, GTM, etc.)</span>
                    </div>
                    <div className="flex items-start gap-2 text-sm text-gray-400">
                      <span className="text-neon-cyan mt-0.5">✓</span>
                      <span>Contextual prompts for each section</span>
                    </div>
                    <div className="flex items-start gap-2 text-sm text-gray-400">
                      <span className="text-neon-cyan mt-0.5">✓</span>
                      <span>Comprehensive market analysis, technical specs, and more</span>
                    </div>
                    <div className="flex items-start gap-2 text-sm text-gray-400">
                      <span className="text-orange-400 mt-0.5">⏱</span>
                      <span>~5-10 minutes</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2 text-neon-cyan font-medium">
                    <span>Start Detailed PRD</span>
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </motion.button>

              {/* Quick PRD Option */}
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={onSelectQuick}
                className="relative p-6 bg-dark-lighter border-2 border-dark-border hover:border-orange-400 rounded-xl text-left transition-all group overflow-hidden"
              >
                {/* Glow effect */}
                <div className="absolute inset-0 bg-gradient-to-br from-orange-400/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                
                <div className="relative">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-3 bg-orange-400/20 rounded-lg">
                      <Zap className="w-8 h-8 text-orange-400" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-white">Quick PRD</h3>
                      <span className="text-xs text-orange-400 font-medium">Fast & Simple</span>
                    </div>
                  </div>
                  
                  <p className="text-gray-300 mb-4">
                    Rapid PRD generation with minimal input. Perfect for brainstorming, creating skeletons, or getting started quickly.
                  </p>
                  
                  <div className="space-y-2 mb-4">
                    <div className="flex items-start gap-2 text-sm text-gray-400">
                      <span className="text-orange-400 mt-0.5">✓</span>
                      <span>Single prompt input</span>
                    </div>
                    <div className="flex items-start gap-2 text-sm text-gray-400">
                      <span className="text-orange-400 mt-0.5">✓</span>
                      <span>AI-generated assumptions and structure</span>
                    </div>
                    <div className="flex items-start gap-2 text-sm text-gray-400">
                      <span className="text-orange-400 mt-0.5">✓</span>
                      <span>Great for brainstorming and iteration</span>
                    </div>
                    <div className="flex items-start gap-2 text-sm text-gray-400">
                      <span className="text-green-400 mt-0.5">⚡</span>
                      <span>~1-2 minutes</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2 text-orange-400 font-medium">
                    <span>Generate Quick PRD</span>
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </motion.button>
            </div>

            {/* Info */}
            <div className="mt-6 p-4 bg-dark-lighter/50 border border-dark-border rounded-lg">
              <p className="text-sm text-gray-400 text-center">
                💡 <span className="text-gray-300">Tip:</span> Start with Quick PRD for brainstorming, then use Detailed PRD for the final document
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default PRDSelectionModal;

