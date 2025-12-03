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
      :user-name="userName"
      @logout="handleLogout"
    />
    
    <!-- Main Content -->
    <div class="pt-16 pb-16 md:pt-0 md:pb-0">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="max-w-4xl mx-auto h-screen flex flex-col">
          <!-- Header with back button when sharing a post -->
          <div class="border-b border-gray-200 p-4">
            <div class="flex items-center">
              <button 
                v-if="isSharingPost" 
                @click="router.push({ query: {} })"
                class="mr-3 p-1 rounded-full hover:bg-gray-100"
              >
                <ArrowLeft class="h-5 w-5 text-gray-500" />
              </button>
              <h1 class="text-xl font-semibold text-gray-900">
                {{ isSharingPost ? 'Send post to...' : 'Messages' }}
              </h1>
            </div>
            <p v-if="isSharingPost" class="text-sm text-gray-500 mt-1">
              Select a chat to share this post
            </p>
          </div>
          
          <div class="px-4 py-5 sm:p-6">
            <!-- Tabs -->
            <div class="border-b border-gray-200 mb-6">
              <nav class="-mb-px flex space-x-8 overflow-x-auto" aria-label="Tabs">
                <button
                  v-for="(tab, index) in tabs"
                  :key="tab.id"
                  @click="selectTab(tab.id)"
                  :class="[
                    'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm',
                    activeTab === tab.id
                      ? 'border-indigo-500 text-indigo-600'
                      : 'cursor-pointer border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  ]"
                  :aria-current="activeTab === tab.id ? 'page' : undefined"
                >
                  {{ tab.name }}
                  <span 
                    v-if="tab.unread > 0"
                    :class="[
                      'ml-2 text-xs font-medium px-2 py-0.5 rounded-full',
                      tab.id === 'archived' 
                        ? 'bg-gray-100 text-gray-600' 
                        : tab.id === 'requests' 
                          ? 'bg-red-100 text-red-600' 
                          : 'bg-indigo-100 text-indigo-600'
                    ]"
                  >
                    {{ tab.unread }}
                  </span>
                </button>
              </nav>
            </div>

            <!-- Conversation List -->
            <div v-if="loading" class="flex justify-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
            </div>
            
            <div v-else-if="conversations.length === 0" class="text-center py-12">
              <p class="text-gray-500">No conversations found in {{ activeTabName }}.</p>
            </div>
            
            <ul v-else id="conversation-list" class="divide-y divide-gray-200">
              <li 
                v-for="conversation in conversations" 
                :key="conversation.id"
                class="py-4 hover:bg-gray-50 px-2 rounded-lg cursor-pointer"
                @click="selectConversation(conversation)"
                :data-id="`conversation-${conversation.id}`"

              >
                <div class="flex items-center">
                  <div class="flex-shrink-0 mr-4">
                    <!-- Show conversation logo for groups or when explicitly showing conversation details -->
                    <div v-if="conversation.is_group || conversation.name" class="h-10 w-10 rounded-full overflow-hidden bg-indigo-100 flex items-center justify-center">
                      <img v-if="conversation.logo" 
                           :src="conversation.logo" 
                           :alt="conversation.name || 'Group'"
                           class="h-full w-full object-cover">
                      <span v-else class="text-indigo-600 font-medium">
                        {{ conversation.name ? conversation.name.charAt(0).toUpperCase() : 'G' }}
                      </span>
                    </div>
                    <!-- Show user profile picture for direct messages -->
                    <div v-else-if="conversation.other_user_list?.length > 0 && conversation.other_user_list[0]?.user?.profile_picture" 
                         class="h-10 w-10 rounded-full overflow-hidden">
                      <img :src="conversation.other_user_list[0].user.profile_picture" 
                           :alt="conversation.other_user_list[0].user.name"
                           class="h-full w-full object-cover">
                    </div>
                    <!-- Fallback to user initial -->
                    <div v-else class="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-medium">
                      {{ 
                        conversation.other_user_list?.length > 0 ? 
                        conversation.other_user_list[0].user.name.charAt(0).toUpperCase() : 'U'
                      }}
                    </div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center justify-between">
                      <p :class="['text-sm truncate', conversation.new_messages_count > 0 ? 'font-bold text-gray-900' : 'font-light text-gray-900']">
                        {{ 
                          conversation.name || 
                          (conversation.other_user_list?.length > 0 ? 
                            conversation.other_user_list[0].user.name : 
                            'New Chat')
                        }}
                      </p>
                    </div>
                    <p :class="['text-sm truncate', conversation.new_messages_count > 0 ? 'font-medium text-gray-900' : 'text-gray-500']">
                      {{ conversation.last_message || 'No messages yet' }}
                    </p>
                  </div>
                  <div class="flex flex-col items-end">
                    <p v-if="conversation.last_message_list.length > 0" class="text-xs text-gray-500">
                      {{ conversation.last_message_list[0].created_since }}
                    </p>
                    <span v-if="conversation.new_messages_count > 0" class="bg-indigo-600 text-white text-xs font-medium px-2 py-0.5 rounded-full ml-2">
                        {{ conversation.new_messages_count > 99 ? '99+' : conversation.new_messages_count }}
                      </span>
                  </div>
                  <DropdownMenu>
                    <template #trigger>
                      <EllipsisVertical class="h-8 py-2 w-8 text-gray-500 cursor-pointer"/>
                    </template>
                    <button 
                      v-if="conversation.my_membership_list[0]?.category !== 'primary'"
                      @click.stop="moveConversation(conversation, 'primary')"
                      class="flex cursor-pointer w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      <ArrowRight class="mr-2 h-4 w-4" />
                      <span>Move to Primary</span>
                      <Check v-if="conversation.my_membership_list[0]?.category === 'primary'" class="ml-auto h-4 w-4 text-indigo-600" />
                    </button>
                    <button 
                      v-if="conversation.my_membership_list[0]?.category !== 'secondary'"
                      @click.stop="moveConversation(conversation, 'secondary')"
                      class="flex cursor-pointer w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      <ArrowRight class="mr-2 h-4 w-4" />
                      <span>Move to Secondary</span>
                      <Check v-if="conversation.my_membership_list[0]?.category === 'secondary'" class="ml-auto h-4 w-4 text-indigo-600" />
                    </button>
                    <button 
                      @click.stop="archiveConversation(conversation)"
                      class="flex cursor-pointer w-full items-center px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
                    >
                      <Archive class="mr-2 h-4 w-4" />
                      <span>Archive</span>
                    </button>
                  </DropdownMenu>
                </div>
              </li>
            </ul>
            
            <!-- Load More Button -->
            <div v-if="!loading && conversations.length > 0 && pagination.hasMore" class="mt-4 flex justify-center">
              <button 
                @click="loadMoreConversations"
                :disabled="pagination.loadingMore"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="pagination.loadingMore">
                  <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Loading...
                </span>
                <span v-else>Load More</span>
              </button>
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
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import api from '@/api/axios';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import { EllipsisVertical, Archive, ArrowRight, Check, ArrowLeft } from 'lucide-vue-next';
import DropdownMenu from '@/components/common/DropdownMenu.vue';

