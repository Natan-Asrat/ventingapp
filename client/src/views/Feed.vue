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
        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
        
        <div v-else-if="posts.length === 0" class="text-center py-12">
          <p class="text-gray-500">No posts to show. Be the first to post something!</p>
        </div>
        
        <div v-else class="space-y-6" id="post-list">
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
          <div v-if="hasNextPage" class="flex justify-center py-4">
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
    <donate-modal
      v-model="showDonationModal"
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
    
    <!-- Mobile Bottom Navigation -->
    <MobileBottomNav :user-initials="userInitials" />

    <!-- Connects Modal -->
    <ConnectsModal
      :is-open="isConnectsModalOpen"
      :current-connects="currentConnects"
      :connects-data="connectsStore.connectsData"
      :loading="connectsStore.isLoading"
      @close="isConnectsModalOpen = false"
      @purchase="connectsStore.handlePurchaseConnects"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, onUnmounted, nextTick } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { message } from 'ant-design-vue';
import { useUserStore } from '@/stores/user';
import api from '@/api/axios';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import FeedItem from '@/components/feed/FeedItem.vue';
import DonateModal from '@/components/feed/DonateModal.vue';
import ConnectionRequestModal from '@/components/feed/ConnectionRequestModal.vue';
import ConnectsModal from '@/components/connects/ConnectsModal.vue';
import { useConnectsStore } from '@/stores/connect';

const connectsStore = useConnectsStore();
const userStore = useUserStore();
const router = useRouter();
const route = useRoute();

// State
const posts = ref([]);
const loading = ref(true);
const loadingMore = ref(false);
const nextPage = ref(null);
const hasNextPage = computed(() => !!nextPage.value);
const showDonationModal = ref(false);
const selectedPost = ref(null);
const likingPostId = ref(null);
const savingPostId = ref(null);
const showConnectionModal = ref(false);
const selectedUserForConnection = ref(null);


const visiblePosts = ref([]);
let visibilityObserver = null;
let mutationObserver = null;

const handleUpdatePostObj = (post) => {
  const index = posts.value.findIndex(p => p.id === post.id);
  if (index !== -1) {
    posts.value[index] = post;
  }
}
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

// Methods
const fetchPosts = async (url = '/post/posts/') => {
  try {
    const response = await api.get(url);
    if (url.includes('page=')) {
      // Append new posts when loading more
      posts.value = [...posts.value, ...response.data.results];
    } else {
      // Set initial posts
      posts.value = response.data.results;
    }
    nextPage.value = response.data.next;
  } catch (error) {
    console.error('Error fetching posts:', error);
    message.error('Failed to load posts. Please try again later.');
  } finally {
    loading.value = false;
    loadingMore.value = false;
  }
};

const loadMore = () => {
  if (nextPage.value && !loadingMore.value) {
    loadingMore.value = true;

    const url = new URL(nextPage.value, window.location.origin);
    // Remove the first path segment
    const segments = url.pathname.split('/').filter(Boolean); // ["api", "post", "posts"]
    const relativePath = '/' + segments.slice(1).join('/') + url.search; // "/post/posts/?page=2"

    fetchPosts(relativePath);
  }
};


const handleChat = async (post) => {
  try {
    // If connected, start a chat
    const chatResponse = await api.post('chat/conversations/chat_with_user/', {
      user_id: post.posted_by.id
    });
    
    // Navigate to the chat
    const conversation = chatResponse.data[0]; // The API returns an array with one conversation
    router.push(`/chat/${conversation.id}`);
  } catch (error) {
    console.error('Error starting chat:', error);
    // Show error message to user
    if (error.response?.data?.error) {
      alert(error.response.data.error);
    } else {
      alert('Failed to start chat. Please try again.');
    }
  }
};

const openDonationModal = (post) => {
  selectedPost.value = post;
  showDonationModal.value = true;
};

const closeDonationModal = async (connected = false) => {
  if (connected && selectedPost.value) {
    // If user just connected, start a chat
    await handleChat(selectedPost.value);
  }
  showDonationModal.value = false;
  setTimeout(() => {
    selectedPost.value = null;
  }, 300);
};

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    message.success('Copied to clipboard!');
  } catch (err) {
    console.error('Failed to copy:', err);
    message.error('Failed to copy to clipboard');
  }
};

const handleImageLoad = (event) => {
  // Optional: Add any image load handling here
};

const handleLike = async (post) => {
  try {
    likingPostId.value = post.id;
    const endpoint = post.liked ? 'unlike' : 'like';
    const response = await api.post(`/post/posts/${post.id}/${endpoint}/`);
    
    // Update the post in the posts array
    const index = posts.value.findIndex(p => p.id === post.id);
    if (index !== -1) {
      // Create a new array to trigger reactivity
      const updatedPosts = [...posts.value];
      updatedPosts[index] = {
        ...updatedPosts[index],
        liked: !post.liked,
        likes: response.data.likes
      };
      posts.value = updatedPosts;
    }
  } catch (error) {
    console.error('Error toggling like:', error);
    message.error('Failed to update like. Please try again.');
  } finally {
    likingPostId.value = null;
  }
};

