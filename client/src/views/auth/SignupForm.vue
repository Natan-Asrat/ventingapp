<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    
    <!-- Profile Picture Upload -->
    <div class="flex justify-center mb-6">
        <div class="relative group cursor-pointer" @click="$refs.fileInput.click()">
            <div class="h-24 w-24 rounded-full overflow-hidden border-4 border-zinc-50 shadow-md transition-all group-hover:shadow-lg bg-zinc-100">
                <img v-if="previewUrl" :src="previewUrl" alt="Profile preview" class="h-full w-full object-cover" />
                <div v-else class="h-full w-full flex items-center justify-center text-zinc-300">
                    <User class="h-10 w-10" />
                </div>
            </div>
            <div class="absolute bottom-0 right-0 bg-zinc-900 rounded-full p-2 text-white border-2 border-white shadow-sm transition-transform group-hover:scale-110">
                <Camera class="h-4 w-4" />
            </div>
            <input
                type="file"
                id="profile_picture"
                ref="fileInput"
                @change="handleFileChange"
                class="hidden"
                accept="image/png, image/jpeg"
            />
        </div>
    </div>

    <div class="grid grid-cols-1 gap-y-5 gap-x-4 sm:grid-cols-6">
      <div class="sm:col-span-3">
        <label for="name" class="block text-sm font-bold text-zinc-700 mb-1">Full Name</label>
        <div class="mt-1">
          <input
            type="text"
            v-model="formData.name"
            id="name"
            autocomplete="name"
            required
            class="block w-full rounded-xl border-zinc-200 bg-zinc-50 px-4 py-2.5 text-zinc-900 placeholder-zinc-400 focus:border-violet-500 focus:bg-white focus:ring-violet-500/20 focus:outline-none focus:ring-4 transition-all sm:text-sm"
            placeholder="John Doe"
          />
        </div>
      </div>

      <div class="sm:col-span-3">
        <label for="username" class="block text-sm font-bold text-zinc-700 mb-1">Username</label>
        <div class="mt-1 relative">
            <span class="absolute inset-y-0 left-0 flex items-center pl-4 text-zinc-400 text-sm font-bold">@</span>
            <input
              type="text"
              v-model="formData.username"
              id="username"
              autocomplete="username"
              required
              class="block w-full rounded-xl border-zinc-200 bg-zinc-50 pl-9 pr-4 py-2.5 text-zinc-900 placeholder-zinc-400 focus:border-violet-500 focus:bg-white focus:ring-violet-500/20 focus:outline-none focus:ring-4 transition-all sm:text-sm"
              placeholder="username"
            />
        </div>
      </div>

      <div class="sm:col-span-6">
        <label for="email" class="block text-sm font-bold text-zinc-700 mb-1">Email address</label>
        <div class="mt-1">
          <input
            id="email"
            v-model="formData.email"
            name="email"
            type="email"
            autocomplete="email"
            required
            class="block w-full rounded-xl border-zinc-200 bg-zinc-50 px-4 py-2.5 text-zinc-900 placeholder-zinc-400 focus:border-violet-500 focus:bg-white focus:ring-violet-500/20 focus:outline-none focus:ring-4 transition-all sm:text-sm"
            placeholder="you@example.com"
          />
        </div>
      </div>

      <div class="sm:col-span-3">
        <label for="password1" class="block text-sm font-bold text-zinc-700 mb-1">Password</label>
        <div class="mt-1">
          <input
            id="password1"
            v-model="formData.password1"
            name="password1"
            type="password"
            autocomplete="new-password"
            required
            class="block w-full rounded-xl border-zinc-200 bg-zinc-50 px-4 py-2.5 text-zinc-900 placeholder-zinc-400 focus:border-violet-500 focus:bg-white focus:ring-violet-500/20 focus:outline-none focus:ring-4 transition-all sm:text-sm"
            placeholder="••••••••"
          />
        </div>
      </div>

      <div class="sm:col-span-3">
        <label for="password2" class="block text-sm font-bold text-zinc-700 mb-1">Confirm</label>
        <div class="mt-1">
          <input
            id="password2"
            v-model="formData.password2"
            name="password2"
            type="password"
            autocomplete="new-password"
            required
            class="block w-full rounded-xl border-zinc-200 bg-zinc-50 px-4 py-2.5 text-zinc-900 placeholder-zinc-400 focus:border-violet-500 focus:bg-white focus:ring-violet-500/20 focus:outline-none focus:ring-4 transition-all sm:text-sm"
            placeholder="••••••••"
          />
        </div>
      </div>
    </div>

    <div class="pt-4">
      <button
        type="submit"
        :disabled="loading"
        class="w-full flex justify-center py-3 px-4 border border-transparent rounded-full shadow-lg shadow-zinc-900/10 text-sm font-bold text-white bg-zinc-900 hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-70 disabled:cursor-not-allowed transition-all hover:-translate-y-0.5 cursor-pointer"
      >
        <span v-if="loading" class="flex items-center">
          <Loader2 class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" />
          Creating Account...
        </span>
        <span v-else>Create Account</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, onUnmounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { message } from 'ant-design-vue';
import { User, Loader2, Camera } from 'lucide-vue-next';

const userStore = useUserStore();
const loading = ref(false);
const fileInput = ref(null);
const previewUrl = ref(null);

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
    // Revoke the previous object URL to avoid memory leaks
    if (previewUrl.value) {
      URL.revokeObjectURL(previewUrl.value);
    }
    
    formData.value.profile_picture = file;
    previewUrl.value = URL.createObjectURL(file);
  }
};

// Clean up object URLs when component is unmounted
onUnmounted(() => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value);
  }
});

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
    const formDataObj = new FormData();
    
    // Append all form data
    Object.entries(formData.value).forEach(([key, value]) => {
      if (key === 'profile_picture' && value) {
        // For the file, we need to append it directly
        formDataObj.append(key, value, value.name);
      } else if (value !== null && value !== undefined) {
        // For all other fields, convert to string if not null/undefined
        formDataObj.append(key, String(value));
      }
    });

    const response = await userStore.register(formDataObj);

    if (response.success) {
      // Save email to localStorage for email verification
      localStorage.setItem('pendingVerificationEmail', formData.value.email);
      emit('signupSuccess', formData.value.email);
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