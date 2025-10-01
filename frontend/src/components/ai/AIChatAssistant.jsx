import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ChatBubbleLeftRightIcon,
  PaperAirplaneIcon,
  XMarkIcon,
  SparklesIcon,
  LightBulbIcon,
  CodeBracketIcon,
  WrenchScrewdriverIcon,
  RocketLaunchIcon
} from '@heroicons/react/24/outline';

// 🤖 AI CHAT ASSISTANT
export const AIChatAssistant = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: "Hi! I'm your AI workflow assistant. I can help you create workflows, debug issues, and optimize your automation. What can I help you with today?",
      timestamp: new Date(),
      suggestions: ['Create a workflow', 'Debug an issue', 'Optimize performance', 'Learn best practices']
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // AI Response Simulation
  const getAIResponse = (userMessage) => {
    const responses = {
      'create': {
        content: "I'd be happy to help you create a workflow! Here are some popular workflow templates:\n\n• **Lead Processing**: Automatically qualify and route leads\n• **Email Automation**: Send personalized follow-up sequences\n• **Data Sync**: Keep your systems synchronized\n• **Customer Onboarding**: Streamline new user experiences\n\nWhich type interests you most?",
        suggestions: ['Lead Processing', 'Email Automation', 'Data Sync', 'Customer Onboarding']
      },
      'debug': {
        content: "Let me help you debug your workflow! Common issues I can help with:\n\n• **Connection Errors**: API authentication problems\n• **Data Transformation**: Mapping and formatting issues\n• **Timing Problems**: Delays and execution order\n• **Error Handling**: Improving resilience\n\nWhat specific issue are you experiencing?",
        suggestions: ['Connection failed', 'Data not mapping', 'Workflow too slow', 'Random errors']
      },
      'optimize': {
        content: "Great! I can help optimize your workflows for better performance:\n\n• **Parallel Processing**: Run tasks simultaneously\n• **Caching**: Store frequently used data\n• **Batch Operations**: Process multiple items together\n• **Smart Scheduling**: Run workflows at optimal times\n\nWhich workflow would you like to optimize?",
        suggestions: ['View my workflows', 'Performance tips', 'Best practices', 'Schedule optimization']
      },
      'default': {
        content: "I understand you're looking for help. I can assist with:\n\n• 🔧 **Creating new workflows**\n• 🐛 **Debugging issues**\n• ⚡ **Performance optimization**\n• 📚 **Best practices and tips**\n• 🔗 **Integration guidance**\n\nJust let me know what you need!",
        suggestions: ['Create workflow', 'Fix an error', 'Improve performance', 'Show examples']
      }
    };

    const userLower = userMessage.toLowerCase();
    if (userLower.includes('create') || userLower.includes('new') || userLower.includes('workflow')) {
      return responses.create;
    } else if (userLower.includes('debug') || userLower.includes('error') || userLower.includes('fix') || userLower.includes('problem')) {
      return responses.debug;
    } else if (userLower.includes('optimize') || userLower.includes('performance') || userLower.includes('speed') || userLower.includes('improve')) {
      return responses.optimize;
    } else {
      return responses.default;
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    // Simulate AI processing time
    setTimeout(() => {
      const aiResponse = getAIResponse(inputValue);
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: aiResponse.content,
        timestamp: new Date(),
        suggestions: aiResponse.suggestions
      };

      setMessages(prev => [...prev, assistantMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const handleSuggestionClick = (suggestion) => {
    setInputValue(suggestion);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <>
      {/* Chat Toggle Button */}
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center z-50"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        initial={{ opacity: 0, scale: 0 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 1 }}
      >
        <AnimatePresence mode="wait">
          {isOpen ? (
            <motion.div
              key="close"
              initial={{ rotate: -90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: 90, opacity: 0 }}
              transition={{ duration: 0.2 }}
            >
              <XMarkIcon className="w-6 h-6" />
            </motion.div>
          ) : (
            <motion.div
              key="chat"
              initial={{ rotate: -90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: 90, opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="relative"
            >
              <ChatBubbleLeftRightIcon className="w-6 h-6" />
              <motion.div
                className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ repeat: Infinity, duration: 2 }}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </motion.button>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 100, scale: 0.8 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 100, scale: 0.8 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className="fixed bottom-24 right-6 w-96 h-[600px] bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col overflow-hidden z-40"
          >
            {/* Header */}
            <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-4 flex items-center space-x-3">
              <div className="relative">
                <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                  <SparklesIcon className="w-6 h-6" />
                </div>
                <motion.div
                  className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-white"
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ repeat: Infinity, duration: 2 }}
                />
              </div>
              <div>
                <h3 className="font-semibold">AI Workflow Assistant</h3>
                <p className="text-sm text-white/80">Online • Ready to help</p>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[80%] ${message.type === 'user' ? 'order-2' : 'order-1'}`}>
                    {message.type === 'assistant' && (
                      <div className="flex items-center space-x-2 mb-1">
                        <div className="w-6 h-6 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center">
                          <SparklesIcon className="w-4 h-4 text-white" />
                        </div>
                        <span className="text-xs text-gray-500">AI Assistant</span>
                      </div>
                    )}

                    <div className={`p-3 rounded-2xl ${
                      message.type === 'user'
                        ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white ml-2'
                        : 'bg-white border border-gray-200 mr-2'
                    }`}>
                      <div className="text-sm whitespace-pre-line">{message.content}</div>
                    </div>

                    {/* Suggestions */}
                    {message.suggestions && message.type === 'assistant' && (
                      <div className="mt-2 flex flex-wrap gap-2">
                        {message.suggestions.map((suggestion, index) => (
                          <motion.button
                            key={index}
                            onClick={() => handleSuggestionClick(suggestion)}
                            className="px-3 py-1 bg-purple-100 text-purple-700 text-xs rounded-full hover:bg-purple-200 transition-colors"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                          >
                            {suggestion}
                          </motion.button>
                        ))}
                      </div>
                    )}
                  </div>
                </motion.div>
              ))}

              {/* Typing Indicator */}
              {isTyping && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex justify-start"
                >
                  <div className="flex items-center space-x-2 mb-1">
                    <div className="w-6 h-6 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center">
                      <SparklesIcon className="w-4 h-4 text-white" />
                    </div>
                    <div className="bg-white border border-gray-200 rounded-2xl p-3">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="border-t border-gray-200 bg-white p-4">
              <div className="flex items-end space-x-3">
                <div className="flex-1">
                  <textarea
                    ref={inputRef}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask me about workflows, debugging, or optimization..."
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none text-sm"
                    rows="2"
                  />
                </div>
                <motion.button
                  onClick={handleSendMessage}
                  disabled={!inputValue.trim() || isTyping}
                  className="w-10 h-10 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <PaperAirplaneIcon className="w-5 h-5" />
                </motion.button>
              </div>

              {/* Quick Actions */}
              <div className="mt-3 flex space-x-2">
                {[
                  { icon: CodeBracketIcon, label: 'Create', action: () => setInputValue('Help me create a new workflow') },
                  { icon: WrenchScrewdriverIcon, label: 'Debug', action: () => setInputValue('I need help debugging an issue') },
                  { icon: RocketLaunchIcon, label: 'Optimize', action: () => setInputValue('How can I optimize my workflow performance?') },
                  { icon: LightBulbIcon, label: 'Tips', action: () => setInputValue('Show me best practices and tips') }
                ].map((action, index) => (
                  <motion.button
                    key={index}
                    onClick={action.action}
                    className="flex items-center space-x-1 px-2 py-1 bg-gray-100 hover:bg-gray-200 rounded-md text-xs text-gray-600 transition-colors"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <action.icon className="w-3 h-3" />
                    <span>{action.label}</span>
                  </motion.button>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default AIChatAssistant;
