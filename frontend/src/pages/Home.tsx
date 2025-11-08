/**
 * Home Page - Landing/Welcome page
 */
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Zap, Shield, Bot, ArrowRight } from 'lucide-react';

export const Home: React.FC = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: Bot,
      title: 'Multi-Agent AI',
      description: '7 specialized agents working together for comprehensive PM support',
    },
    {
      icon: Zap,
      title: 'Workflow Automation',
      description: 'Automate repetitive tasks and focus on strategic decisions',
    },
    {
      icon: Shield,
      title: 'Privacy First',
      description: 'Local LLM processing for sensitive data with optional cloud reasoning',
    },
    {
      icon: Sparkles,
      title: 'NVIDIA Nemotron',
      description: 'Advanced multi-step reasoning for strategic planning',
    },
  ];

  return (
    <div className="min-h-screen bg-charcoal">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-neon-cyan/10 via-transparent to-neon-orange/10" />
        
        <div className="relative max-w-7xl mx-auto px-6 py-24">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <h1 className="text-6xl md:text-7xl font-display font-bold gradient-text mb-6">
              ProdigyPM
            </h1>
            <p className="text-2xl text-gray-300 mb-4">
              Your AI Co-Pilot for Product Management
            </p>
            <p className="text-lg text-gray-400 mb-12 max-w-2xl mx-auto">
              Multi-agent AI platform that helps Product Managers plan, ideate, research, 
              and automate workflows using advanced AI reasoning.
            </p>
            
            <div className="flex gap-4 justify-center">
              <button
                onClick={() => navigate('/dashboard')}
                className="btn btn-primary text-lg px-8 py-4"
              >
                Get Started
                <ArrowRight className="w-5 h-5 ml-2" />
              </button>
              <button
                onClick={() => navigate('/insights')}
                className="btn btn-ghost text-lg px-8 py-4"
              >
                View Insights
              </button>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="max-w-7xl mx-auto px-6 py-24">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-display font-bold text-white mb-4">
            Powerful AI Agents
          </h2>
          <p className="text-lg text-gray-400">
            7 specialized agents orchestrated by NVIDIA Nemotron
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
                className="card card-hover text-center"
              >
                <div className="w-16 h-16 mx-auto mb-4 bg-neon-cyan/10 border border-neon-cyan rounded-full flex items-center justify-center">
                  <Icon className="w-8 h-8 text-neon-cyan" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-400">
                  {feature.description}
                </p>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Agent Showcase */}
      <div className="bg-charcoal-light py-24">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-display font-bold text-white mb-4">
              Meet Your AI Team
            </h2>
            <p className="text-lg text-gray-400">
              Each agent specializes in a different aspect of product management
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { name: 'StrategyAgent', role: 'Market sizing & strategic planning' },
              { name: 'ResearchAgent', role: 'User research & competitive analysis' },
              { name: 'DevAgent', role: 'User stories & technical specs' },
              { name: 'PrototypeAgent', role: 'Design mockups & Figma integration' },
              { name: 'GtmAgent', role: 'Go-to-market & launch planning' },
              { name: 'AutomationAgent', role: 'Workflow automation & reporting' },
              { name: 'RegulationAgent', role: 'Compliance & regulatory review' },
            ].map((agent, index) => (
              <motion.div
                key={agent.name}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.8 + index * 0.1, duration: 0.5 }}
                className="card card-hover"
              >
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-neon-orange/10 border border-neon-orange rounded-lg flex items-center justify-center flex-shrink-0">
                    <Bot className="w-6 h-6 text-neon-orange" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-white">{agent.name}</h3>
                    <p className="text-sm text-gray-400">{agent.role}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-4xl mx-auto px-6 py-24 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.5, duration: 0.8 }}
        >
          <h2 className="text-4xl font-display font-bold text-white mb-6">
            Ready to supercharge your PM workflow?
          </h2>
          <p className="text-lg text-gray-400 mb-8">
            Join the future of product management with AI-powered agents
          </p>
          <button
            onClick={() => navigate('/dashboard')}
            className="btn btn-primary text-lg px-12 py-4 animate-glow"
          >
            Start Free Trial
          </button>
        </motion.div>
      </div>
    </div>
  );
};

export default Home;

