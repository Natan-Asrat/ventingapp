<template>
  <TransitionRoot appear :show="isOpen" as="template">
    <Dialog as="div" @close="closeModal" class="relative z-50">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-zinc-900/60 backdrop-blur-sm" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
              <DialogTitle as="h3" class="text-lg font-bold leading-6 text-zinc-900">
                Reconnect with {{ userName }}
              </DialogTitle>
              
              <div class="mt-4">
                <p class="text-sm text-zinc-500 leading-relaxed">
                  You've connected with this user before. Adding a personal note can help you reconnect.
                </p>
                
                <div class="mt-5">
                  <label for="message" class="block text-xs font-semibold text-zinc-700 mb-2 uppercase tracking-wide">
                    Message (optional)
                  </label>
                  <textarea
                    id="message"
                    v-model="message"
                    rows="4"
                    class="w-full px-4 py-3 bg-zinc-50 border border-zinc-200 rounded-xl shadow-sm placeholder-zinc-400 focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 focus:bg-white transition-all sm:text-sm resize-none"
                    placeholder="Hi, I'd like to reconnect because..."
                  ></textarea>
                </div>
              </div>

              <div class="mt-8 flex justify-end space-x-3">
                <button
                  type="button"
                  class="px-5 py-2.5 text-sm font-medium text-zinc-600 bg-white border border-zinc-200 rounded-full hover:bg-zinc-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-zinc-500 transition-colors cursor-pointer"
                  @click="closeModal"
                  :disabled="isLoading"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  class="px-5 py-2.5 text-sm font-medium text-white bg-zinc-900 border border-transparent rounded-full hover:bg-violet-600 shadow-lg shadow-violet-500/20 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:bg-zinc-400 disabled:cursor-not-allowed disabled:shadow-none transition-all cursor-pointer"
                  @click="sendRequest"
                  :disabled="isLoading"
                >
                  <span v-if="isLoading" class="flex items-center">
                    <Loader2 class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" />
                    Sending...
                  </span>
                  <span v-else>Send Request</span>
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, watch } from 'vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { Loader2 } from 'lucide-vue-next';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  userName: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['close', 'confirm']);

const message = ref('');
const isLoading = ref(false);

const closeModal = () => {
  if (!isLoading.value) {
    emit('close');
  }
};

const sendRequest = () => {
  isLoading.value = true;
  emit('confirm', message.value);
};

// Reset form when modal is opened/closed
watch(() => props.isOpen, (newVal) => {
  if (!newVal) {
    message.value = '';
    isLoading.value = false;
  }
});
</script>
