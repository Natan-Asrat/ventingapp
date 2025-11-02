<template>
  <div class="space-y-2">
    <div class="flex space-x-3 comment-item">
      <div v-if="comment.commented_by?.profile_picture" class="flex-shrink-0 h-8 w-8 rounded-full overflow-hidden">
        <img 
          :src="comment.commented_by.profile_picture" 
          :alt="comment.commented_by.name"
          class="h-full w-full object-cover"
        />
      </div>
      <div v-else class="flex-shrink-0 h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center text-xs text-gray-600">
        {{ comment.commented_by?.name ? comment.commented_by.name.charAt(0).toUpperCase() : 'U' }}
      </div>
      <div class="flex-1 min-w-0">
        <div class="bg-gray-100 rounded-lg px-3 py-2">
          <p class="text-sm font-medium">{{ comment.commented_by?.name || 'Anonymous' }}</p>
          <div class="flex items-start gap-2">
            <div class="flex-1">
              <span class="text-sm text-blue-500 mr-1" v-if="comment.reply_to_username">@{{ comment.reply_to_username }}</span>
              <span class="text-sm">{{ comment.message }}</span>
            </div>
            <button 
              @click="toggleLike"
              class="flex items-center space-x-1 text-xs text-gray-500 hover:text-red-500 cursor-pointer"
              :class="{ 'text-red-500': comment.liked }"
            >
              <Heart 
                :size="14" 
                :fill="comment.liked ? 'currentColor' : 'none'" 
                :stroke-width="comment.liked ? 0 : 2"
                class="w-4 h-4"
              />
              <span>{{ formatNumber(comment.likes || 0) }}</span>
            </button>
          </div>
          <div class="flex items-center mt-1 space-x-4">
            <p class="text-xs text-gray-400">{{ comment.formatted_created_at }}</p>
            <button 
              @click="toggleReplyInput" 
              class="text-xs text-gray-500 hover:text-gray-700 cursor-pointer"
            >
              Reply
            </button>
          </div>
        </div>
        
        <!-- View replies button (only for parent comments) -->
        <button 
          v-if="!isReply && comment.replies > 0"
          @click="$emit('toggle-replies', comment)"
          class="flex items-center space-x-1 text-xs text-gray-500 hover:text-blue-500 mt-1 ml-11 cursor-pointer"
        >
          <span>{{ showReplies ? 'Hide' : 'View' }} {{ comment.replies }} {{ comment.replies === 1 ? 'reply' : 'replies' }}</span>
          <ChevronDown v-if="!showReplies" :size="14" class="w-4 h-4" />
          <ChevronUp v-else :size="14" class="w-4 h-4" />
        </button>
        
        <!-- Reply input -->
        <div v-if="isReplying" class="mt-2 ml-11">
          <div class="flex items-center space-x-2">
            <input
              ref="replyInput"
              v-model="replyContent"
              type="text"
              placeholder="Write a reply..."
              class="flex-1 text-sm border border-gray-300 rounded-full px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
              @keyup.enter="submitReply"
              @keyup.esc="cancelReply"
            />
            <button 
              @click="submitReply"
              :disabled="!replyContent.trim()"
              class="text-blue-500 hover:text-blue-700 disabled:opacity-50 cursor-pointer"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
            <button 
              @click="cancelReply"
              class="text-gray-500 hover:text-gray-700 cursor-pointer"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Replies section -->
        <div v-if="showReplies && !isReply" class="mt-2 space-y-2">
          <!-- Loading indicator -->
          <div v-if="loadingReplies" class="flex justify-center py-2">
            <Loader2 class="h-4 w-4 animate-spin text-blue-500" />
          </div>
          
          <!-- Replies list with transition group -->
          <TransitionGroup 
            name="comment-list" 
            tag="div" 
            class="space-y-2"
          >
            <CommentItem 
              v-for="(reply, i) in replies" 
              :key="reply.id"
              :ref="el => { if (el) replyRefs[reply.id] = el }"
              :comment="reply"
              :is-reply="true"
              :index="i"
              @like="$emit('like', $event)"
              @reply="handleReply"
              @reply-added="handleAddReply"
              class="comment-item"
            />
          </TransitionGroup>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted } from 'vue';
