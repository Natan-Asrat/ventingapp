<template>
  <div class="space-y-6">
    <div class="text-center">
      <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-violet-100 mb-4">
        <Mail class="h-6 w-6 text-violet-600" />
      </div>
      <p class="text-sm text-zinc-500" v-if="email">
        We've sent a 6-digit code to<br/>
        <span class="font-semibold text-zinc-900">{{ email }}</span>
      </p>
    </div>

    <div class="space-y-6">
      <div>
        <label for="otp" class="sr-only">Verification Code</label>
        <input
          id="otp"
          v-model="otp"
          type="text"
          inputmode="numeric"
          pattern="[0-9]*"
          maxlength="6"
          required
          class="block w-full text-center text-2xl font-bold tracking-[0.5em] rounded-xl border-zinc-200 bg-zinc-50 py-3 text-zinc-900 placeholder-zinc-300 focus:border-violet-500 focus:bg-white focus:ring-violet-500/20 focus:outline-none focus:ring-4 transition-all"
          placeholder="000000"
        />
      </div>

      <button
        type="button"
        @click="verifyOtp"
        :disabled="verifying || !otp || otp.length !== 6"
        class="w-full flex justify-center py-3 px-4 border border-transparent rounded-full shadow-lg shadow-zinc-900/10 text-sm font-bold text-white bg-zinc-900 hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-70 disabled:cursor-not-allowed transition-all hover:-translate-y-0.5 cursor-pointer"
      >
        <span v-if="verifying" class="flex items-center">
          <Loader2 class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" />
          Verifying...
        </span>
        <span v-else>Verify Email</span>
      </button>

      <div class="text-center">
        <p class="text-sm text-zinc-500">
          Didn't receive the code?
          <button
            @click="resendOtp"
            :disabled="resendCooldown > 0"
            class="font-semibold text-violet-600 hover:text-violet-500 disabled:text-zinc-400 disabled:cursor-not-allowed cursor-pointer transition-colors ml-1"
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
import { Mail, Loader2 } from 'lucide-vue-next';

const props = defineProps({
  email: {
    type: String,
    default: ''
  }
});

const router = useRouter();
const userStore = useUserStore();
const email = ref('');

onMounted(() => {
  // Try to get email from localStorage if not provided via props
  if (!props.email) {
    email.value = localStorage.getItem('pendingVerificationEmail') || '';
    if (!email.value) {
      // If no email is found, redirect to signup
      router.push('/signup');
    }
  } else {
    email.value = props.email;
  }
});

const emit = defineEmits(['verified']);

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
    const { success, error } = await userStore.verifyEmail(email.value, otp.value);
    
    if (success) {
      // Clear the pending verification email from localStorage
      localStorage.removeItem('pendingVerificationEmail');
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
    const { success, error } = await userStore.resendOtp(email.value);
    
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