const route = useRoute();
const router = useRouter();

// Check for post in URL
const postId = computed(() => route.query.p);
const isSharingPost = computed(() => !!postId.value);
const userStore = useUserStore();
const loading = ref(true);
const activeTab = ref('primary');
const categories = ref([]);
const conversations = ref([]);
const pagination = ref({
  page: 1,
  hasMore: true,
  loadingMore: false
});

const visibleConversations = ref([]);
let visibilityObserver = null;
let mutationObserver = null;

// User data
const userInitials = computed(() => {
  if (!userStore.user?.first_name || !userStore.user?.last_name) return 'U';
  return `${userStore.user.first_name[0]}${userStore.user.last_name[0]}`.toUpperCase();
});

const userName = computed(() => {
  if (!userStore.user) return '';
  return `${userStore.user.first_name} ${userStore.user.last_name}`;
});

const handleLogout = () => {
  userStore.logout();
  router.push({ name: 'Login' });
};

// Fetch conversation categories
const fetchCategories = async () => {
  try {
    const response = await api.get('chat/conversations/categories/');
    categories.value = response.data;
    // Initialize tabs with categories
    tabs.value = response.data.map(category => ({
      id: category,
      name: category.charAt(0).toUpperCase() + category.slice(1),
      unread: 0
    }));
  } catch (error) {
    console.error('Error fetching categories:', error);
  }
};

