import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import {
  Bars3Icon,
  MagnifyingGlassIcon,
} from '@heroicons/react/24/outline';

const Header = () => {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="bg-white border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-6">
            <Link to="/" className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-blue-600 rounded-md flex items-center justify-center text-white font-bold">AF</div>
              <div className="hidden sm:block">
                <div className="text-lg font-bold text-gray-900">AI Framework</div>
                <div className="text-xs text-gray-500">Workflow automation for teams</div>
              </div>
            </Link>

            <nav className="hidden lg:flex items-center space-x-4">
              <Link to="/" className="text-sm text-gray-700 hover:text-gray-900">Home</Link>
              <Link to="/workflows" className="text-sm text-gray-700 hover:text-gray-900">Workflows</Link>
              <Link to="/agents" className="text-sm text-gray-700 hover:text-gray-900">Agents</Link>
              <Link to="/monitoring" className="text-sm text-gray-700 hover:text-gray-900">Monitoring</Link>
              <Link to="/docs" className="text-sm text-gray-700 hover:text-gray-900">Docs</Link>
            </nav>
          </div>

          <div className="flex items-center space-x-4">
            <div className="hidden md:flex items-center bg-gray-100 rounded-lg px-3 py-1 space-x-2">
              <MagnifyingGlassIcon className="w-5 h-5 text-gray-400" />
              <input placeholder="Search" className="bg-transparent outline-none text-sm text-gray-700" />
            </div>

            <div className="hidden sm:flex items-center space-x-3">
              <Link to="/pricing" className="text-sm text-gray-700 hover:text-gray-900">Pricing</Link>
              <Link to="/login" className="text-sm text-gray-700 hover:text-gray-900">Sign in</Link>
              <Link to="/register" className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-md text-sm font-semibold hover:opacity-95">Get started</Link>
            </div>

            <button onClick={() => setMobileOpen(!mobileOpen)} className="lg:hidden p-2 rounded-md text-gray-600 hover:bg-gray-50">
              <Bars3Icon className="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="lg:hidden border-t border-gray-100">
          <div className="px-4 py-3 space-y-2">
            <Link to="/workflows" className="block text-gray-700">Workflows</Link>
            <Link to="/agents" className="block text-gray-700">Agents</Link>
            <Link to="/monitoring" className="block text-gray-700">Monitoring</Link>
            <Link to="/docs" className="block text-gray-700">Docs</Link>
            <div className="pt-2">
              <Link to="/register" className="block w-full text-center px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-md">Get started</Link>
            </div>
          </div>
        </motion.div>
      )}
    </header>
  );
};

export default Header;
