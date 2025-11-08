/**
 * AgentPanel - Displays individual agent status and information
 */
import { motion } from 'framer-motion';
import { Bot, CheckCircle, Clock, AlertCircle, Loader2 } from 'lucide-react';
import { AgentStatus } from '@/hooks/useAgents';

interface AgentPanelProps {
  agent: AgentStatus;
  agentKey: string;
  onClick?: () => void;
}

const statusConfig = {
  idle: {
    icon: Bot,
    color: 'text-gray-400',
    bgColor: 'bg-gray-500/10',
    borderColor: 'border-gray-400/30',
  },
  running: {
    icon: Loader2,
    color: 'text-neon-cyan',
    bgColor: 'bg-neon-cyan/10',
    borderColor: 'border-neon-cyan',
    animate: 'animate-spin',
  },
  completed: {
    icon: CheckCircle,
    color: 'text-green-400',
    bgColor: 'bg-green-500/10',
    borderColor: 'border-green-400/30',
  },
  failed: {
    icon: AlertCircle,
    color: 'text-red-400',
    bgColor: 'bg-red-500/10',
    borderColor: 'border-red-400/30',
  },
  pending: {
    icon: Clock,
    color: 'text-yellow-400',
    bgColor: 'bg-yellow-500/10',
    borderColor: 'border-yellow-400/30',
  },
};

export const AgentPanel: React.FC<AgentPanelProps> = ({ agent, agentKey, onClick }) => {
  const config = statusConfig[agent.status as keyof typeof statusConfig] || statusConfig.idle;
  const StatusIcon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
      transition={{ duration: 0.2 }}
      className={`card card-hover cursor-pointer ${config.borderColor} border-2`}
      onClick={onClick}
    >
      <div className="flex items-start gap-4">
        <div className={`${config.bgColor} ${config.borderColor} border rounded-full p-3`}>
          <StatusIcon className={`w-6 h-6 ${config.color} ${config.animate || ''}`} />
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-1">
            <h3 className="text-lg font-semibold text-white truncate">
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
          
          <p className="text-sm text-gray-400 mb-3">
            {agent.goal}
          </p>
          
          {agent.status === 'running' && (
            <motion.div
              className="h-1 bg-gray-300 rounded-full overflow-hidden"
              initial={{ width: 0 }}
            >
              <motion.div
                className="h-full bg-gradient-to-r from-neon-cyan to-neon-orange"
                animate={{
                  x: ['0%', '100%'],
                }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  ease: 'linear',
                }}
                style={{ width: '50%' }}
              />
            </motion.div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default AgentPanel;

