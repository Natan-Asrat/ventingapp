<template>
  <div class="bg-white rounded-[1.25rem] shadow-sm border border-zinc-100/80 transition-all duration-300 hover:shadow-md overflow-hidden group">
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
    <div class="px-5 pt-5 pb-3 flex items-start justify-between">
      <router-link 
        :to="{ name: 'UsernameProfile', params: { username: post.posted_by.username } }"
        class="flex flex-1 items-center space-x-3 group/user"
      >
        <div v-if="post.posted_by?.profile_picture" class="h-10 w-10 rounded-full overflow-hidden ring-2 ring-zinc-50 group-hover/user:ring-violet-100 transition-all">
          <img 
            :src="post.posted_by.profile_picture" 
            :alt="post.posted_by.name"
            class="h-full w-full object-cover"
          />
        </div>
        <div v-else class="h-10 w-10 rounded-full bg-zinc-100 flex items-center justify-center text-zinc-400 font-semibold ring-2 ring-zinc-50">
          {{ post.posted_by?.name ? post.posted_by.name.charAt(0).toUpperCase() : 'U' }}
        </div>
        <div>
          <p class="font-semibold text-zinc-800 text-[15px] leading-tight group-hover/user:text-violet-700 transition-colors">{{ post.posted_by?.name || 'Anonymous' }}</p>
          <div class="flex items-center gap-2 mt-0.5">
            <p class="text-xs text-zinc-400 font-medium">@{{ post.posted_by?.username || 'user' }}</p>
            <span class="text-[10px] text-zinc-300">•</span>
            <span class="text-xs text-zinc-400">{{ post.formatted_created_at }}</span>
          </div>
        </div>
      </router-link>
      
      <div v-if="!isCurrentUserPost" class="flex items-center space-x-2">
        <!-- Follow/Connect Button -->
        <button 
            @click="handleFollowClick"
            class="h-8 w-8 rounded-full flex items-center justify-center transition-all duration-200 border"
            :class="{
              'bg-emerald-50 text-emerald-600 border-emerald-100 hover:bg-emerald-100': post.connected,
              'bg-amber-50 text-amber-600 border-amber-100': post.pending_connection && !post.rejected_connection,
              'bg-rose-50 text-rose-600 border-rose-100': post.rejected_connection,
              'bg-white text-zinc-400 border-zinc-200 hover:bg-zinc-50 hover:text-zinc-600 hover:border-zinc-300': (!post.connected && !post.pending_connection && !post.rejected_connection) || post.removed_connection,
              'cursor-not-allowed opacity-75': post.rejected_connection || post.banned_connection,
              'cursor-pointer': !post.rejected_connection && !post.banned_connection
            }"
            :disabled="post.rejected_connection || post.banned_connection"
            :title="getFollowButtonTooltip(post)"
        >
            <template v-if="post.connected">
                <UserCheck :size="16" class="stroke-[2.5]" />
            </template>
            <template v-else-if="post.pending_connection">
                <Clock :size="16" class="stroke-[2.5]" />
            </template>
            <template v-else-if="post.banned_connection">
                <UserX :size="16" class="stroke-[2.5]" />
            </template>
            <template v-else-if="post.rejected_connection">
                <UserX :size="16" class="stroke-[2.5]" />
            </template>
            <UserPlus v-else :size="16" class="stroke-[2.5]" />
        </button>

        <!-- Chat Button -->
        <button 
          @click="handleChat(post)"
          class="h-8 w-8 flex items-center justify-center text-zinc-400 hover:text-violet-600 hover:bg-violet-50 rounded-full transition-all duration-200 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed border border-transparent hover:border-violet-100"
          :disabled="processingChat"
          title="Chat"
        >
          <Loader2 v-if="processingChat" class="w-4 h-4 animate-spin" />
          <Send v-else class="w-4 h-4 stroke-[2.5] ml-0.5" />
        </button>

        <!-- Donate Button -->
        <button 
          v-if="post.payment_info_list && post.payment_info_list.length > 0"
          @click="handleDonate(post)"
          class="h-8 px-3.5 bg-zinc-900 hover:bg-violet-600 text-white text-xs font-semibold rounded-full shadow-sm hover:shadow hover:-translate-y-0.5 transition-all duration-300 flex items-center cursor-pointer disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-none ml-1"
          :disabled="processingDonation"
        >
          <Loader2 v-if="processingDonation" class="w-3 h-3 mr-1.5 animate-spin" />
          <span v-else>Support</span>
        </button>
      </div>
    </div>
    
    <!-- Post Content -->
    <div class="px-5 pb-2">
      <div class="text-zinc-700 text-[15px] leading-[1.7] font-normal tracking-wide">
        <ShowMore :text="post.description"/>
      </div>
      
      <!-- Post Image -->
      <div v-if="post.image_url" class="mt-4 rounded-xl overflow-hidden border border-zinc-100 bg-zinc-50 relative group/image">
        <div class="absolute inset-0 bg-black/0 group-hover/image:bg-black/5 transition-colors duration-300 pointer-events-none z-10"></div>
        <img 
          :src="post.image_url" 
          :alt="'Post by ' + (post.posted_by?.username || 'user')" 
          class="w-full h-auto object-cover cursor-zoom-in transition-transform duration-500 group-hover/image:scale-[1.02]"
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
    </div>
    
    <!-- Post Stats -->
    <div class="px-5 pt-3 pb-1 flex items-center justify-between text-xs font-medium text-zinc-400">
        <div class="flex items-center gap-3">
            <span>{{ post.likes }} {{ post.likes === 1 ? 'Like' : 'Likes' }}</span>
            <span>{{ post.comments }} {{ post.comments === 1 ? 'Comment' : 'Comments' }}</span>
        </div>
        <div class="flex items-center gap-3">
            <span>{{ post.views }} {{ post.views === 1 ? 'View' : 'Views' }}</span>
            <span v-if="post.forwards > 0">{{ post.forwards }} {{ post.forwards === 1 ? 'Share' : 'Shares' }}</span>
        </div>
    </div>

    <!-- Action Buttons -->
    <div class="px-3 py-2 border-t border-zinc-50 mt-1">
      <div class="flex items-center justify-between">
        <!-- Like Button -->
        <button 
          @click="likePost" 
          class="cursor-pointer flex-1 flex items-center justify-center py-2.5 rounded-lg transition-all duration-200 group/btn hover:bg-zinc-50"
          :class="[{
            'text-rose-500': post.liked && !liking,
            'text-zinc-400 hover:text-rose-500': !post.liked && !liking,
            'opacity-50 cursor-not-allowed': liking
          }]"
          :disabled="liking"
          title="Like"
        >
          <div class="relative">
             <Loader2 v-if="liking" class="w-5 h-5 animate-spin text-rose-400" />
             <Heart v-else :size="20" :fill="post.liked ? 'currentColor' : 'none'" class="transition-transform duration-200 group-active/btn:scale-90" />
          </div>
        </button>
        
        <!-- Comment Button -->
        <button 
          @click="handleCommentClick(post)" 
          class="cursor-pointer flex-1 flex items-center justify-center py-2.5 rounded-lg text-zinc-400 hover:bg-zinc-50 hover:text-violet-600 transition-all duration-200 group/btn"
          title="Comment"
        >
          <MessageCircle :size="20" class="transition-transform duration-200 group-active/btn:scale-90" />
        </button>
        
        <!-- Save Button -->
        <button 
          @click="savePost" 
          class="cursor-pointer flex-1 flex items-center justify-center py-2.5 rounded-lg transition-all duration-200 group/btn hover:bg-zinc-50"
          :class="[{
            'text-violet-600': post.saved && !saving,
            'text-zinc-400 hover:text-violet-600': !post.saved && !saving,
            'opacity-50 cursor-not-allowed': saving
          }]"
          :disabled="saving"
          title="Save"
        >
           <Loader2 v-if="saving" class="w-5 h-5 animate-spin text-violet-400" />
           <Bookmark v-else :size="20" :fill="post.saved ? 'currentColor' : 'none'" class="transition-transform duration-200 group-active/btn:scale-90" />
        </button>
        
        <!-- Share Button -->
        <button 
          @click="handleShareClick(post)" 
          class="cursor-pointer flex-1 flex items-center justify-center py-2.5 rounded-lg text-zinc-400 hover:bg-zinc-50 hover:text-emerald-600 transition-all duration-200 group/btn"
          title="Share"
        >
          <Share2 :size="20" class="transition-transform duration-200 group-active/btn:scale-90" />
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
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import CommentModal from './CommentModal.vue';
import ShareModal from './ShareModal.vue';
import ConnectionModal from '@/components/feed/ConnectionsModal.vue';
import ImageViewer from '@/components/common/ImageViewer.vue';
import ShowMore from '@/components/ShowMore.vue';
import { Heart, MessageCircle, Bookmark, Share2, Loader2, UserPlus, UserCheck, Clock, UserX, Send } from 'lucide-vue-next';
import ConnectionPromptModal from './ConnectionPromptModal.vue';
import { useConnectionStore } from '@/stores/connection';
const connectionStore = useConnectionStore();

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
    const response = await connectionStore.fetchOurConnections(props.post?.posted_by?.id)
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
