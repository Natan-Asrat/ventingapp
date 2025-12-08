<template>
  <div class="bg-white rounded-2xl shadow-sm border border-zinc-100 overflow-hidden transition-shadow hover:shadow-md">
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
    <div class="px-5 py-4 flex items-center justify-between border-b border-zinc-50/50 bg-zinc-50/30">
      <div class="flex items-center space-x-3">
        <div v-if="post.posted_by?.profile_picture" class="h-10 w-10 rounded-full overflow-hidden ring-2 ring-white shadow-sm">
          <img 
            :src="post.posted_by.profile_picture" 
            :alt="post.posted_by.name"
            class="h-full w-full object-cover"
          />
        </div>
        <div v-else class="h-10 w-10 rounded-full bg-zinc-100 flex items-center justify-center text-zinc-400 font-bold ring-2 ring-white">
          {{ post.posted_by?.name ? post.posted_by.name.charAt(0).toUpperCase() : 'U' }}
        </div>
        <div>
          <p class="font-bold text-sm text-zinc-900 leading-tight">{{ post.posted_by?.name || 'Anonymous' }}</p>
          <p class="text-xs text-zinc-500 font-medium mt-0.5">@{{ post.posted_by?.username || 'user' }}</p>
        </div>
      </div>
      <button 
        @click="post.archived ? $emit('restore') : $emit('archive')"
        class="group p-2 rounded-full hover:bg-white border border-transparent hover:border-zinc-200 hover:shadow-sm transition-all cursor-pointer"
        :title="post.archived ? 'Restore post' : 'Archive post'"
      >
        <component 
          :is="post.archived ? RotateCcw : Trash2" 
          class="h-4 w-4 text-zinc-400 transition-colors" 
          :class="{'group-hover:text-emerald-500': post.archived, 'group-hover:text-rose-500': !post.archived}"
        />
      </button>
    </div>
    
    <!-- Post Content -->
    <div class="px-5 py-4">
      <div class="text-[15px] leading-relaxed text-zinc-700">
        <ShowMore :text="post.description"/>
      </div>
      
      <!-- Post Image -->
      <div v-if="post.image_url" class="mt-4 rounded-xl overflow-hidden border border-zinc-100 bg-zinc-50">
        <img 
          :src="post.image_url" 
          :alt="'Post by ' + (post.posted_by?.username || 'user')" 
          class="w-full h-auto object-cover cursor-zoom-in hover:scale-[1.02] transition-transform duration-500"
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
      <div class="mt-4 flex items-center text-xs font-medium text-zinc-400 space-x-4 border-t border-zinc-50 pt-3">
        <span>{{ post.likes }} {{ post.likes === 1 ? 'like' : 'likes' }}</span>
        <span>{{ post.comments }} {{ post.comments === 1 ? 'comment' : 'comments' }}</span>
        <span>{{ post.views }} {{ post.views === 1 ? 'view' : 'views' }}</span>
        <span class="ml-auto">{{ post.formatted_created_at }}</span>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="px-4 py-3 bg-zinc-50/50 border-t border-zinc-100">
      <div class="flex items-center justify-between">
        <div class="flex space-x-1">
            <button 
              @click="handleCommentClick(post)" 
              class="p-2 rounded-lg text-zinc-400 hover:text-violet-600 hover:bg-violet-50 transition-all cursor-pointer"
              title="Comment"
            >
              <MessageCircle :size="20" class="w-5 h-5" />
            </button>
            
            <button 
              v-if="!post.archived"
              @click="handleShareClick(post)" 
              class="p-2 rounded-lg text-zinc-400 hover:text-emerald-600 hover:bg-emerald-50 transition-all cursor-pointer"
              title="Share"
            >
              <Share2 :size="20" class="w-5 h-5" />
            </button>
        </div>
        
        <div>
          <button 
            @click="showDonationOptions = true"
            class="px-4 py-1.5 bg-white border border-zinc-200 shadow-sm text-zinc-700 text-xs font-semibold rounded-full hover:bg-zinc-50 hover:border-zinc-300 hover:text-zinc-900 transition-all cursor-pointer flex items-center"
          >
            <Wallet class="w-3.5 h-3.5 mr-2 text-zinc-400" />
            Payment Options
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
import { Trash2, MessageCircle, Share2, RotateCcw, Wallet } from 'lucide-vue-next';
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
