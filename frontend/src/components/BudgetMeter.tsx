/**
 * Budget Meter - Shows Nemotron API budget status with editing capability
 */
import { useState, useEffect } from 'react';
import { DollarSign, Edit2, Check, X } from 'lucide-react';
import apiClient from '../utils/apiClient';

export const BudgetMeter: React.FC = () => {
  const [budget, setBudget] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState('');

  useEffect(() => {
    fetchBudget();
    const interval = setInterval(fetchBudget, 10000); // Update every 10 seconds
    return () => clearInterval(interval);
  }, []);

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

  const formatBudgetValue = (value: number): string => {
    if (value >= 1_000_000_000) {
      return `${(value / 1_000_000_000).toFixed(1)} billion USD`;
    } else if (value >= 1_000_000) {
      return `${(value / 1_000_000).toFixed(1)} million USD`;
    } else if (value >= 100_000) {
      return `${(value / 1_000).toFixed(0)}K USD`;
    } else if (value >= 1_000) {
      return `${(value / 1_000).toFixed(1)}K USD`;
    }
    return `${value.toFixed(2)} USD`;
  };

  const handleStartEdit = () => {
    setEditValue(budget?.total_budget?.toString() || '40');
    setIsEditing(true);
  };

  const handleSaveEdit = async () => {
    try {
      const newBudget = parseFloat(editValue);
      if (isNaN(newBudget) || newBudget <= 0) {
        alert('Please enter a valid positive number');
        return;
      }
      
      await apiClient.updateBudget(newBudget);
      await fetchBudget();
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating budget:', error);
      alert('Failed to update budget');
    }
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditValue('');
  };

  const getBudgetStatus = (percentage: number): string => {
    if (percentage >= 95) return 'CRITICAL';
    if (percentage >= 85) return 'DANGER';
    if (percentage >= 75) return 'WARNING';
    if (percentage >= 50) return 'MODERATE';
    return 'HEALTHY';
  };

  const getStatusColor = (percentage: number): string => {
    if (percentage >= 95) return 'text-red-500';
    if (percentage >= 85) return 'text-red-400';
    if (percentage >= 75) return 'text-yellow-400';
    if (percentage >= 50) return 'text-yellow-400';
    return 'text-green-400';
  };

  const getBgColor = (percentage: number): string => {
    if (percentage >= 95) return 'bg-red-500/30';
    if (percentage >= 85) return 'bg-red-500/20';
    if (percentage >= 75) return 'bg-yellow-500/20';
    if (percentage >= 50) return 'bg-yellow-500/20';
    return 'bg-green-500';
  };

  if (loading || !budget) {
    return (
      <div className="card p-4">
        <div className="flex items-center gap-2 text-silver/70">
          <DollarSign className="w-4 h-4" />
          <span className="text-sm">Loading budget...</span>
        </div>
      </div>
    );
  }

  const percentage = budget.percentage_used || 0;
  const statusColor = getStatusColor(percentage);
  const bgColor = getBgColor(percentage);
  const statusLabel = getBudgetStatus(percentage);

  return (
    <div className="card p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <DollarSign className="w-4 h-4 text-white" />
          <span className="text-sm font-medium text-silver">Budget</span>
        </div>
        {!isEditing ? (
          <div className="flex items-center gap-2">
            <span className={`text-sm font-semibold ${statusColor}`}>
              {statusLabel}
            </span>
            <button
              onClick={handleStartEdit}
              className="p-1.5 hover:bg-dark-lighter rounded transition-colors"
              title="Edit budget"
            >
              <Edit2 className="w-3.5 h-3.5 text-silver/70 hover:text-white" />
            </button>
          </div>
        ) : (
          <div className="flex items-center gap-1">
            <button
              onClick={handleSaveEdit}
              className="p-1.5 hover:bg-dark-lighter rounded transition-colors"
              title="Save"
            >
              <Check className="w-4 h-4 text-white" />
            </button>
            <button
              onClick={handleCancelEdit}
              className="p-1.5 hover:bg-dark-lighter rounded transition-colors"
              title="Cancel"
            >
              <X className="w-4 h-4 text-red-400" />
            </button>
          </div>
        )}
      </div>
      
      {isEditing ? (
        <div className="mb-3">
          <input
            type="number"
            value={editValue}
            onChange={(e) => setEditValue(e.target.value)}
            className="w-full px-3 py-2 bg-dark-lighter border border-dark-border rounded text-silver text-sm focus:border-white focus:outline-none"
            placeholder="Enter budget amount"
            autoFocus
          />
          <p className="text-xs text-silver/50 mt-1">
            Enter budget in dollars (e.g., 40, 1000000, 6000000000)
          </p>
        </div>
      ) : (
        <div className="mb-2">
          <div className="flex justify-between text-xs text-silver/70 mb-1">
            <span>Used: {formatBudgetValue(budget.used_budget || 0)}</span>
            <span>Remaining: {formatBudgetValue(budget.remaining_budget || budget.total_budget)}</span>
          </div>
          <div className="mb-1">
            <div className="text-xs text-silver/50">
              Total: {formatBudgetValue(budget.total_budget || 40)}
            </div>
          </div>
          <div className="w-full bg-dark-lighter rounded-full h-2 overflow-hidden">
            <div
              className={`h-full ${bgColor} transition-all duration-300`}
              style={{ width: `${Math.min(100, percentage)}%` }}
            />
          </div>
        </div>
      )}

      {!isEditing && budget.recommendations && budget.recommendations.length > 0 && (
        <div className="mt-2 text-xs text-silver/70">
          {budget.recommendations[0]}
        </div>
      )}
    </div>
  );
};

export default BudgetMeter;
