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
              <Loader2 class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" />
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
              <Loader2 class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" />
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
              <EyeOff v-if="showPassword1" class="h-5 w-5" />
              <Eye v-else class="h-5 w-5" />
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
              <EyeOff v-if="showPassword2" class="h-5 w-5" />
              <Eye v-else class="h-5 w-5" />
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
              <Loader2 class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" />
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
import { Eye, EyeOff, Loader2 } from 'lucide-vue-next';
import { message } from 'ant-design-vue';
import { useUserStore } from '@/stores/user';
const router = useRouter();
const userStore = useUserStore();
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
    await userStore.sendOtp(email.value);
    
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
    await userStore.sendResendOtp(email.value);
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
    const response = await userStore.verifyOtp(email.value, otp.value); 

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
    await userStore.updatePassword(
      password1.value,
      password2.value,
      token
    )

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
