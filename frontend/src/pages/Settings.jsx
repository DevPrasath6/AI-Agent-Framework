import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
    UserIcon,
    CogIcon,
    BellIcon,
    ShieldCheckIcon,
    CreditCardIcon,
    UsersIcon,
    KeyIcon,
    GlobeAltIcon,
    ChevronRightIcon,
    CheckIcon,
    EyeIcon,
    EyeSlashIcon,
    PlusIcon,
    TrashIcon
} from '@heroicons/react/24/outline';

// Components
import Navigation from '../components/navigation/Navigation';

const Settings = () => {
    const [activeSection, setActiveSection] = useState('profile');
    const [showPassword, setShowPassword] = useState(false);
    const [notifications, setNotifications] = useState({
        email: true,
        push: false,
        workflowUpdates: true,
        securityAlerts: true,
        newsletter: false
    });

    const [profile, setProfile] = useState({
        firstName: 'John',
        lastName: 'Doe',
        email: 'john.doe@example.com',
        timezone: 'UTC-8',
        language: 'English'
    });

    const [integrations] = useState([
        {
            id: 1,
            name: 'Slack',
            description: 'Team communication and notifications',
            connected: true,
            lastSync: '2 hours ago',
            icon: '💬'
        },
        {
            id: 2,
            name: 'Google Sheets',
            description: 'Spreadsheet data management',
            connected: true,
            lastSync: '15 minutes ago',
            icon: '📊'
        },
        {
            id: 3,
            name: 'HubSpot',
            description: 'CRM and marketing automation',
            connected: false,
            lastSync: null,
            icon: '🎯'
        },
        {
            id: 4,
            name: 'Salesforce',
            description: 'Customer relationship management',
            connected: true,
            lastSync: '1 hour ago',
            icon: '☁️'
        }
    ]);

    const [apiKeys] = useState([
        {
            id: 1,
            name: 'Production API Key',
            key: 'n8n_pk_1a2b3c4d5e6f...',
            created: '2024-01-15',
            lastUsed: '2 hours ago',
            permissions: ['read', 'write']
        },
        {
            id: 2,
            name: 'Development API Key',
            key: 'n8n_dev_9z8y7x6w5v4u...',
            created: '2024-01-10',
            lastUsed: '1 day ago',
            permissions: ['read']
        }
    ]);

    const menuItems = [
        { id: 'profile', label: 'Profile', icon: UserIcon, description: 'Manage your account details' },
        { id: 'preferences', label: 'Preferences', icon: CogIcon, description: 'Configure your workspace' },
        { id: 'notifications', label: 'Notifications', icon: BellIcon, description: 'Control your alerts' },
        { id: 'security', label: 'Security', icon: ShieldCheckIcon, description: 'Password and authentication' },
        { id: 'billing', label: 'Billing', icon: CreditCardIcon, description: 'Subscription and payments' },
        { id: 'team', label: 'Team', icon: UsersIcon, description: 'Manage team members' },
        { id: 'integrations', label: 'Integrations', icon: GlobeAltIcon, description: 'Connect external services' },
        { id: 'api', label: 'API Keys', icon: KeyIcon, description: 'Manage API access' }
    ];

    const handleNotificationChange = (key) => {
        setNotifications(prev => ({
            ...prev,
            [key]: !prev[key]
        }));
    };

    const renderProfileSection = () => (
        <div className="space-y-6">
            <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Profile Information</h2>
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">First Name</label>
                            <input
                                type="text"
                                value={profile.firstName}
                                onChange={(e) => setProfile({...profile, firstName: e.target.value})}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-rose-500 focus:border-transparent"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Last Name</label>
                            <input
                                type="text"
                                value={profile.lastName}
                                onChange={(e) => setProfile({...profile, lastName: e.target.value})}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-rose-500 focus:border-transparent"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                            <input
                                type="email"
                                value={profile.email}
                                onChange={(e) => setProfile({...profile, email: e.target.value})}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-rose-500 focus:border-transparent"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Timezone</label>
                            <select
                                value={profile.timezone}
                                onChange={(e) => setProfile({...profile, timezone: e.target.value})}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-rose-500 focus:border-transparent"
                            >
                                <option value="UTC-8">Pacific Time (UTC-8)</option>
                                <option value="UTC-5">Eastern Time (UTC-5)</option>
                                <option value="UTC+0">UTC</option>
                                <option value="UTC+1">Central European Time (UTC+1)</option>
                            </select>
                        </div>
                    </div>
                    <div className="flex justify-end mt-6">
                        <button className="px-4 py-2 bg-gradient-to-r from-rose-500 to-orange-500 text-white font-medium rounded-lg hover:from-rose-600 hover:to-orange-600 transition-all duration-200">
                            Save Changes
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderNotificationsSection = () => (
        <div className="space-y-6">
            <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Notification Preferences</h2>
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="space-y-4">
                        {Object.entries(notifications).map(([key, value]) => (
                            <div key={key} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                                <div>
                                    <h3 className="text-sm font-medium text-gray-900">
                                        {key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                                    </h3>
                                    <p className="text-sm text-gray-600">
                                        {key === 'email' && 'Receive email notifications for important updates'}
                                        {key === 'push' && 'Get push notifications on your device'}
                                        {key === 'workflowUpdates' && 'Notifications when workflows complete or fail'}
                                        {key === 'securityAlerts' && 'Important security and login alerts'}
                                        {key === 'newsletter' && 'Product updates and feature announcements'}
                                    </p>
                                </div>
                                <button
                                    onClick={() => handleNotificationChange(key)}
                                    className={`relative inline-flex items-center h-6 rounded-full w-11 transition-colors ${
                                        value ? 'bg-rose-500' : 'bg-gray-200'
                                    }`}
                                >
                                    <span
                                        className={`inline-block w-4 h-4 transform bg-white rounded-full transition-transform ${
                                            value ? 'translate-x-6' : 'translate-x-1'
                                        }`}
                                    />
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );

    const renderSecuritySection = () => (
        <div className="space-y-6">
            <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Security Settings</h2>
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Current Password</label>
                            <div className="relative">
                                <input
                                    type={showPassword ? 'text' : 'password'}
                                    className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-rose-500 focus:border-transparent"
                                    placeholder="Enter current password"
                                />
                                <button
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
                                >
                                    {showPassword ? <EyeSlashIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
                                </button>
                            </div>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">New Password</label>
                            <input
                                type="password"
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-rose-500 focus:border-transparent"
                                placeholder="Enter new password"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Confirm New Password</label>
                            <input
                                type="password"
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-rose-500 focus:border-transparent"
                                placeholder="Confirm new password"
                            />
                        </div>
                        <div className="pt-4 border-t border-gray-200">
                            <div className="flex items-center justify-between">
                                <div>
                                    <h3 className="text-sm font-medium text-gray-900">Two-Factor Authentication</h3>
                                    <p className="text-sm text-gray-600">Add an extra layer of security to your account</p>
                                </div>
                                <button className="px-4 py-2 bg-green-100 text-green-800 font-medium rounded-lg hover:bg-green-200 transition-colors">
                                    <CheckIcon className="w-4 h-4 inline mr-2" />
                                    Enabled
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderIntegrationsSection = () => (
        <div className="space-y-6">
            <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Integrations</h2>
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="grid gap-4">
                        {integrations.map((integration) => (
                            <div key={integration.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                                <div className="flex items-center space-x-4">
                                    <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center text-2xl">
                                        {integration.icon}
                                    </div>
                                    <div>
                                        <h3 className="text-sm font-medium text-gray-900">{integration.name}</h3>
                                        <p className="text-sm text-gray-600">{integration.description}</p>
                                        {integration.connected && integration.lastSync && (
                                            <p className="text-xs text-gray-500 mt-1">Last synced: {integration.lastSync}</p>
                                        )}
                                    </div>
                                </div>
                                <div className="flex items-center space-x-3">
                                    <div className="flex items-center">
                                        <div className={`w-3 h-3 rounded-full mr-2 ${integration.connected ? 'bg-green-500' : 'bg-gray-400'}`}></div>
                                        <span className="text-sm text-gray-600">
                                            {integration.connected ? 'Connected' : 'Not connected'}
                                        </span>
                                    </div>
                                    <button
                                        className={`px-4 py-2 font-medium rounded-lg transition-colors ${
                                            integration.connected
                                                ? 'bg-red-100 text-red-700 hover:bg-red-200'
                                                : 'bg-green-100 text-green-700 hover:bg-green-200'
                                        }`}
                                    >
                                        {integration.connected ? 'Disconnect' : 'Connect'}
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                    <div className="mt-6 pt-6 border-t border-gray-200 text-center">
                        <button className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-rose-500 to-orange-500 text-white font-medium rounded-lg hover:from-rose-600 hover:to-orange-600 transition-all duration-200">
                            <PlusIcon className="w-5 h-5 mr-2" />
                            Add Integration
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderAPISection = () => (
        <div className="space-y-6">
            <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-4">API Keys</h2>
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="space-y-4">
                        {apiKeys.map((apiKey) => (
                            <div key={apiKey.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                                <div>
                                    <h3 className="text-sm font-medium text-gray-900">{apiKey.name}</h3>
                                    <p className="text-sm text-gray-600 font-mono">{apiKey.key}</p>
                                    <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                                        <span>Created: {apiKey.created}</span>
                                        <span>Last used: {apiKey.lastUsed}</span>
                                        <div className="flex items-center space-x-1">
                                            <span>Permissions:</span>
                                            {apiKey.permissions.map((perm) => (
                                                <span key={perm} className="bg-gray-100 px-2 py-1 rounded">
                                                    {perm}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                                <button className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                                    <TrashIcon className="w-5 h-5" />
                                </button>
                            </div>
                        ))}
                    </div>
                    <div className="mt-6 pt-6 border-t border-gray-200">
                        <button className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-rose-500 to-orange-500 text-white font-medium rounded-lg hover:from-rose-600 hover:to-orange-600 transition-all duration-200">
                            <PlusIcon className="w-5 h-5 mr-2" />
                            Generate New API Key
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderContent = () => {
        switch (activeSection) {
            case 'profile':
                return renderProfileSection();
            case 'notifications':
                return renderNotificationsSection();
            case 'security':
                return renderSecuritySection();
            case 'integrations':
                return renderIntegrationsSection();
            case 'api':
                return renderAPISection();
            default:
                return (
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center">
                        <h3 className="text-lg font-medium text-gray-900 mb-2">Coming Soon</h3>
                        <p className="text-gray-600">This section is under development.</p>
                    </div>
                );
        }
    };

    return (
        <div className="min-h-screen bg-gray-50">
            <Navigation />

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
                    <p className="mt-2 text-gray-600">Manage your account settings and preferences</p>
                </div>

                <div className="flex flex-col lg:flex-row gap-8">
                    {/* Sidebar */}
                    <div className="lg:w-80">
                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
                            <nav className="space-y-2">
                                {menuItems.map((item) => {
                                    const Icon = item.icon;
                                    return (
                                        <button
                                            key={item.id}
                                            onClick={() => setActiveSection(item.id)}
                                            className={`w-full flex items-center justify-between p-3 text-left rounded-lg transition-colors ${
                                                activeSection === item.id
                                                    ? 'bg-rose-50 text-rose-700 border-rose-200'
                                                    : 'text-gray-700 hover:bg-gray-50'
                                            }`}
                                        >
                                            <div className="flex items-center space-x-3">
                                                <Icon className="w-5 h-5" />
                                                <div>
                                                    <div className="font-medium">{item.label}</div>
                                                    <div className="text-sm text-gray-500">{item.description}</div>
                                                </div>
                                            </div>
                                            <ChevronRightIcon className="w-4 h-4" />
                                        </button>
                                    );
                                })}
                            </nav>
                        </div>
                    </div>

                    {/* Content */}
                    <div className="flex-1">
                        <motion.div
                            key={activeSection}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.3 }}
                        >
                            {renderContent()}
                        </motion.div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Settings;
