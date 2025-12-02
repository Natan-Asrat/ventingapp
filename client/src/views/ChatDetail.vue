<template>
  <div class="max-w-4xl mx-auto h-screen flex flex-col relative">
    <!-- New Messages Indicator -->
    <div 
      v-if="showNewMessagesIndicator" 
      @click="scrollToNewMessages"
      class="fixed bottom-24 mt-2 right-6 bg-indigo-600 text-white rounded-full p-3 shadow-lg cursor-pointer hover:bg-indigo-700 transition-colors z-10"
      :title="`${newMessagesCount} new message${newMessagesCount > 1 ? 's' : ''}`"
    >
      <div class="flex items-center">
        <span class="text-xs mr-2">{{ newMessagesCount }}</span>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M16.707 10.293a1 1 0 010 1.414l-6 6a1 1 0 01-1.414 0l-6-6a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l4.293-4.293a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
      </div>
    </div>
    <!-- Header -->
    <div class="border-b border-gray-200 p-4 flex items-center">
      <button 
        @click="$router.back()" 
        class="mr-4 p-2 rounded-full hover:bg-gray-100 md:hidden"
      >
        <svg class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <div class="flex-1">
        <h2 class="text-lg font-medium text-gray-900">{{ conversation.name || 'Chat' }}</h2>
        <p class="text-sm text-gray-500" v-if="otherUser">
          {{ otherUser.name || otherUser.username }}
        </p>
      </div>
    </div>


    <!-- Messages -->
    <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-4 messages-container" style="scroll-behavior: smooth;">
      <!-- Load More Button -->
      <div v-if="pagination.next" class="flex justify-center mb-4">
        <button 
          @click="fetchMessages(true)" 
          :disabled="pagination.isLoading"
          :class="{'cursor-pointer': !pagination.isLoading}"
          class="px-4 py-2 text-sm text-indigo-600 bg-indigo-50 hover:bg-indigo-100 rounded-full flex items-center space-x-2 transition-colors"
        >
          <svg v-if="pagination.isLoading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ pagination.isLoading ? 'Loading...' : 'Load More' }}</span>
        </button>
      </div>
      <div 
        v-for="(message, index) in messages" 
        :key="message.id"
        :id="`message-${message.id}`"
        :class="[
          'relative',
          'flex', 
          message.user.id === currentUser.id ? 'justify-end' : 'justify-start',
          { 'bg-blue-50 rounded-lg transition-colors duration-1000': highlightedMessageId === message.id }
        ]"
      >
        <!-- New messages indicator -->
        <div 
          v-if="showNewMessageDivider && index === firstNewMessageIndex" 
          class="w-full mt-2 text-center py-2 text-xs text-gray-500 flex items-center absolute -top-8 left-0 right-0"
        >
          <span class="flex-grow border-t border-gray-300"></span>
          <span class="mx-2">New messages</span>
          <span class="flex-grow border-t border-gray-300"></span>
        </div>
        <!-- Avatar for received messages only -->
        <div v-if="message.user.id !== currentUser.id" class="flex-shrink-0 mr-2 self-end">
          <img 
            v-if="message.user.profile_picture"
            :src="message.user.profile_picture"
            :alt="message.user.name"
            class="h-8 w-8 rounded-full object-cover"
          >
          <div v-else class="h-8 w-8 rounded-full bg-gray-300 flex items-center justify-center text-sm text-gray-600">
            {{ message.user.name ? message.user.name.charAt(0).toUpperCase() : 'U' }}
          </div>
        </div>

        <!-- Message container -->
        <div class="relative group">
          <!-- Reply preview (not part of hover area) -->
          <div v-if="message.reply_to" 
               class="bg-gray-50 rounded-lg p-2 mb-1 text-xs text-gray-500 w-full max-w-xs cursor-pointer"
               @click="scrollToMessage(message.reply_to.id)">
            <div class="font-medium mr-2">
              Replied to {{ message.reply_to.user.id === currentUser.id ? 'You' : `@${message.reply_to.user.username}` }}
            </div>
            <div class="truncate">
              {{ message.reply_to.message }}
            </div>
          </div>
          
          <!-- Message bubble with hover area -->
          <div 
            :class="[
              'max-w-xs md:max-w-md lg:max-w-lg rounded-lg relative',
              message.user.id === currentUser.id 
                ? 'bg-indigo-100 text-indigo-900' 
                : 'bg-gray-100 text-gray-900',
              'hover:bg-opacity-90 transition-colors duration-200',
              'px-4 py-2',
              'flex flex-col',
              message.user.id === currentUser.id ? 'ml-auto' : 'mr-auto'
            ]"
            @mouseenter="showActions = message.id"
            @mouseleave="handleMouseLeave">
            
            <!-- Message content -->
            <p class="text-sm">{{ message.message }}</p>
            
            <!-- Hover actions -->
            <div 
              v-if="showActions === message.id"
              class="absolute flex items-center space-x-1 bg-white rounded-full shadow-md p-1 transition-opacity duration-200"
              :class="{
                'right-0 -bottom-6': message.user.id === currentUser.id,
                'left-0 -bottom-6': message.user.id !== currentUser.id,
                'ml-12': (message.my_reaction_list?.length || message.other_reactions_list?.length) && message.user.id !== currentUser.id,
                'mr-12': (message.my_reaction_list?.length || message.other_reactions_list?.length) && message.user.id === currentUser.id,
                '!left-4': message.user.id !== currentUser.id
              }"
              @mouseenter="showActions = message.id">
              
              <button 
                @click.stop="handleReply(message)"
                class="p-1 cursor-pointer text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-full"
                title="Reply">
                <Reply class="h-4 w-4"/>
              </button>
              
              <div class="relative">
                <button 
                  @click.stop="toggleEmojiPicker(message.id, $event)"
                  @mouseenter="cancelClose()"
                  class="p-1 cursor-pointer text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-full"
                  title="React">
                  <Smile class="h-4 w-4"/>
                </button>
                
                <!-- Emoji Picker Popup -->
                <div 
                  v-if="emojiPickerForMessage === message.id"
                  class="absolute left-0 z-50 shadow-lg rounded-lg overflow-hidden bg-white"
                  :style="{ 
                    left: message.user.id === currentUser.id ? 'auto' : '0px',
                    right: message.user.id === currentUser.id ? '-50px' : 'auto',
                    width: '300px',
                    maxHeight: '300px',
                    overflowY: 'auto' 
                  }"
                  @mouseenter="cancelClose(); showActions = message.id">
                  <Picker 
                    :data="emojiIndex" 
                    set="twitter" 
                    @select="(emoji) => onEmojiSelect(message, emoji)" 
                    :perLine="7"
                    :showPreview="false"
                    :showSearch="true"
                    :showSkinTones="false"
                    :emojiSize="24"
                    :native="true"
                    :autoFocus="true"
                    :enableFrequentEmojiSort="true"
                    title="Pick an emoji"
                    style="width: 300px;"
                  />
                </div>
              </div>
              
              <button 
                class="p-1 cursor-pointer text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-full"
                title="More">
                <EllipsisVertical class="h-4 w-4"/>
              </button>
            </div>
          </div>

          <!-- Message timestamp -->
          <div class="flex justify-end mt-1">
            <p class="text-xs text-gray-500">
              {{ formatTime(message.created_at) }}
            </p>
          </div>
          
          <!-- Reactions (always visible) -->
          <div v-if="message.my_reaction_list?.length || message.other_reactions_list?.length" 
               class="flex items-center space-x-1 mt-1">
            <!-- My reaction -->
            <div v-if="message.my_reaction_list?.length" class="flex items-center">
              <div class="flex items-center -space-x-1">
                <span class="text-sm z-2">{{ message.my_reaction_list[0].reaction }}</span>
                <img v-if="currentUser.profile_picture" 
                     :src="currentUser.profile_picture" 
                     class="h-5 w-5 rounded-full border-2 border-white" 
                     :alt="currentUser.name" />
                <div v-else 
                     class="h-5 w-5 rounded-full bg-indigo-100 text-indigo-600 text-xs flex items-center justify-center border-2 border-white">
                  {{ currentUser.name?.charAt(0) || 'U' }}
                </div>
              </div>
            </div>
            
            <!-- Other users' reactions -->
            <div v-for="reaction in message.other_reactions_list" 
                 :key="reaction.id" 
                 class="flex items-center">
              <div class="flex items-center -space-x-1">
                <span class="text-sm z-2">{{ reaction.reaction }}</span>
                <img v-if="reaction.user.profile_picture" 
                     :src="reaction.user.profile_picture" 
                     class="h-5 w-5 rounded-full border-2 border-white" 
                     :alt="reaction.user.name" 
                     :title="reaction.user.name" />
                <div v-else 
                     class="h-5 w-5 rounded-full bg-gray-200 text-gray-600 text-xs flex items-center justify-center border-2 border-white"
                     :title="reaction.user.name">
                  {{ reaction.user.name?.charAt(0) || 'U' }}
                </div>
              </div>
            </div>
          </div>


        </div>
      </div>
    </div>

    <!-- Message Input -->
    <div class="border-t border-gray-200">
      <!-- Reply Preview -->
      <div v-if="replyingTo" class="bg-gray-50 p-3 flex justify-between items-start border-b border-gray-100">
        <div 
          class="text-xs cursor-pointer text-gray-700 flex-1 cursor-pointer hover:bg-gray-100 -m-1 p-1 rounded"
          @click="scrollToMessage(replyingTo.id)"
        >
          <div class="font-medium text-gray-900">Replying to @{{ replyingTo.user.username }}</div>
          <div class="text-gray-500 mt-1 truncate">{{ replyingTo.message }}</div>
        </div>
        <button 
          @click="cancelReply" 
          class="text-indigo-500 cursor-pointer hover:text-indigo-700 p-1 flex-shrink-0"
        >
          <X class="h-4 w-4" />
        </button>
      </div>
      <form @submit.prevent="sendMessage" class="flex space-x-2 p-4">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Type a message..."
          class="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        />
        <button
          type="submit"
          class="bg-indigo-600 cursor-pointer text-white rounded-full p-2 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
            <Send class="h-5 w-5"/>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, nextTick, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { X, Reply, Smile, EllipsisVertical, Send } from 'lucide-vue-next';
