<template>
  <div class="min-h-screen bg-zinc-50/50 font-sans">
    <DesktopTopNav />    
    <MobileTopNav />
    
    <!-- Main Content -->
    <div class="pt-20 pb-20 md:pt-6 md:pb-0 relative z-0">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex flex-col md:flex-row gap-8">
          <MyProfileDetail />
          <MyProfilePosts />
        </div>
      </div>
    </div>
    <MobileBottomNav />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import MyProfileDetail from '@/components/my_profile/MyProfileDetail.vue';
import MyProfilePosts from '@/components/my_profile/MyProfilePosts.vue';
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
