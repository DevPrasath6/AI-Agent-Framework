// Application Constants
export const APP_NAME = 'AI Agent Framework';
export const APP_VERSION = '1.0.0';
export const APP_DESCRIPTION = 'Advanced AI Agent Management and Orchestration Platform';

// API Constants
export const API_ENDPOINTS = {
  AGENTS: '/agents',
  WORKFLOWS: '/workflows',
  MONITORING: '/monitoring',
  HEALTH: '/health',
  AUTH: '/auth',
  USERS: '/users',
  SETTINGS: '/settings'
};

// Agent Status Constants
export const AGENT_STATUS = {
  ACTIVE: 'active',
  INACTIVE: 'inactive',
  TRAINING: 'training',
  ERROR: 'error',
  PENDING: 'pending'
};

// Workflow Status Constants
export const WORKFLOW_STATUS = {
  RUNNING: 'running',
  COMPLETED: 'completed',
  FAILED: 'failed',
  PAUSED: 'paused',
  SCHEDULED: 'scheduled'
};

// UI Constants
export const THEME = {
  LIGHT: 'light',
  DARK: 'dark',
  AUTO: 'auto'
};

export const TOAST_DURATION = {
  SHORT: 3000,
  MEDIUM: 5000,
  LONG: 8000
};

// Pagination Constants
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100]
};

// Time Ranges for Analytics
export const TIME_RANGES = {
  LAST_HOUR: '1h',
  LAST_24_HOURS: '24h',
  LAST_7_DAYS: '7d',
  LAST_30_DAYS: '30d',
  LAST_90_DAYS: '90d'
};

// File Upload Constants
export const FILE_UPLOAD = {
  MAX_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_TYPES: [
    'application/json',
    'text/plain',
    'text/csv',
    'application/yaml',
    'application/x-yaml'
  ]
};

// Model Providers
export const MODEL_PROVIDERS = {
  OPENAI: 'openai',
  ANTHROPIC: 'anthropic',
  HUGGINGFACE: 'huggingface',
  LOCAL: 'local'
};

// Default Model Configurations
export const DEFAULT_MODELS = {
  [MODEL_PROVIDERS.OPENAI]: {
    'gpt-4': { name: 'GPT-4', maxTokens: 8192 },
    'gpt-3.5-turbo': { name: 'GPT-3.5 Turbo', maxTokens: 4096 }
  },
  [MODEL_PROVIDERS.ANTHROPIC]: {
    'claude-3-opus': { name: 'Claude 3 Opus', maxTokens: 200000 },
    'claude-3-sonnet': { name: 'Claude 3 Sonnet', maxTokens: 200000 }
  }
};

// Validation Rules
export const VALIDATION = {
  AGENT_NAME: {
    MIN_LENGTH: 3,
    MAX_LENGTH: 50,
    PATTERN: /^[a-zA-Z0-9_-]+$/
  },
  WORKFLOW_NAME: {
    MIN_LENGTH: 3,
    MAX_LENGTH: 100,
    PATTERN: /^[a-zA-Z0-9\s_-]+$/
  },
  EMAIL: {
    PATTERN: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  }
};

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error occurred. Please check your connection.',
  UNAUTHORIZED: 'You are not authorized to perform this action.',
  NOT_FOUND: 'The requested resource was not found.',
  SERVER_ERROR: 'Internal server error occurred. Please try again later.',
  VALIDATION_ERROR: 'Please check your input and try again.',
  TIMEOUT_ERROR: 'Request timed out. Please try again.'
};

// Success Messages
export const SUCCESS_MESSAGES = {
  AGENT_CREATED: 'Agent created successfully',
  AGENT_UPDATED: 'Agent updated successfully',
  AGENT_DELETED: 'Agent deleted successfully',
  WORKFLOW_CREATED: 'Workflow created successfully',
  WORKFLOW_UPDATED: 'Workflow updated successfully',
  WORKFLOW_DELETED: 'Workflow deleted successfully',
  SETTINGS_SAVED: 'Settings saved successfully'
};
