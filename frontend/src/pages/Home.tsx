/**
 * Home Page - Modern landing page with NVIDIA/PNC styling
 */
import { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Zap, Shield, Bot, ArrowRight, Cpu, Network, TrendingUp, LogOut, FileText } from 'lucide-react';
import PRDSelectionModal from '../components/PRDSelectionModal';
import DetailedPRDModal from '../components/DetailedPRDModal';
import QuickPRDModal from '../components/QuickPRDModal';
import PRDViewer from '../components/PRDViewer';

export const Home: React.FC = () => {
  const navigate = useNavigate();
  const [showPRDSelection, setShowPRDSelection] = useState(false);
  const [showDetailedPRD, setShowDetailedPRD] = useState(false);
  const [showQuickPRD, setShowQuickPRD] = useState(false);
  const [showPRDViewer, setShowPRDViewer] = useState(false);
  const [prdData, setPRDData] = useState<any>(null);

  const handleSignOut = () => {
    // Clear any auth state if needed
    navigate('/login');
  };

  const handlePRDComplete = (data: any) => {
    setPRDData(data);
    setShowPRDViewer(true);
  };

  const handleSelectDetailed = () => {
    setShowPRDSelection(false);
    setShowDetailedPRD(true);
  };

  const handleSelectQuick = () => {
    setShowPRDSelection(false);
    setShowQuickPRD(true);
  };

  const features = [
    {
      icon: Cpu,
      title: 'Multi-Agent AI',
      description: '9 specialized agents powered by NVIDIA Nemotron for strategic reasoning',
    },
    {
      icon: Zap,
      title: 'Automated Workflows',
      description: 'Streamline repetitive PM tasks and focus on high-impact decisions',
    },
    {
      icon: Shield,
      title: 'Privacy First',
      description: 'Local LLM processing with optional cloud reasoning for sensitive data',
    },
    {
      icon: Network,
      title: 'Intelligent Orchestration',
      description: 'Coordinated multi-agent system with shared memory and context',
    },
  ];

  const agents = [
    { name: 'Strategy', description: 'Market analysis & competitive intelligence' },
    { name: 'Research', description: 'User insights & trend detection' },
    { name: 'Development', description: 'User stories & technical specifications' },
    { name: 'Prototype', description: 'Design mockups & Figma integration' },
    { name: 'Go-to-Market', description: 'Launch strategy & pricing' },
    { name: 'Automation', description: 'Workflow automation & reporting' },
    { name: 'Regulation', description: 'Compliance & risk assessment' },
    { name: 'Prioritization', description: 'RICE framework & feature prioritization' },
    { name: 'Risk Assessment', description: 'Technical & business risk analysis' },
  ];

  return (
    <div className="min-h-screen bg-dark">
      {/* Navigation Bar */}
      <nav className="sticky top-0 z-50 bg-dark/80 backdrop-blur-lg border-b border-dark-border">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <button 
              onClick={() => navigate('/')}
              className="flex items-center gap-2 hover:opacity-80 transition-opacity"
            >
              <Sparkles className="w-6 h-6 text-primary-light" />
              <span className="text-xl font-display font-bold gradient-text">ProdigyPM</span>
            </button>
            
            <button
              onClick={handleSignOut}
              className="flex items-center gap-2 px-4 py-2 text-gray-300 hover:text-white transition-colors"
            >
              <LogOut className="w-4 h-4" />
              <span>Sign Out</span>
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5" />
        
        {/* Animated grid background */}
        <div className="absolute inset-0 opacity-10" 
             style={{
               backgroundImage: `linear-gradient(rgba(173, 181, 189, 0.3) 1px, transparent 1px),
                                linear-gradient(90deg, rgba(173, 181, 189, 0.3) 1px, transparent 1px)`,
               backgroundSize: '50px 50px'
             }} 
        />
        
        <div className="relative max-w-7xl mx-auto px-6 py-20 md:py-32">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center max-w-4xl mx-auto"
          >
            {/* Logo/Title */}
            <div className="mb-6 inline-flex items-center gap-3 px-4 py-2 bg-dark-card border border-dark-border rounded-full">
              <Sparkles className="w-5 h-5 text-primary-light" />
              <span className="text-sm font-medium text-gray-300">
                Powered by NVIDIA Nemotron
              </span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-display font-bold mb-6 leading-tight">
              <span className="gradient-text">ProdigyPM</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-300 mb-4 font-medium">
              Your AI Co-Pilot for Product Management
            </p>
            
            <p className="text-lg text-gray-400 mb-12 max-w-2xl mx-auto">
              Multi-agent AI platform that helps Product Managers plan, research, 
              and automate workflows using advanced reasoning and local-first AI.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <button
                onClick={() => navigate('/dashboard')}
                className="btn btn-primary text-lg px-8 py-4 w-full sm:w-auto"
              >
                Launch Dashboard
                <ArrowRight className="w-5 h-5" />
              </button>
              <button
                onClick={() => setShowPRDSelection(true)}
                className="btn btn-secondary text-lg px-8 py-4 w-full sm:w-auto bg-gradient-to-r from-orange-400/20 to-neon-cyan/20 border-orange-400/50 hover:border-orange-400"
              >
                <FileText className="w-5 h-5" />
                Generate PRD
              </button>
              <button
                onClick={() => navigate('/insights')}
                className="btn btn-secondary text-lg px-8 py-4 w-full sm:w-auto"
              >
                View Analytics
                <TrendingUp className="w-5 h-5" />
              </button>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Agent Showcase */}
      <div className="bg-dark-lighter py-20">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="section-header">
              Nine Specialized Agents
            </h2>
            <p className="section-subtitle">
              Each agent brings unique expertise to your product workflow
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {agents.map((agent, index) => (
              <motion.div
                key={agent.name}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.8 + index * 0.05, duration: 0.5 }}
                className="card card-hover group"
              >
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-accent/20 border border-accent/30 
                                rounded-lg flex items-center justify-center flex-shrink-0
                                group-hover:bg-accent/30 transition-colors">
                    <Bot className="w-5 h-5 text-primary-light" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-display font-semibold text-gray-100 mb-1">
                      {agent.name}
                    </h3>
                    <p className="text-xs text-gray-400 leading-relaxed">
                      {agent.description}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* PRD Modals */}
      <PRDSelectionModal
        isOpen={showPRDSelection}
        onClose={() => setShowPRDSelection(false)}
        onSelectDetailed={handleSelectDetailed}
        onSelectQuick={handleSelectQuick}
      />
      
      <DetailedPRDModal
        isOpen={showDetailedPRD}
        onClose={() => setShowDetailedPRD(false)}
        onComplete={handlePRDComplete}
      />
      
      <QuickPRDModal
        isOpen={showQuickPRD}
        onClose={() => setShowQuickPRD(false)}
        onComplete={handlePRDComplete}
      />
      
      <PRDViewer
        isOpen={showPRDViewer}
        onClose={() => setShowPRDViewer(false)}
        prdData={prdData}
      />
    </div>
  );
};

export default Home;
