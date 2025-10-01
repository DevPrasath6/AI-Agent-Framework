import React from 'react';
import { motion } from 'framer-motion';
import {
  PlayIcon,
  StopIcon,
  PencilIcon,
  ChartBarIcon,
  DocumentTextIcon,
  CogIcon
} from '@heroicons/react/24/outline';
import { Button, Card } from '../common';
import { formatDate, formatRelativeTime, getStatusColor } from '../../utils/helpers';

const AgentDetail = ({ agent, onEdit, onStart, onStop, onViewLogs, onViewMetrics }) => {
  if (!agent) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex items-center justify-center h-64"
      >
        <div className="text-center text-gray-500">
          <DocumentTextIcon className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <p className="text-lg">Select an agent to view details</p>
        </div>
      </motion.div>
    );
  }

  const statusColor = getStatusColor(agent.status);
  const isRunning = agent.status === 'active' || agent.status === 'running';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Header */}
      <Card className="p-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2">
              <h2 className="text-2xl font-bold text-gray-900">{agent.name}</h2>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${statusColor}`}>
                {agent.status}
              </span>
            </div>
            <p className="text-gray-600 mb-4">{agent.description}</p>
            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <span>Created: {formatDate(agent.created_at)}</span>
              <span>Updated: {formatRelativeTime(agent.updated_at)}</span>
              <span>Version: {agent.version || '1.0.0'}</span>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              leftIcon={<PencilIcon className="w-4 h-4" />}
              onClick={() => onEdit(agent)}
            >
              Edit
            </Button>

            {isRunning ? (
              <Button
                variant="danger"
                leftIcon={<StopIcon className="w-4 h-4" />}
                onClick={() => onStop(agent.id)}
              >
                Stop
              </Button>
            ) : (
              <Button
                variant="success"
                leftIcon={<PlayIcon className="w-4 h-4" />}
                onClick={() => onStart(agent.id)}
              >
                Start
              </Button>
            )}
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Configuration */}
        <Card className="p-6">
          <div className="flex items-center mb-4">
            <CogIcon className="w-5 h-5 text-blue-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Configuration</h3>
          </div>

          <div className="space-y-3">
            <div>
              <label className="text-sm font-medium text-gray-500">Model</label>
              <p className="text-gray-900">{agent.model || 'gpt-3.5-turbo'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-500">Temperature</label>
              <p className="text-gray-900">{agent.temperature || 0.7}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-500">Max Tokens</label>
              <p className="text-gray-900">{agent.max_tokens || 1000}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-500">Timeout (ms)</label>
              <p className="text-gray-900">{agent.timeout || 30000}</p>
            </div>
          </div>
        </Card>

        {/* System Prompt */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">System Prompt</h3>
          <div className="bg-gray-50 rounded-lg p-4 max-h-48 overflow-y-auto">
            <pre className="text-sm text-gray-700 whitespace-pre-wrap">
              {agent.system_prompt || 'No system prompt configured'}
            </pre>
          </div>
        </Card>

        {/* Statistics */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Statistics</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{agent.total_executions || 0}</p>
              <p className="text-sm text-gray-500">Total Executions</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">{agent.successful_executions || 0}</p>
              <p className="text-sm text-gray-500">Successful</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-red-600">{agent.failed_executions || 0}</p>
              <p className="text-sm text-gray-500">Failed</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-yellow-600">{agent.avg_response_time || 0}ms</p>
              <p className="text-sm text-gray-500">Avg Response Time</p>
            </div>
          </div>
        </Card>

        {/* Actions */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Actions</h3>
          <div className="space-y-3">
            <Button
              variant="outline"
              className="w-full justify-start"
              leftIcon={<ChartBarIcon className="w-4 h-4" />}
              onClick={() => onViewMetrics(agent.id)}
            >
              View Performance Metrics
            </Button>
            <Button
              variant="outline"
              className="w-full justify-start"
              leftIcon={<DocumentTextIcon className="w-4 h-4" />}
              onClick={() => onViewLogs(agent.id)}
            >
              View Execution Logs
            </Button>
          </div>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
        <div className="space-y-3">
          {agent.recent_activity && agent.recent_activity.length > 0 ? (
            agent.recent_activity.map((activity, index) => (
              <div key={index} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-b-0">
                <div>
                  <p className="text-sm text-gray-900">{activity.action}</p>
                  <p className="text-xs text-gray-500">{formatRelativeTime(activity.timestamp)}</p>
                </div>
                <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(activity.status)}`}>
                  {activity.status}
                </span>
              </div>
            ))
          ) : (
            <p className="text-gray-500 text-center py-4">No recent activity</p>
          )}
        </div>
      </Card>
    </motion.div>
  );
};

export default AgentDetail;