import api from '@/api/axios';

const visibleMessages = ref([]);
let visibilityObserver = null;
let mutationObserver = null;
const showNewMessagesIndicator = ref(false);
const showNewMessageDivider = ref(false);
const firstNewMessageIndex = ref(-1);
const isAtBottom = ref(true);
const newMessagesCount = ref(0);
const hasSentNewMessage = ref(false);
// Emoji Picker
import data from 'emoji-mart-vue-fast/data/all.json';
import 'emoji-mart-vue-fast/css/emoji-mart.css';
import { Picker, EmojiIndex } from 'emoji-mart-vue-fast/src';

// Click outside directive
const vClickOutside = {
  beforeMount(el, binding) {
    el.clickOutsideEvent = function(event) {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event);
      }
    };
    document.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent);
  },
};

// Create emoji data index
const emojiIndex = new EmojiIndex(data);

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();
const currentUser = computed(() => userStore.user);

const conversation = ref({});
const messages = ref([]);
const newMessage = ref('');
const messagesContainer = ref(null);
const replyingTo = ref(null);
const highlightedMessageId = ref(null);
const showActions = ref(null);
const emojiPickerForMessage = ref(null);
const pagination = ref({
  next: null,
  previous: null,
  count: 0,
  isLoading: false
});
let closeTimeout = null;

