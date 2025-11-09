/**
 * Refinement Modal - One-click refinement with A/B comparison
 */
import { useState } from 'react';
import { X, Sparkles, CheckCircle2, AlertCircle } from 'lucide-react';
import apiClient from '@/utils/apiClient';

interface RefinementModalProps {
  isOpen: boolean;
  onClose: () => void;
  agentName: string;
  originalOutput: any;
  onRefined?: (refined: any) => void;
}

export const RefinementModal: React.FC<RefinementModalProps> = ({
  isOpen,
  onClose,
  agentName,
  originalOutput,
  onRefined,
}) => {
  const [feedback, setFeedback] = useState('');
  const [refined, setRefined] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRefine = async () => {
    if (!feedback.trim()) {
      setError('Please provide feedback');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.refineAgentOutput(
        agentName,
        originalOutput,
        feedback
      );

      if (response.refined) {
        setRefined(response.refined);
        onRefined?.(response.refined);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to refine output');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="card p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-neon-cyan" />
            Refine {agentName} Output
          </h3>
          <button
            onClick={onClose}
            className="p-1 hover:bg-dark-lighter rounded transition-colors"
          >
            <X className="w-5 h-5 text-gray-400" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          {/* Original */}
          <div>
            <div className="flex items-center gap-2 mb-2">
              <AlertCircle className="w-4 h-4 text-gray-400" />
              <span className="text-sm font-medium text-gray-300">Original</span>
            </div>
            <div className="p-4 bg-dark-lighter rounded border border-gray-700 max-h-64 overflow-y-auto">
              <pre className="text-xs text-gray-300 whitespace-pre-wrap">
                {typeof originalOutput === 'string'
                  ? originalOutput
                  : JSON.stringify(originalOutput, null, 2)}
              </pre>
            </div>
          </div>

          {/* Refined */}
          <div>
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle2 className="w-4 h-4 text-green-400" />
              <span className="text-sm font-medium text-gray-300">Refined</span>
            </div>
            <div className="p-4 bg-green-500/10 rounded border border-green-500/30 max-h-64 overflow-y-auto">
              {refined ? (
                <pre className="text-xs text-gray-300 whitespace-pre-wrap">
                  {typeof refined === 'string'
                    ? refined
                    : JSON.stringify(refined, null, 2)}
                </pre>
              ) : (
                <div className="text-xs text-gray-500 italic">
                  Refined output will appear here...
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Feedback Input */}
        <div className="mb-4">
          <label className="block text-sm text-gray-400 mb-2">
            What would you like to improve?
          </label>
          <textarea
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            className="w-full input min-h-[100px]"
            placeholder="E.g., Make the user stories more specific, add more technical details, improve the market analysis..."
          />
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded text-sm text-red-400">
            {error}
          </div>
        )}

        {/* Improvements List */}
        {refined?.improvements && refined.improvements.length > 0 && (
          <div className="mb-4 p-3 bg-green-500/10 border border-green-500/30 rounded">
            <div className="text-sm font-medium text-green-400 mb-2">Improvements Made:</div>
            <ul className="space-y-1">
              {refined.improvements.map((improvement: string, i: number) => (
                <li key={i} className="text-xs text-gray-300 flex items-start gap-2">
                  <span className="text-green-400">✓</span>
                  <span>{improvement}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-3">
          <button
            onClick={handleRefine}
            disabled={loading || !feedback.trim()}
            className="btn btn-primary flex-1 disabled:opacity-50"
          >
            {loading ? 'Refining...' : 'Refine Output'}
          </button>
          <button onClick={onClose} className="btn btn-ghost">
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default RefinementModal;

