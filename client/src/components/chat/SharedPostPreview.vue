<template>
  <div 
    class="rounded-xl overflow-hidden cursor-pointer hover:opacity-95 transition-opacity w-full min-w-[240px]"
    :class="isMine ? 'bg-zinc-800 border border-zinc-700' : 'bg-white border border-zinc-200'"
    @click="handleClick"
  >
    <!-- Post Header -->
    <div class="p-3 pb-2 flex items-center space-x-2">
        <div v-if="post.posted_by?.profile_picture" class="h-6 w-6 rounded-full overflow-hidden flex-shrink-0 ring-1 ring-white/10">
          <img 
            :src="post.posted_by.profile_picture" 
            :alt="post.posted_by.name"
            class="h-full w-full object-cover"
          />
        </div>
        <div v-else class="h-6 w-6 rounded-full flex items-center justify-center text-[10px] font-bold flex-shrink-0" :class="isMine ? 'bg-zinc-700 text-zinc-300' : 'bg-zinc-100 text-zinc-500'">
          {{ post.posted_by?.name ? post.posted_by.name.charAt(0).toUpperCase() : 'U' }}
        </div>
        <div class="min-w-0 flex-1">
          <p class="text-xs font-bold truncate" :class="isMine ? 'text-zinc-200' : 'text-zinc-900'">{{ post.posted_by?.name || 'Anonymous' }}</p>
        </div>
    </div>

    <!-- Content Preview -->
    <div class="px-3 pb-2 text-xs">
        <ShowMore :text="post.description" :theme="isMine ? 'dark' : 'light'" />
    </div>

    <!-- Image -->
    <div v-if="post.image_url" class="w-full bg-black/5">
      <img 
        :src="post.image_url" 
        class="w-full h-auto object-cover max-h-[400px]"
      />
    </div>
    
    <!-- Footer -->
    <div class="px-3 py-2 flex items-center justify-between text-[10px]" :class="isMine ? 'bg-zinc-900/50 text-zinc-400' : 'bg-zinc-50 text-zinc-500'">
        <span>Post</span>
        <div class="flex items-center gap-2">
            <span>{{ post.likes }} likes</span>
        </div>
    </div>
  </div>
</template>

<script setup>
import ShowMore from '@/components/ShowMore.vue';

const props = defineProps({
  post: {
    type: Object,
    required: true,
    default: () => ({})
  },
  isMine: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['open-post']);

const handleClick = (e) => {
  // Don't emit if clicking on interactive elements like buttons
  // Note: ShowMore's "Read more" has stopPropagation, so we don't need to check for it specifically if it handles its own click.
  // We just avoid other buttons or links if any were to exist inside.
  if (e.target.closest('button') || e.target.closest('a')) return;
  
  if (props.post?.id) {
    emit('open-post', props.post);
  }
};
</script>