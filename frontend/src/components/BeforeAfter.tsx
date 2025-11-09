/**
 * Before/After Comparison - Shows time saved and quality improvements
 */
import { motion } from 'framer-motion';
import { Clock, TrendingUp, CheckCircle2, Zap } from 'lucide-react';

interface BeforeAfterProps {
  timeSaved?: number; // in hours
  qualityImprovement?: number; // percentage
  itemsGenerated?: number;
  traditionalCount?: number;
  automatedCount?: number;
}

export const BeforeAfter: React.FC<BeforeAfterProps> = ({
  timeSaved = 8.5,
  qualityImprovement = 35,
  itemsGenerated = 23,
  traditionalCount = 8,
  automatedCount = 23,
}) => {
  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
        <TrendingUp className="w-5 h-5 text-neon-cyan" />
        Impact Comparison
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Before - Traditional */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="space-y-4"
        >
          <div className="flex items-center gap-2 mb-3">
            <div className="w-2 h-2 rounded-full bg-red-400" />
            <h4 className="text-sm font-semibold text-gray-300">Traditional PM Workflow</h4>
          </div>
          
          <div className="space-y-3">
            <div className="flex items-center gap-3 p-3 bg-dark-lighter rounded">
              <Clock className="w-5 h-5 text-gray-400" />
              <div>
                <div className="text-xs text-gray-400">Time Required</div>
                <div className="text-lg font-bold text-white">{timeSaved + 2} hours</div>
              </div>
            </div>
            
            <div className="flex items-center gap-3 p-3 bg-dark-lighter rounded">
              <CheckCircle2 className="w-5 h-5 text-gray-400" />
              <div>
                <div className="text-xs text-gray-400">User Stories Generated</div>
                <div className="text-lg font-bold text-white">{traditionalCount} stories</div>
              </div>
            </div>
            
            <div className="flex items-center gap-3 p-3 bg-dark-lighter rounded">
              <TrendingUp className="w-5 h-5 text-gray-400" />
              <div>
                <div className="text-xs text-gray-400">Quality Score</div>
                <div className="text-lg font-bold text-white">65%</div>
              </div>
            </div>
          </div>
        </motion.div>
        
        {/* After - With ProdigyPM */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="space-y-4"
        >
          <div className="flex items-center gap-2 mb-3">
            <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            <h4 className="text-sm font-semibold text-gray-300">With ProdigyPM</h4>
          </div>
          
          <div className="space-y-3">
            <div className="flex items-center gap-3 p-3 bg-green-500/10 border border-green-500/30 rounded">
              <Zap className="w-5 h-5 text-green-400" />
              <div>
                <div className="text-xs text-gray-400">Time Required</div>
                <div className="text-lg font-bold text-green-400">2 hours</div>
              </div>
            </div>
            
            <div className="flex items-center gap-3 p-3 bg-green-500/10 border border-green-500/30 rounded">
              <CheckCircle2 className="w-5 h-5 text-green-400" />
              <div>
                <div className="text-xs text-gray-400">User Stories Generated</div>
                <div className="text-lg font-bold text-green-400">{automatedCount} stories</div>
              </div>
            </div>
            
            <div className="flex items-center gap-3 p-3 bg-green-500/10 border border-green-500/30 rounded">
              <TrendingUp className="w-5 h-5 text-green-400" />
              <div>
                <div className="text-xs text-gray-400">Quality Score</div>
                <div className="text-lg font-bold text-green-400">{65 + qualityImprovement}%</div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
      
      {/* Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="mt-6 p-4 bg-gradient-to-r from-nvidia-green/10 to-pnc-blue/10 border border-neon-cyan/30 rounded"
      >
        <div className="flex items-center justify-between">
          <div>
            <div className="text-xs text-gray-400 mb-1">Time Saved</div>
            <div className="text-2xl font-bold text-neon-cyan">{timeSaved} hours</div>
          </div>
          <div className="text-center">
            <div className="text-xs text-gray-400 mb-1">Quality Improvement</div>
            <div className="text-2xl font-bold text-neon-cyan">+{qualityImprovement}%</div>
          </div>
          <div className="text-right">
            <div className="text-xs text-gray-400 mb-1">More Stories</div>
            <div className="text-2xl font-bold text-neon-cyan">+{automatedCount - traditionalCount}</div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default BeforeAfter;

