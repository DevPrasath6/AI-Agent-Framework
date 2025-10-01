import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  PlayIcon,
  PauseIcon,
  CheckCircleIcon,
  XCircleIcon,
  UserIcon,
  ClockIcon,
  BellIcon,
  ArrowPathIcon,
  SparklesIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';

// 📡 LIVE ACTIVITY FEED
export const LiveActivityFeed = () => {
  const [activities, setActivities] = useState([]);
  const [isLive, setIsLive] = useState(true);
  const [filter, setFilter] = useState('all');

  // Sample activity data
  const generateActivity = () => {
    const activityTypes = [
      {
        type: 'workflow_started',
        icon: PlayIcon,
        color: 'text-green-600 bg-green-100',
        message: 'Workflow "Lead Processing Pipeline" started execution',
        user: 'System',
        details: 'Triggered by incoming webhook'
      },
      {
        type: 'workflow_completed',
        icon: CheckCircleIcon,
        color: 'text-emerald-600 bg-emerald-100',
        message: 'Workflow "Customer Onboarding" completed successfully',
        user: 'System',
        details: '23 steps executed in 2.3 seconds'
      },
      {
        type: 'workflow_failed',
        icon: XCircleIcon,
        color: 'text-red-600 bg-red-100',
        message: 'Workflow "Data Sync" failed at step 5',
        user: 'System',
        details: 'API authentication error'
      },
      {
        type: 'user_action',
        icon: UserIcon,
        color: 'text-blue-600 bg-blue-100',
        message: 'Created new workflow "Email Campaign"',
        user: 'John Doe',
        details: 'Added to Marketing folder'
      },
      {
        type: 'workflow_paused',
        icon: PauseIcon,
        color: 'text-yellow-600 bg-yellow-100',
        message: 'Workflow "Invoice Generation" paused by user',
        user: 'Sarah Smith',
        details: 'Manual intervention required'
      },
      {
        type: 'system_update',
        icon: ArrowPathIcon,
        color: 'text-purple-600 bg-purple-100',
        message: 'System maintenance completed',
        user: 'System',
        details: 'All services are now operational'
      },
      {
        type: 'ai_suggestion',
        icon: SparklesIcon,
        color: 'text-indigo-600 bg-indigo-100',
        message: 'AI suggests optimizing "Lead Processing Pipeline"',
        user: 'AI Assistant',
        details: 'Potential 30% performance improvement'
      },
      {
        type: 'alert',
        icon: ExclamationTriangleIcon,
        color: 'text-orange-600 bg-orange-100',
        message: 'High CPU usage detected on workflow node',
        user: 'System',
        details: 'Consider scaling resources'
      }
    ];

    const randomActivity = activityTypes[Math.floor(Math.random() * activityTypes.length)];

    return {
      id: Date.now() + Math.random(),
      ...randomActivity,
      timestamp: new Date(),
      isNew: true
    };
  };

  // Generate initial activities
  useEffect(() => {
    const initialActivities = Array(8).fill(null).map((_, index) => ({
      ...generateActivity(),
      id: index,
      timestamp: new Date(Date.now() - index * 300000), // Spread over last few hours
      isNew: false
    }));
    setActivities(initialActivities);
  }, []);

  // Add new activities periodically
  useEffect(() => {
    if (!isLive) return;

    const interval = setInterval(() => {
      const newActivity = generateActivity();
      setActivities(prev => {
        const updated = [newActivity, ...prev].slice(0, 20); // Keep only latest 20
        return updated;
      });

      // Remove 'new' flag after animation
      setTimeout(() => {
        setActivities(prev =>
          prev.map(activity =>
            activity.id === newActivity.id
              ? { ...activity, isNew: false }
              : activity
          )
        );
      }, 2000);
    }, 5000 + Math.random() * 10000); // Random interval between 5-15 seconds

    return () => clearInterval(interval);
  }, [isLive]);

  const filteredActivities = activities.filter(activity => {
    if (filter === 'all') return true;
    if (filter === 'workflows') return ['workflow_started', 'workflow_completed', 'workflow_failed', 'workflow_paused'].includes(activity.type);
    if (filter === 'users') return activity.type === 'user_action';
    if (filter === 'system') return ['system_update', 'alert'].includes(activity.type);
    if (filter === 'ai') return activity.type === 'ai_suggestion';
    return true;
  });

  const formatTimeAgo = (timestamp) => {
    const now = new Date();
    const diff = Math.floor((now - timestamp) / 1000);

    if (diff < 60) return 'Just now';
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return `${Math.floor(diff / 86400)}d ago`;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden"
    >
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <BellIcon className="w-6 h-6 text-gray-700" />
              {isLive && (
                <motion.div
                  className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full"
                  animate={{ scale: [1, 1.3, 1] }}
                  transition={{ repeat: Infinity, duration: 2 }}
                />
              )}
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Live Activity Feed</h3>
              <p className="text-sm text-gray-600">Real-time system events and updates</p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            {/* Live toggle */}
            <button
              onClick={() => setIsLive(!isLive)}
              className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                isLive
                  ? 'bg-green-100 text-green-700 hover:bg-green-200'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              <div className={`w-2 h-2 rounded-full ${isLive ? 'bg-green-500' : 'bg-gray-400'}`} />
              <span>{isLive ? 'Live' : 'Paused'}</span>
            </button>

            {/* Filter */}
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Activities</option>
              <option value="workflows">Workflows</option>
              <option value="users">User Actions</option>
              <option value="system">System</option>
              <option value="ai">AI</option>
            </select>
          </div>
        </div>
      </div>

      {/* Activity List */}
      <div className="max-h-96 overflow-y-auto">
        <AnimatePresence>
          {filteredActivities.map((activity) => (
            <motion.div
              key={activity.id}
              initial={{ opacity: 0, x: -20, backgroundColor: activity.isNew ? '#f0f9ff' : 'transparent' }}
              animate={{ opacity: 1, x: 0, backgroundColor: 'transparent' }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3 }}
              className="relative px-6 py-4 border-b border-gray-100 hover:bg-gray-50 transition-colors"
            >
              {activity.isNew && (
                <motion.div
                  initial={{ opacity: 1 }}
                  animate={{ opacity: 0 }}
                  transition={{ duration: 2 }}
                  className="absolute inset-0 bg-gradient-to-r from-blue-50/50 to-transparent pointer-events-none"
                />
              )}

              <div className="flex items-start space-x-4">
                {/* Icon */}
                <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${activity.color}`}>
                  <activity.icon className="w-5 h-5" />
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900 leading-5">
                        {activity.message}
                      </p>
                      <div className="mt-1 flex items-center space-x-3 text-xs text-gray-500">
                        <span className="flex items-center space-x-1">
                          <UserIcon className="w-3 h-3" />
                          <span>{activity.user}</span>
                        </span>
                        <span className="flex items-center space-x-1">
                          <ClockIcon className="w-3 h-3" />
                          <span>{formatTimeAgo(activity.timestamp)}</span>
                        </span>
                      </div>
                      {activity.details && (
                        <p className="mt-1 text-xs text-gray-600 bg-gray-50 rounded px-2 py-1 inline-block">
                          {activity.details}
                        </p>
                      )}
                    </div>

                    {activity.isNew && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="ml-2 w-2 h-2 bg-blue-500 rounded-full"
                      />
                    )}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {filteredActivities.length === 0 && (
          <div className="px-6 py-12 text-center">
            <BellIcon className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 text-sm">No activities to show</p>
            <p className="text-gray-400 text-xs mt-1">Activities will appear here as they happen</p>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="bg-gray-50 px-6 py-3 border-t border-gray-200">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Showing {filteredActivities.length} activities</span>
          <button className="text-blue-600 hover:text-blue-700 font-medium">
            View All →
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default LiveActivityFeed;
