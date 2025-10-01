import React, { lazy, Suspense } from 'react';

// ⚡ PERFORMANCE OPTIMIZATION: Lazy Loading Components
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Workflows = lazy(() => import('./pages/Workflows'));
const Settings = lazy(() => import('./pages/Settings'));

// Advanced Components (loaded on demand)
const AdvancedUIComponents = lazy(() => import('./components/advanced/AdvancedUIComponents'));

// Loading Fallback Component
const LoadingFallback = () => (
  <div className="min-h-screen bg-gray-50 flex items-center justify-center">
    <div className="text-center">
      <div className="w-16 h-16 bg-gradient-to-r from-rose-500 to-orange-500 rounded-2xl flex items-center justify-center text-white font-bold text-2xl mx-auto mb-4 animate-pulse">
        n8n
      </div>
      <div className="flex items-center justify-center space-x-1">
        <div className="w-2 h-2 bg-rose-500 rounded-full animate-bounce"></div>
        <div className="w-2 h-2 bg-orange-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
        <div className="w-2 h-2 bg-rose-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
      </div>
      <p className="text-gray-600 mt-4">Loading...</p>
    </div>
  </div>
);

// Performance Monitoring Hook
export const usePerformanceMonitor = () => {
  const [metrics, setMetrics] = React.useState({
    loadTime: 0,
    renderTime: 0,
    memoryUsage: 0
  });

  React.useEffect(() => {
    // Performance Observer for monitoring
    if ('performance' in window && 'PerformanceObserver' in window) {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry) => {
          if (entry.entryType === 'navigation') {
            setMetrics(prev => ({
              ...prev,
              loadTime: entry.loadEventEnd - entry.loadEventStart
            }));
          }
        });
      });

      observer.observe({ entryTypes: ['navigation', 'measure'] });

      return () => observer.disconnect();
    }
  }, []);

  return metrics;
};

// Code Splitting HOC
export const withCodeSplitting = (Component) => {
  return (props) => (
    <Suspense fallback={<LoadingFallback />}>
      <Component {...props} />
    </Suspense>
  );
};

// Lazy loaded components with error boundaries
export const LazyDashboard = withCodeSplitting(Dashboard);
export const LazyWorkflows = withCodeSplitting(Workflows);
export const LazySettings = withCodeSplitting(Settings);
export const LazyAdvancedComponents = withCodeSplitting(AdvancedUIComponents);

// Preload critical components
export const preloadCriticalComponents = () => {
  // Preload dashboard since it's likely to be visited first
  Dashboard();

  // Preload other components after a delay
  setTimeout(() => {
    Workflows();
    Settings();
  }, 2000);
};

// Performance optimization utilities
export const performanceOptimizations = {
  // Enable React Strict Mode for development
  enableStrictMode: process.env.NODE_ENV === 'development',

  // Lazy load images
  lazyLoadImages: () => {
    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('lazy');
            imageObserver.unobserve(img);
          }
        });
      });

      document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
      });
    }
  },

  // Service Worker registration for caching
  registerServiceWorker: () => {
    if ('serviceWorker' in navigator && process.env.NODE_ENV === 'production') {
      navigator.serviceWorker.register('/sw.js')
        .then(registration => {
          console.log('SW registered: ', registration);
        })
        .catch(registrationError => {
          console.log('SW registration failed: ', registrationError);
        });
    }
  },

  // Memory cleanup
  cleanupMemory: () => {
    if (window.gc && process.env.NODE_ENV === 'development') {
      window.gc();
    }
  }
};

const performanceUtils = {
  LazyDashboard,
  LazyWorkflows,
  LazySettings,
  LazyAdvancedComponents,
  usePerformanceMonitor,
  withCodeSplitting,
  preloadCriticalComponents,
  performanceOptimizations,
  LoadingFallback
};

export default performanceUtils;
