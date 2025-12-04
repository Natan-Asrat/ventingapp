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

    <!-- Main content with padding to account for fixed nav bars -->
    <main class="pt-16 pb-16 md:pt-0 md:pb-0">
      <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:max-w-4xl lg:px-8 py-6">
        <!-- Posts Feed -->
        <div v-if="postStore.loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
        
        <div v-else-if="postStore.posts.length === 0" class="text-center py-12">
          <p class="text-gray-500">No posts to show. Be the first to post something!</p>
        </div>
        
        <div v-else class="space-y-6" id="post-list">
          <FeedItem
            v-for="post in postStore.posts"
            :key="post.id"
            :post="post"
            :data-id="`post-${post.id}`"
            :liking="postStore.likingPostId === post.id"
            :saving="postStore.savingPostId === post.id"
            @donate="postStore.openDonationModal"
            @chat="postStore.handleChat"
            @save="postStore.handleSave"
            @like="postStore.handleLike"
            @follow="handleFollowClick"
            @update:post="postStore.handleUpdatePostObj"
            @connection-updated="postStore.handleConnectionsUpdated(post.id)"
          />
          
          <!-- Load More Button -->
          <div v-if="postStore.hasNextPage" class="flex justify-center py-4">
            <button 
              @click="postStore.loadMore" 
              :disabled="postStore.loadingMore"
              class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              {{ postStore.loadingMore ? 'Loading...' : 'Load More' }}
            </button>
          </div>
        </div>
      </div>
    </main>
    
    <!-- Donation Modal -->
    <donate-modal
      :model-value="postStore.showDonationModal"
      @update:model-value="postStore.setShowDonationModal"
      :payment-methods="postStore.selectedPost?.payment_info_list || []"
    />
    
    <!-- Connection Request Modal -->
    <ConnectionRequestModal
      v-if="postStore.showConnectionModal"
      :is-open="postStore.showConnectionModal"
      :user-name="postStore.selectedUserForConnection?.posted_by?.name || 'this user'"
      @close="postStore.closeConnectionModal"
      @confirm="postStore.confirmConnectionRequest"
    />
    
    <!-- Mobile Bottom Navigation -->
    <MobileBottomNav :user-initials="userInitials" />

    <!-- Connects Modal -->
    <ConnectsModal
      :is-open="postStore.isConnectsModalOpen"
      :current-connects="currentConnects"
      :connects-data="connectsStore.connectsData"
      :loading="connectsStore.isLoading"
      @close="postStore.setIsConnectsModalOpen(false)"
      @purchase="connectsStore.handlePurchaseConnects"
    />
  </div>
</template>

<script setup>
import { onMounted, computed, watch, onUnmounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { useUserStore } from '@/stores/user';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import FeedItem from '@/components/feed/FeedItem.vue';
import DonateModal from '@/components/feed/DonateModal.vue';
import ConnectionRequestModal from '@/components/feed/ConnectionRequestModal.vue';
import ConnectsModal from '@/components/connects/ConnectsModal.vue';
import { useConnectsStore } from '@/stores/connect';
import { usePostStore } from '@/stores/post';
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

// Lifecycle
onMounted(async () => {
  await postStore.fetchPosts();
  // After loading posts, check if we need to load a specific post from URL
  await postStore.checkUrlForPost();
  postStore.observePostVisibility();
    
  // Start polling after initial load
  nextTick(() => {
    postStore.startVisiblePostsPolling();
  });
});


onUnmounted(() => {
  postStore.stopVisiblePostsPolling();
  if (postStore.visibilityObserver) postStore.visibilityObserver.disconnect();
  if (postStore.mutationObserver) postStore.mutationObserver.disconnect();
});
</script>

<style scoped>
/* Add any custom styles here */
.rotate-180 {
  transform: rotate(180deg);
}
</style>
