/**
 * Workflow Visualization - Real-time agent graph showing multi-agent collaboration
 */
import React, { useMemo } from 'react';
import ReactFlow, {
  Node,
  Edge,
  Background,
  Controls,
  MiniMap,
  NodeTypes,
  Handle,
  Position,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { motion } from 'framer-motion';
import { CheckCircle2, Loader2, AlertCircle, Brain, ArrowRight } from 'lucide-react';

interface AgentNode {
  name: string;
  status: 'idle' | 'thinking' | 'working' | 'collaborating' | 'done' | 'error';
  quality_score?: number;
  output?: any;
  reasoning?: string[];
  collaborating_with?: string[];
}

interface WorkflowVisualizationProps {
  agents: AgentNode[];
  contextFlow?: Array<{ from: string; to: string; data_type: string }>;
  onNodeClick?: (agentName: string) => void;
}

const getStatusColor = (status: string): string => {
  switch (status) {
    case 'thinking':
      return 'bg-yellow-500/20 border-yellow-500';
    case 'working':
      return 'bg-blue-500/20 border-blue-500';
    case 'collaborating':
      return 'bg-purple-500/20 border-purple-500';
    case 'done':
      return 'bg-green-500/20 border-green-500';
    case 'error':
      return 'bg-red-500/20 border-red-500';
    default:
      return 'bg-gray-500/20 border-gray-500';
  }
};

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'thinking':
      return <Brain className="w-4 h-4 text-yellow-400 animate-pulse" />;
    case 'working':
      return <Loader2 className="w-4 h-4 text-blue-400 animate-spin" />;
    case 'collaborating':
      return <ArrowRight className="w-4 h-4 text-purple-400" />;
    case 'done':
      return <CheckCircle2 className="w-4 h-4 text-green-400" />;
    case 'error':
      return <AlertCircle className="w-4 h-4 text-red-400" />;
    default:
      return <div className="w-4 h-4 rounded-full bg-gray-400" />;
  }
};

const CustomAgentNode: React.FC<{ data: any }> = ({ data }) => {
  const { agent, onNodeClick } = data;
  
  return (
    <div
      className={`card p-3 min-w-[180px] border-2 ${getStatusColor(agent.status)} cursor-pointer hover:scale-105 transition-transform`}
      onClick={() => onNodeClick?.(agent.name)}
    >
      <div className="flex items-center gap-2 mb-2">
        {getStatusIcon(agent.status)}
        <span className="text-sm font-semibold text-white">{agent.name}</span>
      </div>
      
      {agent.quality_score !== undefined && (
        <div className="mb-2">
          <div className="flex justify-between text-xs text-gray-400 mb-1">
            <span>Quality</span>
            <span>{(agent.quality_score * 100).toFixed(0)}%</span>
          </div>
          <div className="w-full bg-dark-lighter rounded-full h-1.5">
            <div
              className="bg-neon-cyan h-1.5 rounded-full transition-all"
              style={{ width: `${agent.quality_score * 100}%` }}
            />
          </div>
        </div>
      )}
      
      {agent.reasoning && agent.reasoning.length > 0 && (
        <div className="mt-2 text-xs text-gray-400">
          <div className="font-medium mb-1">Thinking:</div>
          <div className="space-y-1">
            {agent.reasoning.slice(0, 2).map((step: string, i: number) => (
              <div key={i} className="flex items-start gap-1">
                <span className="text-neon-cyan">•</span>
                <span className="line-clamp-1">{step}</span>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {agent.collaborating_with && agent.collaborating_with.length > 0 && (
        <div className="mt-2 text-xs text-purple-400">
          ↔ Collaborating with: {agent.collaborating_with.join(', ')}
        </div>
      )}
    </div>
  );
};

const nodeTypes: NodeTypes = {
  agent: CustomAgentNode,
};

export const WorkflowVisualization: React.FC<WorkflowVisualizationProps> = ({
  agents,
  contextFlow = [],
  onNodeClick,
}) => {
  const { nodes, edges } = useMemo(() => {
    // Calculate positions in a grid layout
    const cols = Math.ceil(Math.sqrt(agents.length));
    const nodeWidth = 200;
    const nodeHeight = 150;
    const spacing = 250;
    
    const nodes: Node[] = agents.map((agent, index) => {
      const row = Math.floor(index / cols);
      const col = index % cols;
      
      return {
        id: agent.name,
        type: 'agent',
        position: {
          x: col * spacing,
          y: row * spacing,
        },
        data: {
          agent,
          onNodeClick,
        },
      };
    });
    
    const edges: Edge[] = contextFlow.map((flow, index) => ({
      id: `edge-${flow.from}-${flow.to}-${index}`,
      source: flow.from,
      target: flow.to,
      animated: true,
      style: {
        stroke: '#00FFFF',
        strokeWidth: 2,
      },
      label: flow.data_type,
      labelStyle: {
        fill: '#00FFFF',
        fontSize: 10,
        fontWeight: 500,
      },
      labelBgStyle: {
        fill: '#0F1117',
        fillOpacity: 0.8,
      },
    }));
    
    return { nodes, edges };
  }, [agents, contextFlow, onNodeClick]);
  
  return (
    <div className="w-full h-[600px] bg-dark-lighter rounded-lg border border-dark-border">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        fitView
        minZoom={0.2}
        maxZoom={1.5}
        defaultViewport={{ x: 0, y: 0, zoom: 0.8 }}
      >
        <Background color="#1A1D29" gap={20} />
        <Controls className="bg-dark-card border-dark-border" />
        <MiniMap
          className="bg-dark-card border-dark-border"
          nodeColor={(node) => {
            const status = node.data?.agent?.status || 'idle';
            if (status === 'done') return '#10b981';
            if (status === 'working') return '#3b82f6';
            if (status === 'thinking') return '#eab308';
            return '#6b7280';
          }}
        />
      </ReactFlow>
    </div>
  );
};

export default WorkflowVisualization;

