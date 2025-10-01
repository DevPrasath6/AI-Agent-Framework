// Advanced UI Components for Enhanced User Experience

// 1. ANIMATED STATISTICS CARD WITH PARTICLES
import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';

export const AnimatedStatsCard = ({ title, value, change, icon, particles = true }) => {
  const canvasRef = useRef(null);
  const [isHovered, setIsHovered] = useState(false);

  // Helper to render icon which may be a component, a React element, or a plain string (emoji)
  const renderIcon = () => {
    if (!icon) return null;

    if (React.isValidElement(icon)) return icon;

    if (typeof icon === 'string') {
      return <span className="text-white text-2xl">{icon}</span>;
    }

    // Assume it's a component
    const IconComponent = icon;
    return <IconComponent className="w-6 h-6 text-white" />;
  };

  // Particle system for background effects
  useEffect(() => {
    if (!particles || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const particlesArray = [];

    class Particle {
      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 3 + 1;
        this.speedX = Math.random() * 3 - 1.5;
        this.speedY = Math.random() * 3 - 1.5;
        this.opacity = Math.random() * 0.5 + 0.2;
      }

      update() {
        this.x += this.speedX;
        this.y += this.speedY;

        if (this.x > canvas.width) this.x = 0;
        if (this.x < 0) this.x = canvas.width;
        if (this.y > canvas.height) this.y = 0;
        if (this.y < 0) this.y = canvas.height;
      }

      draw() {
        ctx.fillStyle = `rgba(244, 114, 182, ${this.opacity})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // Create particles
    for (let i = 0; i < 50; i++) {
      particlesArray.push(new Particle());
    }

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particlesArray.forEach(particle => {
        particle.update();
        particle.draw();
      });
      requestAnimationFrame(animate);
    };

    animate();
  }, [particles]);

  return (
    <motion.div
      whileHover={{ y: -5, scale: 1.02 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      className="relative overflow-hidden bg-gradient-to-br from-white/80 to-white/40 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-2xl"
    >
      <canvas
        ref={canvasRef}
        width={300}
        height={150}
        className="absolute inset-0 opacity-30"
      />

      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <motion.div
            animate={{
              rotate: isHovered ? 360 : 0,
              scale: isHovered ? 1.1 : 1
            }}
            transition={{ duration: 0.6 }}
            className="p-3 bg-gradient-to-r from-rose-500 to-orange-500 rounded-2xl"
          >
            {renderIcon()}
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className={`text-sm font-medium px-3 py-1 rounded-full ${
              change > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}
          >
            {change > 0 ? '↗' : '↘'} {Math.abs(change)}%
          </motion.div>
        </div>

        <h3 className="text-lg font-medium text-gray-600 mb-2">{title}</h3>

        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: 'spring' }}
          className="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent"
        >
          {typeof value === 'number' ? value.toLocaleString() : value}
        </motion.div>
      </div>
    </motion.div>
  );
};

// 2. ADVANCED COMMAND PALETTE
export const CommandPalette = ({ isOpen, onClose }) => {
  const [query, setQuery] = useState('');
  const [selectedIndex] = useState(0);

  const commands = [
    { id: 1, name: 'Create New Workflow', shortcut: '⌘N', action: () => {} },
    { id: 2, name: 'Search Workflows', shortcut: '⌘K', action: () => {} },
    { id: 3, name: 'Open Settings', shortcut: '⌘,', action: () => {} },
    { id: 4, name: 'View Analytics', shortcut: '⌘A', action: () => {} },
  ];

  const filteredCommands = commands.filter(cmd =>
    cmd.name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: isOpen ? 1 : 0 }}
      exit={{ opacity: 0 }}
      className={`fixed inset-0 z-50 ${isOpen ? 'pointer-events-auto' : 'pointer-events-none'}`}
    >
      <div className="absolute inset-0 bg-black/20 backdrop-blur-sm" onClick={onClose} />

      <div className="relative min-h-screen flex items-start justify-center pt-[20vh]">
        <motion.div
          initial={{ scale: 0.8, y: 20 }}
          animate={{ scale: isOpen ? 1 : 0.8, y: isOpen ? 0 : 20 }}
          className="w-full max-w-2xl mx-4 bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-gray-200/50"
        >
          <div className="p-4 border-b border-gray-200">
            <input
              type="text"
              placeholder="Type a command or search..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full text-lg bg-transparent border-none outline-none placeholder-gray-500"
              autoFocus
            />
          </div>

          <div className="max-h-80 overflow-y-auto">
            {filteredCommands.map((command, index) => (
              <motion.div
                key={command.id}
                whileHover={{ backgroundColor: 'rgba(244, 114, 182, 0.1)' }}
                className={`flex items-center justify-between px-4 py-3 cursor-pointer ${
                  index === selectedIndex ? 'bg-rose-50' : ''
                }`}
                onClick={command.action}
              >
                <span className="font-medium text-gray-900">{command.name}</span>
                <kbd className="px-2 py-1 bg-gray-100 rounded text-xs text-gray-600">
                  {command.shortcut}
                </kbd>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
};

// 3. WORKFLOW VISUALIZATION WITH INTERACTIVE NODES
export const WorkflowVisualization = ({ workflow }) => {
  const [selectedNode, setSelectedNode] = useState(null);

  const nodes = [
    { id: 1, type: 'trigger', label: 'Webhook', x: 50, y: 100, status: 'active' },
    { id: 2, type: 'action', label: 'Process Data', x: 200, y: 100, status: 'active' },
    { id: 3, type: 'condition', label: 'Check Status', x: 350, y: 100, status: 'pending' },
    { id: 4, type: 'action', label: 'Send Email', x: 500, y: 50, status: 'waiting' },
    { id: 5, type: 'action', label: 'Update CRM', x: 500, y: 150, status: 'waiting' },
  ];

  const connections = [
    { from: 1, to: 2 },
    { from: 2, to: 3 },
    { from: 3, to: 4 },
    { from: 3, to: 5 },
  ];

  return (
    <div className="relative w-full h-96 bg-gradient-to-br from-gray-50 to-blue-50 rounded-xl overflow-hidden">
      <svg className="absolute inset-0 w-full h-full">
        {/* Render connections */}
        {connections.map((conn, index) => {
          const fromNode = nodes.find(n => n.id === conn.from);
          const toNode = nodes.find(n => n.id === conn.to);

          return (
            <motion.path
              key={index}
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 1, delay: index * 0.2 }}
              d={`M ${fromNode.x + 50} ${fromNode.y + 25} Q ${(fromNode.x + toNode.x) / 2} ${fromNode.y + 25} ${toNode.x} ${toNode.y + 25}`}
              stroke="url(#gradient)"
              strokeWidth="2"
              fill="none"
              className="drop-shadow-sm"
            />
          );
        })}

        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#f43f5e" />
            <stop offset="100%" stopColor="#fb923c" />
          </linearGradient>
        </defs>
      </svg>

      {/* Render nodes */}
      {nodes.map((node, index) => (
        <motion.div
          key={node.id}
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: index * 0.1 }}
          whileHover={{ scale: 1.1 }}
          onClick={() => setSelectedNode(node)}
          className={`absolute w-20 h-12 rounded-lg cursor-pointer shadow-lg flex items-center justify-center text-xs font-medium text-white transform -translate-x-1/2 -translate-y-1/2 ${
            selectedNode?.id === node.id ? 'ring-2 ring-blue-400 ' : ''
          }${
            node.status === 'active' ? 'bg-green-500' :
            node.status === 'pending' ? 'bg-yellow-500' :
            'bg-gray-400'
          }`}
          style={{ left: node.x, top: node.y }}
        >
          {node.label}
        </motion.div>
      ))}
    </div>
  );
};

