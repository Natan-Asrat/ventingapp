<template>
  <div>
    <main :class="[ user_id == null && 'pb-16 md:pt-0 md:pb-0', user_id == null && postStore.searchProfileResults.length == 0 && 'pt-16']">
      <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:max-w-4xl lg:px-8 py-6">
        <!-- Posts Feed -->
        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
        
        <div v-else-if="posts.length === 0" class="text-center py-12">
          <p class="text-gray-500">{{ noPostPlaceholder }}</p>
        </div>
        
        <div v-else class="space-y-6" id="post-list">
            <h2 v-if="postStore.isInSearch" class="text-lg font-medium text-gray-900">
                Search Results
                <span v-if="postStore.searchQuery" class="text-indigo-600">"{{ postStore.searchQuery }}"</span>
            </h2>          
            <FeedItem
                v-for="post in posts"
                :key="post.id"
                :post="post"
                :data-id="`post-${post.id}`"
                :liking="likingPostId === post.id"
                :saving="savingPostId === post.id"
                @donate="openDonationModal"
                @chat="handleChat"
                @save="handleSave"
                @like="handleLike"
                @follow="handleFollowClick"
                @update:post="handleUpdatePostObj"
                @connection-updated="handleConnectionsUpdated(post.id)"
            />
          
            <!-- Load More Button -->
            <div v-if="hasNextPage || postStore.showRecommended" class="flex justify-center py-4">
                <button 
                    @click="loadMore" 
                    :disabled="loadingMore"
                    class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                >
                    {{ loadingMore ? 'Loading...' : 'Load More' }}
                </button>
          </div>
        </div>
      </div>
    </main>
    
    <!-- Donation Modal -->
    <DonateModal
      :model-value="showDonationModal"
      @update:model-value="setShowDonationModal"
      :payment-methods="selectedPost?.payment_info_list || []"
    />
    
    <!-- Connection Request Modal -->
    <ConnectionRequestModal
      v-if="showConnectionModal"
      :is-open="showConnectionModal"
      :user-name="selectedUserForConnection?.posted_by?.name || 'this user'"
      @close="closeConnectionModal"
      @confirm="confirmConnectionRequest"
    />
    

    <!-- Connects Modal -->
    <ConnectsModal
      :is-open="isConnectsModalOpen"
      :current-connects="currentConnects"
      :connects-data="connectsStore.connectsData"
      :loading="connectsStore.isLoading"
      @close="setIsConnectsModalOpen(false)"
      @purchase="connectsStore.handlePurchaseConnects"
    />
  </div>
</template>

<script setup>
import { onMounted, computed, watch, onUnmounted, nextTick } from 'vue';
import { useUserStore } from '@/stores/user';
import FeedItem from '@/components/feed/FeedItem.vue';
import DonateModal from '@/components/feed/DonateModal.vue';
import ConnectionRequestModal from '@/components/feed/ConnectionRequestModal.vue';
import ConnectsModal from '@/components/connects/ConnectsModal.vue';
import { useConnectsStore } from '@/stores/connect';
import { usePostStore } from '@/stores/post';
import { useOtherProfilePostStore } from '@/stores/profile';
const connectsStore = useConnectsStore();
const userStore = useUserStore();
const postStore = usePostStore();
const profileStore = useOtherProfilePostStore();

const props = defineProps({
    user_id: {
        type: String,
        required: false
    }
})

const loading = computed(() => props.user_id == null ? postStore.loading : profileStore.loading)
const posts = computed(() => {
    if (props.user_id == null) {
        if (postStore.isInSearch) {
            return postStore.searchPostResults
        }
        return postStore.posts
    }
    return profileStore.posts
})
const noPostPlaceholder = computed(() => {
    if (props.user_id == null) {
        return postStore.isInSearch
            ? "No posts match your search."
            : "No posts yet. Start the conversation!"
    }
    return "This user hasn't posted anything yet."
});

const likingPostId = computed(() => props.user_id == null ? postStore.likingPostId : profileStore.likingPostId)
const savingPostId = computed(() => props.user_id == null ? postStore.savingPostId : profileStore.savingPostId)

const hasNextPage = computed(() => props.user_id == null ? postStore.hasNextPage : profileStore.hasNextPage)
const loadingMore = computed(() => props.user_id == null ? postStore.loadingMore : profileStore.loadingMore)
const showDonationModal = computed(() => props.user_id == null ? postStore.showDonationModal : profileStore.showDonationModal)
const selectedPost = computed(() => props.user_id == null ? postStore.selectedPost : profileStore.selectedPost)
const showConnectionModal = computed(() => props.user_id == null ? postStore.showConnectionModal : profileStore.showConnectionModal)
const selectedUserForConnection = computed(() => props.user_id == null ? postStore.selectedUserForConnection : profileStore.selectedUserForConnection)
const isConnectsModalOpen = computed(() => props.user_id == null ? postStore.isConnectsModalOpen : profileStore.isConnectsModalOpen)


