/**
 * AgentPanel - Displays individual agent status with modern design
 */
import { motion } from 'framer-motion';
import { CheckCircle, Clock, AlertCircle, Loader2, Activity } from 'lucide-react';
import { AgentStatus } from '@/hooks/useAgents';

interface AgentPanelProps {
  agent: AgentStatus;
  agentKey?: string;
  onClick?: () => void;
}

const statusConfig = {
  idle: {
    icon: Activity,
    color: 'text-silver/70',
    bgColor: 'bg-silver/10',
    borderColor: 'border-silver/20',
  },
  running: {
    icon: Loader2,
    color: 'text-white',
    bgColor: 'bg-white/10',
    borderColor: 'border-white/40',
    animate: 'animate-spin',
  },
  completed: {
    icon: CheckCircle,
    color: 'text-white',
    bgColor: 'bg-white/10',
    borderColor: 'border-white/30',
  },
  failed: {
    icon: AlertCircle,
    color: 'text-red-400',
    bgColor: 'bg-red-500/10',
    borderColor: 'border-red-500/30',
  },
  pending: {
    icon: Clock,
    color: 'text-silver',
    bgColor: 'bg-silver/10',
    borderColor: 'border-silver/30',
  },
};

export const AgentPanel: React.FC<AgentPanelProps> = ({ agent, onClick }) => {
  const config = statusConfig[agent.status as keyof typeof statusConfig] || statusConfig.idle;
  const StatusIcon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02, y: -4 }}
      transition={{ duration: 0.2 }}
      className={`card card-hover cursor-pointer ${config.borderColor} border relative overflow-hidden`}
      onClick={onClick}
    >
      {/* Subtle gradient overlay */}
      {agent.status === 'running' && (
        <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent pointer-events-none" />
      )}
      
      <div className="relative flex items-start gap-4">
        {/* Icon */}
        <div className={`${config.bgColor} ${config.borderColor} border rounded-lg p-2.5 flex-shrink-0`}>
          <StatusIcon className={`w-5 h-5 ${config.color} ${'animate' in config ? config.animate : ''}`} />
        </div>
        
        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-base font-display font-semibold text-silver truncate">
              {agent.name}
            </h3>
            <span className={`badge ${
              agent.status === 'completed' ? 'badge-success' :
              agent.status === 'running' ? 'badge-info' :
              agent.status === 'failed' ? 'badge-error' :
              'badge-warning'
            }`}>
              {agent.status}
            </span>
          </div>
          
          <p className="text-xs text-silver/70 leading-relaxed mb-3">
            {agent.goal}
          </p>
          
          {/* Progress bar for running status */}
          {agent.status === 'running' && (
            <div className="relative h-1 bg-dark-border rounded-full overflow-hidden">
              <motion.div
                className="absolute inset-y-0 left-0 bg-gradient-to-r from-white to-silver rounded-full"
                initial={{ width: '0%' }}
                animate={{ width: ['0%', '100%'] }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: 'easeInOut',
                }}
              />
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default AgentPanel;
