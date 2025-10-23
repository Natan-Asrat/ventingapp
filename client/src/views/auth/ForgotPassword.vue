<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Reset your password
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Enter your email and we'll send you a verification code
        </p>
      </div>

      <!-- Email Input Step -->
      <div v-if="currentStep === 'email'" class="mt-8 space-y-6">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email-address" class="sr-only">Email address</label>
            <input
              id="email-address"
              v-model="email"
              name="email"
              type="email"
              autocomplete="email"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="Email address"
            />
          </div>
        </div>

        <div>
          <button
            type="button"
            @click="sendOtp"
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            <span v-if="loading">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            <span v-else>Send Verification Code</span>
          </button>
        </div>
      </div>

      <!-- OTP Verification Step -->
      <div v-else-if="currentStep === 'verify'" class="mt-8 space-y-6">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="otp" class="sr-only">Verification Code</label>
            <input
              id="otp"
              v-model="otp"
              name="otp"
              type="text"
              inputmode="numeric"
              pattern="[0-9]*"
              maxlength="6"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="Enter 6-digit code"
            />
          </div>
        </div>

        <div class="flex items-center justify-between">
          <div class="text-sm">
            <button 
              @click="resendOtp" 
              :disabled="resendCooldown > 0"
              class="font-medium text-indigo-600 hover:text-indigo-500 disabled:text-gray-400 disabled:cursor-not-allowed cursor-pointer"
            >
              <span v-if="resendCooldown > 0">Resend in {{ resendCooldown }}s</span>
              <span v-else>Resend Code</span>
            </button>
          </div>
        </div>

        <div class="flex space-x-2">
          <button
            type="button"
            @click="currentStep = 'email'"
            class="w-1/2 flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer"
          >
            Back
          </button>
          <button
            type="button"
            @click="verifyOtp"
            :disabled="otp.length !== 6 || loading"
            class="w-1/2 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            <span v-if="loading">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            <span v-else>Verify Code</span>
          </button>
        </div>
      </div>

      <!-- New Password Step -->
      <div v-else-if="currentStep === 'newPassword'" class="mt-8 space-y-6">
        <div class="rounded-md shadow-sm -space-y-px">
          <div class="relative">
            <label for="password1" class="sr-only">New Password</label>
            <input
              :type="showPassword1 ? 'text' : 'password'"
              id="password1"
              v-model="password1"
              name="password1"
              autocomplete="new-password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm pr-10"
              placeholder="New Password"
            />
            <button
              type="button"
              @click="showPassword1 = !showPassword1"
              class="absolute inset-y-0 z-100 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-500 cursor-pointer"
              :aria-label="showPassword1 ? 'Hide password' : 'Show password'"
            >
              <svg v-if="showPassword1" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
              </svg>
              <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
          </div>
          <div class="relative">
            <label for="password2" class="sr-only">Confirm New Password</label>
            <input
              :type="showPassword2 ? 'text' : 'password'"
              id="password2"
              v-model="password2"
              name="password2"
              autocomplete="new-password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm pr-10"
              placeholder="Confirm New Password"
              @keyup.enter="updatePassword"
            />
            <button
              type="button"
              @click="showPassword2 = !showPassword2"
              class="absolute inset-y-0 right-0 z-100 pr-3 flex items-center text-gray-400 hover:text-gray-500 cursor-pointer"
              :aria-label="showPassword2 ? 'Hide password' : 'Show password'"
            >
              <svg v-if="showPassword2" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
              </svg>
              <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
          </div>
        </div>

        <div class="flex space-x-2">
          <button
            type="button"
            @click="currentStep = 'verify'"
            class="w-1/2 flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer"
          >
            Back
          </button>
          <button
            type="button"
            @click="updatePassword"
            :disabled="!password1 || password1 !== password2 || loading"
            class="w-1/2 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            <span v-if="loading">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            <span v-else>Update Password</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import axios from 'axios';

