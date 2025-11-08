/**
 * Home Page - Modern landing page with NVIDIA/PNC styling
 */
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Zap, Shield, Bot, ArrowRight, Cpu, Network, TrendingUp } from 'lucide-react';

export const Home: React.FC = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: Cpu,
      title: 'Multi-Agent AI',
      description: '9 specialized agents with adaptive workflows powered by NVIDIA Nemotron',
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
    { name: 'Risk Assessment', description: 'Proactive risk prediction & bottleneck detection' },
    { name: 'Prioritization', description: 'Smart multi-factor feature prioritization' },
  ];

  return (
    <div className="min-h-screen bg-dark">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-nvidia-green/5 via-transparent to-pnc-blue/5" />
        
        {/* Animated grid background */}
        <div className="absolute inset-0 opacity-20" 
             style={{
               backgroundImage: `linear-gradient(rgba(118, 185, 0, 0.1) 1px, transparent 1px),
                                linear-gradient(90deg, rgba(0, 71, 187, 0.1) 1px, transparent 1px)`,
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
              <Sparkles className="w-5 h-5 text-nvidia-green" />
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
                Get Started
                <ArrowRight className="w-5 h-5" />
              </button>
              <button
                onClick={() => navigate('/insights')}
                className="btn btn-ghost text-lg px-8 py-4 w-full sm:w-auto"
              >
                View Demo
                <TrendingUp className="w-5 h-5" />
              </button>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="max-w-7xl mx-auto px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="section-header">
            Intelligent Agent System
          </h2>
          <p className="section-subtitle">
            Powered by NVIDIA Nemotron for strategic orchestration
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.1, duration: 0.8 }}
                className="card card-hover card-interactive"
              >
                <div className="flex flex-col items-center text-center">
                  <div className="w-14 h-14 mb-4 bg-gradient-to-br from-nvidia-green/20 to-pnc-blue/20 
                                border border-nvidia-green/30 rounded-xl flex items-center justify-center">
                    <Icon className="w-7 h-7 text-nvidia-green" />
                  </div>
                  <h3 className="text-lg font-display font-semibold text-gray-100 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-sm text-gray-400 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </motion.div>
            );
          })}
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
                  <div className="w-10 h-10 bg-pnc-blue/20 border border-pnc-blue/30 
                                rounded-lg flex items-center justify-center flex-shrink-0
                                group-hover:bg-pnc-blue/30 transition-colors">
                    <Bot className="w-5 h-5 text-pnc-blue-light" />
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

      {/* CTA Section */}
      <div className="max-w-4xl mx-auto px-6 py-20 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.5, duration: 0.8 }}
          className="card gradient-border p-12"
        >
          <h2 className="text-3xl md:text-4xl font-display font-bold text-gray-100 mb-4">
            Ready to Transform Your Workflow?
          </h2>
          <p className="text-lg text-gray-400 mb-8">
            Join the future of product management with AI-powered agents
          </p>
          <button
            onClick={() => navigate('/dashboard')}
            className="btn btn-primary text-lg px-12 py-4"
          >
            Launch Dashboard
            <ArrowRight className="w-5 h-5" />
          </button>
        </motion.div>
      </div>
    </div>
  );
};

export default Home;
