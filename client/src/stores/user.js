import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { api } from '../main';

export const useUserStore = defineStore('user', () => {
  const user = ref(null);
  const loading = ref(false);
  const error = ref(null);

  const isAuthenticated = computed(() => !!user.value);

  // Set auth tokens in axios headers and localStorage
  const setAuthTokens = (access, refresh) => {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
  };

  // Clear auth tokens
  const clearAuth = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete api.defaults.headers.common['Authorization'];
    user.value = null;
  };

  // Check if user is authenticated on app load
  const checkAuth = async () => {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) return false;

    try {
      const response = await api.get('account/users/me/');
      user.value = response.data;
      return true;
    } catch (error) {
      clearAuth();
      return false;
    }
  };

  // Login user
  const login = async (email, password) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await api.post('account/login/', { email, password });
      const { access, refresh } = response.data;
      setAuthTokens(access, refresh);
      
      // Get user data
      const userResponse = await api.get('account/users/me/');
      user.value = userResponse.data;
      
      return { success: true };
    } catch (err) {
      error.value = err.response?.data?.detail || 'Login failed';
      return { success: false, error: error.value };
    } finally {
      loading.value = false;
    }
  };

  // Logout user
  const logout = () => {
    clearAuth();
  };

  // Register new user
  const register = async (userData) => {
    loading.value = true;
    error.value = null;
    
    try {
      await api.post('account/users/', userData);
      return { success: true, email: userData.email };
    } catch (err) {
      error.value = err.response?.data || 'Registration failed';
      return { success: false, error: error.value };
    } finally {
      loading.value = false;
    }
  };

  // Verify email with OTP
  const verifyEmail = async (email, otp) => {
    try {
      await api.post('account/users/verify_email/', { email, otp });
      return { success: true };
    } catch (err) {
      return { 
        success: false, 
        error: err.response?.data?.error || 'Verification failed' 
      };
    }
  };

  // Resend OTP
  const resendOtp = async (email) => {
    try {
      await api.post('account/users/resend_otp/', { email });
      return { success: true };
    } catch (err) {
      return { 
        success: false, 
        error: err.response?.data?.error || 'Failed to resend OTP' 
      };
    }
  };

  // Update user profile
  const updateProfile = async (userData) => {
    try {
      const response = await api.patch('account/users/me/', userData);
      user.value = { ...user.value, ...response.data };
      return { success: true };
    } catch (err) {
      return {
        success: false,
        error: err.response?.data || 'Failed to update profile'
      };
    }
  };

  // Change password
  const changePassword = async (currentPassword, newPassword) => {
    try {
      await api.post('account/password/change/', {
        current_password: currentPassword,
        new_password: newPassword
      });
      return { success: true };
    } catch (err) {
      return {
        success: false,
        error: err.response?.data || 'Failed to change password'
      };
    }
  };

  // Request password reset
  const requestPasswordReset = async (email) => {
    try {
      await api.post('account/password/reset/', { email });
      return { success: true };
    } catch (err) {
      return {
        success: false,
        error: err.response?.data || 'Failed to request password reset'
      };
    }
  };

  // Reset password with token
  const resetPassword = async (token, uid, newPassword) => {
    try {
      await api.post('account/password/reset/confirm/', {
        token,
        uid,
        new_password: newPassword
      });
      return { success: true };
    } catch (err) {
      return {
        success: false,
        error: err.response?.data || 'Failed to reset password'
      };
    }
  };

  return {
    user,
    loading,
    error,
    isAuthenticated,
    login,
    logout,
    register,
    verifyEmail,
    resendOtp,
    checkAuth
  };
});
