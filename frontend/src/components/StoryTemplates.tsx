/**
 * Story Templates Component
 * 
 * Demonstrates ProdigyPM's compatibility with PNC workshop format
 * Shows how our 9-agent system produces superior results
 */
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FileText, Download, Sparkles, CheckCircle, ExternalLink } from 'lucide-react';

interface Template {
  name: string;
  title: string;
  priority: string;
  estimate: string;
  tags: string[];
  epic: string;
}

export const StoryTemplates: React.FC = () => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<any>(null);
  const [pncDemoStories, setPncDemoStories] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadTemplates();
    loadPNCDemo();
  }, []);

  const loadTemplates = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/templates/list');
      const data = await response.json();
      if (data.success) {
        setTemplates(data.templates || []);
      }
    } catch (error) {
      console.error('Error loading templates:', error);
    }
  };

  const loadPNCDemo = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/demo/pnc_stories');
      const data = await response.json();
      if (data.success) {
        setPncDemoStories(data.stories || []);
      }
    } catch (error) {
      console.error('Error loading PNC demo:', error);
    }
  };

  const viewTemplateDetails = async (templateName: string) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/v1/templates/${templateName}`);
      const data = await response.json();
      if (data.success) {
        setSelectedTemplate(data.template);
      }
    } catch (error) {
      console.error('Error loading template details:', error);
    } finally {
      setLoading(false);
    }
  };

  const exportStories = async (format: string) => {
    if (pncDemoStories.length === 0) return;
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/export/stories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          stories: pncDemoStories,
          format: format,
          title: "ProdigyPM AI-Generated User Stories (PNC Compatible)"
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Download the file
        const blob = new Blob([data.content], { type: data.media_type });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = data.filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('Error exporting stories:', error);
      alert('Export failed. Please try again.');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/30 rounded-lg p-6">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-blue-400" />
              PNC Workshop Compatible Story Templates
            </h3>
            <p className="text-sm text-gray-300">
              Demonstrating how our <span className="text-purple-400 font-semibold">9-Agent AI System</span> produces 
              superior results in the <span className="text-blue-400 font-semibold">PNC workshop format</span>
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => exportStories('csv')}
              className="btn btn-sm bg-green-600 hover:bg-green-700 text-white"
              disabled={pncDemoStories.length === 0}
            >
              <Download className="w-4 h-4 mr-1" />
              CSV
            </button>
            <button
              onClick={() => exportStories('markdown')}
              className="btn btn-sm bg-blue-600 hover:bg-blue-700 text-white"
              disabled={pncDemoStories.length === 0}
            >
              <Download className="w-4 h-4 mr-1" />
              Markdown
            </button>
            <button
              onClick={() => exportStories('jira_csv')}
              className="btn btn-sm bg-purple-600 hover:bg-purple-700 text-white"
              disabled={pncDemoStories.length === 0}
            >
              <Download className="w-4 h-4 mr-1" />
              Jira CSV
            </button>
          </div>
        </div>
      </div>

      {/* Templates Grid */}
      <div>
        <h4 className="text-lg font-semibold text-white mb-3">Available Templates</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {templates.map((template) => (
            <motion.div
              key={template.name}
              whileHover={{ scale: 1.02 }}
              className="bg-dark-lighter border border-dark-border rounded-lg p-4 cursor-pointer"
              onClick={() => viewTemplateDetails(template.name)}
            >
              <h5 className="text-white font-medium mb-2 flex items-center gap-2">
                <FileText className="w-4 h-4 text-blue-400" />
                {template.name.replace('_', ' ').toUpperCase()}
              </h5>
              <p className="text-xs text-gray-400 mb-2 line-clamp-2">{template.title}</p>
              <div className="flex flex-wrap gap-1 mb-2">
                {template.tags.slice(0, 3).map((tag, idx) => (
                  <span key={idx} className="text-xs bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded">
                    {tag}
                  </span>
                ))}
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className={`px-2 py-0.5 rounded ${
                  template.priority === 'High' ? 'bg-red-500/20 text-red-400' :
                  template.priority === 'Medium' ? 'bg-yellow-500/20 text-yellow-400' :
                  'bg-green-500/20 text-green-400'
                }`}>
                  {template.priority}
                </span>
                <span className="text-gray-400">{template.estimate}</span>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* PNC Demo Stories */}
      {pncDemoStories.length > 0 && (
        <div>
          <h4 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
            <CheckCircle className="w-5 h-5 text-green-400" />
            AI-Generated Stories (PNC Format)
          </h4>
          <div className="space-y-3">
            {pncDemoStories.map((story, idx) => (
              <div
                key={idx}
                className="bg-dark-lighter border border-dark-border rounded-lg p-4"
              >
                <div className="flex items-start justify-between mb-2">
                  <h5 className="text-white font-medium flex-1">{story.title}</h5>
                  <span className={`text-xs px-2 py-1 rounded ${
                    story.priority === 'High' ? 'bg-red-500/20 text-red-400' :
                    story.priority === 'Medium' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-green-500/20 text-green-400'
                  }`}>
                    {story.priority}
                  </span>
                </div>
                
                <p className="text-sm text-gray-400 mb-3">{story.description}</p>
                
                {story.acceptance_criteria && story.acceptance_criteria.length > 0 && (
                  <div className="mb-3">
                    <p className="text-xs font-semibold text-gray-300 mb-1">Acceptance Criteria:</p>
                    <ul className="text-xs text-gray-400 space-y-1">
                      {story.acceptance_criteria.map((criterion: string, i: number) => (
                        <li key={i} className="flex items-start gap-2">
                          <CheckCircle className="w-3 h-3 text-green-400 mt-0.5 flex-shrink-0" />
                          <span>{criterion}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                
                <div className="flex items-center justify-between text-xs">
                  <div className="flex gap-2">
                    {story.tags?.map((tag: string, i: number) => (
                      <span key={i} className="bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded">
                        {tag}
                      </span>
                    ))}
                  </div>
                  <span className="text-gray-400">Epic: {story.epic}</span>
                </div>
                
                {story.ai_enhanced && (
                  <div className="mt-3 pt-3 border-t border-dark-border">
                    <p className="text-xs text-purple-300 mb-1 flex items-center gap-1">
                      <Sparkles className="w-3 h-3" />
                      AI Enhancement: {story.generated_by}
                    </p>
                    <ul className="text-xs text-gray-400 space-y-0.5">
                      {story.advantages?.map((adv: string, i: number) => (
                        <li key={i}>• {adv}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Template Details Modal */}
      {selectedTemplate && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div
            className="absolute inset-0 bg-black/80 backdrop-blur-sm"
            onClick={() => setSelectedTemplate(null)}
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="relative bg-dark-card border-2 border-dark-border rounded-xl p-6 max-w-2xl w-full max-h-[80vh] overflow-auto"
          >
            <h3 className="text-xl font-bold text-white mb-4">{selectedTemplate.title}</h3>
            
            <div className="space-y-4">
              <div>
                <p className="text-xs text-gray-400 mb-1">Description:</p>
                <p className="text-sm text-gray-300">{selectedTemplate.description}</p>
              </div>
              
              {selectedTemplate.acceptance_criteria && (
                <div>
                  <p className="text-xs text-gray-400 mb-1">Acceptance Criteria:</p>
                  <ul className="text-sm text-gray-300 space-y-1">
                    {selectedTemplate.acceptance_criteria.map((criterion: string, i: number) => (
                      <li key={i} className="flex items-start gap-2">
                        <CheckCircle className="w-4 h-4 text-green-400 mt-0.5" />
                        {criterion}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-xs text-gray-400">Priority:</p>
                  <p className="text-sm text-white">{selectedTemplate.priority}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-400">Estimate:</p>
                  <p className="text-sm text-white">{selectedTemplate.estimate}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-400">Epic:</p>
                  <p className="text-sm text-white">{selectedTemplate.epic}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-400">Status:</p>
                  <p className="text-sm text-white">{selectedTemplate.status}</p>
                </div>
              </div>
              
              {selectedTemplate.tags && selectedTemplate.tags.length > 0 && (
                <div>
                  <p className="text-xs text-gray-400 mb-2">Tags:</p>
                  <div className="flex flex-wrap gap-2">
                    {selectedTemplate.tags.map((tag: string, i: number) => (
                      <span key={i} className="text-xs bg-blue-500/20 text-blue-300 px-2 py-1 rounded">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            <button
              onClick={() => setSelectedTemplate(null)}
              className="mt-6 w-full btn btn-primary"
            >
              Close
            </button>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default StoryTemplates;

