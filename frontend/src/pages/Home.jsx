import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import {
  CogIcon,
  ShieldCheckIcon,
  BoltIcon,
  ChevronDownIcon,
  Bars3Icon,
  XMarkIcon,
  PlayIcon
} from '@heroicons/react/24/outline';

const Home = () => {
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [productDropdown, setProductDropdown] = useState(false);
  const [solutionsDropdown, setSolutionsDropdown] = useState(false);
  const [learnDropdown, setLearnDropdown] = useState(false);

  const trustedCompanies = [
    { name: 'IBM', logo: 'https://n8n.io/images/logos/ibm.svg' },
    { name: 'GitHub', logo: 'https://n8n.io/images/logos/github.svg' },
    { name: 'Salesforce', logo: 'https://n8n.io/images/logos/salesforce.svg' },
    { name: 'Microsoft', logo: 'https://n8n.io/images/logos/microsoft.svg' },
    { name: 'Spotify', logo: 'https://n8n.io/images/logos/spotify.svg' },
    { name: 'Google', logo: 'https://n8n.io/images/logos/google.svg' },
    { name: 'Notion', logo: 'https://n8n.io/images/logos/notion.svg' },
    { name: 'Slack', logo: 'https://n8n.io/images/logos/slack.svg' }
  ];

  const features = [
    {
      icon: <BoltIcon className="h-8 w-8 text-rose-500" />,
      title: "Drag-and-drop editor",
      description: "Build workflows visually with our intuitive node-based editor"
    },
    {
      icon: <CogIcon className="h-8 w-8 text-rose-500" />,
      title: "400+ integrations",
      description: "Connect all your favorite tools and services in minutes"
    },
    {
      icon: <ShieldCheckIcon className="h-8 w-8 text-rose-500" />,
      title: "Enterprise-ready",
      description: "Self-host or cloud, with advanced security and compliance"
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Header - Exact n8n.io style */}
      <header className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b border-gray-100 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-rose-500 to-orange-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">n8n</span>
              </div>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center space-x-8">
              {/* Products Dropdown */}
              <div className="relative">
                <button
                  onMouseEnter={() => setProductDropdown(true)}
                  onMouseLeave={() => setProductDropdown(false)}
                  className="flex items-center text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors duration-200"
                >
                  Product
                  <ChevronDownIcon className="ml-1 h-4 w-4" />
                </button>
                <AnimatePresence>
                  {productDropdown && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 10 }}
                      transition={{ duration: 0.2 }}
                      onMouseEnter={() => setProductDropdown(true)}
                      onMouseLeave={() => setProductDropdown(false)}
                      className="absolute left-0 mt-2 w-80 bg-white rounded-2xl shadow-xl border border-gray-200 p-6 z-50"
                    >
                      <div className="grid grid-cols-1 gap-4">
                        <Link to="/features" className="flex items-start p-3 rounded-lg hover:bg-gray-50 transition-colors">
                          <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center mr-3">
                            <BoltIcon className="w-5 h-5 text-white" />
                          </div>
                          <div>
                            <h3 className="font-semibold text-gray-900">Features</h3>
                            <p className="text-sm text-gray-600">Explore our powerful automation features</p>
                          </div>
                        </Link>
                        <Link to="/integrations" className="flex items-start p-3 rounded-lg hover:bg-gray-50 transition-colors">
                          <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-teal-600 rounded-lg flex items-center justify-center mr-3">
                            <CogIcon className="w-5 h-5 text-white" />
                          </div>
                          <div>
                            <h3 className="font-semibold text-gray-900">Integrations</h3>
                            <p className="text-sm text-gray-600">400+ apps and services to connect</p>
                          </div>
                        </Link>
                        <Link to="/templates" className="flex items-start p-3 rounded-lg hover:bg-gray-50 transition-colors">
                          <div className="w-10 h-10 bg-gradient-to-r from-orange-500 to-red-600 rounded-lg flex items-center justify-center mr-3">
                            <PlayIcon className="w-5 h-5 text-white" />
                          </div>
                          <div>
                            <h3 className="font-semibold text-gray-900">Templates</h3>
                            <p className="text-sm text-gray-600">Pre-built workflows to get started fast</p>
                          </div>
                        </Link>
                        <Link to="/enterprise" className="flex items-start p-3 rounded-lg hover:bg-gray-50 transition-colors">
                          <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-600 rounded-lg flex items-center justify-center mr-3">
                            <ShieldCheckIcon className="w-5 h-5 text-white" />
                          </div>
                          <div>
                            <h3 className="font-semibold text-gray-900">Enterprise</h3>
                            <p className="text-sm text-gray-600">Advanced security and compliance</p>
                          </div>
                        </Link>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {/* Solutions Dropdown */}
              <div className="relative">
                <button
                  onMouseEnter={() => setSolutionsDropdown(true)}
                  onMouseLeave={() => setSolutionsDropdown(false)}
                  className="flex items-center text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors duration-200"
                >
                  Solutions
                  <ChevronDownIcon className="ml-1 h-4 w-4" />
                </button>
                <AnimatePresence>
                  {solutionsDropdown && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 10 }}
                      transition={{ duration: 0.2 }}
                      onMouseEnter={() => setSolutionsDropdown(true)}
                      onMouseLeave={() => setSolutionsDropdown(false)}
                      className="absolute left-0 mt-2 w-80 bg-white rounded-2xl shadow-xl border border-gray-200 p-6 z-50"
                    >
                      <div className="grid grid-cols-1 gap-4">
                        <Link to="/solutions/marketing" className="flex items-start p-3 rounded-lg hover:bg-gray-50 transition-colors">
                          <div className="w-10 h-10 bg-gradient-to-r from-pink-500 to-rose-600 rounded-lg flex items-center justify-center mr-3">
                            <span className="text-white font-bold text-sm">M</span>
                          </div>
                          <div>
                            <h3 className="font-semibold text-gray-900">Marketing</h3>
                            <p className="text-sm text-gray-600">Automate campaigns and lead generation</p>
                          </div>
                        </Link>
                        <Link to="/solutions/sales" className="flex items-start p-3 rounded-lg hover:bg-gray-50 transition-colors">
                          <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center mr-3">
                            <span className="text-white font-bold text-sm">S</span>
                          </div>
                          <div>
                            <h3 className="font-semibold text-gray-900">Sales</h3>
                            <p className="text-sm text-gray-600">Streamline your sales processes</p>
                          </div>
                        </Link>
                        <Link to="/solutions/it-ops" className="flex items-start p-3 rounded-lg hover:bg-gray-50 transition-colors">
                          <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg flex items-center justify-center mr-3">
                            <span className="text-white font-bold text-sm">IT</span>
                          </div>
                          <div>
                            <h3 className="font-semibold text-gray-900">IT Operations</h3>
                            <p className="text-sm text-gray-600">Automate IT workflows and monitoring</p>
                          </div>
                        </Link>
                        <Link to="/solutions/hr" className="flex items-start p-3 rounded-lg hover:bg-gray-50 transition-colors">
                          <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-violet-600 rounded-lg flex items-center justify-center mr-3">
                            <span className="text-white font-bold text-sm">HR</span>
                          </div>
                          <div>
                            <h3 className="font-semibold text-gray-900">Human Resources</h3>
                            <p className="text-sm text-gray-600">Automate HR processes and onboarding</p>
                          </div>
                        </Link>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {/* Learn Dropdown */}
              <div className="relative">
                <button
                  onMouseEnter={() => setLearnDropdown(true)}
                  onMouseLeave={() => setLearnDropdown(false)}
                  className="flex items-center text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors duration-200"
                >
                  Learn
                  <ChevronDownIcon className="ml-1 h-4 w-4" />
                </button>
                <AnimatePresence>
                  {learnDropdown && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 10 }}
                      transition={{ duration: 0.2 }}
                      onMouseEnter={() => setLearnDropdown(true)}
                      onMouseLeave={() => setLearnDropdown(false)}
                      className="absolute left-0 mt-2 w-80 bg-white rounded-2xl shadow-xl border border-gray-200 p-6 z-50"
                    >
                      <div className="grid grid-cols-1 gap-4">
                        <Link to="/docs" className="flex items-start p-3 rounded-lg hover:bg-gray-50 transition-colors">
                          <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-cyan-600 rounded-lg flex items-center justify-center mr-3">
                            <span className="text-white font-bold text-sm">📚</span>
                          </div>
                          <div>
                            <h3 className="font-semibold text-gray-900">Documentation</h3>
                            <p className="text-sm text-gray-600">Complete guides and API reference</p>
                          </div>
                        </Link>
                        <Link to="/community" className="flex items-start p-3 rounded-lg hover:bg-gray-50 transition-colors">
                          <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-teal-600 rounded-lg flex items-center justify-center mr-3">
                            <span className="text-white font-bold text-sm">💬</span>
                          </div>
                          <div>
                            <h3 className="font-semibold text-gray-900">Community</h3>
                            <p className="text-sm text-gray-600">Connect with other n8n users</p>
                          </div>
                        </Link>
                        <Link to="/blog" className="flex items-start p-3 rounded-lg hover:bg-gray-50 transition-colors">
                          <div className="w-10 h-10 bg-gradient-to-r from-orange-500 to-amber-600 rounded-lg flex items-center justify-center mr-3">
                            <span className="text-white font-bold text-sm">📝</span>
                          </div>
                          <div>
                            <h3 className="font-semibold text-gray-900">Blog</h3>
                            <p className="text-sm text-gray-600">Latest news and tutorials</p>
                          </div>
                        </Link>
                        <Link to="/academy" className="flex items-start p-3 rounded-lg hover:bg-gray-50 transition-colors">
                          <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-indigo-600 rounded-lg flex items-center justify-center mr-3">
                            <span className="text-white font-bold text-sm">🎓</span>
                          </div>
                          <div>
                            <h3 className="font-semibold text-gray-900">Academy</h3>
                            <p className="text-sm text-gray-600">Learn automation best practices</p>
                          </div>
                        </Link>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              <Link to="/pricing" className="text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors duration-200">
                Pricing
              </Link>
            </nav>

            {/* CTA Buttons */}
            <div className="flex items-center space-x-4">
              <Link to="/login" className="text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors duration-200">
                Sign in
              </Link>
              <Link to="/register" className="inline-flex items-center rounded-md bg-rose-500 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-rose-600 transition-colors duration-200">
                Get started free
              </Link>

              {/* Mobile menu button */}
              <button
                type="button"
                className="md:hidden inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              >
                <span className="sr-only">Open main menu</span>
                {mobileMenuOpen ? (
                  <XMarkIcon className="block h-6 w-6" aria-hidden="true" />
                ) : (
                  <Bars3Icon className="block h-6 w-6" aria-hidden="true" />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile menu */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden bg-white border-t border-gray-100"
            >
              <div className="px-4 pt-2 pb-3 space-y-1">
                <Link
                  to="#"
                  className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-md"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Product
                </Link>
                <Link
                  to="#"
                  className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-md"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Solutions
                </Link>
                <Link
                  to="#"
                  className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-md"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Learn
                </Link>
                <Link
                  to="/pricing"
                  className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-md"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Pricing
                </Link>
                <div className="pt-4 pb-2 border-t border-gray-100">
                  <Link
                    to="/login"
                    className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-md"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    Sign in
                  </Link>
                  <Link
                    to="/register"
                    className="block px-3 py-2 text-base font-medium bg-rose-500 text-white hover:bg-rose-600 rounded-md mt-2"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    Get started free
                  </Link>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </header>

      {/* Hero Section - Exact n8n.io style */}
      <section className="relative pt-32 pb-20 px-6 lg:px-8 bg-white">
        <div className="mx-auto max-w-6xl">
          <div className="text-center">
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-5xl sm:text-6xl lg:text-7xl xl:text-8xl font-extrabold tracking-tight text-gray-900 mb-8"
            >
              Make anything{' '}
              <span className="bg-gradient-to-r from-rose-500 to-orange-500 bg-clip-text text-transparent">
                work together
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="mx-auto max-w-3xl text-xl sm:text-2xl text-gray-600 mb-12 leading-relaxed"
            >
              The easiest way to automate your workflows and connect your favorite tools.
              Build automation in minutes, not hours.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            >
              <motion.button
                whileHover={{ scale: 1.02, boxShadow: "0 10px 40px rgba(244, 63, 94, 0.3)" }}
                whileTap={{ scale: 0.98 }}
                className="px-8 py-4 bg-gradient-to-r from-rose-500 to-orange-500 text-white text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
                onClick={() => navigate('/register')}
              >
                Get started for free
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="px-8 py-4 border-2 border-gray-200 text-gray-700 text-lg font-semibold rounded-xl hover:border-gray-300 hover:bg-gray-50 transition-all duration-300 flex items-center gap-2"
              >
                <PlayIcon className="h-5 w-5" />
                See n8n in action
              </motion.button>
            </motion.div>

            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="mt-6 text-sm text-gray-500"
            >
              No credit card required • 5,000 workflow executions/month on free tier
            </motion.p>
          </div>
        </div>
      </section>

      {/* Trusted Companies Section */}
      <section className="py-16 bg-gray-50">
        <div className="mx-auto max-w-6xl px-6 lg:px-8">
          <div className="text-center mb-12">
            <p className="text-sm font-medium text-gray-500 mb-8">
              Trusted by thousands of companies worldwide
            </p>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-8 items-center justify-items-center">
              {trustedCompanies.map((company, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{
                    opacity: [0.4, 0.7, 0.4],
                    y: [0, -5, 0]
                  }}
                  transition={{
                    duration: 3,
                    delay: index * 0.2,
                    repeat: Infinity,
                    repeatType: "loop"
                  }}
                  className="grayscale hover:grayscale-0 transition-all duration-300"
                >
                  <img
                    src={company.logo}
                    alt={`${company.name} logo`}
                    className="h-8 w-auto opacity-60 hover:opacity-100 transition-opacity"
                  />
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="mx-auto max-w-6xl px-6 lg:px-8">
          <div className="text-center mb-16">
            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4"
            >
              Build powerful automations
            </motion.h2>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-xl text-gray-600 max-w-2xl mx-auto"
            >
              Connect your tools, automate your workflows, and focus on what matters most
            </motion.p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                className="text-center p-8 rounded-2xl hover:bg-gray-50 transition-colors duration-300"
              >
                <div className="flex justify-center mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Workflow Showcase Section */}
      <section className="py-20 bg-gray-50">
        <div className="mx-auto max-w-6xl px-6 lg:px-8">
          <div className="text-center mb-16">
            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4"
            >
              See how it works
            </motion.h2>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-xl text-gray-600 max-w-2xl mx-auto mb-8"
            >
              Build powerful workflows in minutes with our visual drag-and-drop editor
            </motion.p>
          </div>

          {/* Workflow Demo */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Connect your favorite tools
              </h3>
              <p className="text-gray-600 mb-6">
                Easily connect APIs, databases, and services with our extensive library of integrations.
                No coding required - just drag, drop, and configure.
              </p>
              <div className="space-y-4">
                {[
                  { name: 'Slack', desc: 'Send notifications and messages' },
                  { name: 'Gmail', desc: 'Automate email workflows' },
                  { name: 'Airtable', desc: 'Sync and update databases' }
                ].map((integration, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: 0.3 + index * 0.1 }}
                    className="flex items-center p-4 bg-white rounded-lg shadow-sm"
                  >
                    <div className="w-10 h-10 bg-gradient-to-r from-rose-500 to-orange-500 rounded-lg flex items-center justify-center mr-4">
                      <span className="text-white font-bold text-sm">{integration.name[0]}</span>
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">{integration.name}</h4>
                      <p className="text-sm text-gray-600">{integration.desc}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="relative"
            >
              {/* Workflow Visual Demo */}
              <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-200">
                <div className="flex items-center justify-between mb-6">
                  <h4 className="text-lg font-semibold text-gray-900">Sample Workflow</h4>
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                    <span className="text-sm text-gray-600">Active</span>
                  </div>
                </div>

                {/* Workflow Steps */}
                <div className="space-y-4">
                  {[
                    { step: 'Trigger', name: 'New Email', color: 'blue' },
                    { step: 'Process', name: 'Extract Data', color: 'purple' },
                    { step: 'Action', name: 'Update CRM', color: 'green' }
                  ].map((node, index) => (
                    <motion.div
                      key={index}
                      initial={{ scale: 0 }}
                      whileInView={{ scale: 1 }}
                      transition={{ duration: 0.5, delay: 0.2 + index * 0.2 }}
                      className="flex items-center"
                    >
                      <div className={`w-12 h-12 rounded-xl flex items-center justify-center mr-4 ${
                        node.color === 'blue' ? 'bg-blue-100 text-blue-600' :
                        node.color === 'purple' ? 'bg-purple-100 text-purple-600' :
                        'bg-green-100 text-green-600'
                      }`}>
                        <BoltIcon className="w-6 h-6" />
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">{node.step}</p>
                        <p className="font-semibold text-gray-900">{node.name}</p>
                      </div>
                      {index < 2 && (
                        <div className="ml-6 flex-1 h-px bg-gray-200 relative">
                          <motion.div
                            initial={{ width: 0 }}
                            whileInView={{ width: '100%' }}
                            transition={{ duration: 1, delay: 1 + index * 0.5 }}
                            className="h-full bg-gradient-to-r from-rose-500 to-orange-500"
                          />
                        </div>
                      )}
                    </motion.div>
                  ))}
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Social Proof Section */}
      <section className="py-20 bg-white">
        <div className="mx-auto max-w-6xl px-6 lg:px-8">
          <div className="text-center mb-16">
            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4"
            >
              Loved by developers and teams worldwide
            </motion.h2>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-xl text-gray-600"
            >
              See what our customers are saying about their automation experience
            </motion.p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            {[
              { number: '500K+', label: 'Active workflows' },
              { number: '50M+', label: 'Workflow executions' },
              { number: '200+', label: 'Countries served' }
            ].map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.5 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                className="text-center"
              >
                <div className="text-4xl font-bold text-gray-900 mb-2">{stat.number}</div>
                <div className="text-gray-600">{stat.label}</div>
              </motion.div>
            ))}
          </div>

          {/* Testimonials */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                quote: "n8n has transformed how we handle our workflows. The visual editor makes complex automations simple.",
                author: "Sarah Chen",
                role: "CTO at TechStart",
                avatar: "SC"
              },
              {
                quote: "The flexibility and power of n8n is unmatched. We've automated processes we never thought possible.",
                author: "Mike Rodriguez",
                role: "Operations Manager",
                avatar: "MR"
              },
              {
                quote: "Amazing tool for connecting our entire tech stack. Saves us hours of manual work every day.",
                author: "Anna Kim",
                role: "Product Manager",
                avatar: "AK"
              }
            ].map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                className="bg-gray-50 rounded-2xl p-8"
              >
                <p className="text-gray-600 mb-6 italic">"{testimonial.quote}"</p>
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-gradient-to-r from-rose-500 to-orange-500 rounded-full flex items-center justify-center text-white font-bold mr-4">
                    {testimonial.avatar}
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">{testimonial.author}</p>
                    <p className="text-sm text-gray-600">{testimonial.role}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-rose-500 to-orange-500">
        <div className="mx-auto max-w-4xl px-6 lg:px-8 text-center">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-3xl sm:text-4xl font-bold text-white mb-4"
          >
            Ready to automate your workflows?
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-xl text-rose-100 mb-8"
          >
            Join thousands of companies using n8n to build powerful automations
          </motion.p>
          <motion.button
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-8 py-4 bg-white text-rose-500 text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
            onClick={() => navigate('/register')}
          >
            Start building for free
          </motion.button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white">
        <div className="mx-auto max-w-6xl px-6 lg:px-8 py-16">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Company Info */}
            <div className="col-span-1">
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-r from-rose-500 to-orange-500 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">n8n</span>
                </div>
                <span className="text-xl font-bold">n8n</span>
              </div>
              <p className="text-gray-400 mb-6">
                The workflow automation platform that puts you in control.
              </p>
              <div className="flex space-x-4">
                <a
                  href="https://twitter.com/n8n_io"
                  className="text-gray-400 hover:text-white transition-colors"
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="Follow us on Twitter"
                >
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
                  </svg>
                </a>
                <a
                  href="https://pinterest.com/n8n_io"
                  className="text-gray-400 hover:text-white transition-colors"
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="Follow us on Pinterest"
                >
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.174-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 3.992-.285 1.193.6 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.097.118.112.222.083.343-.09.369-.293 1.199-.334 1.363-.053.225-.172.271-.402.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.357-.629-2.750-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24.009 12.017 24.009c6.624 0 11.990-5.367 11.990-11.988C24.007 5.367 18.641.001.012.001z.017 0z"/>
                  </svg>
                </a>
                <a
                  href="https://linkedin.com/company/n8n-io"
                  className="text-gray-400 hover:text-white transition-colors"
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="Follow us on LinkedIn"
                >
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                  </svg>
                </a>
              </div>
            </div>

            {/* Product Links */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Product</h3>
              <ul className="space-y-3">
                <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Features</Link></li>
                <li><Link to="/pricing" className="text-gray-400 hover:text-white transition-colors">Pricing</Link></li>
                <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Integrations</Link></li>
                <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Templates</Link></li>
              </ul>
            </div>

            {/* Resources Links */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Resources</h3>
              <ul className="space-y-3">
                <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Documentation</Link></li>
                <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Community</Link></li>
                <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Blog</Link></li>
                <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Support</Link></li>
              </ul>
            </div>

            {/* Company Links */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Company</h3>
              <ul className="space-y-3">
                <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">About</Link></li>
                <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Careers</Link></li>
                <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Contact</Link></li>
                <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Privacy</Link></li>
              </ul>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="border-t border-gray-800 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm">
              © 2025 n8n GmbH. All rights reserved.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <Link to="#" className="text-gray-400 hover:text-white text-sm transition-colors">Terms</Link>
              <Link to="#" className="text-gray-400 hover:text-white text-sm transition-colors">Privacy</Link>
              <Link to="#" className="text-gray-400 hover:text-white text-sm transition-colors">Cookies</Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;