// Fetch conversation details
const fetchConversation = async () => {
  try {
    const response = await api.get(`chat/conversations/${route.params.id}/`);
    conversation.value = response.data;
    await fetchMessages();
  } catch (error) {
    console.error('Error fetching conversation:', error);
  }
};

// Fetch messages
const fetchMessages = async (loadMore = false) => {
  try {
    pagination.value.isLoading = true;
    let url = `chat/conversations/${route.params.id}/messages/`;
    const first_message_id = messages.value.length > 0 ? messages.value[0].id : null;
    
    if (loadMore && pagination.value.next) {
      // Use the next page URL if loading more
      url = pagination.value.next;
    } else if (!loadMore) {
      // Reset messages if it's a fresh load
      // messages.value = [];
    }
    
    const response = await api.get(url);

    const container = messagesContainer.value;

    const prevBehavior = container.style.scrollBehavior;
    container.style.scrollBehavior = 'auto';

    const previousScrollHeight = container.scrollHeight;
    
    if (loadMore) {
      // When loading more, prepend the new messages (they're older)
      messages.value = [...response.data.results.reverse(), ...messages.value];
    } else {
      // For initial load, just set the messages
      messages.value = response.data.results.reverse();
    }
    
    // Update pagination info
    pagination.value = {
      next: response.data.next,
      previous: response.data.previous,
      count: response.data.count,
      isLoading: false
    };
    
    // Scroll to maintain position when loading more
    if (loadMore && messagesContainer.value && messages.value.length > 0) {
      const container = messagesContainer.value;

      nextTick(() => {
        const newScrollHeight = container.scrollHeight;
        container.scrollTop += newScrollHeight - previousScrollHeight;

        // Restore smooth scrolling
        container.style.scrollBehavior = prevBehavior;
      });
    } else if (!loadMore) {
      scrollToBottom();
    }


  } catch (error) {
    console.error('Error fetching messages:', error);
    pagination.value.isLoading = false;
  }
};

