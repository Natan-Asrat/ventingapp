<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Desktop Navigation -->
    <desktop-top-nav 
      :user-initials="userInitials"
      @logout="logout"
    />
    
    <!-- Mobile Top Navigation -->
    <mobile-top-nav 
      :user-initials="userInitials"
      :user-name="user?.name || ''"
      @logout="logout"
    />

    <FeedList />

    <!-- Mobile Bottom Navigation -->
    <MobileBottomNav :user-initials="userInitials" />
  </div>
</template>

<script setup>
import { computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { useUserStore } from '@/stores/user';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import { useConnectsStore } from '@/stores/connect';
import { usePostStore } from '@/stores/post';
import FeedList from '@/components/feed/FeedList.vue';
const connectsStore = useConnectsStore();
const userStore = useUserStore();
const postStore = usePostStore();
const router = useRouter();

// Computed
const user = computed(() => userStore.user);

const userInitials = computed(() => {
  if (!user.value?.name) return 'U';
  return user.value.name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .substring(0, 2);
});

const handleFollowClick = async (post, showDonate = false) => {
    if (post.removed_connection && !post.pending_connection && !post.rejected_connection) {
        // Show modal for reconnection request
        postStore.setSelectedUserForConnection(post);
        postStore.setShowConnectionModal(true);
    } else {
        await postStore.handleFollow(post, showDonate);
        await userStore.checkAuth();
    }
};

const currentConnects = computed(() => userStore.user?.connects || 0);

watch(() => postStore.isConnectsModalOpen, async () => {
    if (postStore.isConnectsModalOpen) {
        await connectsStore.fetchConnectsData();
    }
})

const logout = async () => {
  try {
    await userStore.logout();
    message.success('Successfully logged out');
    router.push('/login');
  } catch (error) {
    console.error('Logout error:', error);
    message.error('Failed to logout. Please try again.');
  }
};

</script>

<style scoped>
/* Add any custom styles here */
.rotate-180 {
  transform: rotate(180deg);
}
</style>
