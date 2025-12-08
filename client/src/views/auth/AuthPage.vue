<template>
  <div class="min-h-screen bg-zinc-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden">
    <!-- Decorative background elements -->
    <div class="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-violet-200/20 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute bottom-0 right-0 w-[600px] h-[600px] bg-indigo-200/10 rounded-full blur-3xl pointer-events-none"></div>

    <div class="sm:mx-auto sm:w-full sm:max-w-md relative z-10">
      <!-- Logo -->
      <div class="flex justify-center items-center gap-2 mb-8" @click="router.push('/')">
         <div class="w-10 h-10 bg-violet-100 rounded-xl flex items-center justify-center text-violet-600 shadow-sm cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
         </div>
         <h1 class="text-2xl font-bold text-zinc-900 tracking-tight cursor-pointer">Venting<span class="text-violet-600">App</span></h1>
      </div>

      <h2 class="text-center text-3xl font-extrabold text-zinc-900 tracking-tight">
        {{ showVerification ? 'Verify Your Email' : showSignup ? 'Create account' : 'Welcome back' }}
      </h2>
      <p v-if="!showVerification" class="mt-2 text-center text-sm text-zinc-500">
        {{ showSignup ? 'Already have an account?' : 'New to VentingApp?' }}
        <button
          @click="showSignup = !showSignup"
          class="font-semibold text-violet-600 hover:text-violet-500 focus:outline-none transition-colors cursor-pointer ml-1"
        >
          {{ showSignup ? 'Sign in' : 'Create an account' }}
        </button>
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md relative z-10">
      <div class="bg-white py-8 px-4 shadow-xl shadow-zinc-200/50 sm:rounded-2xl sm:px-10 border border-zinc-100">
        <transition
          enter-active-class="transition ease-out duration-200"
          enter-from-class="transform opacity-0 scale-95"
          enter-to-class="transform opacity-100 scale-100"
          leave-active-class="transition ease-in duration-150"
          leave-from-class="transform opacity-100 scale-100"
          leave-to-class="transform opacity-0 scale-95"
          mode="out-in"
        >
          <!-- Show verification component if verifying -->
          <div v-if="showVerification" key="verification">
            <EmailVerification
              :email="verificationEmail"
              @verified="handleVerificationComplete"
            />
          </div>
          
          <!-- Show signup form -->
          <div v-else-if="showSignup" key="signup">
            <SignupForm
              @switchToLogin="showSignup = false"
              @signupSuccess="handleSignupSuccess"
            />
          </div>
          
          <!-- Show login form -->
          <div v-else key="login">
            <LoginForm
              @switchToSignup="showSignup = true"
            />
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import LoginForm from './LoginForm.vue';
import SignupForm from './SignupForm.vue';
import EmailVerification from './EmailVerification.vue';

const router = useRouter();
const showSignup = ref(false);
const showVerification = ref(false);
const verificationEmail = ref('');

const handleSignupSuccess = (email) => {
  verificationEmail.value = email;
  showVerification.value = true;
  showSignup.value = false;
  message.success('Verification code sent to your email!');
};

const handleVerificationComplete = () => {
  showVerification.value = false;
  showSignup.value = false;
  message.success('Email verified successfully! You can now sign in.');
};
</script>