import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '@/api/axios';

export const useAuthStore = defineStore('auth', () => {
  
  // State
  const user = ref(null);
  const accessToken = ref(localStorage.getItem('access_token') || null);
  const refreshToken = ref(localStorage.getItem('refresh_token') || null);
  
  // Getters
  const isAuthenticated = computed(() => !!accessToken.value);
  
  // Actions
  const setTokens = (tokens) => {
    accessToken.value = tokens.access;
    localStorage.setItem('access_token', tokens.access);
    
    if (tokens.refresh) {
      refreshToken.value = tokens.refresh;
      localStorage.setItem('refresh_token', tokens.refresh);
    }
  };
  
  const setAccessToken = (token) => {
    accessToken.value = token;
    localStorage.setItem('access_token', token);
  };
  
  const logout = async () => {
    try {
      // If we have a refresh token, try to blacklist it
      if (refreshToken.value) {
        await api.post('/account/logout/', { refresh: refreshToken.value });
      }
    } catch (error) {
      console.error('Error during logout:', error);
    } finally {
      // Clear tokens and user data regardless of the API call result
      accessToken.value = null;
      refreshToken.value = null;
      user.value = null;
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      
      // Redirect to login
      window.location.href = '/login';
    }
  };
  
  // Initialize store from localStorage
  const init = () => {
    const storedAccessToken = localStorage.getItem('access_token');
    const storedRefreshToken = localStorage.getItem('refresh_token');
    
    if (storedAccessToken) {
      accessToken.value = storedAccessToken;
    }
    
    if (storedRefreshToken) {
      refreshToken.value = storedRefreshToken;
    }
  };
  
  // Call init when the store is created
  init();
  
  return {
    // State
    user,
    accessToken,
    refreshToken,
    
    // Getters
    isAuthenticated,
    
    // Actions
    setTokens,
    setAccessToken,
    logout,
  };
});
