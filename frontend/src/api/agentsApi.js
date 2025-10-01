import axios from 'axios';

// Get API client configuration
const getApiClient = () => {
  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

  const client = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Add auth token if available
  const token = localStorage.getItem('authToken');
  if (token) {
    client.defaults.headers.Authorization = `Bearer ${token}`;
  }

  return client;
};

const agentsApi = {
  // Get all agents
  getAgents: async (params = {}) => {
    try {
      const client = getApiClient();
      const response = await client.get('/agents/', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch agents');
    }
  },

  // Get single agent by ID
  getAgent: async (id) => {
    try {
      const client = getApiClient();
      const response = await client.get(`/agents/${id}/`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch agent');
    }
  },

  // Create new agent
  createAgent: async (agentData) => {
    try {
      const client = getApiClient();
      const response = await client.post('/agents/', agentData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to create agent');
    }
  },

  // Update existing agent
  updateAgent: async (id, agentData) => {
    try {
      const client = getApiClient();
      const response = await client.put(`/agents/${id}/`, agentData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to update agent');
    }
  },

  // Delete agent
  deleteAgent: async (id) => {
    try {
      const client = getApiClient();
      await client.delete(`/agents/${id}/`);
      return { success: true };
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to delete agent');
    }
  },

  // Start agent execution
  startAgent: async (id, payload = {}) => {
    try {
      const client = getApiClient();
      const response = await client.post(`/agents/${id}/start/`, payload);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to start agent');
    }
  },

  // Stop agent execution
  stopAgent: async (id) => {
    try {
      const client = getApiClient();
      const response = await client.post(`/agents/${id}/stop/`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to stop agent');
    }
  },

  // Get agent execution logs
  getAgentLogs: async (id, params = {}) => {
    try {
      const client = getApiClient();
      const response = await client.get(`/agents/${id}/logs/`, { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch agent logs');
    }
  },

  // Get agent metrics
  getAgentMetrics: async (id, timeRange = '24h') => {
    try {
      const client = getApiClient();
      const response = await client.get(`/agents/${id}/metrics/`, {
        params: { timeRange }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch agent metrics');
    }
  },

  // Test agent configuration
  testAgent: async (agentData) => {
    try {
      const client = getApiClient();
      const response = await client.post('/agents/test/', agentData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to test agent');
    }
  }
};

export default agentsApi;
