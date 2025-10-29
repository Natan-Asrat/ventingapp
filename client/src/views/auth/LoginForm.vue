<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <div>
      <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
      <div class="mt-1">
        <input
          id="email"
          v-model="email"
          name="email"
          type="email"
          autocomplete="email"
          required
          :class="[
            'appearance-none block w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none sm:text-sm',
            errors.email && errors.email.length > 0 ? 'border-red-300 text-red-900 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500'
          ]"
          @input="clearError('email')"
        />
        <div v-if="errors.email" class="mt-2 space-y-1">
          <p v-for="(error, index) in errors.email" :key="`email-error-${index}`" class="text-sm text-red-600">
            {{ error }}
          </p>
        </div>
      </div>
    </div>

    <div>
      <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
      <div class="mt-1">
        <input
          id="password"
          v-model="password"
          name="password"
          type="password"
          autocomplete="current-password"
          required
          :class="[
            'appearance-none block w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none sm:text-sm',
            errors.password && errors.password.length > 0 ? 'border-red-300 text-red-900 focus:ring-red-500 focus:border-red-500' : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500'
          ]"
          @input="clearError('password')"
        />
        <div v-if="errors.password" class="mt-2 space-y-1">
          <p v-for="(error, index) in errors.password" :key="`password-error-${index}`" class="text-sm text-red-600">
            {{ error }}
          </p>
        </div>
      </div>
    </div>

    <div class="flex items-center justify-end">

      <div class="text-sm">
        <router-link to="/forgot-password" class="font-medium text-indigo-600 hover:text-indigo-500">
          Forgot your password?
        </router-link>
      </div>
    </div>

    <div>
      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
      >
        <span v-if="loading">
          <Loader2 class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" />
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
        router.push({name: 'Feed'});
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
