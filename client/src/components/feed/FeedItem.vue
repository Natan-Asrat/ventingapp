<template>
  <div class="bg-white shadow overflow-hidden rounded-lg">
    <!-- Comment Modal -->
    <CommentModal 
      v-if="showCommentModal"
      :post="post"
      :show="showCommentModal"
      @like="likePost"
      @save="savePost"
      @share="handleShareClick(post)"
      @close="closeCommentModal"
      @update:post="$emit('update:post', $event)"
    />
    <ShareModal
      v-if="showShareModal"
      :post="post"
      :show="showShareModal"
      @close="closeShareModal"
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
      
      <div v-if="!isCurrentUserPost" class="flex items-center space-x-2">
        <button 
          @click="handleChat(post)"
          class="px-1 py-1 text-black text-sm font-medium rounded-full hover:bg-indigo-200 transition-colors flex items-center cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="processingChat"
        >
          <Loader2 v-if="processingChat" class="w-3 h-3 mr-1.5 animate-spin" />
          <Send v-else class="h-4 w-4"/>
        </button>
        <button 
          v-if="post.payment_info_list && post.payment_info_list.length > 0"
          @click="handleDonate(post)"
          class="px-3 py-1 bg-indigo-100 text-indigo-700 text-sm font-medium rounded-full hover:bg-indigo-200 transition-colors flex items-center cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="processingDonation"
        >
          <Loader2 v-if="processingDonation" class="w-3 h-3 mr-1.5 animate-spin" />
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
              'bg-gray-100 text-gray-700 hover:bg-gray-200': (!post.connected && !post.pending_connection && !post.rejected_connection) || post.removed_connection,
              'cursor-not-allowed': post.rejected_connection || post.banned_connection,
              'cursor-pointer': !post.rejected_connection && !post.banned_connection
            }"
            :disabled="post.rejected_connection || post.banned_connection"
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
            <template v-else-if="post.banned_connection">
              <UserX :size="18" class="text-yellow-600" />
            </template>
            <template v-else-if="post.rejected_connection">
              <UserX :size="18" class="text-red-600" />
              <span class="absolute -top-1 -right-1 h-2 w-2 rounded-full bg-red-500 border-2 border-white"></span>
            </template>
            <UserPlus v-else :size="18" class="text-gray-600" />
          </button>
        </div>
      </div>
    </div>
    
    <!-- Post Content -->
    <div class="px-4 py-3">
      
      <ShowMore :text="post.description"/>
      
      <!-- Post Image -->
      <div v-if="post.image_url" class="mt-3 rounded-lg overflow-hidden">
        <img 
          :src="post.image_url" 
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
        :src="post.image_url"
        :alt="'Post by ' + (post.posted_by?.username || 'user')"
        @close="showImageViewer = false"
      />
      
      <!-- Post Stats -->
      <div class="mt-3 flex items-center text-sm text-gray-500 space-x-4">
        <span>{{ post.likes }} {{ post.likes === 1 ? 'like' : 'likes' }}</span>
        <span>{{ post.comments }} {{ post.comments === 1 ? 'comment' : 'comments' }}</span>
        <span>{{ post.views }} {{ post.views === 1 ? 'view' : 'views' }}</span>
        <span>{{ post.forwards }} {{ post.forwards === 1 ? 'share' : 'shares' }}</span>
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
            'text-red-500 hover:text-red-600 cursor-pointer': post.liked && !liking,
            'text-gray-500 hover:text-gray-700 cursor-pointer': !post.liked && !liking,
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
          class="p-2 rounded-full hover:bg-gray-100 text-gray-700 hover:text-blue-500 transition-colors cursor-pointer"
          title="Comment"
        >
          <MessageCircle :size="20" class="w-5 h-5" />
        </button>
        
        <button 
          @click="savePost" 
          class="p-2 rounded-full hover:bg-gray-100 transition-colors relative"
          :class="[{
            'text-yellow-500 hover:text-yellow-600 cursor-pointer': post.saved && !saving,
            'text-gray-500 hover:text-gray-700 cursor-pointer': !post.saved && !saving,
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
          @click="handleShareClick(post)" 
          class="p-2 rounded-full hover:bg-gray-100 text-gray-700 hover:text-green-500 transition-colors cursor-pointer"
          title="Share"
        >
          <Share2 :size="20" class="w-5 h-5" />
        </button>
      </div>
    </div>

    <ConnectionModal 
      v-if="showConnectionsModal" 
      @close="showConnectionsModal = false" 
      @connection-updated="handleConnectionsUpdated"
      :show="showConnectionsModal" 
      :connections="connections"
      :loadingConnections="loadingConnections"
    />
    
    <ConnectionPromptModal
      v-if="showConnectionPrompt"
      :show="showConnectionPrompt"
      :user-name="post.posted_by?.name || 'this user'"
      :is-pending="post.pending_connection"
      :is-rejected="post.rejected_connection"
      :purpose="connectionPromptPurpose"
      @connect="handleConnect"
      @close="showConnectionPrompt = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, onUnmounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/api/axios';
