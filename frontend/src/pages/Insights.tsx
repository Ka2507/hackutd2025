/**
 * Insights Page - Analytics and reporting page
 */
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import ReportView from '@/components/ReportView';

export const Insights: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-charcoal p-6">
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={() => navigate('/dashboard')}
          className="btn btn-ghost mb-4 px-3"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Dashboard
        </button>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-4xl font-display font-bold gradient-text mb-2">
            Insights & Analytics
          </h1>
          <p className="text-gray-400">
            Track your AI agent performance and productivity gains
          </p>
        </motion.div>
      </div>

      {/* Report Content */}
      <ReportView />
    </div>
  );
};

export default Insights;

