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
      return 'bg-silver/20 border-silver';
    case 'working':
      return 'bg-white/20 border-white';
    case 'collaborating':
      return 'bg-silver/20 border-silver';
    case 'done':
      return 'bg-white/20 border-white';
    case 'error':
      return 'bg-red-500/20 border-red-500';
    default:
      return 'bg-silver/20 border-silver';
  }
};

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'thinking':
      return <Brain className="w-4 h-4 text-silver animate-pulse" />;
    case 'working':
      return <Loader2 className="w-4 h-4 text-white animate-spin" />;
    case 'collaborating':
      return <ArrowRight className="w-4 h-4 text-silver" />;
    case 'done':
      return <CheckCircle2 className="w-4 h-4 text-white" />;
    case 'error':
      return <AlertCircle className="w-4 h-4 text-red-400" />;
    default:
      return <div className="w-4 h-4 rounded-full bg-silver/70" />;
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
        <span className="text-sm font-semibold text-silver">{agent.name}</span>
      </div>
      
      {agent.quality_score !== undefined && (
        <div className="mb-2">
          <div className="flex justify-between text-xs text-silver/70 mb-1">
            <span>Quality</span>
            <span>{(agent.quality_score * 100).toFixed(0)}%</span>
          </div>
          <div className="w-full bg-dark-lighter rounded-full h-1.5">
            <div
              className="bg-white h-1.5 rounded-full transition-all"
              style={{ width: `${agent.quality_score * 100}%` }}
            />
          </div>
        </div>
      )}
      
      {agent.reasoning && agent.reasoning.length > 0 && (
        <div className="mt-2 text-xs text-silver/70">
          <div className="font-medium mb-1">Thinking:</div>
          <div className="space-y-1">
            {agent.reasoning.slice(0, 2).map((step: string, i: number) => (
              <div key={i} className="flex items-start gap-1">
                <span className="text-white">•</span>
                <span className="line-clamp-1">{step}</span>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {agent.collaborating_with && agent.collaborating_with.length > 0 && (
        <div className="mt-2 text-xs text-silver">
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
        stroke: '#ffffff',
        strokeWidth: 2,
      },
      label: flow.data_type,
      labelStyle: {
        fill: '#ffffff',
        fontSize: 10,
        fontWeight: 500,
      },
      labelBgStyle: {
        fill: '#020305',
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
        <Background color="#0f1418" gap={20} />
        <Controls className="bg-dark-card border-dark-border" />
        <MiniMap
          className="bg-dark-card border-dark-border"
          nodeColor={(node) => {
            const status = node.data?.agent?.status || 'idle';
            if (status === 'done') return '#ffffff';
            if (status === 'working') return '#ffffff';
            if (status === 'thinking') return '#707b81';
            return '#707b81';
          }}
        />
      </ReactFlow>
    </div>
  );
};

export default WorkflowVisualization;