// Fetch conversations for the active tab
const fetchConversations = async (loadMore = false) => {
  if (!activeTab.value) return;
  
  if (loadMore) {
    pagination.value.loadingMore = true;
    pagination.value.page += 1;
  } else {
    loading.value = true;
    pagination.value.page = 1;
    pagination.value.hasMore = true;
  }

  try {
    const response = await api.get(`chat/conversations/?category=${activeTab.value}&page=${pagination.value.page}`);
    const newConversations = response.data.results || [];
    
    if (loadMore) {
      // Merge new conversations with existing ones, avoiding duplicates
      const existingIds = new Set(conversations.value.map(c => c.id));
      const uniqueNewConversations = newConversations.filter(conv => !existingIds.has(conv.id));
      conversations.value = [...conversations.value, ...uniqueNewConversations];
      
      // Check if there are more pages
      pagination.value.hasMore = response.data.next !== null;
    } else {
      conversations.value = newConversations;
      pagination.value.hasMore = response.data.next !== null;
    }
    
    // Re-sort conversations by updated_at
    conversations.value.sort((a, b) => {
      return new Date(b.updated_at) - new Date(a.updated_at);
    });
  } catch (error) {
    console.error('Error fetching conversations:', error);
    if (loadMore) {
      // Revert page increment on error
      pagination.value.page = Math.max(1, pagination.value.page - 1);
    }
  } finally {
    loading.value = false;
    pagination.value.loadingMore = false;
  }
};

// Update unread counts for each tab
const updateUnreadCounts = async (conversations) => {
  let counts = {};
  categories.value.forEach(cat => counts[cat] = 0);
  
  const response = await api.get("/chat/conversations/unread_counts/")
  console.log("unread_counts", response.data)
  counts = response.data
  
  tabs.value = tabs.value.map(tab => ({
    ...tab,
    unread: counts[tab.id] || 0
  }));
};

const tabs = ref([
  { id: 'primary', name: 'Primary', unread: 0 },
  { id: 'secondary', name: 'Secondary', unread: 0 },
  { id: 'requests', name: 'Requests', unread: 0 },
  { id: 'archived', name: 'Archived', unread: 0 }
]);

const activeTabName = computed(() => {
  const tab = tabs.value.find(t => t.id === activeTab.value);
  return tab ? tab.name : '';
});


const selectConversation = async (conversation) => {
  if (isSharingPost.value) {
    console.log(`Sending post ${postId.value} to chat ${conversation.id}`);
    try {
      // const response = api.post("/chat/conversations/")
      // Here you would typically make an API call to send the post
      const response = await api.post(`/chat/conversations/${conversation.id}/share_post/`, { post_id: postId.value });
      
      // Show success message and navigate back
      // You might want to use a toast notification here
      // toast.success('Post shared successfully');
      
      // Navigate to the chat
      router.push(`/chat/${conversation.id}`);
    } catch (error) {
      console.error('Error sharing post:', error);
      // Show error message
      // toast.error('Failed to share post');
    }
  } else {
    router.push(`/chat/${conversation.id}`);
  }
};

const openChat = (conversationId) => {
  // Navigate to chat detail view
  router.push(`/chat/${conversationId}`);
};

const formatTime = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

function observeConversationVisibility() {
  if (visibilityObserver) visibilityObserver.disconnect();

  visibilityObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const id = entry.target.dataset.id.replace("conversation-", "");
        const index = visibleConversations.value.indexOf(id);

        if (entry.isIntersecting) {
          if (index === -1) {
            visibleConversations.value.push(id);
            console.log("VISIBLE:", id);
          }
        } else {
          if (index !== -1) {
            visibleConversations.value.splice(index, 1);
            console.log("NOT VISIBLE:", id);
          }
        }
      });

      // Always log the current visible conversations
      console.log("VISIBLE:", visibleConversations.value);
    },
    { threshold: 0.1 }
  );

  // Observe all current conversation items
  document.querySelectorAll("[data-id^='conversation-']").forEach((el) => {
    visibilityObserver.observe(el);
  });

  // Observe newly added conversation elements
  if (!mutationObserver) {
    const container = document.querySelector("#conversation-list");
    if (!container) return;

    mutationObserver = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === 1 && node.dataset.id?.startsWith("conversation-")) {
            visibilityObserver.observe(node);
          }
        });
      });
    });

    mutationObserver.observe(container, { childList: true, subtree: true });
  }
}


