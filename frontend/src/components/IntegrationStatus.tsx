/**
 * Integration Status Component
 * Shows connection status for Jira, Figma, and Slack
 */
import { useState, useEffect } from 'react';
import { CheckCircle, XCircle, AlertCircle, Target, MessageSquare } from 'lucide-react';

interface IntegrationHealth {
  jira: { connected: boolean; status: string };
  figma: { connected: boolean; status: string };
  slack: { connected: boolean; status: string };
}

export const IntegrationStatus: React.FC = () => {
  const [health, setHealth] = useState<IntegrationHealth>({
    jira: { connected: false, status: 'checking' },
    figma: { connected: false, status: 'checking' },
    slack: { connected: false, status: 'checking' }
  });

  useEffect(() => {
    checkIntegrations();
  }, []);

  const checkIntegrations = async () => {
    try {
      // Check Jira
      const jiraRes = await fetch('http://localhost:8000/api/v1/jira/health');
      const jiraData = await jiraRes.json();
      
      // Check Figma
      const figmaRes = await fetch('http://localhost:8000/api/v1/figma/health');
      const figmaData = await figmaRes.json();
      
      // Check Slack
      const slackRes = await fetch('http://localhost:8000/api/v1/slack/health');
      const slackData = await slackRes.json();
      
      setHealth({
        jira: { connected: jiraData.connected || false, status: jiraData.status || 'unknown' },
        figma: { connected: figmaData.connected || false, status: figmaData.status || 'unknown' },
        slack: { connected: slackData.connected || false, status: slackData.status || 'unknown' }
      });
    } catch (error) {
      console.error('Error checking integrations:', error);
    }
  };

  const getStatusIcon = (connected: boolean, status: string) => {
    if (connected) {
      return <CheckCircle className="w-4 h-4 text-green-400" />;
    } else if (status === 'mock') {
      return <AlertCircle className="w-4 h-4 text-yellow-400" />;
    } else {
      return <XCircle className="w-4 h-4 text-gray-400" />;
    }
  };

  const getStatusText = (connected: boolean, status: string) => {
    if (connected) return 'Connected';
    if (status === 'mock') return 'Mock Mode';
    return 'Not Connected';
  };

  const getStatusColor = (connected: boolean, status: string) => {
    if (connected) return 'text-green-400';
    if (status === 'mock') return 'text-yellow-400';
    return 'text-gray-400';
  };

  return (
    <div className="bg-dark-lighter border border-dark-border rounded-lg p-4">
      <h3 className="text-sm font-semibold text-white mb-3">Integrations</h3>
      <div className="space-y-2">
        {/* Jira */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Target className="w-4 h-4 text-blue-400" />
            <span className="text-sm text-gray-300">Jira</span>
          </div>
          <div className="flex items-center gap-2">
            {getStatusIcon(health.jira.connected, health.jira.status)}
            <span className={`text-xs ${getStatusColor(health.jira.connected, health.jira.status)}`}>
              {getStatusText(health.jira.connected, health.jira.status)}
            </span>
          </div>
        </div>

        {/* Figma */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4 text-purple-400" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8 24c2.208 0 4-1.792 4-4v-4H8c-2.208 0-4 1.792-4 4s1.792 4 4 4z"/>
              <path d="M4 12c0-2.208 1.792-4 4-4h4v8H8c-2.208 0-4-1.792-4-4z"/>
              <path d="M4 4c0-2.208 1.792-4 4-4h4v8H8C5.792 8 4 6.208 4 4z"/>
              <path d="M12 0h4c2.208 0 4 1.792 4 4s-1.792 4-4 4h-4V0z"/>
              <path d="M20 12c0 2.208-1.792 4-4 4s-4-1.792-4-4 1.792-4 4-4 4 1.792 4 4z"/>
            </svg>
            <span className="text-sm text-gray-300">Figma</span>
          </div>
          <div className="flex items-center gap-2">
            {getStatusIcon(health.figma.connected, health.figma.status)}
            <span className={`text-xs ${getStatusColor(health.figma.connected, health.figma.status)}`}>
              {getStatusText(health.figma.connected, health.figma.status)}
            </span>
          </div>
        </div>

        {/* Slack */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4" viewBox="0 0 54 54" fill="none" xmlns="http://www.w3.org/2000/svg">
              {/* Top-left cyan pill */}
              <rect x="6" y="6" width="14" height="5" rx="2.5" fill="#36C5F0"/>
              {/* Middle-left cyan pill */}
              <rect x="6" y="19" width="14" height="5" rx="2.5" fill="#36C5F0"/>
              
              {/* Top-right green pill */}
              <rect x="34" y="6" width="5" height="14" rx="2.5" fill="#2EB67D"/>
              {/* Middle-right green teardrop */}
              <path d="M34 24 Q34 19 39 19 Q44 19 44 24 Q44 29 39 29 Q34 29 34 24" fill="#2EB67D"/>
              
              {/* Bottom-left magenta teardrop */}
              <path d="M15 29 Q20 29 20 34 Q20 39 15 39 Q10 39 10 34 Q10 29 15 29" fill="#E01E5A"/>
              {/* Bottom-left magenta pill */}
              <rect x="6" y="34" width="5" height="14" rx="2.5" fill="#E01E5A"/>
              
              {/* Bottom-right gold pill */}
              <rect x="19" y="43" width="14" height="5" rx="2.5" fill="#ECB22E"/>
              {/* Bottom-right gold teardrop */}
              <path d="M34 39 Q34 44 39 44 Q44 44 44 39 Q44 34 39 34 Q34 34 34 39" fill="#ECB22E"/>
            </svg>
            <span className="text-sm text-gray-300">Slack</span>
          </div>
          <div className="flex items-center gap-2">
            {getStatusIcon(health.slack.connected, health.slack.status)}
            <span className={`text-xs ${getStatusColor(health.slack.connected, health.slack.status)}`}>
              {getStatusText(health.slack.connected, health.slack.status)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IntegrationStatus;

