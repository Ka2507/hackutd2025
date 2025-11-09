/**
 * PRDGenerateModal - Modal for choosing PRD generation method
 */
import { motion, AnimatePresence } from 'framer-motion';
import { X, Zap, Target, FileText } from 'lucide-react';

interface PRDGenerateModalProps {
  isOpen: boolean;
  onClose: () => void;
  onGenerateDetailed: () => void;
  onGenerateQuick: () => void;
}

export const PRDGenerateModal: React.FC<PRDGenerateModalProps> = ({
  isOpen,
  onClose,
  onGenerateDetailed,
  onGenerateQuick,
}) => {
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-dark/90 backdrop-blur-sm z-50 flex items-center justify-center p-6"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.95, opacity: 0 }}
          className="card max-w-2xl w-full relative"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Close button */}
          <button
            onClick={onClose}
            className="absolute top-4 right-4 p-2 hover:bg-dark-lighter rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-gray-400" />
          </button>

          {/* Header */}
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-primary/20 border border-primary/30 rounded-xl flex items-center justify-center mx-auto mb-4">
              <FileText className="w-8 h-8 text-primary-light" />
            </div>
            <h2 className="text-2xl font-display font-bold text-light mb-2">
              Generate PRD
            </h2>
            <p className="text-gray-400">
              Choose your generation method
            </p>
          </div>

          {/* Options */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Detailed Option */}
            <button
              onClick={() => {
                onClose();
                onGenerateDetailed();
              }}
              className="p-6 bg-dark-lighter border-2 border-dark-border hover:border-primary/50 rounded-xl text-left transition-all hover:scale-105 group"
            >
              <div className="flex items-start gap-4 mb-4">
                <div className="w-12 h-12 bg-primary/20 border border-primary/30 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:bg-primary/30 transition-colors">
                  <Target className="w-6 h-6 text-primary-light" />
                </div>
                <div>
                  <h3 className="text-lg font-display font-semibold text-light mb-1">
                    Detailed PRD
                  </h3>
                  <p className="text-xs text-gray-400">
                    Recommended for thoroughness
                  </p>
                </div>
              </div>
              <p className="text-sm text-gray-300 mb-4">
                Runs all agents to gather comprehensive context before generating PRD
              </p>
              <div className="space-y-2 text-xs text-gray-400">
                <div className="flex items-center gap-2">
                  <span className="text-primary-light">•</span>
                  <span>More detailed and accurate</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-primary-light">•</span>
                  <span>All 9 agents contribute</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-primary-light">•</span>
                  <span>Takes ~2-3 minutes</span>
                </div>
              </div>
            </button>

            {/* Quick Option */}
            <button
              onClick={() => {
                onClose();
                onGenerateQuick();
              }}
              className="p-6 bg-dark-lighter border-2 border-dark-border hover:border-accent/50 rounded-xl text-left transition-all hover:scale-105 group"
            >
              <div className="flex items-start gap-4 mb-4">
                <div className="w-12 h-12 bg-accent/20 border border-accent/30 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:bg-accent/30 transition-colors">
                  <Zap className="w-6 h-6 text-accent-light" />
                </div>
                <div>
                  <h3 className="text-lg font-display font-semibold text-light mb-1">
                    Quick PRD
                  </h3>
                  <p className="text-xs text-gray-400">
                    Fast generation
                  </p>
                </div>
              </div>
              <p className="text-sm text-gray-300 mb-4">
                Enter brief requirements and generate PRD immediately from your input
              </p>
              <div className="space-y-2 text-xs text-gray-400">
                <div className="flex items-center gap-2">
                  <span className="text-accent-light">•</span>
                  <span>Faster generation</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-accent-light">•</span>
                  <span>Minimal context needed</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-accent-light">•</span>
                  <span>Takes ~30 seconds</span>
                </div>
              </div>
            </button>
          </div>

          {/* Info */}
          <div className="mt-6 p-4 bg-dark-lighter/50 border border-dark-border rounded-lg">
            <p className="text-xs text-gray-500 text-center">
              Both options generate a comprehensive PRD with all standard sections
            </p>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default PRDGenerateModal;

