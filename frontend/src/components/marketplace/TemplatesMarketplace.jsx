import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    MagnifyingGlassIcon,
    StarIcon,
    CloudArrowDownIcon,
    EyeIcon,
    FunnelIcon,
    SparklesIcon,
    TrophyIcon,
    UserIcon,
    CalendarIcon,
    ChevronDownIcon,
    HeartIcon,
    ShareIcon,
    PlayIcon
} from '@heroicons/react/24/outline';
import { StarIcon as StarSolidIcon, HeartIcon as HeartSolidIcon } from '@heroicons/react/24/solid';

const TemplatesMarketplace = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('all');
    const [sortBy, setSortBy] = useState('popular');
    const [showFilters, setShowFilters] = useState(false);
    const [favorites, setFavorites] = useState(new Set(['1', '3', '7']));
    const [deployingTemplate, setDeployingTemplate] = useState(null);

    // Sample template data with comprehensive details
    const [templates] = useState([
        {
            id: '1',
            title: 'E-commerce Order Processing',
            description: 'Automated workflow for processing customer orders, inventory updates, and shipping notifications',
            category: 'E-commerce',
            author: 'WorkflowPro',
            authorAvatar: '/api/placeholder/32/32',
            rating: 4.8,
            reviews: 142,
            downloads: 2847,
            image: '/api/placeholder/300/200',
            tags: ['orders', 'inventory', 'shipping', 'notifications'],
            complexity: 'Medium',
            estimatedTime: '15 min setup',
            featured: true,
            premium: false,
            lastUpdated: '2024-01-15',
            price: 0,
            compatibility: ['Shopify', 'WooCommerce', 'Stripe'],
            steps: 12,
            preview: {
                inputs: ['Order ID', 'Customer Email'],
                outputs: ['Shipping Label', 'Tracking Number', 'Receipt'],
                triggers: ['New Order', 'Payment Confirmed']
            }
        },
        {
            id: '2',
            title: 'Social Media Content Scheduler',
            description: 'Schedule and publish content across multiple social media platforms automatically',
            category: 'Marketing',
            author: 'SocialBoost',
            authorAvatar: '/api/placeholder/32/32',
            rating: 4.6,
            reviews: 89,
            downloads: 1923,
            image: '/api/placeholder/300/200',
            tags: ['social-media', 'content', 'scheduling', 'automation'],
            complexity: 'Easy',
            estimatedTime: '10 min setup',
            featured: false,
            premium: true,
            lastUpdated: '2024-01-20',
            price: 29,
            compatibility: ['Twitter', 'Facebook', 'Instagram', 'LinkedIn'],
            steps: 8,
            preview: {
                inputs: ['Content', 'Schedule Time', 'Platforms'],
                outputs: ['Post ID', 'Engagement Stats'],
                triggers: ['Scheduled Time', 'Manual Trigger']
            }
        },
        {
            id: '3',
            title: 'Customer Support Ticket Router',
            description: 'Intelligently route customer support tickets based on content analysis and priority',
            category: 'Customer Support',
            author: 'SupportAI',
            authorAvatar: '/api/placeholder/32/32',
            rating: 4.9,
            reviews: 234,
            downloads: 3456,
            image: '/api/placeholder/300/200',
            tags: ['support', 'AI', 'routing', 'tickets'],
            complexity: 'Advanced',
            estimatedTime: '25 min setup',
            featured: true,
            premium: false,
            lastUpdated: '2024-01-18',
            price: 0,
            compatibility: ['Zendesk', 'Freshdesk', 'Intercom'],
            steps: 18,
            preview: {
                inputs: ['Ticket Content', 'Customer Priority'],
                outputs: ['Assigned Agent', 'Priority Level', 'Category'],
                triggers: ['New Ticket', 'Escalation']
            }
        },
        {
            id: '4',
            title: 'Lead Scoring & Nurturing',
            description: 'Score leads based on behavior and automatically trigger nurturing campaigns',
            category: 'Sales',
            author: 'SalesForce+',
            authorAvatar: '/api/placeholder/32/32',
            rating: 4.7,
            reviews: 167,
            downloads: 2134,
            image: '/api/placeholder/300/200',
            tags: ['leads', 'scoring', 'nurturing', 'sales'],
            complexity: 'Medium',
            estimatedTime: '20 min setup',
            featured: false,
            premium: true,
            lastUpdated: '2024-01-12',
            price: 49,
            compatibility: ['Salesforce', 'HubSpot', 'Mailchimp'],
            steps: 14,
            preview: {
                inputs: ['Lead Data', 'Behavior Score'],
                outputs: ['Lead Score', 'Campaign Assignment'],
                triggers: ['New Lead', 'Score Change']
            }
        },
        {
            id: '5',
            title: 'Data Backup & Sync',
            description: 'Automatically backup and synchronize data across multiple cloud storage providers',
            category: 'Data Management',
            author: 'CloudSync',
            authorAvatar: '/api/placeholder/32/32',
            rating: 4.5,
            reviews: 98,
            downloads: 1567,
            image: '/api/placeholder/300/200',
            tags: ['backup', 'sync', 'cloud', 'storage'],
            complexity: 'Easy',
            estimatedTime: '12 min setup',
            featured: false,
            premium: false,
            lastUpdated: '2024-01-22',
            price: 0,
            compatibility: ['Google Drive', 'Dropbox', 'OneDrive'],
            steps: 9,
            preview: {
                inputs: ['Source Data', 'Destination'],
                outputs: ['Backup Status', 'Sync Report'],
                triggers: ['Schedule', 'File Change']
            }
        },
        {
            id: '6',
            title: 'Invoice Generation & Payment',
            description: 'Generate invoices, send to customers, and track payment status automatically',
            category: 'Finance',
            author: 'FinanceFlow',
            authorAvatar: '/api/placeholder/32/32',
            rating: 4.8,
            reviews: 201,
            downloads: 2891,
            image: '/api/placeholder/300/200',
            tags: ['invoices', 'payments', 'finance', 'tracking'],
            complexity: 'Medium',
            estimatedTime: '18 min setup',
            featured: true,
            premium: false,
            lastUpdated: '2024-01-16',
            price: 0,
            compatibility: ['QuickBooks', 'Xero', 'PayPal'],
            steps: 16,
            preview: {
                inputs: ['Customer Data', 'Invoice Items'],
                outputs: ['PDF Invoice', 'Payment Link'],
                triggers: ['New Sale', 'Payment Due']
            }
        }
    ]);

    const categories = [
        { id: 'all', name: 'All Categories', count: templates.length, icon: SparklesIcon },
        { id: 'E-commerce', name: 'E-commerce', count: 1, icon: SparklesIcon },
        { id: 'Marketing', name: 'Marketing', count: 1, icon: SparklesIcon },
        { id: 'Customer Support', name: 'Customer Support', count: 1, icon: SparklesIcon },
        { id: 'Sales', name: 'Sales', count: 1, icon: SparklesIcon },
        { id: 'Data Management', name: 'Data Management', count: 1, icon: SparklesIcon },
        { id: 'Finance', name: 'Finance', count: 1, icon: SparklesIcon },
    ];

    const sortOptions = [
        { id: 'popular', name: 'Most Popular', icon: TrophyIcon },
        { id: 'recent', name: 'Recently Updated', icon: CalendarIcon },
        { id: 'rating', name: 'Highest Rated', icon: StarIcon },
        { id: 'downloads', name: 'Most Downloaded', icon: CloudArrowDownIcon },
    ];

    // Filter and sort templates
    const filteredTemplates = useMemo(() => {
        let filtered = templates.filter(template => {
            const matchesSearch = template.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                                template.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                                template.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));

            const matchesCategory = selectedCategory === 'all' || template.category === selectedCategory;

            return matchesSearch && matchesCategory;
        });

        // Sort templates
        filtered.sort((a, b) => {
            switch (sortBy) {
                case 'popular':
                    return b.downloads - a.downloads;
                case 'recent':
                    return new Date(b.lastUpdated) - new Date(a.lastUpdated);
                case 'rating':
                    return b.rating - a.rating;
                case 'downloads':
                    return b.downloads - a.downloads;
                default:
                    return 0;
            }
        });

        return filtered;
    }, [templates, searchQuery, selectedCategory, sortBy]);

    const featuredTemplates = templates.filter(template => template.featured);

    const toggleFavorite = (templateId) => {
        setFavorites(prev => {
            const newFavorites = new Set(prev);
            if (newFavorites.has(templateId)) {
                newFavorites.delete(templateId);
            } else {
                newFavorites.add(templateId);
            }
            return newFavorites;
        });
    };

    const deployTemplate = async (template) => {
        setDeployingTemplate(template.id);

        // Simulate deployment process
        await new Promise(resolve => setTimeout(resolve, 2000));

        setDeployingTemplate(null);

        // Show success notification or redirect
        console.log(`Deployed template: ${template.title}`);
    };

    const getComplexityColor = (complexity) => {
        switch (complexity) {
            case 'Easy': return 'text-green-600 bg-green-100 border-green-200';
            case 'Medium': return 'text-yellow-600 bg-yellow-100 border-yellow-200';
            case 'Advanced': return 'text-red-600 bg-red-100 border-red-200';
            default: return 'text-gray-600 bg-gray-100 border-gray-200';
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
            {/* Header */}
            <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-center"
                    >
                        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                            Templates Marketplace
                        </h1>
                        <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
                            Discover and deploy powerful workflow templates created by the community
                        </p>

                        {/* Search and Filters */}
                        <div className="max-w-4xl mx-auto space-y-4">
                            {/* Search Bar */}
                            <div className="relative">
                                <MagnifyingGlassIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <input
                                    type="text"
                                    placeholder="Search templates, categories, or tags..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    className="w-full pl-12 pr-4 py-4 text-lg border border-gray-300 dark:border-gray-600 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 transition-all duration-200"
                                />
                            </div>

                            {/* Filter Controls */}
                            <div className="flex flex-wrap items-center justify-center gap-4">
                                <button
                                    onClick={() => setShowFilters(!showFilters)}
                                    className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
                                >
                                    <FunnelIcon className="w-4 h-4" />
                                    <span>Filters</span>
                                    <ChevronDownIcon className={`w-4 h-4 transition-transform duration-200 ${showFilters ? 'rotate-180' : ''}`} />
                                </button>

                                <select
                                    value={sortBy}
                                    onChange={(e) => setSortBy(e.target.value)}
                                    className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                                >
                                    {sortOptions.map(option => (
                                        <option key={option.id} value={option.id}>
                                            {option.name}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Filters Panel */}
                <AnimatePresence>
                    {showFilters && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="mb-8 bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-6 shadow-sm"
                        >
                            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Categories</h3>
                            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
                                {categories.map(category => (
                                    <motion.button
                                        key={category.id}
                                        onClick={() => setSelectedCategory(category.id)}
                                        className={`p-3 rounded-lg text-left transition-all duration-200 ${
                                            selectedCategory === category.id
                                                ? 'bg-blue-600 text-white shadow-md'
                                                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                                        }`}
                                        whileHover={{ scale: 1.02 }}
                                        whileTap={{ scale: 0.98 }}
                                    >
                                        <div className="text-sm font-medium">{category.name}</div>
                                        <div className="text-xs opacity-75 mt-1">{category.count} templates</div>
                                    </motion.button>
                                ))}
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Featured Templates */}
                {featuredTemplates.length > 0 && searchQuery === '' && selectedCategory === 'all' && (
                    <motion.section
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mb-12"
                    >
                        <div className="flex items-center space-x-3 mb-6">
                            <TrophyIcon className="w-6 h-6 text-yellow-500" />
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Featured Templates</h2>
                        </div>

                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                            {featuredTemplates.map((template, index) => (
                                <motion.div
                                    key={template.id}
                                    initial={{ opacity: 0, scale: 0.95 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    transition={{ delay: index * 0.1 }}
                                    className="bg-gradient-to-br from-blue-600 to-purple-700 rounded-2xl p-6 text-white shadow-xl"
                                >
                                    <div className="flex items-start justify-between mb-4">
                                        <div className="flex items-center space-x-2">
                                            <SparklesIcon className="w-5 h-5 text-yellow-300" />
                                            <span className="text-sm font-medium text-yellow-300">Featured</span>
                                        </div>
                                        <button
                                            onClick={() => toggleFavorite(template.id)}
                                            className="text-white hover:text-yellow-300 transition-colors duration-200"
                                        >
                                            {favorites.has(template.id) ?
                                                <HeartSolidIcon className="w-5 h-5" /> :
                                                <HeartIcon className="w-5 h-5" />
                                            }
                                        </button>
                                    </div>

                                    <h3 className="text-xl font-bold mb-2">{template.title}</h3>
                                    <p className="text-blue-100 mb-4 text-sm">{template.description}</p>

                                    <div className="flex items-center space-x-4 mb-4">
                                        <div className="flex items-center space-x-1">
                                            <StarSolidIcon className="w-4 h-4 text-yellow-300" />
                                            <span className="text-sm">{template.rating}</span>
                                        </div>
                                        <div className="flex items-center space-x-1">
                                            <CloudArrowDownIcon className="w-4 h-4" />
                                            <span className="text-sm">{template.downloads.toLocaleString()}</span>
                                        </div>
                                    </div>

                                    <motion.button
                                        onClick={() => deployTemplate(template)}
                                        disabled={deployingTemplate === template.id}
                                        className="w-full py-3 px-4 bg-white text-blue-600 rounded-xl font-semibold hover:bg-gray-100 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                                        whileHover={{ scale: 1.02 }}
                                        whileTap={{ scale: 0.98 }}
                                    >
                                        {deployingTemplate === template.id ? (
                                            <>
                                                <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
                                                <span>Deploying...</span>
                                            </>
                                        ) : (
                                            <>
                                                <PlayIcon className="w-4 h-4" />
                                                <span>Deploy Template</span>
                                            </>
                                        )}
                                    </motion.button>
                                </motion.div>
                            ))}
                        </div>
                    </motion.section>
                )}

                {/* Templates Grid */}
                <motion.section
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                            All Templates ({filteredTemplates.length})
                        </h2>
                    </div>

                    {filteredTemplates.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {filteredTemplates.map((template, index) => (
                                <motion.div
                                    key={template.id}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: index * 0.05 }}
                                    className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden group"
                                >
                                    {/* Template Image/Preview */}
                                    <div className="relative h-48 bg-gradient-to-br from-blue-500 to-purple-600 overflow-hidden">
                                        <div className="absolute inset-0 bg-black bg-opacity-20 group-hover:bg-opacity-30 transition-all duration-300" />
                                        <div className="absolute top-4 right-4 flex items-center space-x-2">
                                            {template.premium && (
                                                <span className="px-2 py-1 bg-yellow-500 text-white text-xs font-medium rounded">
                                                    Premium
                                                </span>
                                            )}
                                            <button
                                                onClick={() => toggleFavorite(template.id)}
                                                className="p-2 bg-white bg-opacity-20 rounded-full text-white hover:bg-opacity-30 transition-all duration-200"
                                            >
                                                {favorites.has(template.id) ?
                                                    <HeartSolidIcon className="w-4 h-4" /> :
                                                    <HeartIcon className="w-4 h-4" />
                                                }
                                            </button>
                                        </div>

                                        <div className="absolute bottom-4 left-4">
                                            <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium border ${getComplexityColor(template.complexity)}`}>
                                                {template.complexity}
                                            </span>
                                        </div>
                                    </div>

                                    <div className="p-6">
                                        <div className="flex items-start justify-between mb-3">
                                            <h3 className="text-lg font-bold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors duration-200">
                                                {template.title}
                                            </h3>
                                            <div className="flex items-center space-x-1 text-sm text-gray-500 dark:text-gray-400">
                                                <StarSolidIcon className="w-4 h-4 text-yellow-400" />
                                                <span>{template.rating}</span>
                                            </div>
                                        </div>

                                        <p className="text-gray-600 dark:text-gray-300 text-sm mb-4 line-clamp-2">
                                            {template.description}
                                        </p>

                                        <div className="flex items-center space-x-4 mb-4 text-xs text-gray-500 dark:text-gray-400">
                                            <div className="flex items-center space-x-1">
                                                <UserIcon className="w-3 h-3" />
                                                <span>{template.author}</span>
                                            </div>
                                            <div className="flex items-center space-x-1">
                                                <CloudArrowDownIcon className="w-3 h-3" />
                                                <span>{template.downloads.toLocaleString()}</span>
                                            </div>
                                            <div className="flex items-center space-x-1">
                                                <CalendarIcon className="w-3 h-3" />
                                                <span>{template.estimatedTime}</span>
                                            </div>
                                        </div>

                                        <div className="flex flex-wrap gap-1 mb-4">
                                            {template.tags.slice(0, 3).map(tag => (
                                                <span
                                                    key={tag}
                                                    className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 text-xs rounded"
                                                >
                                                    #{tag}
                                                </span>
                                            ))}
                                            {template.tags.length > 3 && (
                                                <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 text-xs rounded">
                                                    +{template.tags.length - 3} more
                                                </span>
                                            )}
                                        </div>

                                        <div className="flex items-center space-x-2">
                                            <motion.button
                                                onClick={() => deployTemplate(template)}
                                                disabled={deployingTemplate === template.id}
                                                className="flex-1 py-2 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 text-sm font-medium"
                                                whileHover={{ scale: 1.02 }}
                                                whileTap={{ scale: 0.98 }}
                                            >
                                                {deployingTemplate === template.id ? (
                                                    <>
                                                        <div className="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin" />
                                                        <span>Deploying...</span>
                                                    </>
                                                ) : (
                                                    <>
                                                        <PlayIcon className="w-3 h-3" />
                                                        <span>{template.premium ? `$${template.price}` : 'Deploy'}</span>
                                                    </>
                                                )}
                                            </motion.button>

                                            <button className="p-2 text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-200">
                                                <EyeIcon className="w-4 h-4" />
                                            </button>

                                            <button className="p-2 text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-200">
                                                <ShareIcon className="w-4 h-4" />
                                            </button>
                                        </div>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    ) : (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="text-center py-12"
                        >
                            <MagnifyingGlassIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No templates found</h3>
                            <p className="text-gray-600 dark:text-gray-400">
                                Try adjusting your search query or filters to find what you're looking for.
                            </p>
                        </motion.div>
                    )}
                </motion.section>
            </div>
        </div>
    );
};

export default TemplatesMarketplace;
