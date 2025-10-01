import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  MagnifyingGlassIcon,
  PlusIcon,
  PlayIcon,
  StopIcon,
  PencilIcon,
  TrashIcon
} from '@heroicons/react/24/outline';
import { Button, Card, Input } from '../common';
import { formatRelativeTime, getStatusColor } from '../../utils/helpers';

const AgentList = ({
  agents = [],
  loading = false,
  onAgentSelect,
  onAgentCreate,
  onAgentEdit,
  onAgentDelete,
  onAgentStart,
  onAgentStop,
  selectedAgent
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [sortBy, setSortBy] = useState('name');

  // Filter and sort agents
  const filteredAgents = agents
    .filter(agent => {
      const matchesSearch = agent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          agent.description?.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = statusFilter === 'all' || agent.status === statusFilter;
      return matchesSearch && matchesStatus;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.name.localeCompare(b.name);
        case 'status':
          return a.status.localeCompare(b.status);
        case 'created':
          return new Date(b.created_at) - new Date(a.created_at);
        case 'updated':
          return new Date(b.updated_at) - new Date(a.updated_at);
        default:
          return 0;
      }
    });

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: 'spring',
        damping: 25,
        stiffness: 300,
      },
    },
  };

  const handleAgentAction = (e, action, agent) => {
    e.stopPropagation();
    action(agent);
  };

  return (
    <div className="space-y-6">
      {/* Header with Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Agents</h2>
          <p className="text-gray-600">Manage your AI agents</p>
        </div>

        <Button
          leftIcon={<PlusIcon className="w-4 h-4" />}
          onClick={onAgentCreate}
        >
          Create Agent
        </Button>
      </div>

      {/* Filters and Search */}
      <Card className="p-4">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <Input
              placeholder="Search agents..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              leftIcon={<MagnifyingGlassIcon className="w-4 h-4" />}
            />
          </div>

          <div className="flex gap-2">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
              <option value="training">Training</option>
              <option value="error">Error</option>
            </select>

            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="name">Sort by Name</option>
              <option value="status">Sort by Status</option>
              <option value="created">Sort by Created</option>
              <option value="updated">Sort by Updated</option>
            </select>
          </div>
        </div>
      </Card>

      {/* Agent Grid */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          <AnimatePresence>
            {filteredAgents.map((agent) => {
              const statusColor = getStatusColor(agent.status);
              const isSelected = selectedAgent?.id === agent.id;
              const isRunning = agent.status === 'active' || agent.status === 'running';

              return (
                <motion.div
                  key={agent.id}
                  variants={itemVariants}
                  layout
                  exit={{ opacity: 0, scale: 0.9 }}
                  whileHover={{ y: -2 }}
                  onClick={() => onAgentSelect(agent)}
                  className={`cursor-pointer ${isSelected ? 'ring-2 ring-blue-500' : ''}`}
                >
                  <Card hover className="p-6 h-full">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 mb-1">
                          {agent.name}
                        </h3>
                        <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${statusColor}`}>
                          {agent.status}
                        </span>
                      </div>

                      <div className="flex items-center space-x-1">
                        <button
                          onClick={(e) => handleAgentAction(e, onAgentEdit, agent)}
                          className="p-1 text-gray-400 hover:text-blue-600 transition-colors"
                          title="Edit Agent"
                        >
                          <PencilIcon className="w-4 h-4" />
                        </button>

                        {isRunning ? (
                          <button
                            onClick={(e) => handleAgentAction(e, () => onAgentStop(agent.id), agent)}
                            className="p-1 text-gray-400 hover:text-red-600 transition-colors"
                            title="Stop Agent"
                          >
                            <StopIcon className="w-4 h-4" />
                          </button>
                        ) : (
                          <button
                            onClick={(e) => handleAgentAction(e, () => onAgentStart(agent.id), agent)}
                            className="p-1 text-gray-400 hover:text-green-600 transition-colors"
                            title="Start Agent"
                          >
                            <PlayIcon className="w-4 h-4" />
                          </button>
                        )}

                        <button
                          onClick={(e) => handleAgentAction(e, () => onAgentDelete(agent.id), agent)}
                          className="p-1 text-gray-400 hover:text-red-600 transition-colors"
                          title="Delete Agent"
                        >
                          <TrashIcon className="w-4 h-4" />
                        </button>
                      </div>
                    </div>

                    <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                      {agent.description || 'No description available'}
                    </p>

                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span>Model: {agent.model || 'gpt-3.5-turbo'}</span>
                      <span>{formatRelativeTime(agent.updated_at)}</span>
                    </div>

                    {/* Statistics */}
                    <div className="mt-4 pt-4 border-t border-gray-100">
                      <div className="flex justify-between text-xs">
                        <span className="text-gray-500">Executions: {agent.total_executions || 0}</span>
                        <span className="text-green-600">Success: {agent.successful_executions || 0}</span>
                        <span className="text-red-600">Failed: {agent.failed_executions || 0}</span>
                      </div>
                    </div>
                  </Card>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </motion.div>
      )}

      {/* Empty State */}
      {!loading && filteredAgents.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-12"
        >
          <div className="text-gray-400 mb-4">
            <svg className="mx-auto h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {searchTerm || statusFilter !== 'all' ? 'No agents found' : 'No agents yet'}
          </h3>
          <p className="text-gray-500 mb-6">
            {searchTerm || statusFilter !== 'all'
              ? 'Try adjusting your search or filter criteria.'
              : 'Get started by creating your first AI agent.'
            }
          </p>
          {(!searchTerm && statusFilter === 'all') && (
            <Button
              leftIcon={<PlusIcon className="w-4 h-4" />}
              onClick={onAgentCreate}
            >
              Create Your First Agent
            </Button>
          )}
        </motion.div>
      )}
    </div>
  );
};

export default AgentList;
