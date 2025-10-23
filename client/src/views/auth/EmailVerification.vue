<template>
  <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
    <div class="text-center mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Verify Your Email</h2>
      <p class="mt-2 text-sm text-gray-600">
        We've sent a verification code to <span class="font-medium">{{ email }}</span>
      </p>
    </div>

  <div class="space-y-6">
    <div>
      <label for="otp" class="block text-sm font-medium text-gray-700">Verification Code</label>
      <div class="mt-1">
        <input
          id="otp"
          v-model="otp"
          type="text"
          inputmode="numeric"
          pattern="[0-9]*"
          maxlength="6"
          required
          class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="Enter 6-digit code"
        />
      </div>
    </div>

    <div>
      <button
        type="button"
        @click="verifyOtp"
        :disabled="verifying || !otp || otp.length !== 6"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="verifying">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </span>
        <span v-else>Verify Email</span>
      </button>
    </div>

    <div class="text-center text-sm">
      <p class="text-gray-600">
        Didn't receive a code?
        <button
          @click="resendOtp"
          :disabled="resendCooldown > 0"
          class="font-medium text-indigo-600 hover:text-indigo-500 disabled:text-gray-400 disabled:cursor-not-allowed"
        >
          <span v-if="resendCooldown > 0">Resend in {{ resendCooldown }}s</span>
          <span v-else>Resend Code</span>
        </button>
      </p>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { message } from 'ant-design-vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  email: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['verified']);

const userStore = useUserStore();
const router = useRouter();

const otp = ref('');
const verifying = ref(false);
const resendCooldown = ref(60);
let countdownInterval = null;

const startCountdown = () => {
  resendCooldown.value = 60;
  countdownInterval = setInterval(() => {
    resendCooldown.value--;
    if (resendCooldown.value <= 0) {
      clearInterval(countdownInterval);
    }
  }, 1000);
};

const verifyOtp = async () => {
  if (!otp.value || otp.value.length !== 6) {
    message.error('Please enter a valid 6-digit code');
    return;
  }

  verifying.value = true;
  
  try {
    const { success, error } = await userStore.verifyEmail(props.email, otp.value);
    
    if (success) {
      message.success('Email verified successfully!');
      emit('verified');
    } else {
      message.error(error || 'Verification failed. Please try again.');
    }
  } catch (error) {
    console.error('Verification error:', error);
    message.error('An error occurred during verification. Please try again.');
  } finally {
    verifying.value = false;
  }
};

const resendOtp = async () => {
  if (resendCooldown.value > 0) return;
  
  try {
    const { success, error } = await userStore.resendOtp(props.email);
    
    if (success) {
      message.success('Verification code resent successfully!');
      startCountdown();
    } else {
      message.error(error || 'Failed to resend verification code');
    }
  } catch (error) {
    console.error('Resend OTP error:', error);
    message.error('An error occurred while resending the verification code');
  }
};

onMounted(() => {
  startCountdown();
});

onUnmounted(() => {
  if (countdownInterval) {
    clearInterval(countdownInterval);
  }
});
</script>
