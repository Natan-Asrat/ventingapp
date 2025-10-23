import { createApp } from 'vue';
import { createPinia } from 'pinia';
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';
import axios from 'axios';

import App from './App.vue';
import router from './router';

// Create app
const app = createApp(App);
const pinia = createPinia();

// Configure Axios defaults
const api = axios.create({
  baseURL: `${import.meta.env.VITE_BACKEND_URL}api/`,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: false,
});

// Request interceptor to add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If error is 401 and we haven't tried to refresh yet
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }
        
        // Try to refresh the token
        const response = await axios.post('http://localhost:8000/api/account/token/refresh/', {
          refresh: refreshToken
        });
        
        const { access } = response.data;
        
        // Update tokens
        localStorage.setItem('access_token', access);
        
        // Update the original request with the new token
        originalRequest.headers['Authorization'] = `Bearer ${access}`;
        
        // Retry the original request
        return api(originalRequest);
      } catch (error) {
        // If refresh fails, clear tokens and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        router.push('/login');
        return Promise.reject(error);
      }
    }
    
    return Promise.reject(error);
  }
);

// Make axios available globally (optional)
app.config.globalProperties.$http = api;

// Use plugins
app.use(pinia);
app.use(router);
app.use(Antd);

// Mount the app
app.mount('#app');

// Export the axios instance for use in stores and components
export { api };