const fetchVisibleConversations = async () => {
  if (!visibleConversations.value.length) return;

  try {
    const ids = visibleConversations.value.join(',');
    const response = await api.get(`chat/conversations/get_bulk/?id=${ids}`);
    const fetchedConversations = response.data; // array of conversation objects

    // Update conversations in place
    fetchedConversations.forEach((conv) => {
      updateOrAddConversation(conv);
    });
  } catch (error) {
    console.error("Error fetching visible conversations:", error);
  }
};

const fetchLatestConversations = async () => {
  if (conversations.value.length === 0) return;
  
  try {
    const latestId = conversations.value[0].id; // Get the most recent conversation ID
    const response = await api.get(`chat/conversations/latest_conversations/?after_id=${latestId}&category=${activeTab.value}`);
    const newConversations = response.data;
    
    if (newConversations.length > 0) {
      // Update or add new conversations
      newConversations.forEach(conv => {
        updateOrAddConversation(conv);
      });
      
      // Sort conversations by updated_at in descending order
      conversations.value.sort((a, b) => {
        return new Date(b.updated_at) - new Date(a.updated_at);
      });
    }
  } catch (error) {
    console.error('Error fetching latest conversations:', error);
  }
};

const updateOrAddConversation = (newConv) => {
  const index = conversations.value.findIndex(c => c.id === newConv.id);
  if (index !== -1) {
    conversations.value[index] = { ...conversations.value[index], ...newConv };
  } else {
    conversations.value.unshift(newConv);
    conversations.value.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
  }
};

const moveConversation = async (conversation, category) => {
  try {
    await api.post(`chat/conversations/${conversation.id}/move_conversation/`, {
      category: category
    });
    
    // Update the local state
    conversations.value = conversations.value.filter(c => c.id !== conversation.id);
    await updateUnreadCounts();
  } catch (error) {
    console.error('Error moving conversation:', error);
  }
};

const archiveConversation = async (conversation) => {
  try {
    await api.post(`chat/conversations/${conversation.id}/archive_conversation_for_me/`);
    conversations.value = conversations.value.filter(c => c.id !== conversation.id);
    await updateUnreadCounts();
  } catch (error) {
    console.error('Error archiving conversation:', error);
  }
};

let visibleConversationsInterval = null;
let latestConversationsInterval = null;

const startVisibleConversationsPolling = () => {
  if (visibleConversationsInterval) clearInterval(visibleConversationsInterval);
  if (latestConversationsInterval) clearInterval(latestConversationsInterval);
  
  visibleConversationsInterval = setInterval(fetchVisibleConversations, 5000);
  latestConversationsInterval = setInterval(fetchLatestConversations, 3000);
};

const stopVisibleConversationsPolling = () => {
  if (visibleConversationsInterval) clearInterval(visibleConversationsInterval);
  if (latestConversationsInterval) clearInterval(latestConversationsInterval);
};

const selectTab = (tabId) => {
  activeTab.value = tabId;
  
  // Reset pagination for the new tab
  pagination.value = {
    page: 1,
    hasMore: true,
    loadingMore: false
  };

  // Reset visible conversations for the new tab
  visibleConversations.value = [];
  if (visibilityObserver) visibilityObserver.disconnect();
  mutationObserver?.disconnect();

  fetchConversations().then(() => {
    // Re-observe the new conversations
    observeConversationVisibility();
  });
};

const loadMoreConversations = async () => {
  if (!pagination.value.hasMore || pagination.value.loadingMore) return;
  await fetchConversations(true);
};

onMounted(async () => {
  await fetchCategories();
  await updateUnreadCounts();
  await fetchConversations();
  observeConversationVisibility();
  
  // Start polling after initial load
  nextTick(() => {
    startVisibleConversationsPolling();
  });
});

onUnmounted(() => {
  stopVisibleConversationsPolling();
  if (visibilityObserver) visibilityObserver.disconnect();
  if (mutationObserver) mutationObserver.disconnect();
});
</script>

<style scoped>
/* Add any custom styles here */
</style>
