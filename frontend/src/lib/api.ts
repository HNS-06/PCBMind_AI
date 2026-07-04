import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('pcbmind_token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && typeof window !== 'undefined') {
      localStorage.removeItem('pcbmind_token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data: { email: string; username: string; password: string; full_name?: string }) =>
    api.post('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

export const projectsAPI = {
  list: (page = 1, perPage = 20) => api.get(`/projects?page=${page}&per_page=${perPage}`),
  get: (id: string) => api.get(`/projects/${id}`),
  create: (data: { name: string; description?: string; prompt: string }) =>
    api.post('/projects', data),
  update: (id: string, data: Record<string, unknown>) => api.patch(`/projects/${id}`, data),
  delete: (id: string) => api.delete(`/projects/${id}`),
  generate: (data: { prompt: string; model?: string; options?: Record<string, unknown> }) =>
    api.post('/projects/generate', data),
};

export const componentsAPI = {
  list: (params?: { category?: string; search?: string; limit?: number }) =>
    api.get('/components', { params }),
  get: (id: string) => api.get(`/components/${id}`),
  categories: () => api.get('/components/categories'),
};

export const chatAPI = {
  send: (data: { message: string; project_id?: string; conversation_id?: string; model?: string }) =>
    api.post('/chat', data),
};

export const exportAPI = {
  kicad: (projectId: string) => `${API_BASE}/export/${projectId}/kicad`,
  gerber: (projectId: string) => `${API_BASE}/export/${projectId}/gerber`,
  bom: (projectId: string) => `${API_BASE}/export/${projectId}/bom`,
  firmware: (projectId: string) => `${API_BASE}/export/${projectId}/firmware`,
};