// Send a new message
const sendMessage = async () => {
  if (!newMessage.value.trim()) return;

  try {
    await api.post(`chat/conversations/${route.params.id}/send_message/`, {
      message: newMessage.value,
      reply_to: replyingTo.value?.id || null
    });
    newMessage.value = '';
    replyingTo.value = null;
    hasSentNewMessage.value = true;
  } catch (error) {
    console.error('Error sending message:', error);
  }
};

// Handle reply to message
const handleReply = (message) => {
  replyingTo.value = message;
  scrollToMessage(message.id);
  nextTick(() => {
    const input = document.querySelector('input[type="text"], textarea');
    if (input) input.focus();
  });
};

// Scroll to and highlight a specific message
const scrollToMessage = (messageId) => {
  // Clear any existing highlight
  console.log("scrolling to ", messageId);
  if (highlightTimeout) {
    clearTimeout(highlightTimeout);
    highlightTimeout = null;
  }
  
  // Set the highlighted message
  highlightedMessageId.value = messageId;
  
  // Scroll to the message
  nextTick(() => {
    const messageElement = document.getElementById(`message-${messageId}`);
    if (messageElement) {
      messageElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      
      // Remove highlight after 3 seconds
      highlightTimeout = setTimeout(() => {
        highlightedMessageId.value = null;
      }, 2000);
    }
  });
};

// Toggle emoji picker for a message
const toggleEmojiPicker = async (messageId, event) => {
  event.stopPropagation();
  event.preventDefault();
  
  if (emojiPickerForMessage.value === messageId) {
    emojiPickerForMessage.value = null;
    return;
  }
  
  emojiPickerForMessage.value = messageId;
  showActions.value = messageId;
  
  // Wait for the next tick to ensure the DOM is updated
  await nextTick();
  
  // Get the button and picker elements
  const button = event.target.closest('button');
  const picker = button?.nextElementSibling;
  
  if (!button || !picker) return;
  
  const buttonRect = button.getBoundingClientRect();
  const pickerHeight = 300; // Approximate height of the picker
  const viewportHeight = window.innerHeight;
  
  // Get the message container's scroll position
  const messagesContainer = document.querySelector('.messages-container');
  const containerRect = messagesContainer?.getBoundingClientRect() || { top: 0 };
  
  // Calculate available space below the button, considering the container's scroll position
  const spaceBelow = viewportHeight - buttonRect.bottom - 20; // 20px buffer from bottom
  const spaceAbove = buttonRect.top - containerRect.top - 20; // 20px buffer from top
  
  // Position the picker above or below based on available space
  if (spaceBelow < pickerHeight && (spaceAbove > pickerHeight || spaceAbove > spaceBelow)) {
    // Position above the button
    picker.style.top = 'auto';
    picker.style.bottom = '100%';
    picker.style.marginTop = '0';
    picker.style.marginBottom = '0.5rem';
    picker.style.maxHeight = `${Math.min(spaceAbove - 20, 300)}px`; // Adjust height to fit
  } else {
    // Position below the button (default)
    picker.style.top = '100%';
    picker.style.bottom = 'auto';
    picker.style.marginTop = '0.5rem';
    picker.style.marginBottom = '0';
    picker.style.maxHeight = `${Math.min(spaceBelow - 20, 300)}px`; // Adjust height to fit
  }
};

