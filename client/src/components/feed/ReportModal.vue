<template>
  <TransitionRoot as="template" :show="isOpen">
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

      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <DialogPanel
              class="relative transform overflow-hidden rounded-2xl bg-white px-6 pb-6 pt-6 text-left shadow-2xl transition-all sm:my-8 sm:w-full sm:max-w-md border border-zinc-100"
            >
              <div>
                 <!-- Warning Icon -->
                <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-rose-50 mb-4 ring-8 ring-rose-50/50">
                   <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-rose-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                </div>
                
                <div class="text-center">
                  <DialogTitle as="h3" class="text-lg font-bold leading-6 text-zinc-900">
                    Report Content
                  </DialogTitle>
                  <p class="text-sm text-zinc-500 mt-2">
                    Please help us understand what's wrong with this content.
                  </p>
                  
                  <div class="mt-5">
                    <label for="reason" class="sr-only">
                      Reason for reporting
                    </label>
                    <textarea
                      id="reason"
                      v-model="reason"
                      rows="4"
                      class="w-full bg-zinc-50 border border-zinc-200 rounded-xl shadow-sm placeholder-zinc-400 focus:ring-2 focus:ring-rose-500/20 focus:border-rose-500 focus:bg-white transition-all text-sm p-3 resize-none"
                      placeholder="Tell us why you are reporting this..."
                    />
                  </div>
                </div>
              </div>
              <div class="mt-6 flex flex-col-reverse sm:flex-row sm:justify-end gap-3">
                <button
                  type="button"
                  class="inline-flex w-full justify-center rounded-full border border-zinc-300 bg-white px-4 py-2 text-base font-medium text-zinc-700 shadow-sm hover:bg-zinc-50 focus:outline-none focus:ring-2 focus:ring-zinc-500 focus:ring-offset-2 sm:mt-0 sm:w-auto sm:text-sm cursor-pointer transition-colors"
                  @click="closeModal"
                  :disabled="isSubmitting"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  class="inline-flex w-full justify-center rounded-full border border-transparent bg-rose-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-rose-700 focus:outline-none focus:ring-2 focus:ring-rose-500 focus:ring-offset-2 sm:w-auto sm:text-sm transition-all cursor-pointer disabled:opacity-70 disabled:cursor-not-allowed"
                  @click="submitReport"
                  :disabled="isSubmitting"
                >
                  <span v-if="isSubmitting" class="flex items-center">
                    <Loader2 class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" />
                    Submitting...
                  </span>
                  <span v-else>
                    Submit Report
                  </span>
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
import { ref, defineProps, defineEmits } from 'vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { Loader2 } from 'lucide-vue-next';
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  isSubmitting: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close', 'submit']);

const reason = ref('');

const closeModal = () => {
  reason.value = '';
  emit('close');
};

const submitReport = () => {
    emit('submit', reason.value.trim());
};
</script>
