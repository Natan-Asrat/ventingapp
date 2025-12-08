<template>
  <div>
    <main :class="[ user_id == null && 'pb-24 md:pt-0 md:pb-0', user_id == null && postStore.searchProfileResults.length == 0 && 'pt-16 md:pt-6']">
      <div class="max-w-xl mx-auto px-0 sm:px-4 py-6">
        <!-- Posts Feed -->
        <div v-if="loading" class="flex flex-col items-center justify-center py-20 space-y-4">
          <div class="animate-spin rounded-full h-8 w-8 border-[3px] border-violet-100 border-t-violet-500"></div>
          <span class="text-sm font-medium text-zinc-400 animate-pulse tracking-wide">Listening for voices...</span>
        </div>
        
        <div v-else-if="posts.length === 0" class="flex flex-col items-center justify-center py-24 px-6 text-center">
            <div class="bg-zinc-100 rounded-full p-6 mb-4">
                <svg class="w-10 h-10 text-zinc-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
            </div>
            <p class="text-zinc-500 font-medium text-lg">{{ noPostPlaceholder }}</p>
            <p class="text-zinc-400 text-sm mt-2">Be the first to share your story.</p>
        </div>
        
        <div v-else class="space-y-6" id="post-list">
            <div v-if="postStore.isInSearch" class="px-4 sm:px-0 mb-6">
                <h2 class="text-lg font-medium text-zinc-800 tracking-tight flex items-center gap-2">
                    Finding results for
                    <span v-if="postStore.searchQuery" class="text-violet-600 bg-violet-50 px-3 py-0.5 rounded-full font-semibold">"{{ postStore.searchQuery }}"</span>
                </h2>
            </div>
                      
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
            <div v-if="hasNextPage || postStore.showRecommended" class="flex justify-center py-10 pb-16">
                <button 
                    @click="loadMore" 
                    :disabled="loadingMore"
                    class="cursor-pointer group relative px-8 py-3 bg-white border border-zinc-200 text-zinc-600 font-medium rounded-full shadow-sm hover:shadow hover:border-violet-200 hover:text-violet-600 focus:outline-none focus:ring-2 focus:ring-violet-500/20 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none"
                >
                    <span class="flex items-center gap-2.5">
                        <span v-if="loadingMore" class="animate-spin h-4 w-4 border-2 border-violet-500 border-t-transparent rounded-full"></span>
                        <span class="tracking-wide text-sm">{{ loadingMore ? 'Loading stories...' : 'Read More Stories' }}</span>
                    </span>
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