// Close emoji picker with delay
const closeEmojiPicker = () => {
  if (closeTimeout) clearTimeout(closeTimeout);
  closeTimeout = setTimeout(() => {
    emojiPickerForMessage.value = null;
    showActions.value = null;
  }, 1000);
};

// Handle mouse leave with delay
const handleMouseLeave = () => {
  closeEmojiPicker();
};

// Cancel pending close when re-entering the button or picker
const cancelClose = () => {
  if (closeTimeout) {
    clearTimeout(closeTimeout);
    closeTimeout = null;
  }
};

// Handle emoji selection
const onEmojiSelect = async (message, emoji) => {
  try {
    // Send reaction to the server and get the updated message
    const response = await api.post(`chat/messages/${message.id}/react/`, {
      emoji: emoji.native
    });
    
    // Update the message in the messages array with the server response
    const updatedMessage = response.data;
    const messageIndex = messages.value.findIndex(m => m.id === updatedMessage.id);
    
    if (messageIndex !== -1) {
      // Create a new array to trigger reactivity
      const updatedMessages = [...messages.value];
      updatedMessages[messageIndex] = {
        ...updatedMessages[messageIndex],
        my_reaction_list: updatedMessage.my_reaction_list,
        other_reactions_list: updatedMessage.other_reactions_list,
        updated_at: updatedMessage.updated_at
      };
      messages.value = updatedMessages;
    }
    
    // Close the picker
    emojiPickerForMessage.value = null;
    
  } catch (error) {
    console.error('Error sending reaction:', error);
  }
};

// Cancel reply
const cancelReply = () => {
  replyingTo.value = null;
};

// Format time
const formatTime = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

// Scroll to the first new message
const scrollToNewMessages = () => {
  if (firstNewMessageIndex.value >= 0) {
    const firstNewMsgId = messages.value[firstNewMessageIndex.value].id;
    let element = document.getElementById(`message-${firstNewMsgId - 1}`);

    // Fallback to the first new message if previous doesn't exist
    if (!element) {
      element = document.getElementById(`message-${firstNewMsgId}`);
    }    
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
    showNewMessagesIndicator.value = false;
  } else {
    scrollToBottom();
  }
};

// Scroll to bottom of messages
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    showNewMessagesIndicator.value = false;
    setTimeout(() => {
      showNewMessageDivider.value = false;
    }, 3000);
    isAtBottom.value = true;
    newMessagesCount.value = 0;
  }
};

// Get other user in conversation
const otherUser = computed(() => {
  if (!conversation.value.members) return null;
  return conversation.value.members.find(
    member => member.user.id !== currentUser.value.id
  )?.user;
});

function observeMessageVisibility() {
  // Disconnect previous observer if any
  if (visibilityObserver) visibilityObserver.disconnect();

  visibilityObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const id = entry.target.id.replace("message-", "");
        const index = visibleMessages.value.indexOf(id);

        if (entry.isIntersecting) {
          if (index === -1) {
            visibleMessages.value.push(id);
            console.log("VISIBLE:", id);
          }
        } else {
          if (index !== -1) {
            visibleMessages.value.splice(index, 1);
            console.log("NOT VISIBLE:", id);
          }
        }
      });
      console.log("VISIBLE:", visibleMessages.value);

    },
    { threshold: 0.1 }
  );

  // Observe all current messages
  document.querySelectorAll("[id^='message-']").forEach((el) => {
    visibilityObserver.observe(el);
  });

  // Watch for newly added messages (pagination or new messages)
  if (!mutationObserver) {
    const container = document.querySelector(".messages-container");
    if (!container) return;

    mutationObserver = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === 1 && node.id?.startsWith("message-")) {
            visibilityObserver.observe(node);
          }
        });
      });
    });

    mutationObserver.observe(container, { childList: true, subtree: true });
  }
}

