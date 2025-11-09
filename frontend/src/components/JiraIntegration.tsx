/**
 * Jira Integration Component
 * 
 * Comprehensive Jira integration UI for Product Management:
 * - Create user stories & epics
 * - View sprint status & backlog
 * - Bulk create from PRD
 * - Manage tickets
 */
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  X, 
  Plus, 
  Send, 
  Loader2, 
  CheckCircle, 
  ExternalLink,
  FileText,
  Target,
  TrendingUp,
  AlertCircle,
  List,
  Sparkles,
  Download
} from 'lucide-react';

interface JiraIntegrationProps {
  isOpen: boolean;
  onClose: () => void;
}

interface Story {
  jira_key?: string;
  jira_url?: string;
  summary: string;
  description: string;
  acceptance_criteria: string[];
  story_points: number;
  priority: string;
  labels: string[];
}

export const JiraIntegration: React.FC<JiraIntegrationProps> = ({ isOpen, onClose }) => {
  const [activeTab, setActiveTab] = useState<'create' | 'sprint' | 'prd' | 'templates'>('create');
  
  // Create Stories State
  const [projectKey, setProjectKey] = useState('PROD');
  const [featureDescription, setFeatureDescription] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const [createdStories, setCreatedStories] = useState<Story[]>([]);
  
  // Sprint State
  const [sprintId, setSprintId] = useState('');
  const [sprintData, setSprintData] = useState<any>(null);
  const [loadingSprint, setLoadingSprint] = useState(false);
  
  // PRD State
  const [prdContent, setPrdContent] = useState('');
  const [creatingFromPRD, setCreatingFromPRD] = useState(false);
  const [prdResults, setPrdResults] = useState<any>(null);
  
  // Templates State
  const [templates, setTemplates] = useState<any[]>([]);
  const [pncDemoStories, setPncDemoStories] = useState<any[]>([]);
  const [loadingTemplates, setLoadingTemplates] = useState(false);
  
  // Auto-load templates when modal opens
  useEffect(() => {
    if (isOpen && templates.length === 0 && !loadingTemplates) {
      loadTemplatesData();
    }
  }, [isOpen]);
  
  // Load templates when Templates tab is opened
  const loadTemplatesData = async () => {
    console.log('🔄 Loading templates...');
    setLoadingTemplates(true);
    try {
      const [templatesRes, demoRes] = await Promise.all([
        fetch('http://localhost:8000/api/v1/templates/list'),
        fetch('http://localhost:8000/api/v1/demo/pnc_stories')
      ]);
      
      console.log('✅ Fetched data, parsing...');
      const templatesData = await templatesRes.json();
      const demoData = await demoRes.json();
      
      console.log('Templates data:', templatesData);
      console.log('Demo data:', demoData);
      
      if (templatesData.success) {
        setTemplates(templatesData.templates || []);
        console.log(`✅ Set ${templatesData.templates?.length || 0} templates`);
      }
      if (demoData.success) {
        setPncDemoStories(demoData.stories || []);
        console.log(`✅ Set ${demoData.stories?.length || 0} demo stories`);
      }
    } catch (error) {
      console.error('❌ Error loading templates:', error);
      alert(`Failed to load templates: ${error}`);
    } finally {
      setLoadingTemplates(false);
      console.log('✅ Loading complete');
    }
  };
  
  const handleCreateStories = async () => {
    if (!featureDescription.trim()) return;
    
    setIsCreating(true);
    setCreatedStories([]);
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/jira/create_stories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_key: projectKey,
          feature_description: featureDescription,
          create_in_jira: true
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        setCreatedStories(data.stories || []);
      } else {
        alert('Failed to create stories');
      }
    } catch (error) {
      console.error('Error creating stories:', error);
      alert('Error creating stories');
    } finally {
      setIsCreating(false);
    }
  };
  
  const handleLoadSprint = async () => {
    if (!sprintId) return;
    
    setLoadingSprint(true);
    
    try {
      const response = await fetch(`http://localhost:8000/api/v1/jira/sprint/${sprintId}/status`);
      const data = await response.json();
      
      if (data.success) {
        setSprintData(data);
      } else {
        alert('Failed to load sprint');
      }
    } catch (error) {
      console.error('Error loading sprint:', error);
      alert('Error loading sprint');
    } finally {
      setLoadingSprint(false);
    }
  };
  
  const handleCreateFromPRD = async () => {
    if (!prdContent.trim()) return;
    
    setCreatingFromPRD(true);
    setPrdResults(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/jira/bulk_create_from_prd', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_key: projectKey,
          prd_content: {
            title: 'Feature from PRD',
            description: prdContent
          },
          create_epic: true,
          create_stories: true
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        setPrdResults(data);
      } else {
        alert('Failed to create from PRD');
      }
    } catch (error) {
      console.error('Error creating from PRD:', error);
      alert('Error creating from PRD');
    } finally {
      setCreatingFromPRD(false);
    }
  };
  
  const exportStories = async (format: string) => {
    if (createdStories.length === 0) return;
    
    try {
      // Format stories for PNC workshop compatibility
      const formattedStories = createdStories.map(story => ({
        title: story.summary,
        description: story.description,
        acceptance_criteria: story.acceptance_criteria || [],
        priority: story.priority,
        estimate: `${story.story_points}sp`,
        tags: story.labels || [],
        epic: '',
        author: 'ProdPlex AI - 9 Agent System',
        status: 'Draft',
        jira_key: story.jira_key || ''
      }));
      
      const response = await fetch('http://localhost:8000/api/v1/export/stories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          stories: formattedStories,
          format: format,
          title: `User Stories - ${projectKey}`
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
  
  if (!isOpen) return null;
  
  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="absolute inset-0 bg-black/80 backdrop-blur-sm"
        />
        
        {/* Modal */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="relative w-full max-w-6xl h-[85vh] bg-dark-card border-2 border-dark-border rounded-xl shadow-2xl flex flex-col"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-dark-border">
            <div>
              <h2 className="text-2xl font-display font-bold text-white flex items-center gap-2">
                <Target className="w-6 h-6 text-blue-400" />
                Jira Integration
              </h2>
              <p className="text-sm text-gray-400 mt-1">
                Create user stories, epics, and manage your backlog with AI
              </p>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-dark-lighter rounded-lg transition-colors"
            >
              <X className="w-6 h-6 text-gray-400" />
            </button>
          </div>
          
          {/* Tabs */}
          <div className="flex gap-2 p-4 border-b border-dark-border">
            <button
              onClick={() => setActiveTab('create')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'create'
                  ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                  : 'text-gray-400 hover:text-white hover:bg-dark-lighter'
              }`}
            >
              <Plus className="w-4 h-4 inline mr-2" />
              Create Stories
            </button>
            <button
              onClick={() => setActiveTab('sprint')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'sprint'
                  ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                  : 'text-gray-400 hover:text-white hover:bg-dark-lighter'
              }`}
            >
              <TrendingUp className="w-4 h-4 inline mr-2" />
              Sprint Status
            </button>
            <button
              onClick={() => setActiveTab('prd')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'prd'
                  ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                  : 'text-gray-400 hover:text-white hover:bg-dark-lighter'
              }`}
            >
              <FileText className="w-4 h-4 inline mr-2" />
              Create from PRD
            </button>
            <button
              onClick={() => {
                setActiveTab('templates');
                if (templates.length === 0) loadTemplatesData();
              }}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'templates'
                  ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                  : 'text-gray-400 hover:text-white hover:bg-dark-lighter'
              }`}
            >
              <List className="w-4 h-4 inline mr-2" />
              Templates (PNC)
            </button>
          </div>
          
          {/* Content */}
          <div className="flex-1 overflow-y-auto p-6">
            {/* Create Stories Tab */}
            {activeTab === 'create' && (
              <div className="space-y-6">
                <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
                  <p className="text-sm text-blue-300">
                    <AlertCircle className="w-4 h-4 inline mr-2" />
                    AI will generate user stories with acceptance criteria, story points, and priorities
                  </p>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Project Key
                  </label>
                  <input
                    type="text"
                    value={projectKey}
                    onChange={(e) => setProjectKey(e.target.value.toUpperCase())}
                    placeholder="PROD"
                    className="w-full px-4 py-2 bg-dark-lighter border border-dark-border rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Feature Description
                  </label>
                  <textarea
                    value={featureDescription}
                    onChange={(e) => setFeatureDescription(e.target.value)}
                    placeholder="Describe the feature you want to build... (e.g., 'User authentication system with OAuth support')"
                    rows={6}
                    className="w-full px-4 py-3 bg-dark-lighter border border-dark-border rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none resize-none"
                  />
                </div>
                
                <button
                  onClick={handleCreateStories}
                  disabled={isCreating || !featureDescription.trim()}
                  className="w-full btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {isCreating ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Generating Stories...
                    </>
                  ) : (
                    <>
                      <Send className="w-5 h-5" />
                      Generate User Stories
                    </>
                  )}
                </button>
                
                {/* Created Stories */}
                {createdStories.length > 0 && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                        <CheckCircle className="w-5 h-5 text-green-400" />
                        Created {createdStories.length} User Stories
                      </h3>
                      <div className="flex gap-2">
                        <button
                          onClick={() => exportStories('csv')}
                          className="text-xs bg-green-600 hover:bg-green-700 text-white px-3 py-1.5 rounded flex items-center gap-1"
                        >
                          <Send className="w-3 h-3" />
                          Export CSV
                        </button>
                        <button
                          onClick={() => exportStories('markdown')}
                          className="text-xs bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded flex items-center gap-1"
                        >
                          <FileText className="w-3 h-3" />
                          Export MD
                        </button>
                        <button
                          onClick={() => exportStories('jira_csv')}
                          className="text-xs bg-purple-600 hover:bg-purple-700 text-white px-3 py-1.5 rounded flex items-center gap-1"
                        >
                          <Target className="w-3 h-3" />
                          Jira Import
                        </button>
                      </div>
                    </div>
                    
                    {createdStories.map((story, idx) => (
                      <div
                        key={idx}
                        className="bg-dark-lighter border border-dark-border rounded-lg p-4"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              {story.jira_key && (
                                <span className="text-xs font-mono text-blue-400 bg-blue-500/20 px-2 py-1 rounded">
                                  {story.jira_key}
                                </span>
                              )}
                              <span className={`text-xs px-2 py-1 rounded ${
                                story.priority === 'High' ? 'bg-red-500/20 text-red-400' :
                                story.priority === 'Medium' ? 'bg-yellow-500/20 text-yellow-400' :
                                'bg-green-500/20 text-green-400'
                              }`}>
                                {story.priority}
                              </span>
                              <span className="text-xs text-gray-400">
                                {story.story_points} points
                              </span>
                            </div>
                            <h4 className="text-white font-medium mb-2">{story.summary}</h4>
                            <p className="text-sm text-gray-400 mb-3">{story.description}</p>
                            
                            <div className="space-y-1">
                              <p className="text-xs font-semibold text-gray-300">Acceptance Criteria:</p>
                              <ul className="list-disc list-inside text-xs text-gray-400 space-y-1">
                                {story.acceptance_criteria.map((criteria, i) => (
                                  <li key={i}>{criteria}</li>
                                ))}
                              </ul>
                            </div>
                          </div>
                          
                          {story.jira_url && (
                            <a
                              href={story.jira_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="ml-4 p-2 hover:bg-dark-bg rounded-lg transition-colors"
                            >
                              <ExternalLink className="w-4 h-4 text-blue-400" />
                            </a>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
            
            {/* Sprint Status Tab */}
            {activeTab === 'sprint' && (
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Sprint ID
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={sprintId}
                      onChange={(e) => setSprintId(e.target.value)}
                      placeholder="Enter sprint ID (e.g., 1)"
                      className="flex-1 px-4 py-2 bg-dark-lighter border border-dark-border rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none"
                    />
                    <button
                      onClick={handleLoadSprint}
                      disabled={loadingSprint || !sprintId}
                      className="btn btn-primary disabled:opacity-50"
                    >
                      {loadingSprint ? (
                        <Loader2 className="w-5 h-5 animate-spin" />
                      ) : (
                        'Load'
                      )}
                    </button>
                  </div>
                </div>
                
                {sprintData && (
                  <div className="space-y-4">
                    {/* Sprint Stats */}
                    <div className="grid grid-cols-4 gap-4">
                      <div className="bg-dark-lighter border border-dark-border rounded-lg p-4">
                        <p className="text-xs text-gray-400 mb-1">Total Issues</p>
                        <p className="text-2xl font-bold text-white">{sprintData.statistics?.total_issues || 0}</p>
                      </div>
                      <div className="bg-dark-lighter border border-dark-border rounded-lg p-4">
                        <p className="text-xs text-gray-400 mb-1">Story Points</p>
                        <p className="text-2xl font-bold text-white">{sprintData.statistics?.total_points || 0}</p>
                      </div>
                      <div className="bg-dark-lighter border border-dark-border rounded-lg p-4">
                        <p className="text-xs text-gray-400 mb-1">Completed</p>
                        <p className="text-2xl font-bold text-green-400">{sprintData.statistics?.completed_points || 0}</p>
                      </div>
                      <div className="bg-dark-lighter border border-dark-border rounded-lg p-4">
                        <p className="text-xs text-gray-400 mb-1">Progress</p>
                        <p className="text-2xl font-bold text-blue-400">
                          {sprintData.statistics?.completion_percentage?.toFixed(0) || 0}%
                        </p>
                      </div>
                    </div>
                    
                    {/* Sprint Issues */}
                    <div>
                      <h3 className="text-lg font-semibold text-white mb-3">Sprint Issues</h3>
                      <div className="space-y-2">
                        {sprintData.issues?.map((issue: any, idx: number) => (
                          <div
                            key={idx}
                            className="bg-dark-lighter border border-dark-border rounded-lg p-3 flex items-center justify-between"
                          >
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-1">
                                <span className="text-xs font-mono text-blue-400">{issue.key}</span>
                                <span className={`text-xs px-2 py-0.5 rounded ${
                                  issue.status === 'Done' ? 'bg-green-500/20 text-green-400' :
                                  issue.status === 'In Progress' ? 'bg-yellow-500/20 text-yellow-400' :
                                  'bg-gray-500/20 text-gray-400'
                                }`}>
                                  {issue.status}
                                </span>
                                {issue.story_points && (
                                  <span className="text-xs text-gray-400">{issue.story_points} pts</span>
                                )}
                              </div>
                              <p className="text-sm text-white">{issue.summary}</p>
                              {issue.assignee && (
                                <p className="text-xs text-gray-400 mt-1">Assignee: {issue.assignee}</p>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
            
            {/* Create from PRD Tab */}
            {activeTab === 'prd' && (
              <div className="space-y-6">
                <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4">
                  <p className="text-sm text-purple-300">
                    <AlertCircle className="w-4 h-4 inline mr-2" />
                    Paste your PRD and AI will create an epic with linked user stories
                  </p>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Project Key
                  </label>
                  <input
                    type="text"
                    value={projectKey}
                    onChange={(e) => setProjectKey(e.target.value.toUpperCase())}
                    placeholder="PROD"
                    className="w-full px-4 py-2 bg-dark-lighter border border-dark-border rounded-lg text-white placeholder-gray-500 focus:border-purple-500 focus:outline-none"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    PRD Content
                  </label>
                  <textarea
                    value={prdContent}
                    onChange={(e) => setPrdContent(e.target.value)}
                    placeholder="Paste your Product Requirements Document here..."
                    rows={10}
                    className="w-full px-4 py-3 bg-dark-lighter border border-dark-border rounded-lg text-white placeholder-gray-500 focus:border-purple-500 focus:outline-none resize-none font-mono text-sm"
                  />
                </div>
                
                <button
                  onClick={handleCreateFromPRD}
                  disabled={creatingFromPRD || !prdContent.trim()}
                  className="w-full bg-purple-500 hover:bg-purple-600 text-white font-bold py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {creatingFromPRD ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Creating Epic & Stories...
                    </>
                  ) : (
                    <>
                      <FileText className="w-5 h-5" />
                      Create Epic & Stories from PRD
                    </>
                  )}
                </button>
                
                {/* PRD Results */}
                {prdResults && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                      <CheckCircle className="w-5 h-5 text-green-400" />
                      Created Successfully!
                    </h3>
                    
                    {prdResults.epic && (
                      <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4">
                        <p className="text-sm text-purple-300 mb-2">Epic Created:</p>
                        <p className="text-white font-mono">{prdResults.epic.epic_key}</p>
                        {prdResults.epic.epic_url && (
                          <a
                            href={prdResults.epic.epic_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-400 text-sm hover:underline mt-2 inline-block"
                          >
                            View in Jira →
                          </a>
                        )}
                      </div>
                    )}
                    
                    {prdResults.stories && prdResults.stories.length > 0 && (
                      <div>
                        <p className="text-sm text-gray-300 mb-2">
                          {prdResults.stories.length} User Stories Created
                        </p>
                        <div className="grid grid-cols-2 gap-2">
                          {prdResults.stories.map((story: any, idx: number) => (
                            <div
                              key={idx}
                              className="bg-dark-lighter border border-dark-border rounded-lg p-3"
                            >
                              <p className="text-xs font-mono text-blue-400 mb-1">{story.jira_key}</p>
                              <p className="text-sm text-white">{story.summary}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
            
            {/* Templates (PNC) Tab */}
            {activeTab === 'templates' && (
              <div className="space-y-6">
                <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/30 rounded-lg p-4">
                  <h3 className="text-lg font-bold text-white mb-2 flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-blue-400" />
                    PNC Workshop Compatible Story Templates
                  </h3>
                  <p className="text-sm text-gray-300">
                    Demonstrating how our <span className="text-purple-400 font-semibold">9-Agent AI System</span> produces 
                    superior results in the <span className="text-blue-400 font-semibold">PNC workshop format</span>
                  </p>
                </div>
                
                {loadingTemplates && templates.length === 0 && pncDemoStories.length === 0 ? (
                  <div className="text-center py-12">
                    <Loader2 className="w-12 h-12 text-blue-400 mx-auto mb-4 animate-spin" />
                    <p className="text-gray-400">Loading templates...</p>
                    <button
                      onClick={loadTemplatesData}
                      className="mt-4 text-sm text-blue-400 hover:underline"
                    >
                      Click here if stuck
                    </button>
                  </div>
                ) : templates.length === 0 && pncDemoStories.length === 0 ? (
                  <div className="text-center py-12">
                    <p className="text-gray-400 mb-4">No templates loaded</p>
                    <button
                      onClick={loadTemplatesData}
                      className="btn btn-primary"
                    >
                      Load Templates
                    </button>
                  </div>
                ) : (
                  <>
                    {/* Available Templates */}
                    <div>
                      <h4 className="text-md font-semibold text-white mb-3 flex items-center gap-2">
                        <FileText className="w-4 h-4 text-blue-400" />
                        Available Templates ({templates.length})
                      </h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {templates.map((template, idx) => (
                          <div
                            key={idx}
                            className="bg-dark-lighter border border-dark-border rounded-lg p-4 hover:border-blue-500/50 transition-colors"
                          >
                            <h5 className="text-white font-medium mb-2">
                              {template.name.replace(/_/g, ' ').toUpperCase()}
                            </h5>
                            <p className="text-xs text-gray-400 mb-2 line-clamp-2">{template.title}</p>
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
                            <div className="flex flex-wrap gap-1 mt-2">
                              {template.tags?.slice(0, 3).map((tag: string, i: number) => (
                                <span key={i} className="text-xs bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded">
                                  {tag}
                                </span>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    {/* PNC Demo Stories - Shows Our AI Advantage */}
                    {pncDemoStories.length > 0 && (
                      <div>
                        <div className="flex items-center justify-between mb-3">
                          <h4 className="text-md font-semibold text-white flex items-center gap-2">
                            <Sparkles className="w-4 h-4 text-purple-400" />
                            AI-Generated Demo Stories (PNC Format)
                          </h4>
                          <div className="flex gap-2">
                            <button
                              onClick={async () => {
                                try {
                                  const formattedStories = pncDemoStories.map(s => ({
                                    title: s.title,
                                    description: s.description,
                                    acceptance_criteria: s.acceptance_criteria || [],
                                    priority: s.priority,
                                    estimate: s.estimate,
                                    tags: s.tags || [],
                                    epic: s.epic,
                                    author: s.author,
                                    status: s.status
                                  }));
                                  
                                  const response = await fetch('http://localhost:8000/api/v1/export/stories', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({ stories: formattedStories, format: 'csv', title: 'PNC Demo Stories' })
                                  });
                                  
                                  const data = await response.json();
                                  if (data.success) {
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
                                  console.error('Export failed:', error);
                                }
                              }}
                              className="text-xs bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded flex items-center gap-1"
                            >
                              <Download className="w-3 h-3" />
                              CSV
                            </button>
                            <button
                              onClick={async () => {
                                try {
                                  const formattedStories = pncDemoStories.map(s => ({
                                    title: s.title,
                                    description: s.description,
                                    acceptance_criteria: s.acceptance_criteria || [],
                                    priority: s.priority,
                                    estimate: s.estimate,
                                    tags: s.tags || [],
                                    epic: s.epic,
                                    author: s.author,
                                    status: s.status
                                  }));
                                  
                                  const response = await fetch('http://localhost:8000/api/v1/export/stories', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({ stories: formattedStories, format: 'markdown', title: 'PNC Demo Stories' })
                                  });
                                  
                                  const data = await response.json();
                                  if (data.success) {
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
                                  console.error('Export failed:', error);
                                }
                              }}
                              className="text-xs bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded flex items-center gap-1"
                            >
                              <Download className="w-3 h-3" />
                              MD
                            </button>
                          </div>
                        </div>
                        
                        <div className="space-y-3">
                          {pncDemoStories.map((story, idx) => (
                            <div
                              key={idx}
                              className="bg-dark-lighter border border-dark-border rounded-lg p-4"
                            >
                              <div className="flex items-start justify-between mb-2">
                                <h5 className="text-white font-medium flex-1">{story.title}</h5>
                                <div className="flex items-center gap-2">
                                  <span className={`text-xs px-2 py-1 rounded ${
                                    story.priority === 'High' ? 'bg-red-500/20 text-red-400' :
                                    story.priority === 'Medium' ? 'bg-yellow-500/20 text-yellow-400' :
                                    'bg-green-500/20 text-green-400'
                                  }`}>
                                    {story.priority}
                                  </span>
                                  <span className="text-xs text-gray-400">{story.estimate}</span>
                                </div>
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
                                      <li key={i}>✓ {adv}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </>
                )}
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default JiraIntegration;

