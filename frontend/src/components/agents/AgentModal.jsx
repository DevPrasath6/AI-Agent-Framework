import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Dialog } from '@headlessui/react';
import {
  XMarkIcon,
  CpuChipIcon,
  InformationCircleIcon,
} from '@heroicons/react/24/outline';

const AgentModal = ({ isOpen, onClose, agent, mode, onSave }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    type: 'conversational',
    model: 'GPT-4',
    config: {
      maxTokens: 1000,
      temperature: 0.7,
      systemPrompt: '',
    },
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (agent && (mode === 'edit' || mode === 'view')) {
      setFormData({
        name: agent.name || '',
        description: agent.description || '',
        type: agent.type || 'conversational',
        model: agent.model || 'GPT-4',
        config: {
          maxTokens: agent.config?.maxTokens || 1000,
          temperature: agent.config?.temperature || 0.7,
          systemPrompt: agent.config?.systemPrompt || '',
        },
      });
    } else if (mode === 'create') {
      setFormData({
        name: '',
        description: '',
        type: 'conversational',
        model: 'GPT-4',
        config: {
          maxTokens: 1000,
          temperature: 0.7,
          systemPrompt: '',
        },
      });
    }
    setErrors({});
  }, [agent, mode, isOpen]);

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));

    // Clear error for this field
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: null,
      }));
    }
  };

  const handleConfigChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      config: {
        ...prev.config,
        [field]: value,
      },
    }));
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Agent name is required';
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    }

    if (formData.config.maxTokens < 1 || formData.config.maxTokens > 4000) {
      newErrors.maxTokens = 'Max tokens must be between 1 and 4000';
    }

    if (formData.config.temperature < 0 || formData.config.temperature > 2) {
      newErrors.temperature = 'Temperature must be between 0 and 2';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (mode === 'view') {
      onClose();
      return;
    }

    if (validateForm()) {
      onSave({
        ...formData,
        status: mode === 'create' ? 'idle' : agent.status,
        created: mode === 'create' ? new Date().toISOString().split('T')[0] : agent.created,
        lastRun: mode === 'create' ? 'Never' : agent.lastRun,
        successRate: mode === 'create' ? 0 : agent.successRate,
      });
    }
  };

  const modalVariants = {
    hidden: { opacity: 0, scale: 0.95 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: {
        type: 'spring',
        damping: 25,
        stiffness: 300,
      }
    },
    exit: {
      opacity: 0,
      scale: 0.95,
      transition: {
        duration: 0.2,
      }
    },
  };

  const getModalTitle = () => {
    switch (mode) {
      case 'create':
        return 'Create New Agent';
      case 'edit':
        return 'Edit Agent';
      case 'view':
        return 'Agent Details';
      default:
        return 'Agent';
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <Dialog
          as={motion.div}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          open={isOpen}
          onClose={onClose}
          className="relative z-50"
        >
          <div className="fixed inset-0 bg-black/25 backdrop-blur-sm" />

          <div className="fixed inset-0 flex items-center justify-center p-4">
            <Dialog.Panel
              as={motion.div}
              variants={modalVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              className="w-full max-w-2xl bg-white rounded-xl shadow-2xl border border-gray-200 overflow-hidden"
            >
              {/* Header */}
              <div className="flex items-center justify-between p-6 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-purple-50">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg">
                    <CpuChipIcon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <Dialog.Title className="text-xl font-semibold text-gray-900">
                      {getModalTitle()}
                    </Dialog.Title>
                    <p className="text-sm text-gray-600">
                      {mode === 'create' && 'Configure your new AI agent'}
                      {mode === 'edit' && 'Modify agent settings'}
                      {mode === 'view' && 'View agent configuration'}
                    </p>
                  </div>
                </div>

                <button
                  onClick={onClose}
                  className="p-2 text-gray-400 hover:text-gray-600 hover:bg-white rounded-lg transition-colors"
                >
                  <XMarkIcon className="w-5 h-5" />
                </button>
              </div>

              {/* Form */}
              <form onSubmit={handleSubmit} className="p-6 space-y-6">
                {/* Basic Information */}
                <div className="space-y-4">
                  <h3 className="text-lg font-medium text-gray-900">Basic Information</h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Agent Name *
                      </label>
                      <input
                        type="text"
                        value={formData.name}
                        onChange={(e) => handleChange('name', e.target.value)}
                        disabled={mode === 'view'}
                        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
                          errors.name ? 'border-red-300' : 'border-gray-300'
                        } ${mode === 'view' ? 'bg-gray-50' : ''}`}
                        placeholder="Enter agent name"
                      />
                      {errors.name && (
                        <p className="mt-1 text-sm text-red-600">{errors.name}</p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Type
                      </label>
                      <select
                        value={formData.type}
                        onChange={(e) => handleChange('type', e.target.value)}
                        disabled={mode === 'view'}
                        className={`w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
                          mode === 'view' ? 'bg-gray-50' : ''
                        }`}
                      >
                        <option value="conversational">Conversational</option>
                        <option value="utility">Utility</option>
                        <option value="analytical">Analytical</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Description *
                    </label>
                    <textarea
                      value={formData.description}
                      onChange={(e) => handleChange('description', e.target.value)}
                      disabled={mode === 'view'}
                      rows={3}
                      className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
                        errors.description ? 'border-red-300' : 'border-gray-300'
                      } ${mode === 'view' ? 'bg-gray-50' : ''}`}
                      placeholder="Describe what this agent does"
                    />
                    {errors.description && (
                      <p className="mt-1 text-sm text-red-600">{errors.description}</p>
                    )}
                  </div>
                </div>

                {/* Model Configuration */}
                <div className="space-y-4">
                  <h3 className="text-lg font-medium text-gray-900">Model Configuration</h3>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Model
                      </label>
                      <select
                        value={formData.model}
                        onChange={(e) => handleChange('model', e.target.value)}
                        disabled={mode === 'view'}
                        className={`w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
                          mode === 'view' ? 'bg-gray-50' : ''
                        }`}
                      >
                        <option value="GPT-4">GPT-4</option>
                        <option value="GPT-3.5">GPT-3.5</option>
                        <option value="Claude-3">Claude-3</option>
                        <option value="Llama-2">Llama-2</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Max Tokens
                      </label>
                      <input
                        type="number"
                        min="1"
                        max="4000"
                        value={formData.config.maxTokens}
                        onChange={(e) => handleConfigChange('maxTokens', parseInt(e.target.value))}
                        disabled={mode === 'view'}
                        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
                          errors.maxTokens ? 'border-red-300' : 'border-gray-300'
                        } ${mode === 'view' ? 'bg-gray-50' : ''}`}
                      />
                      {errors.maxTokens && (
                        <p className="mt-1 text-sm text-red-600">{errors.maxTokens}</p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Temperature
                      </label>
                      <input
                        type="number"
                        min="0"
                        max="2"
                        step="0.1"
                        value={formData.config.temperature}
                        onChange={(e) => handleConfigChange('temperature', parseFloat(e.target.value))}
                        disabled={mode === 'view'}
                        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
                          errors.temperature ? 'border-red-300' : 'border-gray-300'
                        } ${mode === 'view' ? 'bg-gray-50' : ''}`}
                      />
                      {errors.temperature && (
                        <p className="mt-1 text-sm text-red-600">{errors.temperature}</p>
                      )}
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      System Prompt
                    </label>
                    <textarea
                      value={formData.config.systemPrompt}
                      onChange={(e) => handleConfigChange('systemPrompt', e.target.value)}
                      disabled={mode === 'view'}
                      rows={4}
                      className={`w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
                        mode === 'view' ? 'bg-gray-50' : ''
                      }`}
                      placeholder="Enter system instructions for the agent..."
                    />
                    <div className="mt-1 flex items-center text-xs text-gray-500">
                      <InformationCircleIcon className="w-4 h-4 mr-1" />
                      System prompt defines the agent's behavior and personality
                    </div>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex justify-end space-x-3 pt-6 border-t border-gray-200">
                  <button
                    type="button"
                    onClick={onClose}
                    className="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                  >
                    {mode === 'view' ? 'Close' : 'Cancel'}
                  </button>

                  {mode !== 'view' && (
                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      type="submit"
                      className="px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-medium rounded-lg shadow-lg hover:shadow-xl transition-all duration-200"
                    >
                      {mode === 'create' ? 'Create Agent' : 'Save Changes'}
                    </motion.button>
                  )}
                </div>
              </form>
            </Dialog.Panel>
          </div>
        </Dialog>
      )}
    </AnimatePresence>
  );
};

export default AgentModal;
