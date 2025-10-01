import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  HomeIcon,
  CpuChipIcon,
  CircleStackIcon,
  ChartBarIcon,
  CogIcon,
  Bars3Icon,
  XMarkIcon,
} from '@heroicons/react/24/outline';
import { useUIStore } from '../../store/uiStore';

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Agents', href: '/agents', icon: CpuChipIcon },
  { name: 'Workflows', href: '/workflows', icon: CircleStackIcon },
  { name: 'Monitoring', href: '/monitoring', icon: ChartBarIcon },
  { name: 'Settings', href: '/settings', icon: CogIcon },
];

const Sidebar = () => {
  const location = useLocation();
  const { sidebarOpen, toggleSidebar, setCurrentPage } = useUIStore();

  const sidebarVariants = {
    open: {
      width: 256,
      transition: {
        type: 'spring',
        damping: 30,
        stiffness: 300,
      },
    },
    closed: {
      width: 64,
      transition: {
        type: 'spring',
        damping: 30,
        stiffness: 300,
      },
    },
  };

  const itemVariants = {
    open: {
      opacity: 1,
      x: 0,
      transition: {
        type: 'spring',
        damping: 25,
        stiffness: 300,
      },
    },
    closed: {
      opacity: 0,
      x: -20,
    },
  };

  return (
    <motion.div
      variants={sidebarVariants}
      animate={sidebarOpen ? 'open' : 'closed'}
      className="bg-white shadow-lg border-r border-gray-200 flex flex-col h-full"
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <motion.div
          animate={sidebarOpen ? { opacity: 1 } : { opacity: 0 }}
          className="flex items-center space-x-2"
        >
          <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <CpuChipIcon className="w-5 h-5 text-white" />
          </div>
          {sidebarOpen && (
            <motion.span
              variants={itemVariants}
              className="text-xl font-bold text-gray-900"
            >
              AI Framework
            </motion.span>
          )}
        </motion.div>

        <button
          onClick={toggleSidebar}
          className="p-1.5 rounded-md text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition-colors"
        >
          {sidebarOpen ? (
            <XMarkIcon className="w-5 h-5" />
          ) : (
            <Bars3Icon className="w-5 h-5" />
          )}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {navigation.map((item, index) => {
          const isActive = location.pathname === item.href;

          return (
            <motion.div
              key={item.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <NavLink
                to={item.href}
                onClick={() => setCurrentPage(item.name)}
                className={`
                  group flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-all duration-200
                  ${
                    isActive
                      ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg hover-lift'
                      : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
                  }
                `}
              >
                <item.icon
                  className={`
                    flex-shrink-0 w-5 h-5 transition-colors
                    ${isActive ? 'text-white' : 'text-gray-500 group-hover:text-gray-700'}
                  `}
                />
                {sidebarOpen && (
                  <motion.span
                    variants={itemVariants}
                    className="ml-3 truncate"
                  >
                    {item.name}
                  </motion.span>
                )}

                {isActive && (
                  <motion.div
                    layoutId="activeIndicator"
                    className="ml-auto w-1 h-1 bg-white rounded-full"
                    transition={{
                      type: 'spring',
                      damping: 30,
                      stiffness: 300,
                    }}
                  />
                )}
              </NavLink>
            </motion.div>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        <motion.div
          animate={sidebarOpen ? { opacity: 1 } : { opacity: 0 }}
          className="flex items-center space-x-2"
        >
          <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
            <span className="text-xs font-medium text-gray-600">AI</span>
          </div>
          {sidebarOpen && (
            <motion.div variants={itemVariants} className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                AI Agent
              </p>
              <p className="text-xs text-gray-500 truncate">
                v1.0.0
              </p>
            </motion.div>
          )}
        </motion.div>
      </div>
    </motion.div>
  );
};

export default Sidebar;
