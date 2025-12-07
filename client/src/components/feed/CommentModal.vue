<template>
  <TransitionRoot appear :show="show" as="template">
    <Dialog as="div" class="relative z-50" @close="closeModal">
      <TransitionChild
        as="template"
        enter="ease-out duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/25" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-4 text-left align-middle shadow-xl transition-all">
              <!-- Header -->
              <div class="bg-white px-4 py-3 sm:p-6 sm:py-3 border-b border-gray-200">
                <div class="flex justify-between items-center">
                  <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                    Comments
                  </DialogTitle>
                  <button @click="closeModal" class="text-gray-400 hover:text-gray-500 focus:outline-none cursor-pointer">
                    <span class="sr-only">Close</span>
                    <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>

              <!-- Post Content -->
              <div class="px-4 py-3 border-b border-gray-200">
                <div class="flex justify-between items-start">
                  <div class="flex space-x-3 flex-1">
                    <div v-if="post.posted_by?.profile_picture" class="flex-shrink-0 h-10 w-10 rounded-full overflow-hidden">
                      <img 
                        :src="post.posted_by.profile_picture" 
                        :alt="post.posted_by.name"
                        class="h-full w-full object-cover"
                      />
                    </div>
                    <div v-else class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-sm text-gray-600">
                      {{ post.posted_by?.name ? post.posted_by.name.charAt(0).toUpperCase() : 'U' }}
                    </div>
                    <div class="flex-1">
                      <p class="font-medium text-sm">{{ post.posted_by?.name || 'Anonymous' }}</p>
                      <ShowMore :text="post.description"/>
                      <p class="text-xs text-gray-400 mt-1">{{ post.formatted_created_at }}</p>
                    </div>
                  </div>
                  <!-- Three dots menu -->
                  <div class="relative">
                    <button 
                      @click.stop="showReportMenu = !showReportMenu" 
                      class="p-1 rounded-full hover:bg-gray-100 focus:outline-none"
                    >
                      <EllipsisVertical class="h-5 w-5 text-gray-500" />
                    </button>
                    
                    <!-- Dropdown menu -->
                    <div 
                      v-if="showReportMenu" 
                      class="absolute right-0 mt-1 w-48 bg-white rounded-md shadow-lg py-1 z-50"
                      v-click-outside="() => showReportMenu = false"
                    >
                      <button 
                        @click="handleReportPost"
                        class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
                      >
                        Report Post
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Post Actions -->
                <div class="flex justify-between items-center mt-3 pt-2 border-t border-gray-100">
                  <button 
                    @click.stop="handleLike"
                    class="flex items-center space-x-1 text-sm text-gray-500 hover:text-red-500 transition-colors"
                    :class="{ 'text-red-500': post.liked }"
                  >
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      class="h-5 w-5" 
                      :fill="post.liked ? 'currentColor' : 'none'" 
                      viewBox="0 0 24 24" 
                      stroke="currentColor"
                    >
                      <path 
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2" 
                        d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" 
                      />
                    </svg>
                    <span>{{ post.likes || 0 }}</span>
                  </button>
                  
                  <button 
                    @click.stop="handleSave"
                    class="flex items-center space-x-1 text-sm text-gray-500 hover:text-yellow-500 transition-colors"
                    :class="{ 'text-yellow-500': post.saved }"
                  >
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      class="h-5 w-5" 
                      :fill="post.saved ? 'currentColor' : 'none'" 
                      viewBox="0 0 24 24" 
                      stroke="currentColor"
                    >
                      <path 
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2" 
                        d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" 
                      />
                    </svg>
                    <span>Save</span>
                  </button>
                  
                  <button 
                    @click.stop="handleShare"
                    class="flex items-center space-x-1 text-sm text-gray-500 hover:text-blue-500 transition-colors"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                    </svg>
                    <span>Share</span>
                  </button>
                </div>
              </div>

              <!-- Comments Section -->
              <div class="h-[50vh] overflow-y-auto px-4 py-3">
                <div v-if="loading" class="flex justify-center py-8">
                  <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-500"></div>
                </div>
                
                <div v-else-if="comments.length === 0" class="text-center py-12 text-gray-500">
                  No comments yet. Be the first to comment!
                </div>
                
                <div v-else class="space-y-4">
                  <CommentItem 
                    v-for="comment in comments" 
                    :key="comment.id" 
                    :comment="comment"
                    :show-replies="showReplies[comment.id] || false"
                    :loading-replies="loadingReplies[comment.id] || false"
                    :replies="commentReplies[comment.id] || []"
                    @like="handleCommentLike"
                    @reply="handleReply"
                    @toggle-replies="toggleReplies"
                    @reply-added="handleReplyAdded(comment.id, $event)"
                  />
                </div>
              </div>

              <!-- Comment Input -->
              <div v-if="!post.archived" class="bg-gray-50 px-4 py-3 border-t border-gray-200">
                <div class="flex items-center space-x-2">
                  <div v-if="profilePicture" class="h-8 w-8 rounded-full overflow-hidden bg-indigo-100">
                    <img :src="profilePicture" alt="Profile" class="h-full w-full object-cover" />
                  </div>
                  <div v-else class="flex-shrink-0 h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center text-xs text-gray-600">
                    {{ userInitials }}
                  </div>
                  <div class="flex-1 relative">
                    <input
                      v-model="newComment"
                      type="text"
                      placeholder="Write a comment..."
                      class="block w-full rounded-full border-gray-300 pl-4 pr-10 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
                      @keyup.enter="addComment"
                    />
                    <button 
                      @click="addComment"
                      :disabled="!newComment.trim()"
                      class="absolute right-2 top-1/2 transform -translate-y-1/2 text-indigo-600 hover:text-indigo-800 disabled:opacity-50"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clip-rule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
      
      <!-- Report Modal -->
      <ReportModal
        v-if="isReportModalOpen"
        :is-open="isReportModalOpen"
        :is-submitting="isSubmittingReport"
        @close="isReportModalOpen = false"
        @submit="submitReport"
      />
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, watch, computed, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { useUserStore } from '@/stores/user';
import { useRouter, useRoute } from 'vue-router';
import { message } from 'ant-design-vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import ShowMore from '@/components/ShowMore.vue';
import CommentItem from './CommentItem.vue';
import ReportModal from './ReportModal.vue';
import { EllipsisVertical } from 'lucide-vue-next';
import { usePostStore } from '@/stores/post';
import { useCommentStore } from '@/stores/comment';
// Click outside directive
const vClickOutside = {
  beforeMount(el, binding) {
    el.clickOutsideEvent = function(event) {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value();
      }
    };
    document.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent);
  },
};

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  post: {
    type: Object,
    required: true,
    default: () => ({
      id: null,
      posted_by: {},
      description: '',
      formatted_created_at: ''
    })
  }
});

