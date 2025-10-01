import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { CheckIcon, SparklesIcon } from '@heroicons/react/24/outline';

const Pricing = () => {
  const [isYearly, setIsYearly] = useState(false);

  const plans = [
    {
      name: 'Starter',
      description: 'Perfect for individuals and small teams getting started',
      monthlyPrice: 0,
      yearlyPrice: 0,
      features: [
        '5 AI agents',
        '1,000 workflow executions/month',
        'Basic templates',
        'Community support',
        'Email notifications'
      ],
      popular: false,
      cta: 'Get started for free'
    },
    {
      name: 'Professional',
      description: 'For growing teams that need more power and flexibility',
      monthlyPrice: 29,
      yearlyPrice: 290,
      features: [
        'Unlimited AI agents',
        '10,000 workflow executions/month',
        'Advanced templates',
        'Priority support',
        'Custom integrations',
        'Team collaboration',
        'Advanced analytics'
      ],
      popular: true,
      cta: 'Start free trial'
    },
    {
      name: 'Enterprise',
      description: 'For large organizations with advanced requirements',
      monthlyPrice: 99,
      yearlyPrice: 990,
      features: [
        'Everything in Professional',
        'Unlimited executions',
        'Custom AI model integration',
        'Dedicated support',
        'SSO & advanced security',
        'Custom workflows',
        'On-premise deployment',
        'SLA guarantee'
      ],
      popular: false,
      cta: 'Contact sales'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-rose-50 to-orange-50">
      {/* Navigation Header */}
      <header className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b border-gray-100 z-50">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center space-x-2">
              <Link to="/" className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-rose-500 to-orange-500 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">n8n</span>
                </div>
                <span className="text-xl font-bold">n8n</span>
              </Link>
            </div>

            {/* Navigation Menu */}
            <nav className="hidden md:flex items-center space-x-8">
              <Link to="/products" className="text-gray-700 hover:text-gray-900 transition-colors">Products</Link>
              <Link to="/solutions" className="text-gray-700 hover:text-gray-900 transition-colors">Solutions</Link>
              <Link to="/pricing" className="text-rose-500 font-semibold">Pricing</Link>
              <Link to="/learn" className="text-gray-700 hover:text-gray-900 transition-colors">Learn</Link>
            </nav>

            {/* Auth Buttons */}
            <div className="flex items-center space-x-4">
              <Link to="/login" className="text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors duration-200">
                Sign in
              </Link>
              <Link to="/register" className="inline-flex items-center rounded-md bg-rose-500 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-rose-600 transition-colors duration-200">
                Get started free
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-28 pb-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
                Choose your plan
              </h1>
              <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                Start free, then add a site plan to go live. Account plans unlock additional features.
              </p>
            </motion.div>

            {/* Billing Toggle */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="flex items-center justify-center mb-16"
            >
              <span className={`mr-3 text-sm ${!isYearly ? 'text-gray-900 font-semibold' : 'text-gray-500'}`}>
                Monthly
              </span>
              <button
                onClick={() => setIsYearly(!isYearly)}
                className={`relative inline-flex items-center h-6 rounded-full w-11 transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500 ${
                  isYearly ? 'bg-purple-600' : 'bg-gray-200'
                }`}
              >
                <span
                  className={`inline-block w-4 h-4 transform transition-transform bg-white rounded-full ${
                    isYearly ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
              <span className={`ml-3 text-sm ${isYearly ? 'text-gray-900 font-semibold' : 'text-gray-500'}`}>
                Yearly
              </span>
              <span className="ml-2 px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                Save 17%
              </span>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="pb-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {plans.map((plan, index) => (
              <motion.div
                key={plan.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 + index * 0.1 }}
                className={`relative backdrop-blur-xl bg-white/70 border rounded-3xl shadow-xl p-8 ${
                  plan.popular
                    ? 'border-purple-200 ring-2 ring-purple-500 ring-opacity-50'
                    : 'border-gray-200 hover:border-gray-300'
                } transition-all duration-300 hover:shadow-2xl hover:scale-105`}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white text-sm font-semibold rounded-full">
                      <SparklesIcon className="w-4 h-4 mr-1" />
                      Most Popular
                    </span>
                  </div>
                )}

                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                  <p className="text-gray-600 mb-6">{plan.description}</p>

                  <div className="flex items-baseline justify-center">
                    <span className="text-5xl font-bold text-gray-900">
                      ${isYearly ? Math.floor(plan.yearlyPrice / 12) : plan.monthlyPrice}
                    </span>
                    <span className="text-gray-500 ml-1">/month</span>
                  </div>

                  {isYearly && plan.yearlyPrice > 0 && (
                    <p className="text-sm text-gray-500 mt-2">
                      Billed annually (${plan.yearlyPrice}/year)
                    </p>
                  )}
                </div>

                <ul className="space-y-4 mb-8">
                  {plan.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-start">
                      <CheckIcon className="w-5 h-5 text-green-500 mt-0.5 mr-3 flex-shrink-0" />
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>

                <Link
                  to={plan.name === 'Starter' ? '/register' : plan.name === 'Enterprise' ? '/contact' : '/register'}
                  className={`block w-full text-center py-3 px-6 rounded-lg font-semibold transition-all duration-200 ${
                    plan.popular
                      ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white hover:from-purple-700 hover:to-blue-700 shadow-lg'
                      : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                  }`}
                >
                  {plan.cta}
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 bg-white/50 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Frequently asked questions</h2>
            <p className="text-gray-600">Everything you need to know about our pricing and plans.</p>
          </motion.div>

          <div className="space-y-8">
            {[
              {
                question: 'Can I change my plan at any time?',
                answer: 'Yes, you can upgrade or downgrade your plan at any time. Changes will be reflected in your next billing cycle.'
              },
              {
                question: 'What happens if I exceed my workflow execution limit?',
                answer: 'We\'ll notify you when you approach your limit. You can upgrade your plan or purchase additional executions.'
              },
              {
                question: 'Is there a free trial available?',
                answer: 'Yes, we offer a 14-day free trial for all paid plans. No credit card required to get started.'
              },
              {
                question: 'Do you offer discounts for nonprofits or educational institutions?',
                answer: 'Yes, we provide special pricing for qualifying nonprofits and educational institutions. Contact our sales team for details.'
              }
            ].map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.0 + index * 0.1 }}
                className="backdrop-blur-xl bg-white/70 border border-gray-200 rounded-2xl p-6"
              >
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{faq.question}</h3>
                <p className="text-gray-600">{faq.answer}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Pricing;
