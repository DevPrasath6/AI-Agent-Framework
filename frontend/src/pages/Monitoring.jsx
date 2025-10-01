import React, { useState, useEffect, useMemo } from 'react';
import { motion } from 'framer-motion';
import {
  ChartBarIcon,
  CpuChipIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowTrendingUpIcon,
  DocumentTextIcon,
  FunnelIcon,
  MagnifyingGlassIcon,
  PlayIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline';

import Navigation from '../components/navigation/Navigation';

const Monitoring = () => {
  const [logs, setLogs] = useState([
    {
      id: 1,
      timestamp: '2024-09-24T11:55:23Z',
      level: 'info',
      source: 'Customer Support Assistant',
      message: 'Successfully processed user inquiry about billing',
      duration: '1.2s',
      status: 'success'
    },
    {
      id: 2,
      timestamp: '2024-09-24T11:54:15Z',
      level: 'error',
      source: 'Code Review Assistant',
      message: 'Failed to connect to GitHub API - timeout after 30s',
      duration: '30.0s',
      status: 'error'
    },
    {
      id: 3,
      timestamp: '2024-09-24T11:53:45Z',
      level: 'warning',
      source: 'Data Analyst Agent',
      message: 'High memory usage detected: 85% of allocated memory',
      duration: '0.5s',
      status: 'warning'
    },
    {
      id: 4,
      timestamp: '2024-09-24T11:52:30Z',
      level: 'info',
      source: 'Email Classifier',
      message: 'Processed batch of 150 emails with 98.7% accuracy',
      duration: '2.8s',
      status: 'success'
    }
  ]);

  const [filterLevel, setFilterLevel] = useState('all');
  const [filterSource, setFilterSource] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [refreshInterval] = useState(5000);

  const [systemMetrics] = useState({
    cpuUsage: 45,
    memoryUsage: 68,
    activeAgents: 4,
    totalRequests: 2547,
    avgResponseTime: 1.8,
    errorRate: 2.3,
    successRate: 97.7,
    uptime: '15d 8h 23m'
  });

  const [workflowStats] = useState([
    { name: 'Customer Onboarding', executions: 45, success: 43, failed: 2, avgTime: '2.5s' },
    { name: 'Data Processing', executions: 23, success: 22, failed: 1, avgTime: '8.7s' },
    { name: 'Content Review', executions: 67, success: 65, failed: 2, avgTime: '3.1s' },
    { name: 'Email Analysis', executions: 156, success: 152, failed: 4, avgTime: '1.2s' }
  ]);

  const sources = useMemo(() => ['Customer Support Assistant', 'Code Review Assistant', 'Data Analyst Agent', 'Email Classifier'], []);
  const levels = ['info', 'warning', 'error'];

  useEffect(() => {
    if (!autoRefresh) return;
    const interval = setInterval(() => {
      console.log('Auto-refreshing logs...');
    }, refreshInterval);
    return () => clearInterval(interval);
  }, [autoRefresh, refreshInterval]);

  const filteredLogs = useMemo(() => {
    return logs.filter(log => {
      const matchesLevel = filterLevel === 'all' || log.level === filterLevel;
      const matchesSource = filterSource === 'all' || log.source === filterSource;
      const matchesSearch = searchQuery === '' ||
        log.message.toLowerCase().includes(searchQuery.toLowerCase()) ||
        log.source.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesLevel && matchesSource && matchesSearch;
    });
  }, [logs, filterLevel, filterSource, searchQuery]);

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  const getLevelIcon = (level) => {
    switch (level) {
      case 'error': return <XCircleIcon className="w-5 h-5 text-red-500" />;
      case 'warning': return <ExclamationTriangleIcon className="w-5 h-5 text-yellow-500" />;
      case 'info': return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      default: return <DocumentTextIcon className="w-5 h-5 text-gray-500" />;
    }
  };

  const getLevelColor = (level) => {
    switch (level) {
      case 'error': return 'bg-red-100 text-red-800';
      case 'warning': return 'bg-yellow-100 text-yellow-800';
      case 'info': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getSuccessRate = (success, total) => {
    return ((success / total) * 100).toFixed(1);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <Navigation />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-8"
        >
          <div>
            <h1 className="text-3xl font-bold text-gray-900">System Monitoring</h1>
            <p className="text-gray-600 mt-2">Monitor your AI agents and system performance in real-time</p>
          </div>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setAutoRefresh(!autoRefresh)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2 ${
              autoRefresh
                ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                : 'backdrop-blur-xl bg-white/70 text-gray-700 border border-gray-200'
            }`}
          >
            <ArrowPathIcon className={`w-4 h-4 ${autoRefresh ? 'animate-spin' : ''}`} />
            <span>{autoRefresh ? 'Auto Refresh On' : 'Auto Refresh Off'}</span>
          </motion.button>
        </motion.div>

        {/* System Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="backdrop-blur-xl bg-white/70 rounded-xl p-6 border border-white/20"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">CPU Usage</p>
                <p className="text-2xl font-bold text-gray-900">{systemMetrics.cpuUsage}%</p>
              </div>
              <CpuChipIcon className="w-8 h-8 text-purple-600" />
            </div>
            <div className="mt-4 bg-gray-200 rounded-full h-2">
              <div
                className="bg-gradient-to-r from-purple-600 to-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${systemMetrics.cpuUsage}%` }}
              />
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="backdrop-blur-xl bg-white/70 rounded-xl p-6 border border-white/20"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Memory Usage</p>
                <p className="text-2xl font-bold text-gray-900">{systemMetrics.memoryUsage}%</p>
              </div>
              <ChartBarIcon className="w-8 h-8 text-blue-600" />
            </div>
            <div className="mt-4 bg-gray-200 rounded-full h-2">
              <div
                className="bg-gradient-to-r from-blue-600 to-purple-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${systemMetrics.memoryUsage}%` }}
              />
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="backdrop-blur-xl bg-white/70 rounded-xl p-6 border border-white/20"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Active Agents</p>
                <p className="text-2xl font-bold text-gray-900">{systemMetrics.activeAgents}</p>
              </div>
              <PlayIcon className="w-8 h-8 text-green-600" />
            </div>
            <p className="text-sm text-gray-600 mt-2">Currently running</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="backdrop-blur-xl bg-white/70 rounded-xl p-6 border border-white/20"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Success Rate</p>
                <p className="text-2xl font-bold text-gray-900">{systemMetrics.successRate}%</p>
              </div>
              <ArrowTrendingUpIcon className="w-8 h-8 text-green-600" />
            </div>
            <p className="text-sm text-gray-600 mt-2">Last 24 hours</p>
          </motion.div>
        </div>

        {/* Workflow Statistics */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="backdrop-blur-xl bg-white/70 rounded-xl p-6 border border-white/20 mb-8"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Workflow Execution Statistics</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Workflow</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Executions</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Success Rate</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Avg Time</th>
                </tr>
              </thead>
              <tbody>
                {workflowStats.map((workflow, index) => (
                  <motion.tr
                    key={workflow.name}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 + index * 0.1 }}
                    className="border-b border-gray-100 hover:bg-white/50 transition-colors"
                  >
                    <td className="py-4 px-4 font-medium text-gray-900">{workflow.name}</td>
                    <td className="py-4 px-4 text-gray-700">{workflow.executions}</td>
                    <td className="py-4 px-4">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                        getSuccessRate(workflow.success, workflow.executions) >= 95
                          ? 'bg-green-100 text-green-800'
                          : getSuccessRate(workflow.success, workflow.executions) >= 90
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {getSuccessRate(workflow.success, workflow.executions)}%
                      </span>
                    </td>
                    <td className="py-4 px-4 text-gray-700">{workflow.avgTime}</td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>

        {/* Logs Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="backdrop-blur-xl bg-white/70 rounded-xl p-6 border border-white/20 mb-8"
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">System Logs</h2>
            <div className="flex items-center space-x-4">
              <div className="relative">
                <MagnifyingGlassIcon className="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search logs..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white/80 backdrop-blur-sm"
                />
              </div>

              <select
                value={filterLevel}
                onChange={(e) => setFilterLevel(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white/80 backdrop-blur-sm"
              >
                <option value="all">All Levels</option>
                {levels.map(level => (
                  <option key={level} value={level}>{level.charAt(0).toUpperCase() + level.slice(1)}</option>
                ))}
              </select>

              <select
                value={filterSource}
                onChange={(e) => setFilterSource(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white/80 backdrop-blur-sm"
              >
                <option value="all">All Sources</option>
                {sources.map(source => (
                  <option key={source} value={source}>{source}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="space-y-2 max-h-96 overflow-y-auto">
            {filteredLogs.map((log, index) => (
              <motion.div
                key={log.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="flex items-center space-x-4 p-4 bg-white/50 rounded-lg border border-gray-100 hover:bg-white/70 transition-colors"
              >
                <div className="flex items-center space-x-2">
                  {getLevelIcon(log.level)}
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${getLevelColor(log.level)}`}>
                    {log.level.toUpperCase()}
                  </span>
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {log.source}
                    </p>
                    <div className="flex items-center space-x-2 text-xs text-gray-500">
                      <span>{log.duration}</span>
                      <span>{formatDate(log.timestamp)}</span>
                    </div>
                  </div>
                  <p className="text-sm text-gray-700 mt-1">{log.message}</p>
                </div>
              </motion.div>
            ))}
          </div>

          {filteredLogs.length === 0 && (
            <div className="text-center py-8">
              <DocumentTextIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">No logs found matching your filters</p>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default Monitoring;