let visibleMessagesInterval = null;

// Fetch and update messages that are currently visible
const fetchVisibleMessages = async () => {
  if (!visibleMessages.value.length) return;

  try {
    const ids = visibleMessages.value.join(',');
    const response = await api.get(`chat/messages/get_bulk/?id=${ids}`);
    const fetchedMessages = response.data; // assume array of message objects

    // Update messages in place
    fetchedMessages.forEach(fetchedMsg => {
      const index = messages.value.findIndex(m => m.id === fetchedMsg.id);
      if (index !== -1) {
        messages.value[index] = { ...messages.value[index], ...fetchedMsg };
      }
    });
  } catch (error) {
    console.error('Error fetching visible messages:', error);
  }
};

// Start polling
const startVisibleMessagesPolling = () => {
  if (visibleMessagesInterval) clearInterval(visibleMessagesInterval);
  visibleMessagesInterval = setInterval(fetchVisibleMessages, 3000);
};

// Stop polling
const stopVisibleMessagesPolling = () => {
  if (visibleMessagesInterval) clearInterval(visibleMessagesInterval);
};
let newMessagesInterval = null;

// Handle scroll events to track if user is at bottom
const handleScroll = () => {
  if (!messagesContainer.value) return;
  
  const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value;
  const isBottom = scrollHeight - (scrollTop + clientHeight) < 100; // 100px threshold
  
  isAtBottom.value = isBottom;
  if (isBottom) {
    showNewMessagesIndicator.value = false;
    setTimeout(() => {
      showNewMessageDivider.value = false;
    }, 3000);
    newMessagesCount.value = 0;
  }
};

// Fetch new messages since the latest one we have
const fetchNewMessages = async () => {
  if (!messages.value.length) return;

  const latestId = messages.value[messages.value.length - 1].id;
  try {
    const response = await api.get(
      `chat/conversations/${route.params.id}/new_messages/?after_id=${latestId}`
    );
    const newMsgs = response.data.results;

    if (newMsgs.length) {
      const prevLength = messages.value.length;
      messages.value = [...messages.value, ...newMsgs];
      
      // Only update the firstNewMessageIndex if we don't have one yet or if user has scrolled to view previous new messages
      if (firstNewMessageIndex.value === -1 || isAtBottom.value) {
        firstNewMessageIndex.value = prevLength;
        showNewMessageDivider.value = true;
      } else {
        // Keep the existing firstNewMessageIndex but ensure the divider is shown
        showNewMessageDivider.value = true;
      }

      if(hasSentNewMessage.value && newMsgs.some(msg => msg.user.id === currentUser.value.id)){
        hasSentNewMessage.value = false;
        nextTick(() => {
          scrollToBottom();
        });
        showNewMessageDivider.value = false;
      } else if (!isAtBottom.value) {
        showNewMessagesIndicator.value = true;
        newMessagesCount.value += newMsgs.length;
      } else {
        // If at bottom, auto-scroll to show new messages
        scrollToNewMessages();
      }
    }
  } catch (error) {
    console.error("Error fetching new messages:", error);
  }
};

// Start polling for new messages every second
const startNewMessagesPolling = () => {
  if (newMessagesInterval) clearInterval(newMessagesInterval);
  newMessagesInterval = setInterval(fetchNewMessages, 1000);
};

// Stop polling
const stopNewMessagesPolling = () => {
  if (newMessagesInterval) clearInterval(newMessagesInterval);
};

onMounted(async () => {
  await fetchConversation();
  scrollToBottom();
  observeMessageVisibility();
  startVisibleMessagesPolling();
  startNewMessagesPolling();
  
  // Add scroll event listener
  if (messagesContainer.value) {
    messagesContainer.value.addEventListener('scroll', handleScroll);
  }
});

// Stop on unmount
onUnmounted(() => {
  stopVisibleMessagesPolling();
  stopNewMessagesPolling();
  
  // Remove scroll event listener
  if (messagesContainer.value) {
    messagesContainer.value.removeEventListener('scroll', handleScroll);
  }
});
</script>
