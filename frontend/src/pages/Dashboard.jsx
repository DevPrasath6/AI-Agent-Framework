import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import {
    PlusIcon,
    EyeIcon,
    CogIcon,
    PlayIcon,
    CheckCircleIcon,
    ChartBarIcon
} from '@heroicons/react/24/outline';

// Components
import Navigation from '../components/navigation/Navigation';

const Dashboard = () => {
    const [stats] = useState({
        totalWorkflows: 12,
        activeWorkflows: 8,
        completedExecutions: 1247,
        successRate: 94.2,
    });

    const [loading, setLoading] = useState(true);

    // Simulate loading state
    useEffect(() => {
        setTimeout(() => setLoading(false), 1500);
    }, []);

    const recentWorkflows = [
        {
            id: 1,
            name: 'Lead Processing Pipeline',
            status: 'running',
            lastRun: '2 minutes ago',
            executions: 156,
            description: 'Automated lead capture and qualification from website forms',
            progress: 75
        },
        {
            id: 2,
            name: 'Customer Onboarding',
            status: 'paused',
            lastRun: '1 hour ago',
            executions: 89,
            description: 'Welcome email sequence and account setup automation',
            progress: 45
        },
        {
            id: 3,
            name: 'Invoice Generation',
            status: 'running',
            lastRun: '5 minutes ago',
            executions: 234,
            description: 'Automated invoice creation and delivery system',
            progress: 90
        },
        {
            id: 4,
            name: 'Data Sync',
            status: 'error',
            lastRun: '30 minutes ago',
            executions: 45,
            description: 'Sync customer data between CRM and marketing platform',
            progress: 25
        }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
            <Navigation />

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
                {/* Header */}
                <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
                        <p className="text-gray-600 mt-2">Monitor your workflows and automation performance</p>
                    </div>
                    <div className="mt-4 md:mt-0">
                        <Link
                            to="/workflows"
                            className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all duration-200 flex items-center space-x-2"
                        >
                            <PlusIcon className="w-5 h-5" />
                            <span>Create Workflow</span>
                        </Link>
                    </div>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                        className="backdrop-blur-xl bg-white/70 rounded-xl p-6 border border-white/20"
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-gray-600">Total Workflows</p>
                                <p className="text-2xl font-bold text-gray-900">{stats.totalWorkflows}</p>
                            </div>
                            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                                <CogIcon className="w-5 h-5 text-white" />
                            </div>
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
                                <p className="text-sm font-medium text-gray-600">Active Workflows</p>
                                <p className="text-2xl font-bold text-gray-900">{stats.activeWorkflows}</p>
                            </div>
                            <div className="w-8 h-8 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg flex items-center justify-center">
                                <PlayIcon className="w-5 h-5 text-white" />
                            </div>
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
                                <p className="text-sm font-medium text-gray-600">Completed Executions</p>
                                <p className="text-2xl font-bold text-gray-900">{stats.completedExecutions}</p>
                            </div>
                            <div className="w-8 h-8 bg-gradient-to-r from-orange-500 to-red-600 rounded-lg flex items-center justify-center">
                                <CheckCircleIcon className="w-5 h-5 text-white" />
                            </div>
                        </div>
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
                                <p className="text-2xl font-bold text-gray-900">{stats.successRate}%</p>
                            </div>
                            <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-600 rounded-lg flex items-center justify-center">
                                <ChartBarIcon className="w-5 h-5 text-white" />
                            </div>
                        </div>
                    </motion.div>
                </div>

                {/* Recent Workflows */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                    className="backdrop-blur-xl bg-white/70 rounded-xl p-6 border border-white/20 mb-8"
                >
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-xl font-semibold text-gray-900">Recent Workflows</h2>
                        <Link
                            to="/workflows"
                            className="text-sm text-purple-600 hover:text-purple-700 font-medium flex items-center space-x-1"
                        >
                            <span>View all</span>
                            <EyeIcon className="w-4 h-4" />
                        </Link>
                    </div>
                    <div className="space-y-4">
                        {loading ? (
                            // Loading skeletons
                            Array(3).fill(0).map((_, index) => (
                                <div key={index} className="animate-pulse">
                                    <div className="flex items-center space-x-4 p-4 bg-white/50 rounded-lg">
                                        <div className="w-12 h-12 bg-gray-200 rounded-lg"></div>
                                        <div className="flex-1">
                                            <div className="h-4 bg-gray-200 rounded w-1/3 mb-2"></div>
                                            <div className="h-3 bg-gray-200 rounded w-2/3"></div>
                                        </div>
                                    </div>
                                </div>
                            ))
                        ) : (
                            recentWorkflows.map((workflow, index) => (
                                <motion.div
                                    key={workflow.id}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: 0.6 + index * 0.1 }}
                                    className="p-4 bg-white/50 rounded-lg border border-gray-100 hover:bg-white/70 transition-all duration-200"
                                >
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center space-x-4">
                                            <div className={`w-3 h-3 rounded-full ${
                                                workflow.status === 'running' ? 'bg-green-500 animate-pulse' :
                                                workflow.status === 'paused' ? 'bg-yellow-500' :
                                                workflow.status === 'error' ? 'bg-red-500' : 'bg-gray-400'
                                            }`}></div>
                                            <div className="flex-1">
                                                <h3 className="text-sm font-medium text-gray-900">{workflow.name}</h3>
                                                <p className="text-sm text-gray-600 mt-1">{workflow.description}</p>
                                                <div className="flex items-center space-x-4 mt-2">
                                                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                                                        workflow.status === 'running' ? 'bg-green-100 text-green-800' :
                                                        workflow.status === 'paused' ? 'bg-yellow-100 text-yellow-800' :
                                                        workflow.status === 'error' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'
                                                    }`}>
                                                        {workflow.status}
                                                    </span>
                                                    <span className="text-xs text-gray-500">Last run: {workflow.lastRun}</span>
                                                    <span className="text-xs text-gray-500">{workflow.executions} executions</span>
                                                </div>
                                                <div className="mt-3 bg-gray-200 rounded-full h-2">
                                                    <div
                                                        className={`h-2 rounded-full transition-all duration-300 ${
                                                            workflow.status === 'error' ? 'bg-red-500' :
                                                            workflow.status === 'paused' ? 'bg-yellow-500' :
                                                            'bg-gradient-to-r from-purple-600 to-blue-600'
                                                        }`}
                                                        style={{ width: `${workflow.progress}%` }}
                                                    />
                                                </div>
                                            </div>
                                        </div>
                                        <div className="flex items-center space-x-2">
                                            <button className="p-2 text-gray-400 hover:text-purple-600 rounded-lg hover:bg-purple-50 transition-colors">
                                                <EyeIcon className="w-5 h-5" />
                                            </button>
                                            <button className="p-2 text-gray-400 hover:text-purple-600 rounded-lg hover:bg-purple-50 transition-colors">
                                                <CogIcon className="w-5 h-5" />
                                            </button>
                                        </div>
                                    </div>
                                </motion.div>
                            ))
                        )}
                    </div>
                </motion.div>

                {/* Quick Actions */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.8 }}
                    className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-6"
                >
                    <Link to="/workflows" className="backdrop-blur-xl bg-white/70 border border-gray-200 rounded-2xl shadow-xl p-6 hover:shadow-2xl hover:scale-105 transition-all duration-300">
                        <div className="w-12 h-12 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg flex items-center justify-center mb-4">
                            <PlusIcon className="w-6 h-6 text-white" />
                        </div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">Create New Workflow</h3>
                        <p className="text-sm text-gray-600">Build automated workflows with our visual editor</p>
                    </Link>

                    <Link to="/agents" className="backdrop-blur-xl bg-white/70 border border-gray-200 rounded-2xl shadow-xl p-6 hover:shadow-2xl hover:scale-105 transition-all duration-300">
                        <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg flex items-center justify-center mb-4">
                            <EyeIcon className="w-6 h-6 text-white" />
                        </div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">Manage AI Agents</h3>
                        <p className="text-sm text-gray-600">Deploy and configure your AI agents for different tasks</p>
                    </Link>

                    <Link to="/monitoring" className="backdrop-blur-xl bg-white/70 border border-gray-200 rounded-2xl shadow-xl p-6 hover:shadow-2xl hover:scale-105 transition-all duration-300">
                        <div className="w-12 h-12 bg-gradient-to-r from-orange-500 to-red-600 rounded-lg flex items-center justify-center mb-4">
                            <CogIcon className="w-6 h-6 text-white" />
                        </div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">System Monitoring</h3>
                        <p className="text-sm text-gray-600">Monitor system performance and view real-time logs</p>
                    </Link>
                </motion.div>
            </div>

            {/* Clean and simplified dashboard end */}

        </div>
    );
};

export default Dashboard;
