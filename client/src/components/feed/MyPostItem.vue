<template>
  <div class="bg-white shadow overflow-hidden rounded-lg mb-4">
    <!-- Comment Modal -->
    <CommentModal 
      v-if="showCommentModal"
      :post="post"
      :show="showCommentModal"
      @close="closeCommentModal"
      @comment-added="handleCommentAdded"
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
      <button 
        @click="post.archived ? $emit('restore') : $emit('archive')"
        class="text-gray-400 hover:text-green-500 transition-colors cursor-pointer"
        :title="post.archived ? 'Restore post' : 'Archive post'"
      >
        <component 
          :is="post.archived ? RotateCcw : Trash2" 
          class="h-5 w-5" 
          :class="{'hover:text-green-500': post.archived, 'hover:text-red-500': !post.archived}"
        />
      </button>
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
        <span class="text-xs text-gray-400">{{ post.formatted_created_at }}</span>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="px-4 py-2 border-t border-gray-100">
      <div class="flex items-center">
        <button 
          @click="handleCommentClick(post)" 
          class="p-2 rounded-full hover:bg-gray-100 text-gray-700 hover:text-blue-500 transition-colors cursor-pointer"
          title="Comment"
        >
          <MessageCircle :size="20" class="w-5 h-5" />
        </button>
        
        <button 
          v-if="!post.archived"
          @click="handleShareClick(post)" 
          class="p-2 rounded-full hover:bg-gray-100 text-gray-700 hover:text-green-500 transition-colors cursor-pointer"
          title="Share"
        >
          <Share2 :size="20" class="w-5 h-5" />
        </button>
        
        <div class="ml-auto">
          <button 
        
            @click="showDonationOptions = true"
            class="px-3 py-1 bg-indigo-100 text-indigo-700 text-sm font-medium rounded-full hover:bg-indigo-200 transition-colors flex items-center cursor-pointer"
          >
            Donation Options
          </button>
        </div>
      </div>
    </div>
    
    <!-- Donation Options Modal -->
    <DonationOptionsModal
      v-if="showDonationOptions"
      :show="showDonationOptions"
      :payment-info-list="post.payment_info_list"
      :post-id="post.id"
      :archived="post.archived"
      @close="showDonationOptions = false"
      @update:payment-info-list="handlePaymentInfoUpdate"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Trash2, MessageCircle, Share2, RotateCcw } from 'lucide-vue-next';
import CommentModal from '@/components/feed/CommentModal.vue';
import ShareModal from '@/components/feed/ShareModal.vue';
import ImageViewer from '@/components/common/ImageViewer.vue';
import ShowMore from '@/components/ShowMore.vue';
import DonationOptionsModal from './DonationOptionsModal.vue';

const props = defineProps({
  post: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['update:post', 'archive', 'restore']);

// State
const showCommentModal = ref(false);
const showShareModal = ref(false);
const showImageViewer = ref(false);
const showDonationOptions = ref(false);

// Methods
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

const handleCommentAdded = () => {
  // Increment comments count
  emit('update:post', {
    ...props.post,
    comments: (props.post.comments || 0) + 1
  });
};

const openImageViewer = (e) => {
  if (e) {
    e.stopPropagation();
  }
  showImageViewer.value = true;
};

const handlePaymentInfoUpdate = (updatedPaymentInfo) => {
  emit('update:post', {
    ...props.post,
    payment_info_list: updatedPaymentInfo
  });
};
</script>
