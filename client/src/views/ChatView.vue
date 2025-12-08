<template>
  <div class="min-h-screen bg-zinc-50/50 font-sans">
    <DesktopTopNav />    
    <MobileTopNav />
    
    <!-- Main Content -->
    <div class="pt-20 pb-20 md:pt-6 md:pb-0 relative z-0">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="bg-white shadow-sm border border-zinc-100 rounded-2xl overflow-hidden h-[calc(100vh-140px)] flex flex-col">
          <!-- Header with back button when sharing a post -->
          <div class="border-b border-zinc-100 p-5 bg-white/50 backdrop-blur-sm z-10">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <button 
                  v-if="isSharingPost" 
                  @click="router.push({ query: {} })"
                  class="p-2 rounded-full hover:bg-zinc-100 text-zinc-500 transition-colors"
                >
                  <ArrowLeft class="h-5 w-5" />
                </button>
                <div>
                  <h1 class="text-xl font-bold text-zinc-900 tracking-tight">
                    {{ isSharingPost ? 'Send post to...' : 'Messages' }}
                  </h1>
                  <p v-if="isSharingPost" class="text-sm text-zinc-500 mt-0.5">
                    Select a chat to share this post
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="flex flex-col h-full overflow-hidden">
            <div class="px-5 pt-2">
               <ChatTabs @select-tab="selectTab"/>
            </div>

            <!-- Conversation List -->
            <div class="flex-1 overflow-y-auto px-2" id="conversation-list-container">
                <div v-if="chatStore.loading" class="flex flex-col items-center justify-center py-12">
                  <div class="animate-spin rounded-full h-8 w-8 border-[3px] border-violet-100 border-t-violet-500 mb-3"></div>
                  <span class="text-xs font-medium text-zinc-400">Loading conversations...</span>
                </div>
                
                <div v-else-if="chatStore.conversations.length === 0" class="flex flex-col items-center justify-center py-20 text-center">
                  <div class="w-16 h-16 bg-zinc-50 rounded-full flex items-center justify-center mb-4 ring-8 ring-zinc-50/50">
                    <MessageSquareOff class="h-8 w-8 text-zinc-300" />
                  </div>
                  <p class="text-zinc-900 font-medium">No conversations found</p>
                  <p class="text-zinc-500 text-sm mt-1">in {{ chatStore.activeTabName }}</p>
                </div>
                
                <ul v-else id="conversation-list" class="divide-y divide-zinc-50 space-y-1 p-2">
                  <ConversationItem
                    v-for="conversation in chatStore.conversations" 
                    :key="conversation.id"
                    :conversation="conversation"
                    @select-conversation="selectConversation"
                    :data-id="`conversation-${conversation.id}`"
                  />
                </ul>
                
                <!-- Load More Button -->
                <div v-if="!chatStore.loading && chatStore.conversations.length > 0 && chatStore.pagination.hasMore" class="py-6 flex justify-center">
                  <button 
                    @click="chatStore.loadMoreConversations"
                    :disabled="chatStore.pagination.loadingMore"
                    class="inline-flex items-center px-4 py-2 border border-zinc-200 text-sm font-medium rounded-full shadow-sm text-zinc-600 bg-white hover:bg-zinc-50 hover:text-violet-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                  >
                    <span v-if="chatStore.pagination.loadingMore" class="flex items-center">
                      <div class="animate-spin rounded-full h-4 w-4 border-2 border-zinc-400 border-t-zinc-600 mr-2"></div>
                      Loading...
                    </span>
                    <span v-else>Load More</span>
                  </button>
                </div>
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
import { ArrowLeft, MessageSquareOff } from 'lucide-vue-next';
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
    try {
      await chatStore.sharePost(conversation.id, postId.value);
      router.push(`/chat/${conversation.id}`);
    } catch (error) {
      console.error('Error sharing post:', error);
      message.error(error.response?.data?.error || 'Failed to share post')
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
          }
        } else {
          if (index !== -1) {
            chatStore.removeVisibleConversation(index)
          }
        }
      });
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