const router = useRouter();

const currentStep = ref('email');
const loading = ref(false);
const email = ref('');
const otp = ref('');
const password1 = ref('');
const password2 = ref('');
const showPassword1 = ref(false);
const showPassword2 = ref(false);
const resendCooldown = ref(0);
let countdownInterval = null;

const startCountdown = () => {
  resendCooldown.value = 60; // 60 seconds cooldown
  
  // Clear any existing interval to prevent multiple timers
  if (countdownInterval) clearInterval(countdownInterval);
  
  // Update the countdown every second
  countdownInterval = setInterval(() => {
    if (resendCooldown.value > 0) {
      resendCooldown.value--;
    } else {
      clearInterval(countdownInterval);
    }
  }, 1000);
};

// Check if we're coming back from email verification
onMounted(() => {
  const storedEmail = localStorage.getItem('resetEmail');
  const storedToken = localStorage.getItem('resetToken');
  
  if (storedEmail && storedToken) {
    email.value = storedEmail;
    currentStep.value = 'newPassword';
  } else if (storedEmail) {
    email.value = storedEmail;
    currentStep.value = 'verify';
  }
});

const sendOtp = async () => {
  if (!email.value) {
    message.error('Please enter your email');
    return;
  }

  loading.value = true;
  try {
    await axios.post('http://localhost:8000/api/account/users/send_reset_otp/', {
      email: email.value
    });
    
    localStorage.setItem('resetEmail', email.value);
    currentStep.value = 'verify';
    startCountdown();
    message.success('Verification code sent to your email!');
  } catch (error) {
    console.error('Error sending OTP:', error);
    message.error(error.response?.data?.error || 'Failed to send verification code');
  } finally {
    loading.value = false;
  }
};

const resendOtp = async () => {
  if (!email.value || resendCooldown.value > 0) {
    return;
  }
  
  loading.value = true;
  try {
    await axios.post('http://localhost:8000/api/account/users/send_reset_otp/', {
      email: email.value
    });
    startCountdown();
    message.success('Verification code resent!');
  } catch (error) {
    console.error('Error resending OTP:', error);
    message.error(error.response?.data?.error || 'Failed to resend verification code');
  } finally {
    loading.value = false;
  }
};

const verifyOtp = async () => {
  if (otp.value.length !== 6) {
    message.error('Please enter a valid 6-digit code');
    return;
  }

  loading.value = true;
  try {
    const response = await axios.post('http://localhost:8000/api/account/users/verify_reset_otp/', {
      email: email.value,
      otp: otp.value
    });

    const { access } = response.data;
    localStorage.setItem('resetToken', access);
    currentStep.value = 'newPassword';
  } catch (error) {
    console.error('Error verifying OTP:', error);
    message.error(error.response?.data?.error || 'Invalid verification code');
  } finally {
    loading.value = false;
  }
};

const updatePassword = async () => {
  if (password1.value !== password2.value) {
    message.error('Passwords do not match');
    return;
  }

  if (password1.value.length < 8) {
    message.error('Password must be at least 8 characters long');
    return;
  }

  const token = localStorage.getItem('resetToken');
  if (!token) {
    message.error('Session expired. Please start over.');
    resetFlow();
    return;
  }

  loading.value = true;
  try {
    await axios.post(
      'http://localhost:8000/api/account/users/reset_password/',
      {
        password1: password1.value,
        password2: password2.value
      },
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );

    message.success('Password updated successfully! Please login with your new password.');
    resetFlow();
    router.push('/login');
  } catch (error) {
    console.error('Error updating password:', error);
    message.error(error.response?.data?.error || 'Failed to update password');
  } finally {
    loading.value = false;
  }
};

const resetFlow = () => {
  localStorage.removeItem('resetEmail');
  localStorage.removeItem('resetToken');
  email.value = '';
  otp.value = '';
  password1.value = '';
  password2.value = '';
  currentStep.value = 'email';
};
</script>
