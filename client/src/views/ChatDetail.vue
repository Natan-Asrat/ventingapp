<template>
  <div class="max-w-4xl mx-auto h-screen flex flex-col">
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
      <div 
        v-for="message in messages" 
        :key="message.id"
        :id="`message-${message.id}`"
        :class="[
          'flex', 
          message.user.id === currentUser.id ? 'justify-end' : 'justify-start',
          { 'bg-blue-50 rounded-lg transition-colors duration-1000': highlightedMessageId === message.id }
        ]"
      >
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
import { ref, onMounted, computed, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { X, Reply, Smile, EllipsisVertical, Send } from 'lucide-vue-next';
import api from '@/api/axios';

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
const emojiPickerForMessage = ref(null);
const showActions = ref(null);
const emojiPickerPosition = ref({ x: 0, y: 0 });
let highlightTimeout = null;
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
const fetchMessages = async () => {
  try {
    const response = await api.get(`chat/conversations/${route.params.id}/messages/`);
    // Reverse the array to show newest messages at the bottom
    messages.value = response.data.reverse();
  } catch (error) {
    console.error('Error fetching messages:', error);
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
    await fetchMessages();
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

// Scroll to bottom of messages
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
};

// Get other user in conversation
const otherUser = computed(() => {
  if (!conversation.value.members) return null;
  return conversation.value.members.find(
    member => member.user.id !== currentUser.value.id
  )?.user;
});

onMounted(async () => {
  await fetchConversation();
  scrollToBottom();
  // Set up polling for new messages (every 5 seconds)
  const pollInterval = setInterval(fetchMessages, 5000);
  
  // Clean up interval on component unmount
  return () => clearInterval(pollInterval);
});
</script>
