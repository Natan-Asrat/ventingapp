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
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex flex-col md:flex-row gap-6">
          <ProfileDetail />
          
          <ProfilePosts />
        </div>
      </div>
    </div>
    
    <!-- Mobile Bottom Navigation -->
    <mobile-bottom-nav :user-initials="userInitials" />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import ProfileDetail from '@/components/my_profile/MyProfileDetail.vue';
import ProfilePosts from '@/components/my_profile/MyProfilePosts.vue';
import { useMyProfileStore } from '@/stores/my_profile';
const router = useRouter();
const userStore = useUserStore();
const myProfileStore = useMyProfileStore();

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

// Handle logout
const handleLogout = () => {
  userStore.logout();
  router.push('/login');
};

// Fetch user data and posts when component mounts
onMounted(async () => {
  if (!user.value) {
    await userStore.checkAuth();
  }
  myProfileStore.setLoading(true);
  await myProfileStore.fetchUserPosts();
  await myProfileStore.fetchArchivedUserPosts();
  myProfileStore.setLoading(false);
});
</script>
