/**
 * ReportView - Displays reports and metrics
 */
import { motion } from 'framer-motion';
import { TrendingUp, Clock, Zap, Target } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface ReportViewProps {
  data?: any;
}

export const ReportView: React.FC<ReportViewProps> = () => {
  // Mock data for charts
  const activityData = [
    { name: 'Mon', tasks: 12 },
    { name: 'Tue', tasks: 19 },
    { name: 'Wed', tasks: 15 },
    { name: 'Thu', tasks: 25 },
    { name: 'Fri', tasks: 22 },
    { name: 'Sat', tasks: 8 },
    { name: 'Sun', tasks: 5 },
  ];

  const metrics = [
    {
      label: 'Time Saved',
      value: '12.5h',
      change: '+15%',
      icon: Clock,
      color: 'text-white',
      bgColor: 'bg-white/10',
    },
    {
      label: 'Tasks Completed',
      value: '87',
      change: '+23%',
      icon: Target,
      color: 'text-white',
      bgColor: 'bg-white/10',
    },
    {
      label: 'AI Decisions',
      value: '145',
      change: '+18%',
      icon: Zap,
      color: 'text-silver',
      bgColor: 'bg-silver/10',
    },
    {
      label: 'Efficiency',
      value: '94%',
      change: '+5%',
      icon: TrendingUp,
      color: 'text-silver',
      bgColor: 'bg-silver/10',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((metric, index) => {
          const Icon = metric.icon;
          return (
            <motion.div
              key={metric.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="card card-hover"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-silver/70 mb-1">{metric.label}</p>
                  <h3 className="text-3xl font-bold text-silver mb-1">
                    {metric.value}
                  </h3>
                  <span className="text-sm text-white">{metric.change}</span>
                </div>
                <div className={`${metric.bgColor} p-3 rounded-lg`}>
                  <Icon className={`w-6 h-6 ${metric.color}`} />
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Activity Chart */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="card"
      >
        <h3 className="text-lg font-semibold mb-4">Agent Activity</h3>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={activityData}>
            <defs>
              <linearGradient id="colorTasks" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ffffff" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#ffffff" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1a1f24" />
            <XAxis dataKey="name" stroke="#707b81" />
            <YAxis stroke="#707b81" />
            <Tooltip
              contentStyle={{
                backgroundColor: '#0f1418',
                border: '1px solid #1a1f24',
                borderRadius: '8px',
                color: '#707b81',
              }}
            />
            <Area
              type="monotone"
              dataKey="tasks"
              stroke="#ffffff"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorTasks)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Agent Performance */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="card"
      >
        <h3 className="text-lg font-semibold mb-4">Agent Performance</h3>
        <div className="space-y-4">
          {[
            { name: 'StrategyAgent', usage: 85, color: 'bg-white' },
            { name: 'ResearchAgent', usage: 72, color: 'bg-silver' },
            { name: 'DevAgent', usage: 68, color: 'bg-white' },
            { name: 'GtmAgent', usage: 55, color: 'bg-silver' },
            { name: 'AutomationAgent', usage: 45, color: 'bg-white' },
          ].map((agent) => (
            <div key={agent.name}>
              <div className="flex justify-between mb-2">
                <span className="text-sm text-silver">{agent.name}</span>
                <span className="text-sm text-silver/70">{agent.usage}%</span>
              </div>
              <div className="h-2 bg-dark-border rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${agent.usage}%` }}
                  transition={{ duration: 1, ease: 'easeOut' }}
                  className={`h-full ${agent.color}`}
                />
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default ReportView;

