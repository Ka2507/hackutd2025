/**
 * AgentPanel - Displays individual agent status with modern design
 */
import { motion } from 'framer-motion';
import { CheckCircle, Clock, AlertCircle, Loader2, Activity, Brain } from 'lucide-react';
import { AgentStatus } from '@/hooks/useAgents';

interface AgentPanelProps {
  agent: AgentStatus;
  agentKey?: string;
  onClick?: () => void;
}

const statusConfig = {
  idle: {
    icon: Activity,
    color: 'text-gray-400',
    bgColor: 'bg-gray-500/10',
    borderColor: 'border-gray-500/20',
  },
  thinking: {
    icon: Brain,
    color: 'text-yellow-400',
    bgColor: 'bg-yellow-500/10',
    borderColor: 'border-yellow-500/40',
    animate: 'animate-pulse',
  },
  running: {
    icon: Loader2,
    color: 'text-nvidia-green',
    bgColor: 'bg-nvidia-green/10',
    borderColor: 'border-nvidia-green/40',
    animate: 'animate-spin',
  },
  completed: {
    icon: CheckCircle,
    color: 'text-nvidia-green-light',
    bgColor: 'bg-nvidia-green/10',
    borderColor: 'border-nvidia-green/30',
  },
  failed: {
    icon: AlertCircle,
    color: 'text-red-400',
    bgColor: 'bg-red-500/10',
    borderColor: 'border-red-500/30',
  },
  pending: {
    icon: Clock,
    color: 'text-pnc-orange',
    bgColor: 'bg-pnc-orange/10',
    borderColor: 'border-pnc-orange/30',
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
        <div className="absolute inset-0 bg-gradient-to-br from-nvidia-green/5 to-transparent pointer-events-none" />
      )}
      
      <div className="relative flex items-start gap-4">
        {/* Icon */}
        <div className={`${config.bgColor} ${config.borderColor} border rounded-lg p-2.5 flex-shrink-0`}>
          <StatusIcon className={`w-5 h-5 ${config.color} ${'animate' in config ? config.animate : ''}`} />
        </div>
        
        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-base font-display font-semibold text-gray-100 truncate">
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
          
          <p className="text-xs text-gray-400 leading-relaxed mb-3">
            {agent.goal}
          </p>
          
          {/* Thinking/Reasoning display */}
          {(agent.status === 'thinking' || agent.status === 'running') && agent.reasoning && (
            <div className="mt-2 p-2 bg-dark-lighter rounded text-xs">
              <div className="text-yellow-400 font-medium mb-1 flex items-center gap-1">
                <Brain className="w-3 h-3" />
                Thinking...
              </div>
              <div className="space-y-1 text-gray-400">
                {agent.reasoning.slice(0, 2).map((step: string, i: number) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.3 }}
                    className="flex items-start gap-1"
                  >
                    <span className="text-neon-cyan">•</span>
                    <span>{step}</span>
                  </motion.div>
                ))}
              </div>
            </div>
          )}
          
          {/* Progress bar for running status */}
          {agent.status === 'running' && (
            <div className="relative h-1 bg-dark-border rounded-full overflow-hidden mt-2">
              <motion.div
                className="absolute inset-y-0 left-0 bg-gradient-to-r from-nvidia-green to-nvidia-green-light rounded-full"
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
