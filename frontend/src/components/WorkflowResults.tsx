/**
 * WorkflowResults - Enhanced display of workflow results with risk, prioritization, etc.
 */
import { motion } from 'framer-motion';
import { AlertTriangle, TrendingUp, Target, Zap, CheckCircle2 } from 'lucide-react';

interface WorkflowResultsProps {
  result: any;
}

export const WorkflowResults: React.FC<WorkflowResultsProps> = ({ result }) => {
  if (!result || !result.result) return null;

  const workflowResult = result.result;
  const steps = workflowResult.steps || [];
  
  // Extract risk assessment
  const riskStep = steps.find((s: any) => s.agent === 'RiskAssessmentAgent' || s.result?.risk_score !== undefined);
  const riskData = riskStep?.result?.result;
  
  // Extract prioritization
  const priorityStep = steps.find((s: any) => s.agent === 'PrioritizationAgent' || s.result?.prioritized_features);
  const priorityData = priorityStep?.result?.result;
  
  // Check for adaptive workflow
  const isAdaptive = workflowResult.workflow === 'adaptive' || workflowResult.adaptations;
  const adaptations = workflowResult.adaptations || [];

  return (
    <div className="space-y-4">
      {/* Adaptive Workflow Indicator */}
      {isAdaptive && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="card border-l-4 border-l-nvidia-green bg-nvidia-green/5"
        >
          <div className="flex items-center gap-3">
            <Zap className="w-5 h-5 text-nvidia-green" />
            <div>
              <h4 className="text-sm font-semibold text-white">Adaptive Workflow</h4>
              <p className="text-xs text-gray-400">
                Agents were dynamically selected based on task analysis
              </p>
              {adaptations.length > 0 && (
                <p className="text-xs text-yellow-400 mt-1">
                  {adaptations.length} workflow adaptation(s) applied
                </p>
              )}
            </div>
          </div>
        </motion.div>
      )}

      {/* Risk Assessment Display */}
      {riskData && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="card border-l-4 border-l-red-400 bg-red-500/5"
        >
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <div className="flex items-center justify-between mb-2">
                <h4 className="text-sm font-semibold text-white">Risk Assessment</h4>
                <span className={`badge ${
                  (riskData.risk_score || 0) > 0.7 ? 'badge-error' :
                  (riskData.risk_score || 0) > 0.4 ? 'badge-warning' :
                  'badge-success'
                }`}>
                  {(riskData.risk_score || 0).toFixed(2)} - {riskData.risk_level || 'Low'}
                </span>
              </div>
              
              {riskData.predicted_bottlenecks && riskData.predicted_bottlenecks.length > 0 && (
                <div className="mt-2">
                  <p className="text-xs text-gray-400 mb-1">Predicted Bottlenecks:</p>
                  <ul className="text-xs text-gray-300 space-y-1">
                    {riskData.predicted_bottlenecks.slice(0, 3).map((b: any, i: number) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-red-400 mt-0.5">•</span>
                        <span>{b.description || b.agent || 'Potential issue detected'}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              
              {riskData.mitigations && riskData.mitigations.length > 0 && (
                <div className="mt-2 p-2 bg-dark-lighter rounded">
                  <p className="text-xs text-gray-400 mb-1">Mitigations:</p>
                  <ul className="text-xs text-gray-300 space-y-1">
                    {riskData.mitigations.slice(0, 2).map((m: any, i: number) => (
                      <li key={i} className="flex items-start gap-2">
                        <CheckCircle2 className="w-3 h-3 text-green-400 mt-0.5 flex-shrink-0" />
                        <span>{m.strategy || m}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      )}

      {/* Prioritization Display */}
      {priorityData && priorityData.prioritized_features && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="card border-l-4 border-l-blue-400 bg-blue-500/5"
        >
          <div className="flex items-start gap-3">
            <TrendingUp className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <div className="flex items-center justify-between mb-2">
                <h4 className="text-sm font-semibold text-white">Smart Prioritization</h4>
                <span className="text-xs text-gray-400">
                  {priorityData.total_features || priorityData.prioritized_features.length} features
                </span>
              </div>
              
              {priorityData.prioritized_features.slice(0, 3).map((feature: any, i: number) => (
                <div key={i} className="mt-2 p-2 bg-dark-lighter rounded">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-medium text-white">
                      {feature.feature?.title || feature.feature?.name || `Feature ${i + 1}`}
                    </span>
                    <span className="text-xs font-semibold text-blue-400">
                      Score: {(feature.score || 0).toFixed(2)}
                    </span>
                  </div>
                  {feature.factors && (
                    <div className="text-xs text-gray-400 mt-1">
                      Market: {(feature.factors.market_impact || 0).toFixed(2)} • 
                      Value: {(feature.factors.user_value || 0).toFixed(2)} • 
                      Effort: {(feature.factors.effort || 0).toFixed(2)}
                    </div>
                  )}
                </div>
              ))}
              
              {priorityData.explanation && (
                <p className="text-xs text-gray-400 mt-2 italic">
                  {priorityData.explanation.substring(0, 150)}...
                </p>
              )}
            </div>
          </div>
        </motion.div>
      )}

      {/* Agent Collaboration Indicator */}
      {workflowResult.summary?.adaptations !== undefined && workflowResult.summary.adaptations > 0 && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="card border-l-4 border-l-purple-400 bg-purple-500/5"
        >
          <div className="flex items-center gap-3">
            <Target className="w-5 h-5 text-purple-400" />
            <div>
              <h4 className="text-sm font-semibold text-white">Agent Collaboration</h4>
              <p className="text-xs text-gray-400">
                Agents validated and refined each other's outputs
              </p>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default WorkflowResults;

