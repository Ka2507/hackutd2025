/**
 * Integration Status Component
 * Shows connection status for Jira, Figma, and Slack
 */
import { useState, useEffect } from 'react';
import { CheckCircle, XCircle, AlertCircle, Target } from 'lucide-react';

interface IntegrationHealth {
  jira: { connected: boolean; status: string };
  figma: { connected: boolean; status: string };
  slack: { connected: boolean; status: string };
}

// Figma Logo Component
const FigmaLogo = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M8 24c2.208 0 4-1.792 4-4v-4H8c-2.208 0-4 1.792-4 4s1.792 4 4 4z" fill="#0ACF83"/>
    <path d="M4 12c0-2.208 1.792-4 4-4h4v8H8c-2.208 0-4-1.792-4-4z" fill="#A259FF"/>
    <path d="M4 4c0-2.208 1.792-4 4-4h4v8H8C5.792 8 4 6.208 4 4z" fill="#F24E1E"/>
    <path d="M12 0h4c2.208 0 4 1.792 4 4s-1.792 4-4 4h-4V0z" fill="#FF7262"/>
    <path d="M20 12c0 2.208-1.792 4-4 4s-4-1.792-4-4 1.792-4 4-4 4 1.792 4 4z" fill="#1ABCFE"/>
  </svg>
);

// Slack Logo Component
const SlackLogo = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M5.042 15.165a2.528 2.528 0 0 1-2.52 2.523A2.528 2.528 0 0 1 0 15.165a2.527 2.527 0 0 1 2.522-2.52h2.52v2.52z" fill="#E01E5A"/>
    <path d="M6.313 15.165a2.527 2.527 0 0 1 2.521-2.52 2.527 2.527 0 0 1 2.521 2.52v6.313A2.528 2.528 0 0 1 8.834 24a2.528 2.528 0 0 1-2.521-2.522v-6.313z" fill="#E01E5A"/>
    <path d="M8.834 5.042a2.528 2.528 0 0 1-2.521-2.52A2.528 2.528 0 0 1 8.834 0a2.528 2.528 0 0 1 2.521 2.522v2.52H8.834z" fill="#36C5F0"/>
    <path d="M8.834 6.313a2.528 2.528 0 0 1 2.521 2.521 2.528 2.528 0 0 1-2.521 2.521H2.522A2.528 2.528 0 0 1 0 8.834a2.528 2.528 0 0 1 2.522-2.521h6.312z" fill="#36C5F0"/>
    <path d="M18.956 8.834a2.528 2.528 0 0 1 2.522-2.521A2.528 2.528 0 0 1 24 8.834a2.528 2.528 0 0 1-2.522 2.521h-2.522V8.834z" fill="#2EB67D"/>
    <path d="M17.688 8.834a2.528 2.528 0 0 1-2.523 2.521 2.527 2.527 0 0 1-2.52-2.521V2.522A2.527 2.527 0 0 1 15.165 0a2.528 2.528 0 0 1 2.523 2.522v6.312z" fill="#2EB67D"/>
    <path d="M15.165 18.956a2.528 2.528 0 0 1 2.523 2.522A2.528 2.528 0 0 1 15.165 24a2.527 2.527 0 0 1-2.52-2.522v-2.522h2.52z" fill="#ECB22E"/>
    <path d="M15.165 17.688a2.527 2.527 0 0 1-2.52-2.523 2.526 2.526 0 0 1 2.52-2.52h6.313A2.527 2.527 0 0 1 24 15.165a2.528 2.528 0 0 1-2.522 2.523h-6.313z" fill="#ECB22E"/>
  </svg>
);

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
            <FigmaLogo className="w-4 h-4" />
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
            <SlackLogo className="w-4 h-4" />
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

