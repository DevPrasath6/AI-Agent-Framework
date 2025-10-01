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

const monitoringApi = {
  // Get system health status
  getHealth: async () => {
    try {
      const client = getApiClient();
      const response = await client.get('/monitoring/health/');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch system health');
    }
  },

  // Get system metrics
  getMetrics: async (params = {}) => {
    try {
      const client = getApiClient();
      const response = await client.get('/monitoring/metrics/', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch metrics');
    }
  },

  // Get system logs
  getLogs: async (params = {}) => {
    try {
      const client = getApiClient();
      const response = await client.get('/monitoring/logs/', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch logs');
    }
  },

  // Get performance analytics
  getPerformanceData: async (timeRange = '24h') => {
    try {
      const client = getApiClient();
      const response = await client.get('/monitoring/performance/', {
        params: { timeRange }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch performance data');
    }
  },

  // Get alerts and notifications
  getAlerts: async (params = {}) => {
    try {
      const client = getApiClient();
      const response = await client.get('/monitoring/alerts/', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch alerts');
    }
  },

  // Create alert rule
  createAlert: async (alertData) => {
    try {
      const client = getApiClient();
      const response = await client.post('/monitoring/alerts/', alertData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to create alert');
    }
  },

  // Update alert rule
  updateAlert: async (id, alertData) => {
    try {
      const client = getApiClient();
      const response = await client.put(`/monitoring/alerts/${id}/`, alertData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to update alert');
    }
  },

  // Delete alert rule
  deleteAlert: async (id) => {
    try {
      const client = getApiClient();
      await client.delete(`/monitoring/alerts/${id}/`);
      return { success: true };
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to delete alert');
    }
  },

  // Get resource usage statistics
  getResourceUsage: async () => {
    try {
      const client = getApiClient();
      const response = await client.get('/monitoring/resources/');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch resource usage');
    }
  },

  // Get error statistics
  getErrorStats: async (timeRange = '24h') => {
    try {
      const client = getApiClient();
      const response = await client.get('/monitoring/errors/', {
        params: { timeRange }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to fetch error statistics');
    }
  }
};

export default monitoringApi;
