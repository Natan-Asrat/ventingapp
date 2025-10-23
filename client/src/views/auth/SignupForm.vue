<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
      <div class="sm:col-span-3">
        <label for="name" class="block text-sm font-medium text-gray-700">Full Name</label>
        <div class="mt-1">
          <input
            type="text"
            v-model="formData.name"
            id="name"
            autocomplete="name"
            required
            class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
      </div>

      <div class="sm:col-span-3">
        <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
        <div class="mt-1">
          <div class="flex rounded-md shadow-sm">
            <span class="inline-flex items-center rounded-l-md border border-r-0 border-gray-300 bg-gray-50 px-3 text-gray-500 sm:text-sm">
              @
            </span>
            <input
              type="text"
              v-model="formData.username"
              id="username"
              autocomplete="username"
              required
              class="block w-full min-w-0 flex-1 rounded-none rounded-r-md border border-gray-300 px-3 py-2 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
          </div>
        </div>
      </div>

      <div class="sm:col-span-6">
        <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
        <div class="mt-1">
          <input
            id="email"
            v-model="formData.email"
            name="email"
            type="email"
            autocomplete="email"
            required
            class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
      </div>

      <div class="sm:col-span-3">
        <label for="password1" class="block text-sm font-medium text-gray-700">Password</label>
        <div class="mt-1">
          <input
            id="password1"
            v-model="formData.password1"
            name="password1"
            type="password"
            autocomplete="new-password"
            required
            class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
      </div>

      <div class="sm:col-span-3">
        <label for="password2" class="block text-sm font-medium text-gray-700">Confirm Password</label>
        <div class="mt-1">
          <input
            id="password2"
            v-model="formData.password2"
            name="password2"
            type="password"
            autocomplete="new-password"
            required
            class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
      </div>

      <div class="sm:col-span-6">
        <label for="profile_picture" class="block text-sm font-medium text-gray-700">
          Profile Picture (Optional)
        </label>
        <div class="mt-1 flex items-center">
          <span class="h-12 w-12 overflow-hidden rounded-full bg-gray-100">
            <svg class="h-full w-full text-gray-300" fill="currentColor" viewBox="0 0 24 24">
              <path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </span>
          <input
            type="file"
            id="profile_picture"
            ref="fileInput"
            @change="handleFileChange"
            class="ml-5 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
          />
        </div>
      </div>
    </div>

    <div class="flex items-center justify-between">


      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="loading">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </span>
        <span v-else>Create Account</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { message } from 'ant-design-vue';

const userStore = useUserStore();
const loading = ref(false);
const fileInput = ref(null);

const formData = ref({
  name: '',
  username: '',
  email: '',
  password1: '',
  password2: '',
  profile_picture: null
});

const emit = defineEmits(['signupSuccess', 'switchToLogin']);

const handleFileChange = (e) => {
  const file = e.target.files[0];
  if (file) {
    formData.value.profile_picture = file;
  }
};

const handleSubmit = async () => {
  // Basic validation
  if (formData.value.password1 !== formData.value.password2) {
    message.error('Passwords do not match');
    return;
  }

  if (formData.value.password1.length < 8) {
    message.error('Password must be at least 8 characters long');
    return;
  }

  loading.value = true;
  
  try {
    const response = await userStore.register({
      name: formData.value.name,
      username: formData.value.username,
      email: formData.value.email,
      password1: formData.value.password1,
      password2: formData.value.password2,
      profile_picture: formData.value.profile_picture
    });

    if (response.success) {
      emit('signupSuccess', response.email);
    } else {
      // Handle specific errors from the API
      if (response.error) {
        if (typeof response.error === 'object') {
          // Handle field-specific errors
          const errorMessages = Object.values(response.error).flat();
          message.error(errorMessages.join(' '));
        } else {
          message.error(response.error);
        }
      } else {
        message.error('Registration failed. Please try again.');
      }
    }
  } catch (error) {
    console.error('Registration error:', error);
    message.error('An error occurred during registration. Please try again.');
  } finally {
    loading.value = false;
  }
};
</script>
