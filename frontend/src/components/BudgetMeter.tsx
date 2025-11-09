/**
 * Budget Meter - Shows Nemotron API budget status
 */
import { useState, useEffect } from 'react';
import { DollarSign, Settings, X } from 'lucide-react';
import apiClient from '@/utils/apiClient';

/**
 * Format large currency values in a readable format
 * Dynamically handles any number size: Million, Billion, Trillion, Quadrillion, Quintillion, etc.
 * Examples: 
 * - 1100000 -> "$1.1 Million"
 * - 50000 -> "$50 Thousand"
 * - 2500000000 -> "$2.5 Billion"
 * - 5000000000000 -> "$5 Trillion"
 * - 1000000000000000 -> "$1 Quadrillion"
 */
const formatCurrency = (value: number): string => {
  if (value === 0) return '$0.00';
  
  const absValue = Math.abs(value);
  const sign = value < 0 ? '-' : '';
  
  // For values less than 1000, show with 2 decimal places
  if (absValue < 1000) {
    return `${sign}$${value.toFixed(2)}`;
  }
  
  // Calculate which power of 1000 we're dealing with
  // log10(absValue) / 3 gives us the power (e.g., 6 -> Million, 9 -> Billion)
  const power = Math.floor(Math.log10(absValue) / 3);
  
  // Unit names for powers of 1000
  const unitNames = [
    '',           // 10^0 (not used, we handle < 1000 separately)
    'Thousand',   // 10^3
    'Million',    // 10^6
    'Billion',    // 10^9
    'Trillion',   // 10^12
    'Quadrillion', // 10^15
    'Quintillion', // 10^18
    'Sextillion',  // 10^21
    'Septillion',  // 10^24
    'Octillion',   // 10^27
    'Nonillion',   // 10^30
    'Decillion',   // 10^33
    'Undecillion', // 10^36
    'Duodecillion', // 10^39
    'Tredecillion', // 10^42
    'Quattuordecillion', // 10^45
    'Quindecillion', // 10^48
    'Sexdecillion', // 10^51
    'Septendecillion', // 10^54
    'Octodecillion', // 10^57
    'Novemdecillion', // 10^60
    'Vigintillion', // 10^63
  ];
  
  // Get unit name - dynamically handles any power
  let unitName: string;
  if (power < unitNames.length && unitNames[power]) {
    unitName = unitNames[power];
  } else {
    // For numbers beyond our predefined list, generate the name systematically
    // Using the standard naming convention for large numbers
    const generateUnitName = (p: number): string => {
      // Standard prefixes for powers of 1000
      const prefixes = [
        '', 'un', 'duo', 'tre', 'quattuor', 'quin', 'sex', 'septen', 'octo', 'novem',
        'dec', 'undec', 'duodec', 'tredec', 'quattuordec', 'quindec', 'sexdec',
        'septendec', 'octodec', 'novemdec', 'vigint', 'unvigint', 'duovigint',
        'trevigint', 'quattuorvigint', 'quinvigint', 'sexvigint', 'septenvigint',
        'octovigint', 'novemvigint', 'trigint'
      ];
      
      if (p <= 30) {
        return prefixes[p] + 'illion';
      } else {
        // For extremely large numbers beyond standard naming, use scientific notation
        return `10^${p * 3}`;
      }
    };
    
    unitName = generateUnitName(power);
    // Capitalize first letter
    unitName = unitName.charAt(0).toUpperCase() + unitName.slice(1);
  }
  
  // Calculate the divisor (1000^power)
  const divisor = Math.pow(1000, power);
  const converted = absValue / divisor;
  
  // Show 1 decimal place if needed, otherwise show whole number
  const formatted = converted % 1 === 0 
    ? converted.toFixed(0) 
    : converted.toFixed(1);
  
  return `${sign}$${formatted} ${unitName}`;
};

