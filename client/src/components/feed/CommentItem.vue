<template>
  <div class="space-y-3">
    <div class="flex space-x-3 comment-item">
      <!-- Avatar -->
      <div v-if="comment.commented_by?.profile_picture" class="flex-shrink-0 h-9 w-9 rounded-full overflow-hidden ring-2 ring-white shadow-sm">
        <img 
          :src="comment.commented_by.profile_picture" 
          :alt="comment.commented_by.name"
          class="h-full w-full object-cover"
        />
      </div>
      <div v-else class="flex-shrink-0 h-9 w-9 rounded-full bg-zinc-100 flex items-center justify-center text-xs font-bold text-zinc-400 ring-2 ring-white shadow-sm">
        {{ comment.commented_by?.name ? comment.commented_by.name.charAt(0).toUpperCase() : 'U' }}
      </div>

      <div class="flex-1 min-w-0">
        <!-- Comment Bubble -->
        <div class="bg-zinc-50 rounded-2xl px-4 py-3 border border-zinc-100/50">
          <div class="flex items-center justify-between mb-1">
             <p class="text-sm font-bold text-zinc-900">{{ comment.commented_by?.name || 'Anonymous' }}</p>
             <p class="text-[10px] text-zinc-400 font-medium">{{ comment.formatted_created_at }}</p>
          </div>
          
          <div class="text-[15px] text-zinc-700 leading-relaxed break-words">
              <span class="font-medium text-violet-600 mr-1" v-if="comment.reply_to_username">@{{ comment.reply_to_username }}</span>
              {{ comment.message }}
          </div>
        </div>

        <!-- Actions Row -->
        <div class="flex items-center mt-1.5 space-x-4 pl-2">
            <!-- Like -->
            <button 
              @click="toggleLike"
              class="flex items-center space-x-1.5 text-xs font-medium transition-colors cursor-pointer group"
              :class="comment.liked ? 'text-rose-500' : 'text-zinc-500 hover:text-rose-500'"
            >
              <Heart 
                :size="14" 
                :fill="comment.liked ? 'currentColor' : 'none'" 
                :stroke-width="comment.liked ? 0 : 2"
                class="transition-transform group-active:scale-90"
              />
              <span v-if="comment.likes > 0">{{ formatNumber(comment.likes) }}</span>
              <span v-else>Like</span>
            </button>

            <!-- Reply -->
            <button 
              @click="toggleReplyInput" 
              class="text-xs font-medium text-zinc-500 hover:text-violet-600 transition-colors cursor-pointer"
            >
              Reply
            </button>
        </div>
        
        <!-- View replies button -->
        <button 
          v-if="!isReply && comment.replies > 0"
          @click="$emit('toggle-replies', comment)"
          class="flex items-center space-x-1.5 text-xs font-semibold text-violet-600 hover:text-violet-700 mt-2 pl-2 transition-colors cursor-pointer"
        >
          <div class="w-6 h-[1px] bg-violet-200"></div>
          <span>{{ showReplies ? 'Hide' : 'View' }} {{ comment.replies }} {{ comment.replies === 1 ? 'reply' : 'replies' }}</span>
        </button>
        
        <!-- Reply input -->
        <div v-if="isReplying" class="mt-3 pl-2">
          <div class="flex items-center space-x-2">
             <div class="relative flex-1">
                <input
                ref="replyInput"
                v-model="replyContent"
                type="text"
                maxlength="400"
                placeholder="Write a reply..."
                class="w-full text-sm border border-zinc-200 bg-zinc-50 rounded-full px-4 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 transition-all placeholder-zinc-400"
                @keyup.enter="submitReply"
                @keyup.esc="cancelReply"
                />
                 <button 
                  @click="submitReply"
                  :disabled="!replyContent.trim()"
                  class="absolute right-1.5 top-1/2 transform -translate-y-1/2 p-1 rounded-full text-violet-600 hover:bg-violet-50 disabled:opacity-40 disabled:hover:bg-transparent transition-all cursor-pointer"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
             </div>
             <button 
              @click="cancelReply"
              class="p-2 text-zinc-400 hover:text-zinc-600 rounded-full hover:bg-zinc-100 cursor-pointer transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Replies section -->
        <div v-if="showReplies && !isReply" class="mt-3 space-y-3 pl-4 border-l-2 border-zinc-100">
          <!-- Loading indicator -->
          <div v-if="loadingReplies" class="flex justify-center py-2">
            <Loader2 class="h-4 w-4 animate-spin text-violet-500" />
          </div>
          
          <!-- Replies list -->
          <TransitionGroup 
            name="comment-list" 
            tag="div" 
            class="space-y-3"
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
import { ref, nextTick } from 'vue';
import { ChevronDown, ChevronUp, Heart, Loader2 } from 'lucide-vue-next';
import { message } from 'ant-design-vue';
import { useCommentStore } from '@/stores/comment';
const commentStore = useCommentStore();

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
    const response = await commentStore.likeComment(
      props.comment.id,
      props.comment.liked
    )
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
    const response = await commentStore.replyComment(props.comment.id, replyContent.value.trim())
    
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
