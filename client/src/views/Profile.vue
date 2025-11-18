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
              <!-- Profile Picture -->
              <div class="flex items-center space-x-4">
                <div class="flex-shrink-0">
                  <div v-if="user?.profile_picture" class="h-20 w-20 rounded-full overflow-hidden bg-gray-200">
                    <img :src="user.profile_picture" :alt="user.name" class="h-full w-full object-cover">
                  </div>
                  <div v-else class="h-20 w-20 rounded-full bg-indigo-100 flex items-center justify-center">
                    <span class="text-2xl font-medium text-indigo-600">{{ userInitials }}</span>
                  </div>
                </div>
                <div>
                  <h2 class="text-xl font-semibold text-gray-900">{{ user?.name || 'User' }}</h2>
                  <p class="text-sm text-gray-500">Member since {{ formattedJoinDate }}</p>
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
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';

const router = useRouter();
const userStore = useUserStore();

// Get user data from the store
const user = computed(() => userStore.user);

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
