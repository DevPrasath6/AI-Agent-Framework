import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import {
  ChartBarIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  ClockIcon,
  CogIcon
} from '@heroicons/react/24/outline';

// 📊 REAL-TIME ANALYTICS CHARTS
export const RealTimeChart = ({ data, title, color = 'blue', type = 'line' }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current || !data?.length) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const { width, height } = canvas;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // Setup
    const padding = 20;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;

    const maxValue = Math.max(...data.map(d => d.value));
    const minValue = Math.min(...data.map(d => d.value));
    const valueRange = maxValue - minValue || 1;

    // Draw grid
    ctx.strokeStyle = '#f3f4f6';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
      const y = padding + (chartHeight / 5) * i;
      ctx.beginPath();
      ctx.moveTo(padding, y);
      ctx.lineTo(width - padding, y);
      ctx.stroke();
    }

    // Draw chart
    if (type === 'line') {
      // Line chart
      ctx.strokeStyle = color === 'blue' ? '#3b82f6' : color === 'green' ? '#10b981' : '#ef4444';
      ctx.lineWidth = 3;
      ctx.beginPath();

      data.forEach((point, index) => {
        const x = padding + (chartWidth / (data.length - 1)) * index;
        const y = padding + chartHeight - ((point.value - minValue) / valueRange) * chartHeight;

        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      ctx.stroke();

      // Add glow effect
      ctx.shadowColor = color === 'blue' ? '#3b82f6' : color === 'green' ? '#10b981' : '#ef4444';
      ctx.shadowBlur = 10;
      ctx.stroke();
      ctx.shadowBlur = 0;

      // Draw points
      data.forEach((point, index) => {
        const x = padding + (chartWidth / (data.length - 1)) * index;
        const y = padding + chartHeight - ((point.value - minValue) / valueRange) * chartHeight;

        ctx.beginPath();
        ctx.arc(x, y, 4, 0, 2 * Math.PI);
        ctx.fillStyle = color === 'blue' ? '#3b82f6' : color === 'green' ? '#10b981' : '#ef4444';
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();
      });
    } else if (type === 'bar') {
      // Bar chart
      const barWidth = chartWidth / data.length * 0.8;

      data.forEach((point, index) => {
        const x = padding + (chartWidth / data.length) * index + (chartWidth / data.length - barWidth) / 2;
        const barHeight = ((point.value - minValue) / valueRange) * chartHeight;
        const y = padding + chartHeight - barHeight;

        // Gradient fill
        const gradient = ctx.createLinearGradient(0, y, 0, y + barHeight);
        gradient.addColorStop(0, color === 'blue' ? '#3b82f6' : color === 'green' ? '#10b981' : '#ef4444');
        gradient.addColorStop(1, color === 'blue' ? '#1d4ed8' : color === 'green' ? '#047857' : '#dc2626');

        ctx.fillStyle = gradient;
        ctx.fillRect(x, y, barWidth, barHeight);

        // Add glow
        ctx.shadowColor = color === 'blue' ? '#3b82f6' : color === 'green' ? '#10b981' : '#ef4444';
        ctx.shadowBlur = 5;
        ctx.fillRect(x, y, barWidth, barHeight);
        ctx.shadowBlur = 0;
      });
    }
  }, [data, color, type]);

  return (
    <div className="relative">
      <canvas
        ref={canvasRef}
        width={400}
        height={200}
        className="w-full h-full"
      />
    </div>
  );
};

