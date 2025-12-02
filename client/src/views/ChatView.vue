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
        <div class="bg-white shadow sm:rounded-lg overflow-hidden">
          <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h3 class="text-lg leading-6 font-medium text-gray-900">Messages</h3>
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
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  ]"
                  :aria-current="activeTab === tab.id ? 'page' : undefined"
                >
                  {{ tab.name }}
                  <span 
                    v-if="tab.unread > 0"
                    class="ml-2 bg-indigo-100 text-indigo-600 text-xs font-medium px-2 py-0.5 rounded-full"
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
            
            <ul v-else class="divide-y divide-gray-200">
              <li 
                v-for="conversation in conversations" 
                :key="conversation.id"
                class="py-4 hover:bg-gray-50 px-2 rounded-lg cursor-pointer"
                @click="openChat(conversation.id)"
              >
                <div class="flex items-center space-x-4">
                  <div class="flex-shrink-0">
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
                    <p class="text-sm font-medium text-gray-900 truncate">
                      {{ 
                        conversation.name || 
                        (conversation.other_user_list?.length > 0 ? 
                          conversation.other_user_list[0].user.name : 
                          'New Chat')
                      }}
                    </p>
                    <p class="text-sm text-gray-500 truncate">
                      {{ conversation.last_message || 'No messages yet' }}
                    </p>
                  </div>
                  <div class="flex flex-col items-end">
                    <p class="text-xs text-gray-500">
                      {{ formatTime(conversation.updated_at) }}
                    </p>
                    <span 
                      v-if="conversation.unread_count > 0"
                      class="mt-1 inline-flex items-center justify-center px-2 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800"
                    >
                      {{ conversation.unread_count }}
                    </span>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Mobile Bottom Navigation -->
    <mobile-bottom-nav :user-initials="userInitials" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import api from '@/api/axios';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';

const router = useRouter();
const userStore = useUserStore();
const loading = ref(true);
const activeTab = ref('primary');
const categories = ref([]);
const conversations = ref([]);

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
const fetchConversations = async () => {
  if (!activeTab.value) return;
  
  loading.value = true;
  try {
    const response = await api.get('chat/conversations/', {
      params: { category: activeTab.value }
    });
    conversations.value = response.data.results;
    
    // Update unread counts in tabs
    // updateUnreadCounts(response.data.results);
  } catch (error) {
    console.error('Error fetching conversations:', error);
  } finally {
    loading.value = false;
  }
};

// Update unread counts for each tab
const updateUnreadCounts = (conversations) => {
  const counts = {};
  categories.value.forEach(cat => counts[cat] = 0);
  
  conversations.forEach(conv => {
    const category = conv.my_membership_list?.[0]?.category;
    if (category && counts[category] !== undefined) {
      counts[category]++;
    }
  });
  
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

const selectTab = (tabId) => {
  activeTab.value = tabId;
  fetchConversations();
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

onMounted(async () => {
  await fetchCategories();
  await fetchConversations();
});
</script>

<style scoped>
/* Add any custom styles here */
</style>
