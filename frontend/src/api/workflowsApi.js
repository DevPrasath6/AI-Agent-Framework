import axios from 'axios';
const BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
export default {
  list: () => axios.get(`${BASE}/workflows/`),
  retrieve: (id) => axios.get(`${BASE}/workflows/${id}/`),
  start: (id, payload) => axios.post(`${BASE}/workflows/${id}/start/`, payload),
};
