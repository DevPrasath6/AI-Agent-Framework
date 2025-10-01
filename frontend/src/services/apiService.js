// API service for authentication and backend integration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class ApiService {
  constructor() {
    this.token = localStorage.getItem('authToken');
  }

  // Set authentication token
  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('authToken', token);
    } else {
      localStorage.removeItem('authToken');
    }
  }

  // Get default headers
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Token ${this.token}`;
    }

    return headers;
  }

  // Make API request
  async makeRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: this.getHeaders(),
      ...options,
    };

    // Automatic request logging to help debug from browser Console when user triggers form submit
    try {
      const safeHeaders = { ...config.headers };
      if (safeHeaders.Authorization) safeHeaders.Authorization = 'REDACTED';
      console.log('[apiService] Request ->', { url, method: config.method || 'GET', headers: safeHeaders, body: config.body });
    } catch (logErr) {
      // Ignore logging errors
    }

    try {
      const response = await fetch(url, config);

      // Attempt to parse JSON safely
      let data = null;
      try {
        data = await response.json();
      } catch (parseErr) {
        // Non-JSON response
        data = null;
      }

      if (!response.ok) {
        // If backend returned structured errors (e.g. field errors), include them
        const errorPayload = data || { detail: response.statusText };
        const err = new Error(errorPayload.detail || 'An error occurred');
        err.status = response.status;
        err.payload = errorPayload;
        throw err;
      }

      return data;
    } catch (error) {
      // Enhanced logging for network/CORS problems
      console.error('API Request Error:', {
        url,
        options: config,
        message: error && error.message,
        stack: error && error.stack,
      });

      // If this is a network-level error (e.g. CORS preflight blocked or server unreachable), normalize it
      const msg = (error && error.message) || '';
      if (msg.includes('Failed to fetch') || msg.includes('NetworkError') || msg.includes('Network request failed')) {
        const netErr = new Error('Network error: could not reach API. Check that the backend is running and CORS allows this origin.');
        netErr.payload = { detail: `Network error connecting to ${url}` };
        throw netErr;
      }

      throw error;
    }
  }

  // Authentication methods
  async register(userData) {
    const response = await this.makeRequest('/auth/register/', {
      method: 'POST',
      body: JSON.stringify({
        email: userData.email,
        first_name: userData.firstName,
        last_name: userData.lastName,
        password: userData.password,
        confirm_password: userData.confirmPassword,
      }),
    });

    if (response.token) {
      this.setToken(response.token);
    }

    return response;
  }

  async login(credentials) {
    const response = await this.makeRequest('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password,
      }),
    });

    if (response.token) {
      this.setToken(response.token);
    }

    return response;
  }

  async logout() {
    try {
      await this.makeRequest('/auth/logout/', {
        method: 'POST',
      });
    } finally {
      this.setToken(null);
    }
  }

  async getCurrentUser() {
    return this.makeRequest('/auth/me/');
  }

  async updateProfile(profileData) {
    return this.makeRequest('/auth/profile/', {
      method: 'PATCH',
      body: JSON.stringify(profileData),
    });
  }

  async changePassword(passwordData) {
    return this.makeRequest('/auth/change-password/', {
      method: 'POST',
      body: JSON.stringify(passwordData),
    });
  }

  // Agent methods
  async getAgents() {
    return this.makeRequest('/agents/');
  }

  async createAgent(agentData) {
    return this.makeRequest('/agents/', {
      method: 'POST',
      body: JSON.stringify(agentData),
    });
  }

  async getAgent(id) {
    return this.makeRequest(`/agents/${id}/`);
  }

  async updateAgent(id, agentData) {
    return this.makeRequest(`/agents/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(agentData),
    });
  }

  async deleteAgent(id) {
    return this.makeRequest(`/agents/${id}/`, {
      method: 'DELETE',
    });
  }

  // Workflow methods
  async getWorkflows() {
    return this.makeRequest('/workflows/');
  }

  async createWorkflow(workflowData) {
    return this.makeRequest('/workflows/', {
      method: 'POST',
      body: JSON.stringify(workflowData),
    });
  }

  async getWorkflow(id) {
    return this.makeRequest(`/workflows/${id}/`);
  }

  async updateWorkflow(id, workflowData) {
    return this.makeRequest(`/workflows/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(workflowData),
    });
  }

  async deleteWorkflow(id) {
    return this.makeRequest(`/workflows/${id}/`, {
      method: 'DELETE',
    });
  }

  // Monitoring methods
  async getMonitoringData() {
    return this.makeRequest('/monitoring/');
  }

  async getSystemStats() {
    return this.makeRequest('/monitoring/stats/');
  }
}

// Create and export singleton instance
const apiService = new ApiService();
export default apiService;
