/**
 * WorkflowTemplates - Display and select workflow templates
 */
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Layers, Sparkles, TrendingUp } from 'lucide-react';
import apiClient from '@/utils/apiClient';

interface WorkflowTemplatesProps {
  onSelectTemplate: (templateName: string) => void;
}

export const WorkflowTemplates: React.FC<WorkflowTemplatesProps> = ({ onSelectTemplate }) => {
  const [templates, setTemplates] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        const response = await apiClient.listWorkflowTemplates();
        if (response.success) {
          setTemplates(response.templates || []);
        }
      } catch (error) {
        console.error('Error fetching templates:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTemplates();
  }, []);

  if (loading) {
    return (
      <div className="card p-4">
        <div className="flex items-center gap-2 text-gray-400">
          <Layers className="w-4 h-4 animate-spin" />
          <span className="text-sm">Loading templates...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="card p-4">
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-5 h-5 text-neon-cyan" />
        <h3 className="text-sm font-semibold text-white">Workflow Templates</h3>
      </div>
      
      <div className="space-y-2">
        {templates.map((template, index) => (
          <motion.button
            key={template.name}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            onClick={() => onSelectTemplate(template.name)}
            className="w-full text-left p-3 bg-dark-lighter hover:bg-dark-border rounded-lg transition-colors group"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="text-sm font-medium text-white group-hover:text-neon-cyan transition-colors">
                    {template.display_name || template.name}
                  </h4>
                  {template.type === 'prebuilt' && (
                    <span className="text-xs px-2 py-0.5 bg-nvidia-green/20 text-nvidia-green rounded">
                      Pre-built
                    </span>
                  )}
                </div>
                <p className="text-xs text-gray-400">{template.description}</p>
                <div className="flex items-center gap-3 mt-2">
                  <span className="text-xs text-gray-500">
                    {template.agents?.length || 0} agents
                  </span>
                  {template.usage_count > 0 && (
                    <span className="text-xs text-gray-500">
                      <TrendingUp className="w-3 h-3 inline mr-1" />
                      Used {template.usage_count} times
                    </span>
                  )}
                </div>
              </div>
            </div>
          </motion.button>
        ))}
      </div>
    </div>
  );
};

export default WorkflowTemplates;