const emit = defineEmits([
  'close',
  'update:post',
  'comment-added',
  'like',
  'save',
  'share'
]);

const router = useRouter();
const route = useRoute();
const postStore = usePostStore();
const commentStore = useCommentStore();
// Handle browser back button
const handlePopState = () => {
  if (props.show) {
    closeModal();
  }
};

// Setup popstate listener when component mounts
onMounted(() => {
  window.addEventListener('popstate', handlePopState);
});

// Cleanup popstate listener when component unmounts
onBeforeUnmount(() => {
  window.removeEventListener('popstate', handlePopState);
});

const closeModal = () => {
  // Remove the post ID from URL when closing
  if (route.query.p) {
    const query = { ...route.query };
    delete query.p;
    router.replace({ query });
  }
  
  emit('close');
};

const handleLike = () => {
  emit('like')
}

const handleSave = () => {
  emit('save')
};

const handleShare = async () => {
  emit('share')
};

const isReportModalOpen = ref(false);
const isSubmittingReport = ref(false);

const handleReportPost = () => {
  showReportMenu.value = false;
  isReportModalOpen.value = true;
};

const submitReport = async (reason) => {
  isSubmittingReport.value = true;
  
  try {
    const response = await postStore.submitReport(props.post.id, reason);
    
    if (response.data.error) {
      message.error(response.data.error);
    } else {
      message.success('Post reported successfully');
    }
  } catch (error) {
    console.error('Error reporting post:', error);
    const errorMessage = error.response?.data?.error || 'Failed to report post';
    message.error(errorMessage);
  } finally {
    isSubmittingReport.value = false;
    isReportModalOpen.value = false;
  }
};
const userStore = useUserStore();

const comments = ref([]);
const loading = ref(false);
const newComment = ref('');
const loadingReplies = ref({});
const showReplies = ref({});
const commentReplies = ref({});
const commentRefs = ref({});
const showReportMenu = ref(false);

// Scroll to a specific comment
const scrollToComment = (id) => {
  nextTick(() => {
    const el = commentRefs.value[id]?.$el || commentRefs.value[id];
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      el.classList.add('highlight-new');
      setTimeout(() => {
        el.classList.remove('highlight-new');
      }, 1500);
    }
  });
};

const userInitials = computed(() => {
  if (!userStore.user?.name) return 'U';
  return userStore.user.name
    .split(' ')
    .map(n => n[0].toUpperCase())
    .join('')
    .substring(0, 2);
});

const profilePicture = computed(() => {
  return userStore.user?.profile_picture;
});

