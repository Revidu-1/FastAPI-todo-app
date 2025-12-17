import axios from 'axios';

const API_BASE_URL = '/api/v1';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 errors (unauthorized) - clear token and redirect to login
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: async (username, password) => {
    const response = await apiClient.post('/auth/register', {
      username,
      password,
    });
    return response.data;
  },

  login: async (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await apiClient.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },
};

// Todo API
export const todoAPI = {
  getAll: async () => {
    const response = await apiClient.get('/todos');
    return response.data;
  },

  getById: async (id) => {
    const response = await apiClient.get(`/todos/${id}`);
    return response.data;
  },

  create: async (todo) => {
    const response = await apiClient.post('/todos', todo);
    return response.data;
  },

  update: async (id, todo) => {
    const response = await apiClient.patch(`/todos/${id}`, todo);
    return response.data;
  },

  delete: async (id) => {
    await apiClient.delete(`/todos/${id}`);
  },
};

export default apiClient;





