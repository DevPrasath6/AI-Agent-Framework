import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MagnifyingGlassIcon, CommandLineIcon } from '@heroicons/react/24/outline';

// 🎯 QUICK WIN #1: Command Palette (⌘+K)
export const CommandPalette = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);

  const commands = [
    {
      id: 'create-workflow',
      name: 'Create New Workflow',
      shortcut: '⌘N',
      description: 'Start building a new automation',
      action: () => window.location.href = '/workflows/create'
    },
    {
      id: 'search-workflows',
      name: 'Search Workflows',
      shortcut: '⌘K',
      description: 'Find existing workflows',
      action: () => window.location.href = '/workflows'
    },
    {
      id: 'open-settings',
      name: 'Open Settings',
      shortcut: '⌘,',
      description: 'Configure your account',
      action: () => window.location.href = '/settings'
    },
    {
      id: 'view-dashboard',
      name: 'View Dashboard',
      shortcut: '⌘D',
      description: 'See workflow analytics',
      action: () => window.location.href = '/dashboard'
    },
  ];

  const filteredCommands = commands.filter(cmd =>
    cmd.name.toLowerCase().includes(query.toLowerCase()) ||
    cmd.description.toLowerCase().includes(query.toLowerCase())
  );

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Open command palette with ⌘+K or Ctrl+K
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen(true);
      }

      // Close with Escape
      if (e.key === 'Escape') {
        setIsOpen(false);
        setQuery('');
      }

      // Navigation with arrow keys
      if (isOpen) {
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          setSelectedIndex(prev =>
            prev < filteredCommands.length - 1 ? prev + 1 : 0
          );
        }

        if (e.key === 'ArrowUp') {
          e.preventDefault();
          setSelectedIndex(prev =>
            prev > 0 ? prev - 1 : filteredCommands.length - 1
          );
        }

        if (e.key === 'Enter' && filteredCommands[selectedIndex]) {
          e.preventDefault();
          filteredCommands[selectedIndex].action();
          setIsOpen(false);
          setQuery('');
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, selectedIndex, filteredCommands]);

  // Reset selection when query changes
  useEffect(() => {
    setSelectedIndex(0);
  }, [query]);

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-start justify-center pt-[20vh] px-4"
        >
          <div
            className="absolute inset-0 bg-black/20 backdrop-blur-sm"
            onClick={() => setIsOpen(false)}
          />

          <motion.div
            initial={{ scale: 0.8, y: 20 }}
            animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.8, y: 20 }}
            className="relative w-full max-w-2xl bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-gray-200/50 overflow-hidden"
          >
            {/* Search Input */}
            <div className="flex items-center p-4 border-b border-gray-200">
              <MagnifyingGlassIcon className="w-5 h-5 text-gray-400 mr-3" />
              <input
                type="text"
                placeholder="Type a command or search..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="flex-1 text-lg bg-transparent border-none outline-none placeholder-gray-500"
                autoFocus
              />
              <kbd className="px-2 py-1 bg-gray-100 rounded text-xs text-gray-600">
                ESC
              </kbd>
            </div>

            {/* Commands List */}
            <div className="max-h-80 overflow-y-auto">
              {filteredCommands.length > 0 ? (
                filteredCommands.map((command, index) => (
                  <motion.div
                    key={command.id}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: index * 0.05 }}
                    className={`flex items-center justify-between px-4 py-3 cursor-pointer transition-colors ${
                      index === selectedIndex ? 'bg-rose-50 border-l-4 border-rose-500' : 'hover:bg-gray-50'
                    }`}
                    onClick={() => {
                      command.action();
                      setIsOpen(false);
                      setQuery('');
                    }}
                  >
                    <div className="flex items-center space-x-3">
                      <CommandLineIcon className="w-4 h-4 text-gray-400" />
                      <div>
                        <div className="font-medium text-gray-900">{command.name}</div>
                        <div className="text-sm text-gray-500">{command.description}</div>
                      </div>
                    </div>
                    <kbd className="px-2 py-1 bg-gray-100 rounded text-xs text-gray-600">
                      {command.shortcut}
                    </kbd>
                  </motion.div>
                ))
              ) : (
                <div className="px-4 py-8 text-center text-gray-500">
                  No commands found for "{query}"
                </div>
              )}
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

