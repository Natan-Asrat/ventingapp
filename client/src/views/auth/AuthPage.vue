<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        {{ showVerification ? 'Verify Your Email' : showSignup ? 'Create your account' : 'Sign in to your account' }}
      </h2>
      <p v-if="!showVerification" class="mt-2 text-center text-sm text-gray-600">
        Or
        <button
          @click="showSignup = !showSignup"
          class="font-medium cursor-pointer text-indigo-600 hover:text-indigo-500 focus:outline-none"
        >
          {{ showSignup ? 'sign in to your account' : 'create a new account' }}
        </button>
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <!-- Show verification component if verifying -->
        <EmailVerification
          v-if="showVerification"
          :email="verificationEmail"
          @verified="handleVerificationComplete"
        />
        
        <!-- Show signup form or login form based on state -->
        <LoginForm
          v-else-if="!showSignup"
          @switchToSignup="showSignup = true"
        />
        
        <SignupForm
          v-else
          @switchToLogin="showSignup = false"
          @signupSuccess="handleSignupSuccess"
        />
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