export const BudgetMeter: React.FC = () => {
  const [budget, setBudget] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [newBudget, setNewBudget] = useState<string>('');
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    const fetchBudget = async () => {
      try {
        const response = await apiClient.getBudgetStatus();
        if (response.budget) {
          setBudget(response.budget);
          setError(false);
        } else {
          setError(true);
        }
      } catch (error) {
        console.error('Error fetching budget:', error);
        setError(true);
      } finally {
        setLoading(false);
      }
    };

    fetchBudget();
    const interval = setInterval(fetchBudget, 10000); // Update every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const handleUpdateBudget = async () => {
    const budgetValue = parseFloat(newBudget);
    if (isNaN(budgetValue) || budgetValue < 0) {
      alert('Please enter a valid positive number');
      return;
    }

    setUpdating(true);
    try {
      const response = await apiClient.updateBudget(budgetValue);
      if (response.budget) {
        setBudget(response.budget);
        setShowSettings(false);
        setNewBudget('');
      }
    } catch (error: any) {
      console.error('Error updating budget:', error);
      alert(error.response?.data?.detail || 'Failed to update budget');
    } finally {
      setUpdating(false);
    }
  };

  // Show loading only while actually loading
  if (loading) {
    return (
      <div className="card p-4">
        <div className="flex items-center gap-2 text-gray-400">
          <DollarSign className="w-4 h-4" />
          <span className="text-sm">Loading budget...</span>
        </div>
      </div>
    );
  }

  // Show fallback/default budget if API failed or no budget data
  if (error || !budget) {
    return (
      <div className="card p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <DollarSign className="w-4 h-4 text-neon-cyan" />
            <span className="text-sm font-medium text-gray-300">Budget</span>
          </div>
          <span className="text-sm font-semibold text-green-400">HEALTHY</span>
        </div>
        
        <div className="mb-2">
          <div className="flex justify-between text-xs text-gray-400 mb-1">
            <span>Used: {formatCurrency(0)}</span>
            <span>Remaining: {formatCurrency(40)}</span>
          </div>
          <div className="w-full bg-dark-lighter rounded-full h-2 overflow-hidden">
            <div
              className="h-full bg-green-500/20 transition-all duration-300"
              style={{ width: '0%' }}
            />
          </div>
        </div>

        <div className="mt-2 text-xs text-gray-400">
          Budget tracking unavailable - using default values
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
    <>
      <div className="card p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <DollarSign className="w-4 h-4 text-neon-cyan" />
            <span className="text-sm font-medium text-gray-300">Budget</span>
            <button
              onClick={() => {
                setShowSettings(true);
                setNewBudget(budget.total_budget?.toString() || '40');
              }}
              className="ml-2 p-1 hover:bg-dark-lighter rounded transition-colors"
              title="Configure budget"
            >
              <Settings className="w-3.5 h-3.5 text-gray-400 hover:text-neon-cyan" />
            </button>
          </div>
          <span className={`text-sm font-semibold ${statusColor}`}>
            {budget.budget_status?.toUpperCase() || 'HEALTHY'}
          </span>
        </div>
      
      <div className="mb-2">
        <div className="flex justify-between text-xs text-gray-400 mb-1">
          <span>Used: {formatCurrency(budget.used_budget || 0)}</span>
          <span>Remaining: {formatCurrency(budget.remaining_budget || 40)}</span>
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

      {/* Budget Settings Modal */}
      {showSettings && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="card p-6 max-w-md w-full mx-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">Configure Budget</h3>
              <button
                onClick={() => {
                  setShowSettings(false);
                  setNewBudget('');
                }}
                className="p-1 hover:bg-dark-lighter rounded transition-colors"
              >
                <X className="w-5 h-5 text-gray-400" />
              </button>
            </div>

            <div className="mb-4">
              <label className="block text-sm text-gray-400 mb-2">
                Total Budget ($)
              </label>
              <input
                type="number"
                min="0"
                step="0.01"
                value={newBudget}
                onChange={(e) => setNewBudget(e.target.value)}
                className="w-full input"
                placeholder="Enter budget amount"
              />
              <p className="text-xs text-gray-500 mt-1">
                Current: {formatCurrency(budget.total_budget || 40)} | Used: {formatCurrency(budget.used_budget || 0)}
              </p>
            </div>

            <div className="flex gap-3">
              <button
                onClick={handleUpdateBudget}
                disabled={updating || !newBudget}
                className="btn btn-primary flex-1 disabled:opacity-50"
              >
                {updating ? 'Updating...' : 'Update Budget'}
              </button>
              <button
                onClick={() => {
                  setShowSettings(false);
                  setNewBudget('');
                }}
                className="btn btn-ghost"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default BudgetMeter;

