import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import {
    PlusIcon,
    MagnifyingGlassIcon,
    FunnelIcon,
    CheckCircleIcon,
    DocumentDuplicateIcon,
    ArrowPathIcon,
    ChevronDownIcon
} from '@heroicons/react/24/outline';

// Components
import Navigation from '../components/navigation/Navigation';
import { AdvancedDataTable, WorkflowVisualization } from '../components/advanced/AdvancedUIComponents';

const Workflows = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [filterStatus, setFilterStatus] = useState('all');
    const [showFilterDropdown, setShowFilterDropdown] = useState(false);

    const workflows = [
        {
            id: 1,
            name: 'Lead Processing Pipeline',
            description: 'Automated lead capture and qualification from website forms',
            status: 'running',
            lastRun: '2 minutes ago',
            executions: 156,
            successRate: 98.7,
            createdAt: '2024-01-15',
            tags: ['lead-generation', 'automation']
        },
        {
            id: 2,
            name: 'Customer Onboarding',
            description: 'Welcome email sequence and account setup automation',
            status: 'paused',
            lastRun: '1 hour ago',
            executions: 89,
            successRate: 95.5,
            createdAt: '2024-01-10',
            tags: ['onboarding', 'email']
        },
        {
            id: 3,
            name: 'Invoice Generation',
            description: 'Automated invoice creation and delivery system',
            status: 'running',
            lastRun: '5 minutes ago',
            executions: 234,
            successRate: 99.1,
            createdAt: '2024-01-05',
            tags: ['billing', 'automation']
        },
        {
            id: 4,
            name: 'Data Sync',
            description: 'Sync customer data between CRM and marketing platform',
            status: 'error',
            lastRun: '30 minutes ago',
            executions: 45,
            successRate: 87.2,
            createdAt: '2024-01-12',
            tags: ['sync', 'crm']
        },
        {
            id: 5,
            name: 'Social Media Posting',
            description: 'Automated social media content scheduling and posting',
            status: 'running',
            lastRun: '10 minutes ago',
            executions: 78,
            successRate: 92.3,
            createdAt: '2024-01-08',
            tags: ['social-media', 'content']
        },
        {
            id: 6,
            name: 'Inventory Management',
            description: 'Monitor stock levels and trigger reorder workflows',
            status: 'paused',
            lastRun: '3 hours ago',
            executions: 67,
            successRate: 94.8,
            createdAt: '2024-01-03',
            tags: ['inventory', 'monitoring']
        }
    ];

    const templates = [
        {
            id: 1,
            name: 'Email Marketing Campaign',
            description: 'Complete email marketing automation with segmentation',
            category: 'Marketing',
            uses: 1247
        },
        {
            id: 2,
            name: 'Customer Support Ticket',
            description: 'Automated ticket routing and escalation workflow',
            category: 'Support',
            uses: 892
        },
        {
            id: 3,
            name: 'E-commerce Order Processing',
            description: 'End-to-end order fulfillment automation',
            category: 'E-commerce',
            uses: 654
        },
        {
            id: 4,
            name: 'HR Onboarding Process',
            description: 'Complete new employee onboarding workflow',
            category: 'HR',
            uses: 423
        }
    ];

    const filteredWorkflows = workflows.filter(workflow => {
        const matchesSearch = workflow.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                             workflow.description.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesFilter = filterStatus === 'all' || workflow.status === filterStatus;
        return matchesSearch && matchesFilter;
    });

    return (
        <div className="min-h-screen bg-gray-50">
            <Navigation />

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Header */}
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Workflows</h1>
                        <p className="mt-2 text-gray-600">Create, manage and monitor your automation workflows</p>
                    </div>
                    <div className="mt-4 sm:mt-0 flex space-x-3">
                        <button className="inline-flex items-center px-4 py-2 bg-white border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-all duration-200">
                            <DocumentDuplicateIcon className="w-5 h-5 mr-2" />
                            Import
                        </button>
                        <Link
                            to="/workflows/create"
                            className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-rose-500 to-orange-500 text-white font-medium rounded-lg hover:from-rose-600 hover:to-orange-600 transition-all duration-200 shadow-lg"
                        >
                            <PlusIcon className="w-5 h-5 mr-2" />
                            Create Workflow
                        </Link>
                    </div>
                </div>

                {/* Search and Filters */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
                    <div className="flex flex-col sm:flex-row sm:items-center space-y-4 sm:space-y-0 sm:space-x-4">
                        <div className="flex-1 relative">
                            <MagnifyingGlassIcon className="w-5 h-5 absolute left-3 top-3 text-gray-400" />
                            <input
                                type="text"
                                placeholder="Search workflows..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-rose-500 focus:border-transparent"
                            />
                        </div>
                        <div className="relative">
                            <button
                                onClick={() => setShowFilterDropdown(!showFilterDropdown)}
                                className="inline-flex items-center px-4 py-2 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 transition-all duration-200"
                            >
                                <FunnelIcon className="w-5 h-5 mr-2" />
                                Filter: {filterStatus === 'all' ? 'All' : filterStatus.charAt(0).toUpperCase() + filterStatus.slice(1)}
                                <ChevronDownIcon className="w-4 h-4 ml-2" />
                            </button>
                            {showFilterDropdown && (
                                <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-10">
                                    {['all', 'running', 'paused', 'error'].map((status) => (
                                        <button
                                            key={status}
                                            onClick={() => {
                                                setFilterStatus(status);
                                                setShowFilterDropdown(false);
                                            }}
                                            className="w-full text-left px-4 py-2 hover:bg-gray-50 text-gray-700"
                                        >
                                            {status === 'all' ? 'All Status' : status.charAt(0).toUpperCase() + status.slice(1)}
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Workflows List */}
                    <div className="lg:col-span-2">
                        <div className="bg-white rounded-xl shadow-sm border border-gray-200">
                            <div className="px-6 py-4 border-b border-gray-200">
                                <h2 className="text-lg font-semibold text-gray-900">
                                    Your Workflows ({filteredWorkflows.length})
                                </h2>
                            </div>
                            <div className="p-6">
                                <AdvancedDataTable
                                    data={filteredWorkflows.map(workflow => ({
                                        id: workflow.id,
                                        name: workflow.name,
                                        status: workflow.status,
                                        lastRun: workflow.lastRun,
                                        executions: workflow.executions,
                                        successRate: `${workflow.successRate}%`,
                                        description: workflow.description
                                    }))}
                                    columns={[
                                        { key: 'name', title: 'Name', sortable: true },
                                        { key: 'status', title: 'Status', sortable: true },
                                        { key: 'lastRun', title: 'Last Run', sortable: true },
                                        { key: 'executions', title: 'Executions', sortable: true },
                                        { key: 'successRate', title: 'Success Rate', sortable: true }
                                    ]}
                                    searchable={true}
                                    itemsPerPage={10}
                                />
                            </div>
                        </div>

                        {/* Workflow Visualization */}
                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 mt-8">
                            <div className="px-6 py-4 border-b border-gray-200">
                                <h2 className="text-lg font-semibold text-gray-900">
                                    Workflow Visualization
                                </h2>
                                <p className="text-sm text-gray-600">Interactive workflow builder and editor</p>
                            </div>
                            <div className="p-6">
                                <WorkflowVisualization />
                            </div>
                        </div>
                    </div>

                    {/* Sidebar */}
                    <div className="space-y-6">
                        {/* Quick Stats */}
                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h3>
                            <div className="space-y-4">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center">
                                        <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                                        <span className="text-sm text-gray-600">Running</span>
                                    </div>
                                    <span className="text-sm font-medium text-gray-900">
                                        {workflows.filter(w => w.status === 'running').length}
                                    </span>
                                </div>
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center">
                                        <div className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
                                        <span className="text-sm text-gray-600">Paused</span>
                                    </div>
                                    <span className="text-sm font-medium text-gray-900">
                                        {workflows.filter(w => w.status === 'paused').length}
                                    </span>
                                </div>
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center">
                                        <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
                                        <span className="text-sm text-gray-600">Error</span>
                                    </div>
                                    <span className="text-sm font-medium text-gray-900">
                                        {workflows.filter(w => w.status === 'error').length}
                                    </span>
                                </div>
                            </div>
                        </div>

                        {/* Templates */}
                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">Popular Templates</h3>
                            <div className="space-y-4">
                                {templates.map((template) => (
                                    <motion.div
                                        key={template.id}
                                        whileHover={{ scale: 1.02 }}
                                        className="p-4 border border-gray-200 rounded-lg hover:border-rose-300 transition-colors cursor-pointer"
                                    >
                                        <h4 className="text-sm font-medium text-gray-900">{template.name}</h4>
                                        <p className="text-xs text-gray-600 mt-1">{template.description}</p>
                                        <div className="flex items-center justify-between mt-2">
                                            <span className="text-xs text-rose-600 bg-rose-50 px-2 py-1 rounded">
                                                {template.category}
                                            </span>
                                            <span className="text-xs text-gray-500">
                                                {template.uses.toLocaleString()} uses
                                            </span>
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                            <button className="w-full mt-4 text-sm text-rose-600 hover:text-rose-700 font-medium">
                                Browse all templates →
                            </button>
                        </div>

                        {/* Quick Actions */}
                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
                            <div className="space-y-3">
                                <button className="w-full flex items-center px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors">
                                    <ArrowPathIcon className="w-4 h-4 mr-3 text-gray-400" />
                                    Sync all workflows
                                </button>
                                <button className="w-full flex items-center px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors">
                                    <DocumentDuplicateIcon className="w-4 h-4 mr-3 text-gray-400" />
                                    Export workflows
                                </button>
                                <button className="w-full flex items-center px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors">
                                    <CheckCircleIcon className="w-4 h-4 mr-3 text-gray-400" />
                                    Run diagnostics
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Workflows;
