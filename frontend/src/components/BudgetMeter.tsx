/**
 * Budget Meter - Shows Nemotron API budget status
 */
import { useState, useEffect } from 'react';
import { DollarSign } from 'lucide-react';
import apiClient from '@/utils/apiClient';

export const BudgetMeter: React.FC = () => {
  const [budget, setBudget] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBudget = async () => {
      try {
        const response = await apiClient.getBudgetStatus();
        setBudget(response.budget);
      } catch (error) {
        console.error('Error fetching budget:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchBudget();
    const interval = setInterval(fetchBudget, 10000); // Update every 10 seconds
    return () => clearInterval(interval);
  }, []);

  if (loading || !budget) {
    return (
      <div className="card p-4">
        <div className="flex items-center gap-2 text-gray-400">
          <DollarSign className="w-4 h-4" />
          <span className="text-sm">Loading budget...</span>
        </div>
      </div>
    );
  }

  const percentage = budget.percentage_used || 0;
  const statusColor = 
    percentage >= 90 ? 'text-red-400' :
    percentage >= 75 ? 'text-yellow-400' :
    percentage >= 50 ? 'text-blue-400' :
    'text-green-400';

  const bgColor = 
    percentage >= 90 ? 'bg-red-500/20' :
    percentage >= 75 ? 'bg-yellow-500/20' :
    percentage >= 50 ? 'bg-blue-500/20' :
    'bg-green-500/20';

  return (
    <div className="card p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <DollarSign className="w-4 h-4 text-neon-cyan" />
          <span className="text-sm font-medium text-gray-300">API Budget</span>
        </div>
        <span className={`text-sm font-semibold ${statusColor}`}>
          {budget.budget_status?.toUpperCase() || 'HEALTHY'}
        </span>
      </div>
      
      <div className="mb-2">
        <div className="flex justify-between text-xs text-gray-400 mb-1">
          <span>Used: ${budget.used_budget?.toFixed(2) || '0.00'}</span>
          <span>Remaining: ${budget.remaining_budget?.toFixed(2) || '40.00'}</span>
        </div>
        <div className="w-full bg-dark-lighter rounded-full h-2 overflow-hidden">
          <div
            className={`h-full ${bgColor} transition-all duration-300`}
            style={{ width: `${Math.min(100, percentage)}%` }}
          />
        </div>
      </div>

      {budget.recommendations && budget.recommendations.length > 0 && (
        <div className="mt-2 text-xs text-gray-400">
          {budget.recommendations[0]}
        </div>
      )}
    </div>
  );
};

export default BudgetMeter;

