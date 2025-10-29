<template>
  <div class="bg-white shadow overflow-hidden rounded-lg">
    <!-- Comment Modal -->
    <CommentModal 
      v-model="showCommentModal"
      :post="post"
      :show="showCommentModal"
      @close="closeCommentModal"
      @comment-added="handleCommentAdded"
    />
    <!-- Post Header -->
    <div class="px-4 py-3 flex items-center justify-between border-b border-gray-200">
      <div class="flex items-center space-x-3">
        <div v-if="post.posted_by?.profile_picture" class="h-10 w-10 rounded-full overflow-hidden">
          <img 
            :src="post.posted_by.profile_picture" 
            :alt="post.posted_by.name"
            class="h-full w-full object-cover"
          />
        </div>
        <div v-else class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-600 font-medium">
          {{ post.posted_by?.name ? post.posted_by.name.charAt(0).toUpperCase() : 'U' }}
        </div>
        <div>
          <p class="font-medium text-sm">{{ post.posted_by?.name || 'Anonymous' }}</p>
          <p class="text-xs text-gray-500">@{{ post.posted_by?.username || 'user' }}</p>
        </div>
      </div>
      
      <div class="flex items-center space-x-2">
        <button 
          v-if="post.payment_info_list && post.payment_info_list.length > 0"
          @click="$emit('donate', post)"
          class="px-3 py-1 bg-indigo-100 text-indigo-700 text-sm font-medium rounded-full hover:bg-indigo-200 transition-colors flex items-center"
        >
          Donate
        </button>
        <div class="relative">
          <button 
            @click="handleFollowClick"
            class="p-1.5 rounded-full transition-colors flex items-center justify-center"
            :class="{
              'bg-green-100 text-green-700 hover:bg-green-200': post.connected,
              'bg-yellow-100 text-yellow-700': post.pending_connection && !post.rejected_connection,
              'bg-red-100 text-red-700': post.rejected_connection,
              'bg-gray-100 text-gray-700 hover:bg-gray-200': !post.connected && !post.pending_connection && !post.rejected_connection && !post.removed_connection,
              'bg-blue-50 text-blue-700 hover:bg-blue-100': post.removed_connection && !post.pending_connection && !post.rejected_connection,
              'cursor-not-allowed': post.pending_connection || post.rejected_connection
            }"
            :disabled="post.pending_connection || post.rejected_connection"
            :title="getFollowButtonTooltip(post)"
          >
            <template v-if="post.connected">
              <UserCheck :size="18" class="text-green-600" />
              <span class="absolute -top-1 -right-1 h-2 w-2 rounded-full bg-green-500 border-2 border-white"></span>
            </template>
            <template v-else-if="post.pending_connection">
              <Clock :size="18" class="text-yellow-600" />
              <span class="absolute -top-1 -right-1 h-2 w-2 rounded-full bg-yellow-500 border-2 border-white"></span>
            </template>
            <template v-else-if="post.rejected_connection">
              <UserX :size="18" class="text-red-600" />
              <span class="absolute -top-1 -right-1 h-2 w-2 rounded-full bg-red-500 border-2 border-white"></span>
            </template>
            <template v-else-if="post.removed_connection">
              <UserPlus :size="18" class="text-blue-600" />
              <span class="absolute -top-1 -right-1 h-2 w-2 rounded-full bg-blue-500 border-2 border-white"></span>
            </template>
            <UserPlus v-else :size="18" class="text-gray-600" />
          </button>
        </div>
      </div>
    </div>
    
    <!-- Post Content -->
    <div class="px-4 py-3">
      <p class="text-gray-800 whitespace-pre-line">{{ post.description }}</p>
      
      <!-- Post Image -->
      <div v-if="post.image" class="mt-3 rounded-lg overflow-hidden">
        <img 
          :src="post.image" 
          :alt="'Post by ' + (post.posted_by?.username || 'user')" 
          class="w-full h-auto object-cover cursor-zoom-in"
          @load="$emit('image-loaded')"
          @click="openImageViewer"
        />
      </div>
      
      <!-- Image Viewer -->
      <ImageViewer
        v-if="showImageViewer"
        v-model="showImageViewer"
        :src="post.image"
        :alt="'Post by ' + (post.posted_by?.username || 'user')"
        @close="showImageViewer = false"
      />
      
      <!-- Post Stats -->
      <div class="mt-3 flex items-center text-sm text-gray-500 space-x-4">
        <span>{{ post.likes }} {{ post.likes === 1 ? 'like' : 'likes' }}</span>
        <span>{{ post.comments }} {{ post.comments === 1 ? 'comment' : 'comments' }}</span>
        <span>{{ post.views }} {{ post.views === 1 ? 'view' : 'views' }}</span>
        <span class="text-xs text-gray-400">{{ post.formatted_created_at }}</span>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="px-4 py-2 border-t border-gray-100">
      <div class="flex items-center justify-between">
        <button 
          @click="likePost" 
          class="p-2 rounded-full hover:bg-gray-100 transition-colors relative"
          :class="[{
            'text-red-500 hover:text-red-600': post.liked && !liking,
            'text-gray-500 hover:text-gray-700': !post.liked && !liking,
            'opacity-50 cursor-not-allowed': liking
          }]"
          :disabled="liking"
          title="Like"
        >
          <template v-if="liking">
            <Loader2 class="w-5 h-5 animate-spin" />
          </template>
          <template v-else>
            <Heart 
              :size="20" 
              :fill="post.liked ? 'currentColor' : 'none'" 
              :stroke-width="post.liked ? 0 : 2"
              class="w-5 h-5"
            />
          </template>
        </button>
        
        <button 
          @click="handleCommentClick(post)" 
          class="p-2 rounded-full hover:bg-gray-100 text-gray-700 hover:text-blue-500 transition-colors"
          title="Comment"
        >
          <MessageCircle :size="20" class="w-5 h-5" />
        </button>
        
        <button 
          @click="savePost" 
          class="p-2 rounded-full hover:bg-gray-100 transition-colors relative"
          :class="[{
            'text-yellow-500 hover:text-yellow-600': post.saved && !saving,
            'text-gray-500 hover:text-gray-700': !post.saved && !saving,
            'opacity-50 cursor-not-allowed': saving
          }]"
          :disabled="saving"
          title="Save"
        >
          <template v-if="saving">
            <Loader2 class="w-5 h-5 animate-spin" />
          </template>
          <template v-else>
            <Bookmark 
              :size="20" 
              :fill="post.saved ? 'currentColor' : 'none'" 
              :stroke-width="post.saved ? 0 : 2"
              class="w-5 h-5"
            />
          </template>
        </button>
        
        <button 
          @click="$emit('share', post)" 
          class="p-2 rounded-full hover:bg-gray-100 text-gray-700 hover:text-green-500 transition-colors"
          title="Share"
        >
          <Share2 :size="20" class="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import CommentModal from './CommentModal.vue';
