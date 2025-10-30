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
              <div class="flex justify-between items-center pb-3 border-b">
                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                  Share Post
                </DialogTitle>
                <button @click="closeModal" class="text-gray-400 hover:text-gray-500 focus:outline-none cursor-pointer">
                  <span class="sr-only">Close</span>
                  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <!-- Post Content -->
              <div class="mt-4">
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
                  <div>
                    <p class="font-medium text-sm">{{ post.posted_by?.name || 'Anonymous' }}</p>
                    <p class="text-xs text-gray-500">@{{ post.posted_by?.username || 'user' }}</p>
                  </div>
                </div>
                
                <!-- <p class="mt-2 text-gray-800 whitespace-pre-line">{{ post.description }}</p> -->
                <ShowMore :text="post.description"/>
                <!-- Post Image -->
                <div v-if="post.image" class="mt-3 rounded-lg overflow-hidden">
                  <img 
                    :src="post.image" 
                    :alt="'Post by ' + (post.posted_by?.username || 'user')" 
                    class="w-full h-auto object-cover"
                  />
                </div>
              </div>

              <!-- Share Options -->
              <div class="mt-6">
                <div @click="copyToClipboard" class="bg-gray-50 p-3 rounded-md flex justify-between items-center cursor-pointer hover:bg-gray-100 transition-colors">
                  <div class="overflow-hidden">
                    <p class="text-xs text-gray-500">Shareable Link</p>
                    <p class="font-mono text-sm truncate">{{ shareableLink }}</p>
                  </div>
                  <button 
                    class="text-indigo-600 hover:text-indigo-800 p-1 cursor-pointer"
                    title="Copy to clipboard"
                    @click.stop="copyToClipboard"
                  >
                    <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                    </svg>
                  </button>
                </div>
                <p v-if="copyButtonText === 'Copied!'" class="text-xs text-green-600 mt-1 text-center">
                  {{ copyButtonText }}
                </p>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, computed } from 'vue';
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
      image: null
    })
  }
});

const emit = defineEmits(['close']);

const copyButtonText = ref('Copy Link');

const shareableLink = computed(() => {
  return `${window.location.origin}${window.location.pathname}?p=${props.post.id}`;
});

const closeModal = () => {
  emit('close');
};

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(shareableLink.value);
    copyButtonText.value = 'Copied!';
    setTimeout(() => {
      copyButtonText.value = 'Copy Link';
    }, 2000);
  } catch (err) {
    console.error('Failed to copy:', err);
  }
};
</script>
