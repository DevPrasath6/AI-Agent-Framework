import axios from 'axios';
const BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
export default {
  health: () => axios.get(`${BASE}/monitoring/health/`),
  logs: (params) => axios.get(`${BASE}/monitoring/logs/`, { params }),
  metrics: (params) => axios.get(`${BASE}/monitoring/metrics/`, { params }),
};
