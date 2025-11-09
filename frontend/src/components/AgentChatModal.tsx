/**
 * Agent Chat Modal - Interactive chat with specific agent using real NVIDIA AI
 */
import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Send, ArrowLeft, Loader2, Sparkles } from 'lucide-react';
import apiClient from '../utils/apiClient';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  cost?: number;
  model?: string;
}

interface AgentChatModalProps {
  isOpen: boolean;
  onClose: () => void;
  agentName: string;
  agentDescription: string;
  agentKey: string;
}

export const AgentChatModal: React.FC<AgentChatModalProps> = ({
  isOpen,
  onClose,
  agentName,
  agentDescription,
  agentKey,
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [totalCost, setTotalCost] = useState(0);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen) {
      // Add welcome message
      setMessages([{
        role: 'assistant',
        content: `Hello! I'm the ${agentName}. ${agentDescription}\n\nHow can I help you today?`,
        timestamp: new Date()
      }]);
      setTotalCost(0);
    }
  }, [isOpen, agentName, agentDescription]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Call the agent with user's message
      const response = await apiClient.executeAgent(
        agentKey,
        'chat',
        {
          message: input,
          conversation_history: messages.map(m => ({
            role: m.role,
            content: m.content
          }))
        }
      );

      // Parse the nested response structure
      const resultData = response.result?.result || {};
      const aiResponse = resultData.response || 'I apologize, but I encountered an issue processing your request.';
      
      const assistantMessage: Message = {
        role: 'assistant',
        content: aiResponse,
        timestamp: new Date(),
        cost: resultData.cost,
        model: resultData.model
      };

      // Update total cost
      if (resultData.cost) {
        setTotalCost(prev => prev + resultData.cost);
      }

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const getAgentColor = (agentKey: string): string => {
    const colorMap: Record<string, string> = {
      'strategy': 'text-purple-400',
      'research': 'text-blue-400',
      'dev': 'text-green-400',
      'prototype': 'text-pink-400',
      'gtm': 'text-orange-400',
      'automation': 'text-yellow-400',
      'regulation': 'text-red-400',
      'risk_assessment': 'text-amber-400',
      'prioritization': 'text-cyan-400',
    };
    return colorMap[agentKey] || 'text-neon-cyan';
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
          className="relative w-full max-w-4xl h-[80vh] bg-dark-card border-2 border-dark-border rounded-xl shadow-2xl flex flex-col"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-dark-border">
            <div className="flex items-center gap-3">
              <button
                onClick={onClose}
                className="p-2 hover:bg-dark-lighter rounded-lg transition-colors"
                title="Back"
              >
                <ArrowLeft className="w-5 h-5 text-gray-400" />
              </button>
              <div>
                <h2 className={`text-2xl font-display font-bold flex items-center gap-2 ${getAgentColor(agentKey)}`}>
                  <Sparkles className="w-6 h-6" />
                  {agentName}
                </h2>
                <p className="text-sm text-gray-400 mt-1">
                  {agentDescription}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              {totalCost > 0 && (
                <div className="text-xs text-gray-400">
                  Cost: <span className="text-neon-cyan font-mono">${totalCost.toFixed(4)}</span>
                </div>
              )}
              <button
                onClick={onClose}
                className="p-2 hover:bg-dark-lighter rounded-lg transition-colors"
              >
                <X className="w-6 h-6 text-gray-400" />
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-4 ${
                    message.role === 'user'
                      ? 'bg-neon-cyan/20 border border-neon-cyan/30'
                      : 'bg-dark-lighter border border-dark-border'
                  }`}
                >
                  <div className="flex items-start gap-2 mb-2">
                    <span className={`text-xs font-semibold ${
                      message.role === 'user' ? 'text-neon-cyan' : getAgentColor(agentKey)
                    }`}>
                      {message.role === 'user' ? 'You' : agentName}
                    </span>
                    <span className="text-xs text-gray-500">
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                    {message.model && (
                      <span className="text-xs text-gray-500 ml-auto">
                        {message.model.split('/').pop()}
                      </span>
                    )}
                  </div>
                  <p className="text-gray-200 whitespace-pre-wrap text-sm leading-relaxed">
                    {message.content}
                  </p>
                  {message.cost !== undefined && message.cost > 0 && (
                    <div className="mt-2 text-xs text-gray-500">
                      Cost: ${message.cost.toFixed(4)}
                    </div>
                  )}
                </div>
              </motion.div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-dark-lighter border border-dark-border rounded-lg p-4">
                  <div className="flex items-center gap-2 text-gray-400">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="text-sm">{agentName} is thinking...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-6 border-t border-dark-border">
            <div className="flex gap-3">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder={`Ask ${agentName} anything...`}
                className="flex-1 px-4 py-3 bg-dark-lighter border border-dark-border rounded-lg text-white placeholder-gray-500 focus:border-neon-cyan focus:outline-none resize-none"
                rows={3}
                disabled={isLoading}
              />
              <button
                onClick={handleSend}
                disabled={!input.trim() || isLoading}
                className="btn btn-primary h-full px-6 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2">
              Press Enter to send, Shift+Enter for new line • Powered by NVIDIA Nemotron
            </p>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default AgentChatModal;

