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
          <div class="flex space-x-3">
            <div v-if="post.posted_by?.profile_picture" class="flex-shrink-0 h-10 w-10 rounded-full overflow-hidden">
              <img 
                :src="post.posted_by.profile_picture" 
                :alt="post.posted_by.name"
                class="h-full w-full object-cover"
              />
            </div>
            <div v-else class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-600 font-medium">
              {{ post.posted_by?.name ? post.posted_by.name.charAt(0).toUpperCase() : 'U' }}
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-medium text-sm">{{ post.posted_by?.name || 'Anonymous' }}</p>
              <ShowMore :text="post.description"/>
              <p class="text-xs text-gray-400 mt-1">{{ post.formatted_created_at }}</p>
              
              
            </div>
          </div>
          <!-- Action Buttons -->
              <div class="flex items-center justify-between space-x-4 mt-2 pt-2 border-t border-gray-100">
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
            <div v-for="comment in comments" :key="comment.id" class="flex space-x-3">
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
              <div class="bg-gray-100 rounded-lg px-3 py-2">
                <p class="text-sm font-medium">{{ comment.commented_by?.name || 'Anonymous' }}</p>
                <p class="text-sm">{{ comment.message }}</p>
                <p class="text-xs text-gray-400 mt-1">{{ comment.formatted_created_at }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Comment Input -->
        <div class="bg-gray-50 px-4 py-3 border-t border-gray-200">
          <div class="flex items-center space-x-2">
            <div class="flex-shrink-0 h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center text-xs text-gray-600">
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
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, watch, computed, onMounted, onBeforeUnmount } from 'vue';
import { useUserStore } from '@/stores/user';
import { useRouter, useRoute } from 'vue-router';
import api from '@/api/axios';
import { message } from 'ant-design-vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import ShowMore from '@/components/ShowMore.vue';

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
  'comment-added',
  'like',
  'unlike',
  'save',
  'unsave',
  'share'
]);

const router = useRouter();
const route = useRoute();

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
  if (props.post.liked) {
    emit('unlike', props.post.id);
  } else {
    emit('like', props.post.id);
  }
};

const handleSave = () => {
  if (props.post.saved) {
    emit('unsave', props.post.id);
  } else {
    emit('save', props.post.id);
  }
};

const handleShare = async () => {
  try {
    const shareData = {
      title: 'Check out this post',
      text: props.post.description,
      url: window.location.href,
    };
    
    if (navigator.share) {
      await navigator.share(shareData);
    } else {
      // Fallback for browsers that don't support Web Share API
      await navigator.clipboard.writeText(window.location.href);
      message.success('Link copied to clipboard!');
    }
    
    emit('share', props.post.id);
  } catch (error) {
    if (error.name !== 'AbortError') {
      console.error('Error sharing:', error);
      message.error('Failed to share post');
    }
  }
};
const userStore = useUserStore();

const comments = ref([]);
const loading = ref(false);
const newComment = ref('');

const userInitials = computed(() => {
  if (!userStore.user?.name) return 'U';
  return userStore.user.name
    .split(' ')
    .map(n => n[0].toUpperCase())
    .join('')
    .substring(0, 2);
});

const fetchComments = async () => {
  if (!props.post.id) return;
  
  try {
    loading.value = true;
    const response = await api.get(`/post/posts/${props.post.id}/comments/`);
    comments.value = response.data.results || [];
  } catch (error) {
    console.error('Error fetching comments:', error);
    message.error('Failed to load comments');
  } finally {
    loading.value = false;
  }
};

const addComment = async () => {
  if (!newComment.value.trim()) return;
  
  try {
    const response = await api.post(`/post/posts/${props.post.id}/comment/`, {
      message: newComment.value.trim()
    });
    
    comments.value = [response.data, ...comments.value];
    newComment.value = '';
    emit('comment-added');
  } catch (error) {
    console.error('Error adding comment:', error);
    message.error('Failed to add comment');
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
