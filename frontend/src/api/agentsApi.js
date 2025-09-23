import axios from 'axios';
const BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
export default {
  list: () => axios.get(`${BASE}/agents/`),
  retrieve: (id) => axios.get(`${BASE}/agents/${id}/`),
  start: (id, payload) => axios.post(`${BASE}/agents/${id}/start/`, payload),
};
