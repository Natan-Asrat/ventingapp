<template>
  <div class="min-h-screen flex items-center justify-center bg-zinc-50 py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
    <!-- Background Decor -->
    <div class="absolute top-0 right-0 w-[500px] h-[500px] bg-violet-200/20 rounded-full blur-3xl pointer-events-none translate-x-1/2 -translate-y-1/2"></div>
    
    <div class="max-w-md w-full space-y-8 relative z-10">
      <div class="bg-white py-8 px-4 shadow-xl shadow-zinc-200/50 sm:rounded-2xl sm:px-10 border border-zinc-100">
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-violet-100 mb-4 text-violet-600">
             <KeyRound v-if="currentStep === 'newPassword'" class="h-6 w-6" />
             <Mail v-else class="h-6 w-6" />
          </div>
          <h2 class="text-2xl font-bold text-zinc-900 tracking-tight">
            {{ currentStep === 'newPassword' ? 'Set New Password' : currentStep === 'verify' ? 'Verify Code' : 'Reset Password' }}
          </h2>
          <p class="mt-2 text-sm text-zinc-500">
            {{ 
              currentStep === 'newPassword' ? 'Create a strong password for your account' : 
              currentStep === 'verify' ? 'Enter the code sent to your email' : 
              "Enter your email and we'll send you instructions" 
            }}
          </p>
        </div>

        <!-- Email Input Step -->
        <div v-if="currentStep === 'email'" class="space-y-6">
          <div>
            <label for="email-address" class="block text-sm font-bold text-zinc-700 mb-1">Email address</label>
            <input
              id="email-address"
              v-model="email"
              name="email"
              type="email"
              autocomplete="email"
              required
              class="block w-full rounded-xl border-zinc-200 bg-zinc-50 px-4 py-3 text-zinc-900 placeholder-zinc-400 focus:border-violet-500 focus:bg-white focus:ring-violet-500/20 focus:outline-none focus:ring-4 transition-all sm:text-sm"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <button
              type="button"
              @click="sendOtp"
              :disabled="loading"
              class="w-full flex justify-center py-3 px-4 border border-transparent rounded-full shadow-lg shadow-zinc-900/10 text-sm font-bold text-white bg-zinc-900 hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-70 disabled:cursor-not-allowed transition-all hover:-translate-y-0.5 cursor-pointer"
            >
              <span v-if="loading" class="flex items-center">
                <Loader2 class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" />
                Sending...
              </span>
              <span v-else>Send Verification Code</span>
            </button>
          </div>
          
          <div class="text-center">
            <router-link to="/login" class="text-sm font-medium text-zinc-500 hover:text-zinc-900 transition-colors">
              Back to Sign in
            </router-link>
          </div>
        </div>

        <!-- OTP Verification Step -->
        <div v-else-if="currentStep === 'verify'" class="space-y-6">
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
              class="block w-full text-center text-2xl font-bold tracking-[0.5em] rounded-xl border-zinc-200 bg-zinc-50 py-3 text-zinc-900 placeholder-zinc-300 focus:border-violet-500 focus:bg-white focus:ring-violet-500/20 focus:outline-none focus:ring-4 transition-all"
              placeholder="000000"
            />
          </div>

          <div class="text-center text-sm">
            <p class="text-zinc-500">
              Didn't receive it?
              <button 
                @click="resendOtp" 
                :disabled="resendCooldown > 0"
                class="font-semibold text-violet-600 hover:text-violet-500 disabled:text-zinc-400 disabled:cursor-not-allowed cursor-pointer ml-1"
              >
                <span v-if="resendCooldown > 0">Resend in {{ resendCooldown }}s</span>
                <span v-else>Resend Code</span>
              </button>
            </p>
          </div>

          <div class="flex space-x-3">
            <button
              type="button"
              @click="currentStep = 'email'"
              class="w-1/3 flex justify-center py-3 px-4 border border-zinc-200 rounded-full text-sm font-semibold text-zinc-700 bg-white hover:bg-zinc-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-zinc-500 transition-all cursor-pointer"
            >
              Back
            </button>
            <button
              type="button"
              @click="verifyOtp"
              :disabled="otp.length !== 6 || loading"
              class="w-2/3 flex justify-center py-3 px-4 border border-transparent rounded-full shadow-lg shadow-zinc-900/10 text-sm font-bold text-white bg-zinc-900 hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-70 disabled:cursor-not-allowed transition-all hover:-translate-y-0.5 cursor-pointer"
            >
              <span v-if="loading" class="flex items-center">
                <Loader2 class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" />
                Verifying...
              </span>
              <span v-else>Verify Code</span>
            </button>
          </div>
        </div>

        <!-- New Password Step -->
        <div v-else-if="currentStep === 'newPassword'" class="space-y-6">
          <div class="space-y-4">
            <div>
              <label for="password1" class="block text-sm font-bold text-zinc-700 mb-1">New Password</label>
              <div class="relative">
                <input
                  :type="showPassword1 ? 'text' : 'password'"
                  id="password1"
                  v-model="password1"
                  name="password1"
                  autocomplete="new-password"
                  required
                  class="block w-full rounded-xl border-zinc-200 bg-zinc-50 px-4 py-3 pr-10 text-zinc-900 placeholder-zinc-400 focus:border-violet-500 focus:bg-white focus:ring-violet-500/20 focus:outline-none focus:ring-4 transition-all sm:text-sm"
                  placeholder="At least 8 characters"
                />
                <button
                  type="button"
                  @click="showPassword1 = !showPassword1"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-zinc-400 hover:text-zinc-600 cursor-pointer"
                >
                  <component :is="showPassword1 ? EyeOff : Eye" class="h-5 w-5" />
                </button>
              </div>
            </div>
            
            <div>
              <label for="password2" class="block text-sm font-bold text-zinc-700 mb-1">Confirm Password</label>
              <div class="relative">
                <input
                  :type="showPassword2 ? 'text' : 'password'"
                  id="password2"
                  v-model="password2"
                  name="password2"
                  autocomplete="new-password"
                  required
                  class="block w-full rounded-xl border-zinc-200 bg-zinc-50 px-4 py-3 pr-10 text-zinc-900 placeholder-zinc-400 focus:border-violet-500 focus:bg-white focus:ring-violet-500/20 focus:outline-none focus:ring-4 transition-all sm:text-sm"
                  placeholder="Repeat new password"
                  @keyup.enter="updatePassword"
                />
                <button
                  type="button"
                  @click="showPassword2 = !showPassword2"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-zinc-400 hover:text-zinc-600 cursor-pointer"
                >
                  <component :is="showPassword2 ? EyeOff : Eye" class="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>

          <div class="flex space-x-3">
            <button
              type="button"
              @click="currentStep = 'verify'"
              class="w-1/3 flex justify-center py-3 px-4 border border-zinc-200 rounded-full text-sm font-semibold text-zinc-700 bg-white hover:bg-zinc-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-zinc-500 transition-all cursor-pointer"
            >
              Back
            </button>
            <button
              type="button"
              @click="updatePassword"
              :disabled="!password1 || password1 !== password2 || loading"
              class="w-2/3 flex justify-center py-3 px-4 border border-transparent rounded-full shadow-lg shadow-zinc-900/10 text-sm font-bold text-white bg-zinc-900 hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-70 disabled:cursor-not-allowed transition-all hover:-translate-y-0.5 cursor-pointer"
            >
              <span v-if="loading" class="flex items-center">
                <Loader2 class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" />
                Updating...
              </span>
              <span v-else>Update Password</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { Eye, EyeOff, Loader2, Mail, KeyRound } from 'lucide-vue-next';
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