// 🎯 QUICK WIN #2: Loading Skeletons
export const WorkflowCardSkeleton = () => (
  <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 animate-pulse">
    <div className="flex items-center space-x-4 mb-4">
      <div className="w-4 h-4 bg-gray-200 rounded"></div>
      <div className="flex-1">
        <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
        <div className="h-3 bg-gray-200 rounded w-1/2"></div>
      </div>
    </div>
    <div className="space-y-2">
      <div className="h-3 bg-gray-200 rounded w-full"></div>
      <div className="h-3 bg-gray-200 rounded w-2/3"></div>
    </div>
    <div className="flex items-center justify-between mt-4">
      <div className="flex space-x-2">
        <div className="h-6 bg-gray-200 rounded-full w-16"></div>
        <div className="h-6 bg-gray-200 rounded-full w-20"></div>
      </div>
      <div className="flex space-x-2">
        <div className="w-8 h-8 bg-gray-200 rounded"></div>
        <div className="w-8 h-8 bg-gray-200 rounded"></div>
      </div>
    </div>
  </div>
);

// 🎯 QUICK WIN #3: Real-time Status Indicators
export const StatusIndicator = ({ status, withPulse = false }) => {
  const statusConfig = {
    running: { color: 'bg-green-500', label: 'Running', pulseColor: 'bg-green-400' },
    paused: { color: 'bg-yellow-500', label: 'Paused', pulseColor: 'bg-yellow-400' },
    error: { color: 'bg-red-500', label: 'Error', pulseColor: 'bg-red-400' },
    stopped: { color: 'bg-gray-500', label: 'Stopped', pulseColor: 'bg-gray-400' },
  };

  const config = statusConfig[status] || statusConfig.stopped;

  return (
    <div className="flex items-center space-x-2">
      <div className="relative">
        <div className={`w-3 h-3 rounded-full ${config.color}`} />
        {withPulse && (
          <div className={`absolute inset-0 rounded-full ${config.pulseColor} animate-ping opacity-75`} />
        )}
      </div>
      <span className="text-sm font-medium text-gray-700">{config.label}</span>
    </div>
  );
};

// 🎯 QUICK WIN #4: Contextual Tooltips
export const SmartTooltip = ({ children, content, position = 'top' }) => {
  const [isVisible, setIsVisible] = useState(false);

  const positionClasses = {
    top: '-top-2 left-1/2 transform -translate-x-1/2 -translate-y-full',
    bottom: '-bottom-2 left-1/2 transform -translate-x-1/2 translate-y-full',
    left: '-left-2 top-1/2 transform -translate-x-full -translate-y-1/2',
    right: '-right-2 top-1/2 transform translate-x-full -translate-y-1/2',
  };

  return (
    <div
      className="relative inline-block"
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
    >
      {children}

      <AnimatePresence>
        {isVisible && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            transition={{ duration: 0.15 }}
            className={`absolute z-50 px-3 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg shadow-lg whitespace-nowrap ${positionClasses[position]}`}
          >
            {content}
            {/* Arrow */}
            <div className={`absolute w-2 h-2 bg-gray-900 transform rotate-45 ${
              position === 'top' ? 'bottom-[-4px] left-1/2 -translate-x-1/2' :
              position === 'bottom' ? 'top-[-4px] left-1/2 -translate-x-1/2' :
              position === 'left' ? 'right-[-4px] top-1/2 -translate-y-1/2' :
              'left-[-4px] top-1/2 -translate-y-1/2'
            }`} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

// 🎯 QUICK WIN #5: Interactive Progress Bar
export const ProgressBar = ({ value, max = 100, label, showPercentage = true }) => {
  const percentage = Math.round((value / max) * 100);

  return (
    <div className="w-full">
      {(label || showPercentage) && (
        <div className="flex justify-between items-center mb-2">
          {label && <span className="text-sm font-medium text-gray-700">{label}</span>}
          {showPercentage && <span className="text-sm text-gray-500">{percentage}%</span>}
        </div>
      )}

      <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          className="h-full bg-gradient-to-r from-rose-500 to-orange-500 rounded-full relative overflow-hidden"
        >
          {/* Shimmer effect */}
          <div className="absolute inset-0 -skew-x-12 -inset-x-10 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer" />
        </motion.div>
      </div>
    </div>
  );
};

// Export all components
const QuickWinsComponents = {
  CommandPalette,
  WorkflowCardSkeleton,
  StatusIndicator,
  SmartTooltip,
  ProgressBar
};

export default QuickWinsComponents;