import { useUserStore } from '@/stores/user';
import CommentModal from './CommentModal.vue';
import ShareModal from './ShareModal.vue';
import ConnectionModal from '@/components/feed/ConnectionsModal.vue';
import ImageViewer from '@/components/common/ImageViewer.vue';
import ShowMore from '@/components/ShowMore.vue';
import { Heart, MessageCircle, Bookmark, Share2, Loader2, UserPlus, UserCheck, Clock, UserX, Send } from 'lucide-vue-next';
import ConnectionPromptModal from './ConnectionPromptModal.vue';

const getFollowButtonTooltip = (post) => {
  if (post.connected) return 'Connected';
  if (post.pending_connection) return 'Connection Pending';
  if (post.rejected_connection) return 'Connection Rejected';
  return 'Follow User';
};

const handleFollowClick = () => {
  console.log("clicked follow")
  if (props.post.pending_connection) {
    fetchConnections();
  } else if (!props.post.rejected_connection) {
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

const emit = defineEmits(['donate', 'chat', 'update:post', 'image-loaded', 'save', 'like', 'connection-updated', 'follow']);
const showCommentModal = ref(false);
const showShareModal = ref(false);
const route = useRoute();
const connectionPromptPurpose = ref('donate'); 
const handleCommentClick = (post) => {
  showCommentModal.value = true;
};
const closeCommentModal = () => {
  showCommentModal.value = false;
};

const closeShareModal = () => {
  showShareModal.value = false;
};

const handleShareClick = (post) => {
  showShareModal.value = true;
};


const userStore = useUserStore();
const showImageViewer = ref(false);
const showConnectionsModal = ref(false);
const showConnectionPrompt = ref(false);
const connections = ref([]);
const loadingConnections = ref(false);
const processingDonation = ref(false);
const processingChat = ref(false);

const fetchConnections = async () => {
  if (!props.post?.posted_by?.id) return;
  
  try {
    loadingConnections.value = true;
    const response = await api.get(`/account/users/${props.post.posted_by.id}/our_connection/`);
    connections.value = response.data;
    showConnectionsModal.value = true;
  } catch (error) {
    console.error('Error fetching connections:', error);
  } finally {
    loadingConnections.value = false;
  }
};


const handleConnectionsUpdated = async () => {
  await fetchConnections()
  emit('connection-updated')
  showConnectionsModal.value = false;
}

// Check if the current post is made by the logged-in user
const isCurrentUserPost = computed(() => {
  return userStore.user && props.post.posted_by && userStore.user.id === props.post.posted_by.id;
});

// Watch for URL changes to handle direct comment modal opening
watch(() => route.query.p, (newPostId) => {
  if (newPostId && String(props.post.id) === String(newPostId)) {
    handleCommentClick(props.post)
  } else if (showCommentModal.value && !newPostId) {
    showCommentModal.value = false;
  }
}, { immediate: true });

// Handle initial load
onMounted(() => {
  if (route.query.p && String(props.post.id) === String(route.query.p)) {
    showCommentModal.value = true;
  }
});

const openImageViewer = (e) => {
  if (!props.post.image_url) return;
  showImageViewer.value = true;
};

const likePost = () => {
  emit('like', props.post);
};

const savePost = () => {
  emit('save', props.post);
};

const handleDonate = async (post) => {
  if (post.connected) {
    // If already connected, proceed with donation
    emit('donate', post);
  } else if (post.pending_connection || post.rejected_connection) {
    // Show pending connection message
    connectionPromptPurpose.value = 'donate';
    showConnectionPrompt.value = true;
  } else {
    // Show connection prompt
    connectionPromptPurpose.value = 'donate';
    showConnectionPrompt.value = true;
  }
};

const handleConnect = async () => {
  if (!props.post?.posted_by?.id) return;
  
  try {
    processingDonation.value = true;
    await emit('follow', props.post, true);
    showConnectionPrompt.value = false;
  } catch (error) {
    console.error('Error connecting:', error);
  } finally {
    processingDonation.value = false;
  }
};


const handleChat = async (post) => {
  if (post.connected) {
    // If already connected, proceed with donation
    emit('chat', post);
  } else if (post.pending_connection || post.rejected_connection) {
    // Show pending connection message
    connectionPromptPurpose.value = 'chat';
    showConnectionPrompt.value = true;
  } else {
    // Show connection prompt
    connectionPromptPurpose.value = 'chat';
    showConnectionPrompt.value = true;
  }
};

</script>
