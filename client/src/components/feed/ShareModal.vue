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
        <div class="fixed inset-0 bg-zinc-900/60 backdrop-blur-sm transition-opacity" />
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
            <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-2xl transition-all border border-zinc-100">
              <!-- Header -->
              <div class="flex justify-between items-center pb-4 border-b border-zinc-100">
                <DialogTitle as="h3" class="text-lg font-bold leading-6 text-zinc-900">
                  Share Post
                </DialogTitle>
                <button @click="closeModal" class="rounded-full p-1 text-zinc-400 hover:text-zinc-600 hover:bg-zinc-100 focus:outline-none transition-all cursor-pointer">
                  <span class="sr-only">Close</span>
                  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <!-- Post Preview -->
              <div class="mt-5 p-4 bg-zinc-50 rounded-xl border border-zinc-100">
                <div class="flex space-x-3 items-center mb-3">
                  <div v-if="post.posted_by?.profile_picture" class="flex-shrink-0 h-9 w-9 rounded-full overflow-hidden ring-2 ring-white">
                    <img 
                      :src="post.posted_by.profile_picture" 
                      :alt="post.posted_by.name"
                      class="h-full w-full object-cover"
                    />
                  </div>
                  <div v-else class="flex-shrink-0 h-9 w-9 rounded-full bg-zinc-200 flex items-center justify-center text-zinc-500 font-bold text-xs ring-2 ring-white">
                    {{ post.posted_by?.name ? post.posted_by.name.charAt(0).toUpperCase() : 'U' }}
                  </div>
                  <div class="min-w-0">
                    <p class="font-semibold text-sm text-zinc-900 truncate">{{ post.posted_by?.name || 'Anonymous' }}</p>
                    <p class="text-xs text-zinc-500 truncate">@{{ post.posted_by?.username || 'user' }}</p>
                  </div>
                </div>
                
                <div class="text-sm text-zinc-600">
                  <ShowMore :text="post.description"/>
                </div>
                
                <!-- Post Image Thumbnail -->
                <div v-if="post.image_url" class="mt-3 rounded-lg overflow-hidden border border-zinc-200 aspect-[16/9] bg-zinc-100">
                  <img 
                    :src="post.image_url" 
                    :alt="'Post by ' + (post.posted_by?.username || 'user')" 
                    class="w-full h-full object-cover"
                  />
                </div>
              </div>

              <!-- Share Options -->
              <div class="mt-6 space-y-3">
                <!-- Send in Chat Button -->
                <button 
                  @click="sendInChat"
                  class="w-full cursor-pointer flex items-center justify-center space-x-2.5 bg-violet-600 text-white px-4 py-3 rounded-xl hover:bg-violet-700 shadow-md shadow-violet-500/20 hover:-translate-y-0.5 transition-all duration-300 font-medium text-sm"
                >
                  <Send class="h-4 w-4" />
                  <span>Send in chat</span>
                </button>
                
                <!-- Shareable Link -->
                <div @click="copyToClipboard" class="group bg-white border border-zinc-200 p-3 rounded-xl flex justify-between items-center cursor-pointer hover:border-violet-300 hover:shadow-sm transition-all duration-300">
                  <div class="overflow-hidden mr-3">
                    <p class="text-[10px] uppercase font-bold text-zinc-400 tracking-wide mb-0.5">Shareable Link</p>
                    <p class="font-mono text-sm text-zinc-700 truncate select-all">{{ shareableLink }}</p>
                  </div>
                  <button 
                    class="flex-shrink-0 text-zinc-400 group-hover:text-violet-600 p-2 rounded-lg hover:bg-violet-50 transition-colors"
                    title="Copy to clipboard"
                    @click.stop="copyToClipboard"
                  >
                    <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                    </svg>
                  </button>
                </div>
                
                <div class="h-5 flex items-center justify-center">
                    <transition
                        enter-active-class="transition ease-out duration-200"
                        enter-from-class="transform opacity-0 scale-95"
                        enter-to-class="transform opacity-100 scale-100"
                        leave-active-class="transition ease-in duration-150"
                        leave-from-class="transform opacity-100 scale-100"
                        leave-to-class="transform opacity-0 scale-95"
                    >
                        <p v-if="copyButtonText === 'Copied!'" class="text-xs font-semibold text-emerald-600 flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                            </svg>
                            Link copied to clipboard
                        </p>
                    </transition>
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
import { ref, computed } from 'vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { useRouter } from 'vue-router';
import ShowMore from '@/components/ShowMore.vue';
import { Send } from 'lucide-vue-next';
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

const router = useRouter();
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
      copyButtonText.value = 'Copy';
    }, 2000);
  } catch (err) {
    console.error('Failed to copy text: ', err);
    copyButtonText.value = 'Failed to copy';
  }
};

const sendInChat = () => {
  closeModal();
  router.push(`/chat?p=${props.post.id}`);
};
</script>