const loadMore = () => {
    if (props.user_id == null) {
        postStore.loadMore();
    } else {
        profileStore.loadMore();
    }
}
const openDonationModal = (post) => {
    if (props.user_id == null) {
        postStore.openDonationModal(post);
    } else {
        profileStore.openDonationModal(post);
    }
}
const handleChat = async (post) => {
    if (props.user_id == null) {
        await postStore.handleChat(post);
    } else {
        await profileStore.handleChat(post);
    }
}

const handleSave = async (post) => {
    if (props.user_id == null) {
        await postStore.handleSave(post);
    } else {
        await profileStore.handleSave(post);
    }
}

const handleLike = async (post) => {
    if (props.user_id == null) {
        await postStore.handleLike(post);
    } else {
        await profileStore.handleLike(post);
    }
}

const handleUpdatePostObj = (post) => {
    if (props.user_id == null) {
        postStore.handleUpdatePostObj(post);
    } else {
        profileStore.handleUpdatePostObj(post);
    }
}

const handleConnectionsUpdated = async (postId) => {
    if (props.user_id == null) {
        await postStore.handleConnectionsUpdated(postId);
    } else {
        await profileStore.handleConnectionsUpdated(postId);
    }
}

const setShowDonationModal = (value) => {
    if (props.user_id == null) {
        postStore.setShowDonationModal(value);
    } else {
        profileStore.setShowDonationModal(value);
    }
}

const closeConnectionModal = () => {
    if (props.user_id == null) {
        postStore.closeConnectionModal();
    } else {
        profileStore.closeConnectionModal();
    }
}

const confirmConnectionRequest = async (messageText = '') => {
    if (props.user_id == null) {
        await postStore.confirmConnectionRequest(messageText);
    } else {
        await profileStore.confirmConnectionRequest(messageText);
    }
}

const setIsConnectsModalOpen = (value) => {
    if (props.user_id == null) {
        postStore.setIsConnectsModalOpen(value);
    } else {
        profileStore.setIsConnectsModalOpen(value);
    }
}

const handleFollowClick = async (post, showDonate = false) => {
    if (post.removed_connection && !post.pending_connection && !post.rejected_connection) {
        // Show modal for reconnection request
        if (props.user_id == null) {
            postStore.setSelectedUserForConnection(post);
            postStore.setShowConnectionModal(true);
        } else {
            profileStore.setSelectedUserForConnection(post);
            profileStore.setShowConnectionModal(true);
        }
    } else {
        if (props.user_id == null) {
            await postStore.handleFollow(post, showDonate);
        } else {
            await profileStore.handleFollow(post, showDonate);
        }
        await userStore.checkAuth();
    }
};


const currentConnects = computed(() => userStore.user?.connects || 0);

watch(() => profileStore.isConnectsModalOpen, async () => {
    if (profileStore.isConnectsModalOpen) {
        await connectsStore.fetchConnectsData();
    }
})
watch(() => postStore.isConnectsModalOpen, async () => {
    if (postStore.isConnectsModalOpen) {
        await connectsStore.fetchConnectsData();
    }
})

// Lifecycle
onMounted(async () => {
    if (props.user_id == null) {
        await postStore.fetchPosts();
        // After loading posts, check if we need to load a specific post from URL
        await postStore.checkUrlForPost();
        postStore.observePostVisibility();
            
        // Start polling after initial load
        nextTick(() => {
            postStore.startVisiblePostsPolling();
        });
    } else {
        await profileStore.fetchUserPosts();
        // After loading posts, check if we need to load a specific post from URL
        await profileStore.checkUrlForPost();
        profileStore.observePostVisibility();
            
        // Start polling after initial load
        nextTick(() => {
            profileStore.startVisiblePostsPolling();
        });
    }
});


onUnmounted(() => {
    if (props.user_id == null) {
        postStore.stopVisiblePostsPolling();
        if (postStore.visibilityObserver) postStore.visibilityObserver.disconnect();
        if (postStore.mutationObserver) postStore.mutationObserver.disconnect();
    } else {
        profileStore.stopVisiblePostsPolling();
        if (profileStore.visibilityObserver) profileStore.visibilityObserver.disconnect();
        if (profileStore.mutationObserver) profileStore.mutationObserver.disconnect();
    }
});
</script>