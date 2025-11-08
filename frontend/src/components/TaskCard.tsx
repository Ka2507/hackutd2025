/**
 * TaskCard - Displays individual task information
 */
import { motion } from 'framer-motion';
import { CheckCircle2, Clock, XCircle, ArrowRight } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import WorkflowResults from './WorkflowResults';

interface TaskCardProps {
  task: {
    id?: string;
    workflow_type?: string;
    status: string;
    timestamp?: string;
    agent?: string;
    task_type?: string;
    result?: any;
  };
  index?: number;
}

export const TaskCard: React.FC<TaskCardProps> = ({ task, index = 0 }) => {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="w-5 h-5 text-green-400" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-400" />;
      default:
        return <Clock className="w-5 h-5 text-yellow-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'border-green-400/30 bg-green-500/5';
      case 'failed':
        return 'border-red-400/30 bg-red-500/5';
      case 'running':
        return 'border-neon-cyan bg-neon-cyan/5 glow-border';
      default:
        return 'border-gray-300';
    }
  };

  const timeAgo = task.timestamp
    ? formatDistanceToNow(new Date(task.timestamp), { addSuffix: true })
    : 'just now';

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1 }}
      className={`card ${getStatusColor(task.status)} border-l-4`}
    >
      <div className="flex items-start gap-4">
        <div className="flex-shrink-0 mt-1">
          {getStatusIcon(task.status)}
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2 mb-2">
            <div>
              <h4 className="text-sm font-semibold text-white">
                {task.workflow_type || task.task_type || 'Task'}
              </h4>
              {task.agent && (
                <p className="text-xs text-gray-400 mt-1">
                  Agent: {task.agent}
                </p>
              )}
            </div>
            <span className="text-xs text-gray-500 whitespace-nowrap">
              {timeAgo}
            </span>
          </div>
          
          {task.result && typeof task.result === 'object' && (
            <div className="mt-3">
              {/* Enhanced workflow results display */}
              {task.workflow_type && (
                <WorkflowResults result={task} />
              )}
              
              {/* Fallback JSON preview for non-workflow results */}
              {!task.workflow_type && (
                <div className="p-3 bg-charcoal rounded-lg">
                  <div className="flex items-center gap-2 text-xs text-gray-400 mb-2">
                    <ArrowRight className="w-3 h-3" />
                    <span>Result Preview</span>
                  </div>
                  <pre className="text-xs text-gray-300 overflow-x-auto scrollbar-hide">
                    {JSON.stringify(task.result, null, 2).slice(0, 200)}
                    {JSON.stringify(task.result, null, 2).length > 200 && '...'}
                  </pre>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default TaskCard;