import ImageViewer from '@/components/common/ImageViewer.vue';
import { Heart, MessageCircle, Bookmark, Share2, Loader2, UserPlus, UserCheck, Clock, UserX, UserMinus } from 'lucide-vue-next';

const getFollowButtonTooltip = (post) => {
  if (post.connected) return 'Connected';
  if (post.pending_connection) return 'Connection Pending';
  if (post.rejected_connection) return 'Connection Rejected';
  if (post.removed_connection) return 'Reconnect';
  return 'Follow User';
};

const handleFollowClick = () => {
  if (!props.post.pending_connection && !props.post.rejected_connection) {
    emit('follow', props.post);
  }
};

const props = defineProps({
  post: {
    type: Object,
    required: true
  },
  liking: {
    type: Boolean,
    default: false
  },
  saving: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['donate', 'image-loaded', 'comment', 'comment-added', 'save', 'share', 'like'])
const showCommentModal = ref(false);

const handleCommentClick = (post) => {
  showCommentModal.value = true;
  emit('comment', post);
};
const closeCommentModal = () => {
  showCommentModal.value = false;
}
const handleCommentAdded = () => {
  emit('comment-added');
};

const showImageViewer = ref(false);

const openImageViewer = (e) => {
  if (!props.post.image) return;
  showImageViewer.value = true;
};

const likePost = () => {
  emit('like', props.post);
};

const savePost = () => {
  emit('save', props.post);
};

</script>
