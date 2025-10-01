import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const PerformanceMonitor = () => {
  const [metrics, setMetrics] = useState({
    loadTime: 0,
    renderTime: 0,
    memoryUsage: 0,
    fps: 0,
    isVisible: false
  });

  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    // Performance monitoring
    const updateMetrics = () => {
      const navigation = performance.getEntriesByType('navigation')[0];
      const memory = performance.memory || {};

      setMetrics(prev => ({
        ...prev,
        loadTime: navigation ? Math.round(navigation.loadEventEnd - navigation.loadEventStart) : 0,
        memoryUsage: memory.usedJSHeapSize ? Math.round(memory.usedJSHeapSize / 1048576) : 0, // Convert to MB
        isVisible: process.env.NODE_ENV === 'development'
      }));
    };

    // FPS counter
    let frameCount = 0;
    let lastTime = performance.now();

    const countFPS = () => {
      frameCount++;
      const currentTime = performance.now();
      if (currentTime >= lastTime + 1000) {
        setMetrics(prev => ({ ...prev, fps: frameCount }));
        frameCount = 0;
        lastTime = currentTime;
      }
      requestAnimationFrame(countFPS);
    };

    updateMetrics();
    countFPS();

    // Update metrics every 5 seconds
    const interval = setInterval(updateMetrics, 5000);

    return () => clearInterval(interval);
  }, []);

  if (!metrics.isVisible) return null;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      className="fixed bottom-4 right-4 z-50"
    >
      <motion.div
        className="bg-black/80 backdrop-blur-sm text-white rounded-lg shadow-lg border border-gray-600 overflow-hidden"
        whileHover={{ scale: 1.02 }}
      >
        <div
          className="px-3 py-2 cursor-pointer flex items-center space-x-2"
          onClick={() => setShowDetails(!showDetails)}
        >
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span className="text-xs font-mono">PERF</span>
          <span className="text-xs text-gray-300">{metrics.fps} FPS</span>
        </div>

        <AnimatePresence>
          {showDetails && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="border-t border-gray-600"
            >
              <div className="p-3 space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-gray-300">Load Time:</span>
                  <span className="font-mono">{metrics.loadTime}ms</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-gray-300">Memory:</span>
                  <span className="font-mono">{metrics.memoryUsage}MB</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-gray-300">FPS:</span>
                  <span className={`font-mono ${metrics.fps >= 30 ? 'text-green-400' : 'text-yellow-400'}`}>
                    {metrics.fps}
                  </span>
                </div>
                <div className="pt-2 border-t border-gray-600">
                  <div className="text-xs text-gray-400">
                    React {React.version} • Dev Mode
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
};

export default PerformanceMonitor;
