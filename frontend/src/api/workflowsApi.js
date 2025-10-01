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

const workflowsApi = {
  // Get all workflows
  getWorkflows: async (params = {}) => {
    try {
      const client = getApiClient();
      const response = await client.get('/workflows/', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch workflows');
    }
  },

  // Get single workflow by ID
  getWorkflow: async (id) => {
    try {
      const client = getApiClient();
      const response = await client.get(`/workflows/${id}/`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch workflow');
    }
  },

  // Create new workflow
  createWorkflow: async (workflowData) => {
    try {
      const client = getApiClient();
      const response = await client.post('/workflows/', workflowData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to create workflow');
    }
  },

  // Update existing workflow
  updateWorkflow: async (id, workflowData) => {
    try {
      const client = getApiClient();
      const response = await client.put(`/workflows/${id}/`, workflowData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to update workflow');
    }
  },

  // Delete workflow
  deleteWorkflow: async (id) => {
    try {
      const client = getApiClient();
      await client.delete(`/workflows/${id}/`);
      return { success: true };
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to delete workflow');
    }
  },

  // Start workflow execution
  startWorkflow: async (id, payload = {}) => {
    try {
      const client = getApiClient();
      const response = await client.post(`/workflows/${id}/start/`, payload);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to start workflow');
    }
  },

  // Stop workflow execution
  stopWorkflow: async (id) => {
    try {
      const client = getApiClient();
      const response = await client.post(`/workflows/${id}/stop/`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to stop workflow');
    }
  },

  // Get workflow execution history
  getWorkflowHistory: async (id, params = {}) => {
    try {
      const client = getApiClient();
      const response = await client.get(`/workflows/${id}/history/`, { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch workflow history');
    }
  },

  // Get workflow step details
  getWorkflowSteps: async (id) => {
    try {
      const client = getApiClient();
      const response = await client.get(`/workflows/${id}/steps/`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch workflow steps');
    }
  },

  // Validate workflow configuration
  validateWorkflow: async (workflowData) => {
    try {
      const client = getApiClient();
      const response = await client.post('/workflows/validate/', workflowData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to validate workflow');
    }
  },

  // Get workflow templates
  getWorkflowTemplates: async () => {
    try {
      const client = getApiClient();
      const response = await client.get('/workflows/templates/');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch workflow templates');
    }
  },

  // Clone workflow
  cloneWorkflow: async (id, newName) => {
    try {
      const client = getApiClient();
      const response = await client.post(`/workflows/${id}/clone/`, { name: newName });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to clone workflow');
    }
  }
};

export default workflowsApi;
