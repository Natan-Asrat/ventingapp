<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <div>
      <label for="email" class="block text-sm font-bold text-zinc-700 mb-1">Email address</label>
      <div class="mt-1">
        <input
          id="email"
          v-model="email"
          name="email"
          type="email"
          autocomplete="email"
          required
          :class="[
            'block w-full rounded-xl px-4 py-3 text-zinc-900 placeholder-zinc-400 shadow-sm focus:outline-none focus:ring-4 transition-all sm:text-sm',
            errors.email && errors.email.length > 0 
                ? 'border-rose-300 bg-rose-50 text-rose-900 focus:border-rose-500 focus:ring-rose-500/20' 
                : 'border border-zinc-200 bg-zinc-50 focus:border-violet-500 focus:bg-white focus:ring-violet-500/20'
          ]"
          placeholder="you@example.com"
          @input="clearError('email')"
        />
        <div v-if="errors.email" class="mt-1.5 space-y-1">
          <p v-for="(error, index) in errors.email" :key="`email-error-${index}`" class="text-xs text-rose-600 font-medium">
            {{ error }}
          </p>
        </div>
      </div>
    </div>

    <div>
      <div class="flex items-center justify-between mb-1">
        <label for="password" class="block text-sm font-bold text-zinc-700">Password</label>
        <router-link to="/forgot-password" class="text-xs font-semibold text-violet-600 hover:text-violet-500 transition-colors">
          Forgot password?
        </router-link>
      </div>
      <div class="mt-1">
        <input
          id="password"
          v-model="password"
          name="password"
          type="password"
          autocomplete="current-password"
          required
          :class="[
            'block w-full rounded-xl px-4 py-3 text-zinc-900 placeholder-zinc-400 shadow-sm focus:outline-none focus:ring-4 transition-all sm:text-sm',
            errors.password && errors.password.length > 0 
                ? 'border-rose-300 bg-rose-50 text-rose-900 focus:border-rose-500 focus:ring-rose-500/20' 
                : 'border border-zinc-200 bg-zinc-50 focus:border-violet-500 focus:bg-white focus:ring-violet-500/20'
          ]"
          placeholder="Enter your password"
          @input="clearError('password')"
        />
        <div v-if="errors.password" class="mt-1.5 space-y-1">
          <p v-for="(error, index) in errors.password" :key="`password-error-${index}`" class="text-xs text-rose-600 font-medium">
            {{ error }}
          </p>
        </div>
      </div>
    </div>

    <div class="pt-2">
      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center py-3 px-4 border border-transparent rounded-full shadow-lg shadow-zinc-900/10 text-sm font-bold text-white bg-zinc-900 hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-70 disabled:cursor-not-allowed transition-all hover:-translate-y-0.5 cursor-pointer"
      >
        <span v-if="loading" class="flex items-center">
          <Loader2 class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" />
          Signing in...
        </span>
        <span v-else>Sign in</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { Loader2 } from 'lucide-vue-next';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';

const userStore = useUserStore();
const router = useRouter();

const email = ref('');
const password = ref('');
const loading = ref(false);
const errors = ref({
  email: [],
  password: []
});

const clearError = (field) => {
  if (errors.value[field] && errors.value[field].length > 0) {
    errors.value[field] = [];
  }
};

const emit = defineEmits(['switchToSignup']);

const handleSubmit = async () => {
  if (!email.value || !password.value) {
    message.error('Please fill in all fields');
    return;
  }

  loading.value = true;
  
  try {
      const { success, error } = await userStore.login(email.value, password.value);
      
      if (success) {
        message.success('Login successful!');
        const redirectTo = userStore.user?.is_staff 
          ? '/admin' 
          : router.currentRoute.value.query.redirect || '/';
        await router.push(redirectTo);
      } else if (error) {
        // Handle field-specific errors
        if (typeof error === 'object') {
          // Reset all errors
          errors.value.email = [];
          errors.value.password = [];
          
          // Set new errors
          if (Array.isArray(error.email)) {
            errors.value.email = [...error.email];
          } else if (error.email) {
            errors.value.email = [error.email];
          }
          
          if (Array.isArray(error.password)) {
            errors.value.password = [...error.password];
          } else if (error.password) {
            errors.value.password = [error.password];
          }
          
          // Show general errors if no field-specific errors
          if (error.general) {
            const generalErrors = Array.isArray(error.general) ? error.general : [error.general];
            generalErrors.forEach(msg => message.error(msg));
          } else if (errors.value.email.length === 0 && errors.value.password.length === 0) {
            message.error('Login failed. Please check your credentials.');
          }
        } else {
          message.error('Login failed. Please check your credentials.');
        }
      }
  } catch (error) {
    message.error('An error occurred during login. Please try again.');
  } finally {
    loading.value = false;
  }
};
</script>