import { ChevronDown, ChevronUp, Heart, Loader2 } from 'lucide-vue-next';
import api from '@/api/axios';
import { message } from 'ant-design-vue';

const props = defineProps({
  comment: {
    type: Object,
    required: true
  },
  isReply: {
    type: Boolean,
    default: false
  },
  showReplies: {
    type: Boolean,
    default: false
  },
  loadingReplies: {
    type: Boolean,
    default: false
  },
  replies: {
    type: Array,
    default: () => []
  },
  index: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['like', 'reply', 'toggle-replies', 'reply-added']);

const isReplying = ref(false);
const replyContent = ref('');
const replyInput = ref(null);
const replyRefs = ref({});

// Add a method to scroll to a specific reply
const scrollToReply = (id) => {
  nextTick(() => {
    const el = replyRefs.value[id]?.$el || replyRefs.value[id];
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      el.classList.add('highlight-new');
      setTimeout(() => {
        el.classList.remove('highlight-new');
      }, 1500);
    }
  });
};

const handleAddReply = (new_data) => {
  // If this is a new reply to the current comment, scroll to it
  if (!new_data.is_reply && new_data.data?.comment?.id) {
    nextTick(() => {
      scrollToReply(new_data.data.comment.id);
    });
  }
  emit('reply-added', new_data);
}
const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k';
  }
  return num.toString();
};

const toggleLike = async () => {
  try {
    const endpoint = props.comment.liked 
      ? `/post/comments/${props.comment.id}/unlike_comment/`
      : `/post/comments/${props.comment.id}/like_comment/`;
    
    const response = await api.post(endpoint);
    
    // Update the comment with the server's response
    emit('like', {
      ...props.comment,
      liked: !props.comment.liked,
      likes: response.data.likes
    });
  } catch (error) {
    console.error('Error toggling like:', error);
    message.error('Failed to update like status');
  }
};

const toggleReplyInput = async () => {
  isReplying.value = !isReplying.value;
  if (isReplying.value) {
    await nextTick();
    if (replyInput.value) {
      replyInput.value.focus();
    }
  } else {
    replyContent.value = '';
  }
};

const cancelReply = () => {
  isReplying.value = false;
  replyContent.value = '';
};

const handleReply = (commentId) => {
  emit('reply', commentId);
};

const submitReply = async () => {
  if (!replyContent.value.trim()) return;
  
  try {
    const response = await api.post(`/post/comments/${props.comment.id}/reply/`, {
      message: replyContent.value.trim()
    });
    
    // Add the reply to the UI immediately
    const newReply = response.data;
    
    // If this is a reply to a top-level comment, add it to the replies list
    emit('reply-added', {is_reply: props.isReply, index: props.index, data: newReply});
    
    // Reset the reply input
    replyContent.value = '';
    isReplying.value = false;
    
    // Show success message
    message.success('Reply added successfully');
  } catch (error) {
    console.error('Error adding reply:', error);
    message.error(error.response?.data?.message || 'Failed to add reply');
  }
};

</script>

<style scoped>
/* Animation for new comments */
.comment-list-move, /* apply transition to moving elements */
.comment-list-enter-active,
.comment-list-leave-active {
  transition: all 0.3s ease;
}

/* Starting state for entering elements */
.comment-list-enter-from,
.comment-list-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

/* Ensure leaving elements are taken out of layout flow so that moving
   animations can be calculated correctly. */
.comment-list-leave-active {
  position: absolute;
  width: 100%;
}

/* Highlight animation for new comments */
@keyframes highlight {
  0% { background-color: rgba(239, 246, 255, 0.5); }
  100% { background-color: transparent; }
}

.highlight-new {
  animation: highlight 1.5s ease-out;
  border-radius: 0.5rem;
}

/* Smooth transition for the reply input */
.reply-enter-active,
.reply-leave-active {
  transition: all 0.3s ease;
  max-height: 100px;
  overflow: hidden;
}

.reply-enter-from,
.reply-leave-to {
  opacity: 0;
  max-height: 0;
  margin-top: 0;
  margin-bottom: 0;
  padding-top: 0;
  padding-bottom: 0;
}
</style>