// 📈 ANALYTICS DASHBOARD WIDGET
export const AnalyticsWidget = ({ title, value, change, trend, color = 'blue', icon: Icon }) => {
  const [animatedValue, setAnimatedValue] = useState(0);

  useEffect(() => {
    const duration = 1500;
    const steps = 60;
    const stepValue = value / steps;
    let currentStep = 0;

    const timer = setInterval(() => {
      currentStep++;
      setAnimatedValue(Math.round(stepValue * currentStep));

      if (currentStep >= steps) {
        clearInterval(timer);
        setAnimatedValue(value);
      }
    }, duration / steps);

    return () => clearInterval(timer);
  }, [value]);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: 1.02 }}
      className="relative bg-white rounded-2xl shadow-lg border border-gray-200 p-6 overflow-hidden"
    >
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute -right-4 -top-4 w-24 h-24 rounded-full bg-gradient-to-br from-current to-transparent"></div>
        <div className="absolute -left-2 -bottom-2 w-16 h-16 rounded-full bg-gradient-to-tr from-current to-transparent"></div>
      </div>

      <div className="relative">
        <div className="flex items-center justify-between mb-4">
          <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${
            color === 'blue' ? 'from-blue-500 to-blue-600' :
            color === 'green' ? 'from-green-500 to-green-600' :
            color === 'purple' ? 'from-purple-500 to-purple-600' :
            'from-orange-500 to-orange-600'
          } flex items-center justify-center text-white shadow-lg`}>
            <Icon className="w-6 h-6" />
          </div>

          {change && (
            <div className={`flex items-center space-x-1 text-sm font-medium ${
              trend === 'up' ? 'text-green-600' : 'text-red-600'
            }`}>
              {trend === 'up' ?
                <ArrowTrendingUpIcon className="w-4 h-4" /> :
                <ArrowTrendingDownIcon className="w-4 h-4" />
              }
              <span>{Math.abs(change)}%</span>
            </div>
          )}
        </div>

        <h3 className="text-sm font-medium text-gray-600 mb-2">{title}</h3>

        <div className="text-3xl font-bold text-gray-900 mb-1">
          {typeof animatedValue === 'number' && animatedValue >= 1000
            ? `${(animatedValue / 1000).toFixed(1)}k`
            : animatedValue.toLocaleString()
          }
        </div>

        {/* Animated progress bar */}
        <div className="mt-4">
          <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${(animatedValue / value) * 100}%` }}
              transition={{ duration: 1.5, ease: "easeOut" }}
              className={`h-full rounded-full bg-gradient-to-r ${
                color === 'blue' ? 'from-blue-500 to-blue-600' :
                color === 'green' ? 'from-green-500 to-green-600' :
                color === 'purple' ? 'from-purple-500 to-purple-600' :
                'from-orange-500 to-orange-600'
              }`}
            />
          </div>
        </div>
      </div>
    </motion.div>
  );
};

// 📊 COMPREHENSIVE ANALYTICS DASHBOARD
export const AnalyticsDashboard = () => {
  const [timeRange, setTimeRange] = useState('7d');
  const [isLive, setIsLive] = useState(true);

  // Sample data - in real app, this would come from API
  const [analyticsData, setAnalyticsData] = useState({
    executions: [
      { time: '00:00', value: 120 },
      { time: '04:00', value: 89 },
      { time: '08:00', value: 200 },
      { time: '12:00', value: 278 },
      { time: '16:00', value: 189 },
      { time: '20:00', value: 239 },
      { time: '24:00', value: 156 }
    ],
    performance: [
      { time: 'Mon', value: 94.2 },
      { time: 'Tue', value: 96.1 },
      { time: 'Wed', value: 92.8 },
      { time: 'Thu', value: 97.3 },
      { time: 'Fri', value: 95.7 },
      { time: 'Sat', value: 91.4 },
      { time: 'Sun', value: 93.9 }
    ]
  });

  // Simulate real-time updates
  useEffect(() => {
    if (!isLive) return;

    const interval = setInterval(() => {
      setAnalyticsData(prev => ({
        ...prev,
        executions: prev.executions.map(point => ({
          ...point,
          value: point.value + Math.random() * 20 - 10
        }))
      }));
    }, 3000);

    return () => clearInterval(interval);
  }, [isLive]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h2>

        <div className="flex items-center space-x-4">
          {/* Live indicator */}
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${isLive ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}`}></div>
            <span className="text-sm text-gray-600">{isLive ? 'Live' : 'Paused'}</span>
            <button
              onClick={() => setIsLive(!isLive)}
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              {isLive ? 'Pause' : 'Resume'}
            </button>
          </div>

          {/* Time range selector */}
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="1d">24 Hours</option>
            <option value="7d">7 Days</option>
            <option value="30d">30 Days</option>
            <option value="90d">90 Days</option>
          </select>
        </div>
      </div>

      {/* Analytics Widgets Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <AnalyticsWidget
          title="Total Executions"
          value={2847}
          change={12.5}
          trend="up"
          color="blue"
          icon={ChartBarIcon}
        />
        <AnalyticsWidget
          title="Success Rate"
          value={94.2}
          change={2.1}
          trend="up"
          color="green"
          icon={ArrowTrendingUpIcon}
        />
        <AnalyticsWidget
          title="Avg Response Time"
          value={245}
          change={-5.3}
          trend="down"
          color="purple"
          icon={ClockIcon}
        />
        <AnalyticsWidget
          title="Active Workflows"
          value={18}
          change={8.7}
          trend="up"
          color="orange"
          icon={CogIcon}
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Executions Chart */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Workflow Executions</h3>
            <div className="text-sm text-gray-500">Last 24 hours</div>
          </div>
          <RealTimeChart
            data={analyticsData.executions}
            title="Executions"
            color="blue"
            type="line"
          />
        </motion.div>

        {/* Performance Chart */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Success Rate</h3>
            <div className="text-sm text-gray-500">Weekly average</div>
          </div>
          <RealTimeChart
            data={analyticsData.performance}
            title="Performance"
            color="green"
            type="bar"
          />
        </motion.div>
      </div>
    </motion.div>
  );
};

export default AnalyticsDashboard;
