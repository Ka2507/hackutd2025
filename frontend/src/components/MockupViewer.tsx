/**
 * Mockup Viewer Component
 * Displays AI-generated design mockups and wireframes
 */
import { motion } from 'framer-motion';
import { ExternalLink, Palette, Type, Layout } from 'lucide-react';

interface MockupViewerProps {
  mockup: {
    title: string;
    screens: Array<{
      name: string;
      layout: string;
      components: Array<{ type: string; content: string }>;
      wireframe_svg: string;
      notes: string;
    }>;
    design_concept: string;
    color_palette: {
      primary: string;
      secondary: string;
      background: string;
      surface: string;
      text: string;
    };
    typography: {
      heading: string;
      body: string;
    };
    figma_integration: {
      available: boolean;
      status: string;
    };
  };
}

export const MockupViewer: React.FC<MockupViewerProps> = ({ mockup }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gradient-to-br from-purple-500/10 to-pink-500/10 border-2 border-purple-500/30 rounded-lg p-4 my-4"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-bold text-purple-300 flex items-center gap-2">
            <Layout className="w-5 h-5" />
            {mockup.title}
          </h3>
          <p className="text-xs text-gray-400 mt-1">
            AI-Generated Design Mockup
          </p>
        </div>
        {mockup.figma_integration.available && (
          <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded flex items-center gap-1">
            <ExternalLink className="w-3 h-3" />
            Figma Ready
          </span>
        )}
      </div>
      
      {/* Wireframe Preview */}
      {mockup.screens && mockup.screens[0]?.wireframe_svg && (
        <div className="mb-4 bg-dark-bg rounded-lg p-4 border border-purple-500/20">
          <p className="text-xs text-purple-300 mb-2 font-semibold">Visual Wireframe:</p>
          <div 
            className="wireframe-container bg-white rounded"
            dangerouslySetInnerHTML={{ __html: mockup.screens[0].wireframe_svg }}
          />
        </div>
      )}
      
      {/* Design Specifications */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
        {/* Color Palette */}
        <div className="bg-dark-bg rounded-lg p-3 border border-purple-500/20">
          <h4 className="text-xs font-semibold text-purple-300 mb-2 flex items-center gap-1">
            <Palette className="w-3 h-3" />
            Color Palette
          </h4>
          <div className="grid grid-cols-5 gap-2">
            {Object.entries(mockup.color_palette).map(([name, color]) => (
              <div key={name} className="text-center">
                <div
                  className="w-full h-8 rounded border border-gray-700 mb-1"
                  style={{ backgroundColor: color }}
                  title={color}
                />
                <p className="text-xs text-gray-400 truncate">{name}</p>
              </div>
            ))}
          </div>
        </div>
        
        {/* Typography */}
        <div className="bg-dark-bg rounded-lg p-3 border border-purple-500/20">
          <h4 className="text-xs font-semibold text-purple-300 mb-2 flex items-center gap-1">
            <Type className="w-3 h-3" />
            Typography
          </h4>
          <div className="space-y-2">
            <div>
              <p className="text-xs text-gray-400">Heading:</p>
              <p className="text-sm text-white font-bold" style={{ fontFamily: mockup.typography.heading }}>
                {mockup.typography.heading}
              </p>
            </div>
            <div>
              <p className="text-xs text-gray-400">Body:</p>
              <p className="text-sm text-white" style={{ fontFamily: mockup.typography.body }}>
                {mockup.typography.body}
              </p>
            </div>
          </div>
        </div>
      </div>
      
      {/* Components List */}
      {mockup.screens && mockup.screens[0]?.components && (
        <div className="bg-dark-bg rounded-lg p-3 border border-purple-500/20 mb-3">
          <h4 className="text-xs font-semibold text-purple-300 mb-2">UI Components:</h4>
          <ul className="space-y-1">
            {mockup.screens[0].components.map((comp, idx) => (
              <li key={idx} className="text-xs text-gray-300 flex items-start gap-2">
                <span className="text-purple-400">•</span>
                <span><strong className="text-purple-300">{comp.type}:</strong> {comp.content}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      
      {/* Figma Integration Status */}
      <div className="bg-dark-bg rounded-lg p-3 border border-purple-500/20">
        <p className="text-xs text-gray-400">
          {mockup.figma_integration.status}
        </p>
      </div>
    </motion.div>
  );
};

export default MockupViewer;

