<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Desktop Navigation -->
    <desktop-top-nav 
      :user-initials="userInitials"
      @logout="handleLogout"
    />
    
    <!-- Mobile Top Navigation -->
    <mobile-top-nav 
      :user-initials="userInitials"
      :user-name="user?.name || 'User'"
      @logout="handleLogout"
    />
    
    <!-- Main Content -->
    <div class="pt-16 pb-16 md:pt-0 md:pb-0">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="bg-white shadow sm:rounded-lg overflow-hidden">
          <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h3 class="text-lg leading-6 font-medium text-gray-900">Profile Information</h3>
            <p class="mt-1 max-w-2xl text-sm text-gray-500">Your personal details and account information.</p>
          </div>
          
          <div class="px-4 py-5 sm:p-6">
            <div class="space-y-6">
              <!-- Profile Picture and Name -->
              <div class="flex items-start space-x-4">
                <div class="flex-shrink-0 relative group">
                  <div v-if="user?.profile_picture" class="h-24 w-24 rounded-full overflow-hidden bg-gray-200">
                    <img :src="user.profile_picture" :alt="user.name" class="h-full w-full object-cover">
                  </div>
                  <div v-else class="h-24 w-24 rounded-full bg-indigo-100 flex items-center justify-center">
                    <span class="text-3xl font-medium text-indigo-600">{{ userInitials }}</span>
                  </div>
                  <button
                    @click="triggerFileInput"
                    class="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-white px-3 py-1 rounded-full text-xs font-medium text-indigo-600 shadow-sm border border-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Change
                  </button>
                  <input
                    ref="fileInput"
                    type="file"
                    accept="image/*"
                    class="hidden"
                    @change="handleProfilePictureChange"
                  />
                </div>
                <div class="flex-1">
                  <div v-if="!isEditingName" class="flex items-center">
                    <h2 class="text-2xl font-semibold text-gray-900">{{ user?.name || 'User' }}</h2>
                    <button
                      @click="startEditingName"
                      class="ml-2 p-1 rounded-full text-gray-400 hover:text-indigo-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      <PencilIcon class="h-4 w-4" />
                    </button>
                  </div>
                  <div v-else class="flex items-center space-x-2">
                    <input
                      v-model="editingName"
                      type="text"
                      class="py-2 px-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      @keyup.enter="saveName"
                    >
                    <button
                      @click="saveName"
                      :disabled="isSaving"
                      class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                    >
                      <span v-if="isSaving" class="flex items-center">
                        <svg class="animate-spin -ml-1 mr-2 h-3 w-3 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Saving...
                      </span>
                      <span v-else>Save</span>
                    </button>
                    <button
                      @click="cancelEditingName"
                      class="p-1 text-gray-400 hover:text-gray-500 focus:outline-none"
                      :disabled="isSaving"
                    >
                      <X class="h-4 w-4" />
                    </button>
                  </div>
                  <p class="mt-1 text-sm text-gray-500">Member since {{ formattedJoinDate }}</p>
                </div>
              </div>
              
              <!-- User Details -->
              <div class="border-t border-gray-200 pt-4">
                <dl class="divide-y divide-gray-200">
                  <div class="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
                    <dt class="text-sm font-medium text-gray-500">Email address</dt>
                    <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ user?.email || 'Not provided' }}</dd>
                  </div>
                  <div v-if="user?.username" class="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
                    <dt class="text-sm font-medium text-gray-500">Username</dt>
                    <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ user.username }}</dd>
                  </div>
                  <div class="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
                    <dt class="text-sm font-medium text-gray-500">Account created</dt>
                    <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ formattedJoinDate }}</dd>
                  </div>
                </dl>
              </div>
              
              <!-- Actions -->
              <div class="pt-4 border-t border-gray-200">
                <router-link 
                  to="/home"
                  class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Back to Feed
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Mobile Bottom Navigation -->
    <mobile-bottom-nav :user-initials="userInitials" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { PencilIcon, X } from 'lucide-vue-next';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import api from '@/api/axios';
import { message } from 'ant-design-vue';

const router = useRouter();
const userStore = useUserStore();
const fileInput = ref(null);

// State
const isEditingName = ref(false);
const editingName = ref('');
const isSaving = ref(false);

// Get user data from the store
const user = computed(() => userStore.user);

// Initialize editing name when user data is available
watch(() => user.value?.name, (newName) => {
  if (newName) {
    editingName.value = newName;
  }
}, { immediate: true });

// Methods
const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleProfilePictureChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // Store the current profile picture URL to revert if the update fails
  const previousProfilePicture = user.value?.profile_picture;
  
  // Optimistically update the UI
  const tempProfilePicture = URL.createObjectURL(file);
  userStore.user = { ...user.value, profile_picture: tempProfilePicture };

  const formData = new FormData();
  formData.append('profile_picture', file);

  try {
    isSaving.value = true;
    const response = await api.patch('/account/users/edit_profile/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    // Update with server response data
    userStore.user = { ...user.value, ...response.data };
    message.success('Profile picture updated successfully!');
  } catch (error) {
    console.error('Error updating profile picture:', error);
    // Revert to previous profile picture on error
    userStore.user = { ...user.value, profile_picture: previousProfilePicture };
    message.error('Failed to update profile picture. Please try again.');
  } finally {
    isSaving.value = false;
    // Clean up the object URL to prevent memory leaks
    if (tempProfilePicture) {
      URL.revokeObjectURL(tempProfilePicture);
    }
    // Reset file input
    if (fileInput.value) {
      fileInput.value.value = '';
    }
  }
};
const startEditingName = () => {
  editingName.value = user.value?.name || '';
  isEditingName.value = true;
};

const cancelEditingName = () => {
  isEditingName.value = false;
  editingName.value = user.value?.name || '';
};

const saveName = async () => {
  if (!editingName.value.trim() || editingName.value === user.value?.name) {
    isEditingName.value = false;
    return;
  }

  try {
    isSaving.value = true;
    const response = await api.patch('/account/users/edit_profile/', {
      name: editingName.value.trim(),
    });
    
    // Update user data in the store
    userStore.user = { ...user.value, ...response.data };
    isEditingName.value = false;
    
    // Show success message
    message.success('Name updated successfully!');

  } catch (error) {
    console.error('Error updating name:', error);
    message.error('Failed to update name. Please try again.');
  } finally {
    isSaving.value = false;
  }
};

// Format user initials for avatar
const userInitials = computed(() => {
  if (!user.value?.name) return 'U';
  return user.value.name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .substring(0, 2);
});

// Format join date
const formattedJoinDate = computed(() => {
  if (!user.value?.date_joined) return 'N/A';
  return new Date(user.value.date_joined).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
});

// Handle logout
const handleLogout = () => {
  userStore.logout();
  router.push('/login');
};

// Fetch user data when component mounts
onMounted(async () => {
  if (!user.value) {
    await userStore.checkAuth();
  }
});
</script>
