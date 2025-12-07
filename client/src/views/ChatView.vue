<template>
  <div class="min-h-screen bg-gray-50">
    <DesktopTopNav />    
    <MobileTopNav />
    
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
            <ChatTabs @select-tab="selectTab"/>

            <!-- Conversation List -->
            <div v-if="chatStore.loading" class="flex justify-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
            </div>
            
            <div v-else-if="chatStore.conversations.length === 0" class="text-center py-12">
              <p class="text-gray-500">No conversations found in {{ chatStore.activeTabName }}.</p>
            </div>
            
            <ul v-else id="conversation-list" class="divide-y divide-gray-200">
              <ConversationItem
                v-for="conversation in chatStore.conversations" 
                :key="conversation.id"
                :conversation="conversation"
                @select-conversation="selectConversation"
                :data-id="`conversation-${conversation.id}`"
              />
            </ul>
            
            <!-- Load More Button -->
            <div v-if="!chatStore.loading && chatStore.conversations.length > 0 && chatStore.pagination.hasMore" class="mt-4 flex justify-center">
              <button 
                @click="chatStore.loadMoreConversations"
                :disabled="chatStore.pagination.loadingMore"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="chatStore.pagination.loadingMore">
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
    
    <MobileBottomNav />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import { ArrowLeft } from 'lucide-vue-next';
import { message } from 'ant-design-vue';
import ChatTabs from '@/components/chat/ChatTabs.vue';
import { useChatStore } from '@/stores/chat';
import ConversationItem from '@/components/chat/ConversationItem.vue';
const chatStore = useChatStore();
const route = useRoute();
const router = useRouter();

// Check for post in URL
const postId = computed(() => route.query.p);
const isSharingPost = computed(() => !!postId.value);

let visibilityObserver = null;
let mutationObserver = null;

const selectConversation = async (conversation) => {
  if (isSharingPost.value) {
    console.log(`Sending post ${postId.value} to chat ${conversation.id}`);
    try {
      await chatStore.sharePost(conversation.id, postId.value);
      router.push(`/chat/${conversation.id}`);
    } catch (error) {
      console.error('Error sharing post:', error);
      message.error(error.response.data.error)
    }
  } else {
    router.push(`/chat/${conversation.id}`);
  }
};
function observeConversationVisibility() {
  if (visibilityObserver) visibilityObserver.disconnect();

  visibilityObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const id = entry.target.dataset.id.replace("conversation-", "");
        const index = chatStore.visibleConversations.indexOf(id);

        if (entry.isIntersecting) {
          if (index === -1) {
            chatStore.addToVisibleConversations(id);
            console.log("VISIBLE:", id);
          }
        } else {
          if (index !== -1) {
            chatStore.removeVisibleConversation(index)
            console.log("NOT VISIBLE:", id);
          }
        }
      });

      // Always log the current visible conversations
      console.log("VISIBLE:", chatStore.visibleConversations);
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

const selectTab = (tabId) => {
  chatStore.setActiveTab(tabId);
  chatStore.setPagination({
    page: 1,
    hasMore: true,
    loadingMore: false
  });
  chatStore.resetVisibleConversations();

  if (visibilityObserver) visibilityObserver.disconnect();
  mutationObserver?.disconnect();

  chatStore.fetchConversations().then(() => {
    // Re-observe the new conversations
    observeConversationVisibility();
  });
};

onMounted(async () => {
  await chatStore.fetchCategories();
  await chatStore.updateUnreadCounts();
  await chatStore.fetchConversations();
  observeConversationVisibility();
  
  // Start polling after initial load
  nextTick(() => {
    chatStore.startVisibleConversationsPolling();
  });
});

onUnmounted(() => {
  chatStore.stopVisibleConversationsPolling();
  if (visibilityObserver) visibilityObserver.disconnect();
  if (mutationObserver) mutationObserver.disconnect();
});
</script>