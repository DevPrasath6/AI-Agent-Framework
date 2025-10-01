import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  PlusIcon,
  PlayIcon,
  PauseIcon,
  PencilIcon,
  TrashIcon,
  DocumentDuplicateIcon,
  CogIcon,
  UserIcon,
  ChartBarIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  FunnelIcon,
  MagnifyingGlassIcon,
  CpuChipIcon,
  BoltIcon
} from '@heroicons/react/24/outline';

// Components
import Navigation from '../components/navigation/Navigation';

const Agents = () => {
  const [agents, setAgents] = useState([
    {
      id: 1,
      name: 'Customer Support Assistant',
      description: 'Handles customer inquiries and provides automated support responses',
      type: 'Chat Bot',
      status: 'active',
      model: 'GPT-4',
      lastActive: '2024-09-24T11:45:00Z',
      totalInteractions: 1247,
      successRate: 94.2,
      tags: ['Customer Support', 'Chat', 'AI']
    },
    {
      id: 2,
      name: 'Data Analyst Agent',
      description: 'Analyzes data patterns and generates insights from business metrics',
      type: 'Analytics',
      status: 'active',
      model: 'Claude-3',
      lastActive: '2024-09-24T10:20:00Z',
      totalInteractions: 89,
      successRate: 98.9,
      tags: ['Analytics', 'Data', 'Insights']
    },
    {
      id: 3,
      name: 'Content Generator',
      description: 'Creates marketing content, blog posts, and social media updates',
      type: 'Content',
      status: 'paused',
      model: 'GPT-4',
      lastActive: '2024-09-23T16:30:00Z',
      totalInteractions: 456,
      successRate: 91.7,
      tags: ['Content', 'Marketing', 'Writing']
    },
    {
      id: 4,
      name: 'Code Review Assistant',
      description: 'Reviews code submissions and provides development suggestions',
      type: 'Development',
      status: 'error',
      model: 'CodeLlama',
      lastActive: '2024-09-24T08:15:00Z',
      totalInteractions: 234,
      successRate: 89.3,
      tags: ['Development', 'Code Review', 'QA']
    },
    {
      id: 5,
      name: 'Email Classifier',
      description: 'Categorizes incoming emails and routes them to appropriate departments',
      type: 'Classification',
      status: 'active',
      model: 'BERT',
      lastActive: '2024-09-24T11:55:00Z',
      totalInteractions: 2341,
      successRate: 96.8,
      tags: ['Email', 'Classification', 'Routing']
    }
  ]);

  const [filterStatus, setFilterStatus] = useState('all');
  const [filterType, setFilterType] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showConfigModal, setShowConfigModal] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState(null);

  const agentTypes = ['Chat Bot', 'Analytics', 'Content', 'Development', 'Classification'];
  const models = ['GPT-4', 'Claude-3', 'CodeLlama', 'BERT', 'Gemini-Pro'];

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      case 'paused':
        return <PauseIcon className="w-5 h-5 text-yellow-500" />;
      case 'error':
        return <XCircleIcon className="w-5 h-5 text-red-500" />;
      default:
        return <ClockIcon className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'paused':
        return 'bg-yellow-100 text-yellow-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'Chat Bot':
        return <UserIcon className="w-5 h-5 text-blue-500" />;
      case 'Analytics':
        return <ChartBarIcon className="w-5 h-5 text-purple-500" />;
      case 'Content':
        return <PencilIcon className="w-5 h-5 text-green-500" />;
      case 'Development':
        return <CpuChipIcon className="w-5 h-5 text-orange-500" />;
      case 'Classification':
        return <BoltIcon className="w-5 h-5 text-indigo-500" />;
      default:
        return <CogIcon className="w-5 h-5 text-gray-500" />;
    }
  };

  const filteredAgents = agents.filter(agent => {
    const matchesStatus = filterStatus === 'all' || agent.status === filterStatus;
    const matchesType = filterType === 'all' || agent.type === filterType;
    const matchesSearch = agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         agent.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesStatus && matchesType && matchesSearch;
  });

  const handleStatusToggle = (id) => {
    setAgents(agents.map(agent =>
      agent.id === id
        ? {
            ...agent,
            status: agent.status === 'active' ? 'paused' : 'active'
          }
        : agent
    ));
  };

  const handleDelete = (id) => {
    setAgents(agents.filter(agent => agent.id !== id));
  };

  const handleConfigure = (agent) => {
    setSelectedAgent(agent);
    setShowConfigModal(true);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <Navigation />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">AI Agents</h1>
            <p className="text-gray-600 mt-2">Deploy and manage your AI agents across different tasks</p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="mt-4 md:mt-0 bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all duration-200 flex items-center space-x-2"
          >
            <PlusIcon className="w-5 h-5" />
            <span>Create Agent</span>
          </button>
        </div>

        {/* Filters and Search */}
        <div className="mt-8 flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
          <div className="flex items-center space-x-4">
            <div className="relative">
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="appearance-none bg-white/70 backdrop-blur-sm border border-gray-300 rounded-lg px-4 py-2 pr-8 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="all">All Status</option>
                <option value="active">Active</option>
                <option value="paused">Paused</option>
                <option value="error">Error</option>
              </select>
              <FunnelIcon className="w-4 h-4 text-gray-400 absolute right-2 top-1/2 transform -translate-y-1/2 pointer-events-none" />
            </div>

            <div className="relative">
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="appearance-none bg-white/70 backdrop-blur-sm border border-gray-300 rounded-lg px-4 py-2 pr-8 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="all">All Types</option>
                {agentTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
              <FunnelIcon className="w-4 h-4 text-gray-400 absolute right-2 top-1/2 transform -translate-y-1/2 pointer-events-none" />
            </div>
          </div>

          <div className="relative">
            <input
              type="text"
              placeholder="Search agents..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-white/70 backdrop-blur-sm border border-gray-300 rounded-lg pl-10 pr-4 py-2 w-full sm:w-80 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
            <MagnifyingGlassIcon className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
          </div>
        </div>
      </div>

      {/* Agents Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAgents.map((agent, index) => (
            <motion.div
              key={agent.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="backdrop-blur-xl bg-white/70 rounded-xl p-6 border border-white/20 hover:shadow-2xl hover:scale-105 transition-all duration-300"
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  {getTypeIcon(agent.type)}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 truncate">
                      {agent.name}
                    </h3>
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(agent.status)}
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(agent.status)}`}>
                        {agent.status}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Type and Model */}
              <div className="flex items-center justify-between mb-4">
                <span className="px-3 py-1 bg-gray-100 text-gray-800 text-sm rounded-full">
                  {agent.type}
                </span>
                <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                  {agent.model}
                </span>
              </div>

              {/* Description */}
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                {agent.description}
              </p>

              {/* Tags */}
              <div className="flex flex-wrap gap-2 mb-4">
                {agent.tags.map((tag, tagIndex) => (
                  <span
                    key={tagIndex}
                    className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full"
                  >
                    {tag}
                  </span>
                ))}
              </div>

              {/* Stats */}
              <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
                <div>
                  <div className="text-gray-500">Interactions</div>
                  <div className="font-semibold text-gray-900">{agent.totalInteractions.toLocaleString()}</div>
                </div>
                <div>
                  <div className="text-gray-500">Success Rate</div>
                  <div className="font-semibold text-gray-900">{agent.successRate}%</div>
                </div>
              </div>

              {/* Last Active */}
              <div className="text-xs text-gray-500 mb-4">
                Last active: {formatDate(agent.lastActive)}
              </div>

              {/* Actions */}
              <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => handleStatusToggle(agent.id)}
                    className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                    title={agent.status === 'active' ? 'Pause' : 'Start'}
                  >
                    {agent.status === 'active' ?
                      <PauseIcon className="w-4 h-4" /> :
                      <PlayIcon className="w-4 h-4" />
                    }
                  </button>

                  <button
                    onClick={() => handleConfigure(agent)}
                    className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                    title="Configure"
                  >
                    <CogIcon className="w-4 h-4" />
                  </button>

                  <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors" title="Edit">
                    <PencilIcon className="w-4 h-4" />
                  </button>

                  <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors" title="Duplicate">
                    <DocumentDuplicateIcon className="w-4 h-4" />
                  </button>
                </div>

                <button
                  onClick={() => handleDelete(agent.id)}
                  className="p-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-lg transition-colors"
                  title="Delete"
                >
                  <TrashIcon className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Empty State */}
        {filteredAgents.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <div className="backdrop-blur-xl bg-white/70 border border-gray-200 rounded-2xl shadow-xl p-8 max-w-md mx-auto">
              <div className="text-gray-400 mb-4">
                <CpuChipIcon className="w-16 h-16 mx-auto" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No agents found</h3>
              <p className="text-gray-600 mb-4">
                {searchQuery || filterStatus !== 'all' || filterType !== 'all'
                  ? 'Try adjusting your search or filters'
                  : 'Get started by creating your first AI agent'
                }
              </p>
              {(!searchQuery && filterStatus === 'all' && filterType === 'all') && (
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all duration-200"
                >
                  Create Agent
                </button>
              )}
            </div>
          </motion.div>
        )}
      </div>

      {/* Create Agent Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4">
            <div className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm" onClick={() => setShowCreateModal(false)}></div>

            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="relative backdrop-blur-xl bg-white/70 rounded-xl p-8 max-w-lg w-full border border-white/20 shadow-2xl"
            >
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Create New Agent</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Agent Name
                  </label>
                  <input
                    type="text"
                    className="w-full px-4 py-3 bg-white/50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="Enter agent name"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Description
                  </label>
                  <textarea
                    rows={3}
                    className="w-full px-4 py-3 bg-white/50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="Describe what this agent does"
                  ></textarea>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Agent Type
                    </label>
                    <select className="w-full px-4 py-3 bg-white/50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                      <option value="">Select type</option>
                      {agentTypes.map(type => (
                        <option key={type} value={type}>{type}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      AI Model
                    </label>
                    <select className="w-full px-4 py-3 bg-white/50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                      <option value="">Select model</option>
                      {models.map(model => (
                        <option key={model} value={model}>{model}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    System Prompt
                  </label>
                  <textarea
                    rows={4}
                    className="w-full px-4 py-3 bg-white/50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="Define the agent's behavior and instructions..."
                  ></textarea>
                </div>
              </div>

              <div className="flex justify-end space-x-4 mt-8">
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="px-6 py-2 text-gray-700 hover:text-gray-900 font-medium"
                >
                  Cancel
                </button>
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all duration-200"
                >
                  Create Agent
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      )}

      {/* Configure Agent Modal */}
      {showConfigModal && selectedAgent && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4">
            <div className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm" onClick={() => setShowConfigModal(false)}></div>

            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="relative backdrop-blur-xl bg-white/90 border border-gray-200 rounded-3xl shadow-2xl p-8 max-w-2xl w-full max-h-[80vh] overflow-y-auto"
            >
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Configure {selectedAgent.name}</h2>

              <div className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Response Timeout (ms)
                    </label>
                    <input
                      type="number"
                      defaultValue="5000"
                      className="w-full px-4 py-3 bg-white/50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Max Tokens
                    </label>
                    <input
                      type="number"
                      defaultValue="2048"
                      className="w-full px-4 py-3 bg-white/50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Temperature
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    defaultValue="0.7"
                    className="w-full"
                  />
                  <div className="flex justify-between text-sm text-gray-500 mt-1">
                    <span>Focused (0)</span>
                    <span>Creative (1)</span>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    System Instructions
                  </label>
                  <textarea
                    rows={6}
                    defaultValue={`You are ${selectedAgent.name}, a ${selectedAgent.type} agent. Your role is to ${selectedAgent.description.toLowerCase()}.`}
                    className="w-full px-4 py-3 bg-white/50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  ></textarea>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Features</h3>
                  <div className="space-y-3">
                    <label className="flex items-center">
                      <input type="checkbox" defaultChecked className="rounded border-gray-300 text-purple-600 focus:ring-purple-500" />
                      <span className="ml-2 text-sm text-gray-700">Enable conversation memory</span>
                    </label>
                    <label className="flex items-center">
                      <input type="checkbox" defaultChecked className="rounded border-gray-300 text-purple-600 focus:ring-purple-500" />
                      <span className="ml-2 text-sm text-gray-700">Log all interactions</span>
                    </label>
                    <label className="flex items-center">
                      <input type="checkbox" className="rounded border-gray-300 text-purple-600 focus:ring-purple-500" />
                      <span className="ml-2 text-sm text-gray-700">Enable web search</span>
                    </label>
                    <label className="flex items-center">
                      <input type="checkbox" className="rounded border-gray-300 text-purple-600 focus:ring-purple-500" />
                      <span className="ml-2 text-sm text-gray-700">Allow file attachments</span>
                    </label>
                  </div>
                </div>
              </div>

              <div className="flex justify-end space-x-4 mt-8">
                <button
                  onClick={() => setShowConfigModal(false)}
                  className="px-6 py-2 text-gray-700 hover:text-gray-900 font-medium"
                >
                  Cancel
                </button>
                <button
                  onClick={() => setShowConfigModal(false)}
                  className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all duration-200"
                >
                  Save Configuration
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Agents;