const handleSave = async (post) => {
  try {
    savingPostId.value = post.id;
    const endpoint = post.saved ? 'unsave' : 'save';
    const response = await api.post(`/post/posts/${post.id}/${endpoint}/`);
    
    // Update the post in the posts array
    const index = posts.value.findIndex(p => p.id === post.id);
    if (index !== -1) {
      // Create a new array to trigger reactivity
      const updatedPosts = [...posts.value];
      updatedPosts[index] = {
        ...updatedPosts[index],
        saved: !post.saved,
        saves: response.data.saves
      };
      posts.value = updatedPosts;
    }
  } catch (error) {
    console.error('Error toggling save:', error);
    message.error('Failed to update save status. Please try again.');
  } finally {
    savingPostId.value = null;
  }
};

const handleFollowClick = (post, showDonate = false) => {
  if (post.removed_connection && !post.pending_connection && !post.rejected_connection) {
    // Show modal for reconnection request
    selectedUserForConnection.value = post;
    showConnectionModal.value = true;
  } else {
    handleFollow(post, showDonate);
  }
};

const closeConnectionModal = () => {
  showConnectionModal.value = false;
  selectedUserForConnection.value = null;
};

const confirmConnectionRequest = async (messageText = '') => {
  if (!selectedUserForConnection.value) return;
  
  const post = selectedUserForConnection.value;
  closeConnectionModal();
  
  try {
    const postIndex = posts.value.findIndex(p => p.id === post.id);
    if (postIndex !== -1) {
      posts.value[postIndex].pending_connection = true;
    }
    
    const response = await api.post(`/account/users/${post.posted_by.id}/connect/`, {
      message: messageText
    });
    
    if (postIndex !== -1) {
      if (response.status === 201) {
        // Connection was just established (201 Created)
        posts.value[postIndex].connected = true;
        posts.value[postIndex].pending_connection = false;
        posts.value[postIndex].removed_connection = false;
        message.success(`You are now following ${post.posted_by.name || 'this user'}`);
      } else if (response.status === 200) {
        // Connection request sent
        posts.value[postIndex].pending_connection = true;
        posts.value[postIndex].removed_connection = false;
        message.success('Connection request sent');
      }
    }
  } catch (error) {
    console.error('Error sending connection request:', error);
    
    const postIndex = posts.value.findIndex(p => p.id === post.id);
    if (postIndex !== -1) {
      posts.value[postIndex].pending_connection = false;
    }
    
    let errorMessage = 'Failed to send connection request. Please try again.';
    
    if (error.response?.status === 400) {
      if (error.response?.data?.detail?.includes('already connected')) {
        errorMessage = 'You are already connected with this user';
      } else if (error.response?.data?.detail?.includes('pending')) {
        errorMessage = 'Connection request already pending';
        if (postIndex !== -1) {
          posts.value[postIndex].pending_connection = true;
        }
      }
    }
    
    message.error(errorMessage);
  }
};
const handleConnectionsUpdated = async (postId) => {
  if (!postId) return;

  // Check if post is already in the feed
  const newPostData = await fetchPostById(postId);
  const existingPost = posts.value.find(p => String(p.id) === String(postId));
  if (existingPost) {
    const postIndex = posts.value.findIndex(p => p.id === postId);
    if (postIndex !== -1) {
      posts.value[postIndex] = newPostData;
    }
    return;
  }

  // If not, fetch the post
  if (newPostData) {
    // Add to the beginning of the posts array
    posts.value.unshift(newPostData);
  }
};
const isConnectsModalOpen = ref(false);
const currentConnects = computed(() => userStore.user?.connects || 0);

const openConnectsModal = async () => {
  isConnectsModalOpen.value = true;
  await connectsStore.fetchConnectsData();
};