const fetchComments = async () => {
  if (!props.post.id) return;
  
  try {
    loading.value = true;
    const response = await postStore.fetchComments(props.post.id);
    comments.value = response.data.results || [];
  } catch (error) {
    console.error('Error fetching comments:', error);
    message.error('Failed to load comments');
  } finally {
    loading.value = false;
  }
};

const handleCommentLike = (updatedComment) => {
  // Update the comment in the comments list
  const index = comments.value.findIndex(c => c.id === updatedComment.id);
  if (index !== -1) {
    comments.value[index] = { ...comments.value[index], ...updatedComment };
  }
  
  // If this is a reply, update it in the replies list
  for (const commentId in commentReplies.value) {
    const replyIndex = commentReplies.value[commentId].findIndex(r => r.id === updatedComment.id);
    if (replyIndex !== -1) {
      commentReplies.value[commentId][replyIndex] = updatedComment;
      break;
    }
  }
};

const handleReply = (commentId) => {
  // This is handled within the CommentItem component now
};

const handleReplyAdded = (top_id, data) => {
  if (!top_id) return; // safety check

  const is_nested = data['is_reply'];
  const newObj = data['data']['comment'];
  const post_comments_count = data['data']['post_comments'];

  // Ensure outer object exists
  commentReplies.value ??= {};

  // Ensure replies array exists for this comment (use shallow clone for reactivity)
  if (!Array.isArray(commentReplies.value[top_id])) {
    commentReplies.value = { ...commentReplies.value, [top_id]: [] };
  }

  if (is_nested) {
    // Insert nested reply after parent
    const insertIndex = data['index'] + 1;
    commentReplies.value[top_id].splice(insertIndex, 0, newObj);
  } else {
    // Add new top-level reply at the front
    commentReplies.value[top_id].unshift(newObj);
  }

  // Update replies count in parent comment
  const comment = comments.value.find(c => c.id === top_id);
  if (comment) {
    comment.replies = (comment.replies || 0) + 1;
  }

  // Show replies section
  showReplies.value[top_id] = true;

  // Update post's total comment count
  emit('update:post', {
    ...props.post,
    comments: post_comments_count
  });
};

const addComment = async () => {
  if (!newComment.value.trim()) return;
  
  try {
    const response = await postStore.submitComment(props.post.id, newComment.value.trim());
    const post_comments_count = response.data.post_comments;
    const new_comment_obj = response.data.comment;
    
    // Add the new comment to the beginning of the list
    comments.value = [new_comment_obj, ...comments.value];
    newComment.value = '';
    
    // Scroll to the new comment after it's added
    nextTick(() => {
      scrollToComment(new_comment_obj.id);
    });
    
    emit('update:post', {
      ...props.post,
      comments: post_comments_count
    });
  } catch (error) {
    console.error('Error adding comment:', error);
    message.error('Failed to add comment');
  }
};

const toggleReplies = async (comment) => {
  showReplies.value[comment.id] = !showReplies.value[comment.id];
  
  // If we're showing replies and haven't loaded them yet, fetch them
  if (showReplies.value[comment.id] && !commentReplies.value[comment.id]) {
    await fetchReplies(comment.id);
  }
};

const fetchReplies = async (commentId) => {
  try {
    loadingReplies.value[commentId] = true;
    const response = await commentStore.getReplies(commentId);
    commentReplies.value[commentId] = response.data.results || [];
  } catch (error) {
    console.error('Error fetching replies:', error);
    message.error('Failed to load replies');
  } finally {
    loadingReplies.value[commentId] = false;
  }
};

// Handle URL and fetch comments when modal is opened/closed
watch(() => props.show, (newVal) => {
  if (newVal) {
    // Add post ID to URL when modal opens
    if (props.post?.id && route.query.p !== String(props.post.id)) {
      router.replace({
        query: { ...route.query, p: props.post.id }
      });
    }
    fetchComments();
  } else if (route.query.p) {
    // Remove post ID from URL when modal closes
    const query = { ...route.query };
    delete query.p;
    router.replace({ query });
  }
}, { immediate: true });
</script>

<style scoped>
/* Animation for comments list */
.comment-list-move,
.comment-list-enter-active,
.comment-list-leave-active {
  transition: all 0.3s ease;
}

.comment-list-enter-from,
.comment-list-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

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

/* Smooth transition for the comment input */
.comment-input-enter-active,
.comment-input-leave-active {
  transition: all 0.3s ease;
  max-height: 100px;
  overflow: hidden;
}

.comment-input-enter-from,
.comment-input-leave-to {
  opacity: 0;
  max-height: 0;
  margin: 0;
  padding: 0;
}
</style>
