/**
 * PRD Viewer - Display generated PRD document
 */
import { motion } from 'framer-motion';
import { X, Download, Copy, Check } from 'lucide-react';
import { useState } from 'react';

interface PRDViewerProps {
  isOpen: boolean;
  onClose: () => void;
  prdData: any;
}

export const PRDViewer: React.FC<PRDViewerProps> = ({ isOpen, onClose, prdData }) => {
  const [copied, setCopied] = useState(false);

  if (!isOpen || !prdData) return null;

  const handleCopy = () => {
    const text = JSON.stringify(prdData, null, 2);
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([JSON.stringify(prdData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `PRD-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
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
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="relative w-full max-w-5xl max-h-[90vh] bg-dark-card border-2 border-dark-border rounded-xl shadow-2xl flex flex-col"
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-dark-border">
          <h2 className="text-2xl font-display font-bold gradient-text">
            Product Requirements Document
          </h2>
          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="p-2 hover:bg-dark-lighter rounded-lg transition-colors"
              title="Copy to clipboard"
            >
              {copied ? (
                <Check className="w-5 h-5 text-green-400" />
              ) : (
                <Copy className="w-5 h-5 text-gray-400" />
              )}
            </button>
            <button
              onClick={handleDownload}
              className="p-2 hover:bg-dark-lighter rounded-lg transition-colors"
              title="Download PRD"
            >
              <Download className="w-5 h-5 text-gray-400" />
            </button>
            <button
              onClick={onClose}
              className="p-2 hover:bg-dark-lighter rounded-lg transition-colors"
            >
              <X className="w-6 h-6 text-gray-400" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-6">
          <div className="prose prose-invert max-w-none">
            <pre className="bg-dark-lighter p-4 rounded-lg text-sm text-gray-300 overflow-x-auto whitespace-pre-wrap">
              {JSON.stringify(prdData, null, 2)}
            </pre>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default PRDViewer;

