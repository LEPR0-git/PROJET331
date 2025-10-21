import axios from 'axios';

// URL de ton backend Flask
const API_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Utilisateurs
export const getUsers = () => api.get('/users');
export const getUserById = (id) => api.get(`/users/${id}`);
export const createUser = (data) => api.post('/users', data);
export const updateUser = (id, data) => api.put(`/users/${id}`, data);
export const deleteUser = (id) => api.delete(`/users/${id}`);

// Freelance Profiles
export const getProfiles = (params) => api.get('/freelance/profiles', { params });
export const getProfileById = (id) => api.get(`/freelance/profiles/${id}`);
export const createProfile = (data) => api.post('/freelance/profiles', data);
export const updateProfile = (id, data) => api.put(`/freelance/profiles/${id}`, data);
export const deleteProfile = (id) => api.delete(`/freelance/profiles/${id}`);

export default api;
