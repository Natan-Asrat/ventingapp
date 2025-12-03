<template>
  <div 
    class="border border-gray-200 rounded-lg overflow-hidden bg-white shadow-sm hover:shadow transition-shadow cursor-pointer"
    @click="navigateToPost"
  >
    <!-- Post Header -->
    <div class="p-4">
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
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 truncate">{{ post.posted_by?.name || 'Anonymous' }}</p>
          <p class="text-xs text-gray-500">@{{ post.posted_by?.username || 'user' }}</p>
        </div>
      </div>
    </div>

    <!-- Post Content -->
    <div class="px-4 pb-3">
        <ShowMore :text="post.description"/>
    </div>

    <!-- Post Image -->
    <div v-if="post.image_url" class="w-full">
      <img 
        :src="post.image_url" 
        :alt="'Post by ' + (post.posted_by?.username || 'user')" 
        class="w-full h-auto object-cover"
      />
    </div>

    <!-- Post Stats -->
    <div class="px-4 py-2 border-t border-gray-100">
      <div class="flex items-center text-xs text-gray-500 space-x-4">
        <span>{{ post.likes || 0 }} {{ post.likes === 1 ? 'like' : 'likes' }}</span>
        <span>{{ post.comments || 0 }} {{ post.comments === 1 ? 'comment' : 'comments' }}</span>
        <span>{{ post.views || 0 }} {{ post.views === 1 ? 'view' : 'views' }}</span>
        <span>{{ post.forwards || 0 }} {{ post.forwards === 1 ? 'share' : 'shares' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import ShowMore from '@/components/ShowMore.vue';

const props = defineProps({
  post: {
    type: Object,
    required: true,
    default: () => ({
      id: null,
      description: '',
      image_url: null,
      likes: 0,
      comments: 0,
      views: 0,
      posted_by: {
        id: null,
        name: 'Anonymous',
        username: 'user',
        profile_picture: null
      },
      created_at: null
    })
  }
});

const router = useRouter();

const formatTime = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
};

const navigateToPost = () => {
  if (props.post?.id) {
    router.push(`/home?p=${props.post.id}`);
  }
};
</script>