// 4. ADVANCED DATA TABLE WITH VIRTUAL SCROLLING
export const AdvancedDataTable = ({ data, columns }) => {
  const [sortField, setSortField] = useState(null);
  const [sortDirection, setSortDirection] = useState('asc');
  const [selectedRows, setSelectedRows] = useState(new Set());

  const sortedData = React.useMemo(() => {
    if (!sortField) return data;

    return [...data].sort((a, b) => {
      const aVal = a[sortField];
      const bVal = b[sortField];

      if (sortDirection === 'asc') {
        return aVal > bVal ? 1 : -1;
      } else {
        return aVal < bVal ? 1 : -1;
      }
    });
  }, [data, sortField, sortDirection]);

  return (
    <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gradient-to-r from-gray-50 to-gray-100">
            <tr>
              <th className="p-4">
                <input
                  type="checkbox"
                  className="rounded border-gray-300 text-rose-500 focus:ring-rose-500"
                  onChange={(e) => {
                    if (e.target.checked) {
                      setSelectedRows(new Set(data.map(row => row.id)));
                    } else {
                      setSelectedRows(new Set());
                    }
                  }}
                />
              </th>
              {columns.map((column) => (
                <th
                  key={column.key}
                  className="p-4 text-left font-semibold text-gray-900 cursor-pointer hover:bg-gray-200 transition-colors"
                  onClick={() => {
                    if (sortField === column.key) {
                      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
                    } else {
                      setSortField(column.key);
                      setSortDirection('asc');
                    }
                  }}
                >
                  <div className="flex items-center space-x-2">
                    <span>{column.label}</span>
                    {sortField === column.key && (
                      <motion.span
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="text-rose-500"
                      >
                        {sortDirection === 'asc' ? '↑' : '↓'}
                      </motion.span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sortedData.map((row, index) => (
              <motion.tr
                key={row.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                className={`hover:bg-gray-50 transition-colors ${
                  selectedRows.has(row.id) ? 'bg-rose-50' : ''
                }`}
              >
                <td className="p-4">
                  <input
                    type="checkbox"
                    checked={selectedRows.has(row.id)}
                    className="rounded border-gray-300 text-rose-500 focus:ring-rose-500"
                    onChange={(e) => {
                      const newSelected = new Set(selectedRows);
                      if (e.target.checked) {
                        newSelected.add(row.id);
                      } else {
                        newSelected.delete(row.id);
                      }
                      setSelectedRows(newSelected);
                    }}
                  />
                </td>
                {columns.map((column) => (
                  <td key={column.key} className="p-4 text-gray-900">
                    {column.render ? column.render(row[column.key], row) : row[column.key]}
                  </td>
                ))}
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// 5. REAL-TIME NOTIFICATION SYSTEM
export const NotificationSystem = () => {
  const [notifications, setNotifications] = useState([]);

  // Function to add notifications (currently unused but available for future use)
  // const addNotification = (notification) => {
  //   const id = Date.now();
  //   setNotifications(prev => [...prev, { ...notification, id }]);

  //   setTimeout(() => {
  //     setNotifications(prev => prev.filter(n => n.id !== id));
  //   }, 5000);
  // };

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {notifications.map((notification) => (
        <motion.div
          key={notification.id}
          initial={{ opacity: 0, x: 300, scale: 0.3 }}
          animate={{ opacity: 1, x: 0, scale: 1 }}
          exit={{ opacity: 0, x: 300, scale: 0.3 }}
          className={`p-4 rounded-2xl shadow-2xl backdrop-blur-xl border max-w-sm ${
            notification.type === 'success' ? 'bg-green-500/90 border-green-400 text-white' :
            notification.type === 'error' ? 'bg-red-500/90 border-red-400 text-white' :
            notification.type === 'warning' ? 'bg-yellow-500/90 border-yellow-400 text-white' :
            'bg-blue-500/90 border-blue-400 text-white'
          }`}
        >
          <div className="flex items-start space-x-3">
            <div className="flex-1">
              <h4 className="font-semibold">{notification.title}</h4>
              <p className="text-sm opacity-90">{notification.message}</p>
            </div>
            <button
              onClick={() => setNotifications(prev => prev.filter(n => n.id !== notification.id))}
              className="text-white/70 hover:text-white"
            >
              ✕
            </button>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

const AdvancedUIComponents = {
  AnimatedStatsCard,
  CommandPalette,
  WorkflowVisualization,
  AdvancedDataTable,
  NotificationSystem
};

export default AdvancedUIComponents;