const handleFollow = async (post, showDonate = false) => {
  if (!post?.posted_by?.id || post.pending_connection || post.rejected_connection) {
    return;
  }

  const userId = post.posted_by.id;
  const isConnected = post.connected;
  const endpoint = isConnected ? 'disconnect' : 'connect';

  try {
    // Set pending state
    const postIndex = posts.value.findIndex(p => p.id === post.id);
    if (postIndex !== -1) {
      posts.value[postIndex].pending_connection = true;
    }

    // Make the API call to either connect or disconnect
    const response = await api.post(`/account/users/${userId}/${endpoint}/`);
    
    // Update the UI based on response status
    if (postIndex !== -1) {
      if (response.status === 201) {
        // Connection was just established (201 Created)
        posts.value[postIndex].connected = true;
        posts.value[postIndex].pending_connection = false;
        posts.value[postIndex].removed_connection = false;
        message.success(`You are now following ${post.posted_by.name || 'this user'}`);
        if(showDonate){
          openDonationModal(post)
        }
      } else if (response.status === 200) {
        if (isConnected) {
          // Disconnected successfully - reset all connection states
          posts.value[postIndex].connected = false;
          posts.value[postIndex].pending_connection = false;
          posts.value[postIndex].rejected_connection = false;
          posts.value[postIndex].removed_connection = true;
          message.success(`You have unfollowed ${post.posted_by.name || 'this user'}`);
        } else {
          // Connection request sent but not yet accepted (shouldn't happen with new flow)
          posts.value[postIndex].pending_connection = true;
          message.success('Connection request sent');
        }
      }
    }
    await userStore.checkAuth();
  } catch (error) {
    console.error(`Error ${isConnected ? 'unfollowing' : 'following'} user:`, error);
    
    // Reset pending state on error
    const postIndex = posts.value.findIndex(p => p.id === post.id);
    if (postIndex !== -1) {
      posts.value[postIndex].pending_connection = false;
    }
    
    let errorMessage = `Failed to ${isConnected ? 'unfollow' : 'follow'} user. Please try again.`;
    
    if (error.response?.data?.error) errorMessage = error.response?.data?.error;
    else if (error.response?.data?.message) errorMessage = error.response?.data?.message;  

      message.error(errorMessage);
    if (error.response?.status === 402) {
      // Not enough connects - open the connects modal
      openConnectsModal();
      return; // Don't show error message as we're handling it with the modal
    } else {
      message.error(errorMessage);
    }
  }
};

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

// Fetch a single post by ID
const fetchPostById = async (postId) => {
  try {
    const response = await api.get(`/post/posts/${postId}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching post:', error);
    message.error('Failed to load post');
    return null;
  }
};

// Check URL for post ID and handle post loading
const checkUrlForPost = async () => {
  const postId = route.query.p;
  if (!postId) return;

  // Check if post is already in the feed
  const existingPost = posts.value.find(p => String(p.id) === String(postId));
  if (existingPost) return;

  // If not, fetch the post
  const post = await fetchPostById(postId);
  if (post) {
    // Add to the beginning of the posts array
    posts.value.unshift(post);
  }
};


function observePostVisibility() {
  if (visibilityObserver) visibilityObserver.disconnect();

  visibilityObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const id = entry.target.dataset.id.replace("post-", "");
        const index = visiblePosts.value.indexOf(id);

        if (entry.isIntersecting) {
          if (index === -1) {
            visiblePosts.value.push(id);
            console.log("VISIBLE:", id);
          }
        } else {
          if (index !== -1) {
            visiblePosts.value.splice(index, 1);
            console.log("NOT VISIBLE:", id);
          }
        }
      });

      // Always log the current visible posts
      console.log("VISIBLE:", visiblePosts.value);
    },
    { threshold: 0.1 }
  );

  // Observe all current post items
  document.querySelectorAll("[data-id^='post-']").forEach((el) => {
    visibilityObserver.observe(el);
  });

  // Observe newly added post elements
  if (!mutationObserver) {
    const container = document.querySelector("#post-list");
    if (!container) return;

    mutationObserver = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === 1 && node.dataset.id?.startsWith("post-")) {
            visibilityObserver.observe(node);
          }
        });
      });
    });

    mutationObserver.observe(container, { childList: true, subtree: true });
  }
}


const fetchVisiblePosts = async () => {
  if (!visiblePosts.value.length) return;

  try {
    const ids = visiblePosts.value.join(',');
    const response = await api.get(`post/posts/get_bulk/?id=${ids}`);
    const fetchedPosts = response.data.results; // array of conversation objects

    // Update conversations in place
    fetchedPosts.forEach((post) => {
      updateOrAddPost(post);
    });
  } catch (error) {
    console.error("Error fetching visible posts:", error);
  }
};


const updateOrAddPost = (newPost) => {
  console.log("UPDATE OR ADD POST", newPost);
  const index = posts.value.findIndex(p => p.id === newPost.id);
  if (index !== -1) {
    posts.value[index] = { ...posts.value[index], ...newPost };
  } else {
    posts.value.unshift(newPost);
    posts.value.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
  }
};


let visiblePostsInterval = null;

const startVisiblePostsPolling = () => {
  if (visiblePostsInterval) clearInterval(visiblePostsInterval);
  
  visiblePostsInterval = setInterval(fetchVisiblePosts, 5000);
};

const stopVisiblePostsPolling = () => {
  if (visiblePostsInterval) clearInterval(visiblePostsInterval);
};

// Lifecycle
onMounted(async () => {
  await fetchPosts();
  // After loading posts, check if we need to load a specific post from URL
  await checkUrlForPost();
  observePostVisibility();
    
  // Start polling after initial load
  nextTick(() => {
    startVisiblePostsPolling();
  });
});


onUnmounted(() => {
  stopVisiblePostsPolling();
  if (visibilityObserver) visibilityObserver.disconnect();
  if (mutationObserver) mutationObserver.disconnect();
});
</script>

<style scoped>
/* Add any custom styles here */
.rotate-180 {
  transform: rotate(180deg);
}
</style>
