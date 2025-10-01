import React from 'react';
import { motion } from 'framer-motion';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <motion.footer initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div className="text-2xl font-bold mb-2">AI Framework</div>
            <p className="text-sm text-gray-300">Build, host, and scale AI workflows with confidence.</p>
            <div className="mt-4 text-sm text-gray-400">© {currentYear} AI Framework</div>
          </div>

          <div>
            <h4 className="font-semibold mb-3 text-gray-200">Product</h4>
            <ul className="text-sm text-gray-400 space-y-2">
              <li>Features</li>
              <li>Integrations</li>
              <li>Pricing</li>
              <li>Templates</li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-3 text-gray-200">Company</h4>
            <ul className="text-sm text-gray-400 space-y-2">
              <li>About</li>
              <li>Careers</li>
              <li>Contact</li>
              <li>Press</li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-3 text-gray-200">Get updates</h4>
            <p className="text-sm text-gray-400 mb-3">Subscribe for product news and tips.</p>
            <form onSubmit={(e) => e.preventDefault()} className="flex space-x-2">
              <input placeholder="Your email" className="w-full px-3 py-2 rounded-md text-gray-900" />
              <button className="px-4 py-2 bg-blue-600 rounded-md text-white">Subscribe</button>
            </form>
          </div>
        </div>

        <div className="mt-12 border-t border-gray-800 pt-6 flex flex-col md:flex-row items-center justify-between text-sm text-gray-400">
          <div className="mb-3 md:mb-0">Terms • Privacy • Security</div>
          <div>Built with care • Designed for scale</div>
        </div>
      </div>
    </motion.footer>
  );
};

export default Footer;
