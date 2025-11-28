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
        <div class="fixed inset-0 bg-gray-500/75 transition-opacity" />
      </TransitionChild>

      <div class="fixed inset-0 z-50 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center sm:p-0">
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <DialogPanel class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
              <!-- Close button -->
              <div class="absolute top-0 right-0 pt-4 pr-4">
                <button
                  type="button"
                  class="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  @click="closeModal"
                >
                  <span class="sr-only">Close</span>
                  <X class="h-6 w-6 cursor-pointer" />
                </button>
              </div>

              <div class="sm:flex sm:items-start">
                <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
                  <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                    What's your decision?
                  </DialogTitle>
                  
                  <div class="mt-4">
                    <label for="reason" class="block text-sm font-medium text-gray-700">Reason</label>
                    <div class="mt-1">
                      <textarea
                        id="reason"
                        v-model="reason"
                        rows="3"
                        class="shadow-sm placeholder-gray-500 focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border border-gray-300 rounded-md p-2"
                        placeholder="Enter the reason for your decision"
                      />
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                <button
                  type="button"
                  class="w-full inline-flex cursor-pointer justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:col-start-2 sm:text-sm"
                  :disabled="isSubmitting"
                  @click="handleReject"
                >
                  <span v-if="isSubmitting" class="animate-spin mr-2">↻</span>
                  Reject
                </button>
                <button
                  type="button"
                  class="mt-3 w-full cursor-pointer inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:col-start-1 sm:text-sm"
                  :disabled="isSubmitting"
                  @click="handleApprove"
                >
                  <span v-if="isSubmitting" class="animate-spin mr-2">↻</span>
                  Approve
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
import { X } from 'lucide-vue-next';

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  reportId: {
    type: [String, Number],
    required: true
  }
});

const emit = defineEmits(['close', 'approve', 'reject']);

const reason = ref('');
const isSubmitting = ref(false);

const closeModal = () => {
  emit('close');
};

const handleApprove = async () => {
  if (!reason.value.trim()) {
    alert('Please provide a reason for your decision');
    return;
  }
  
  isSubmitting.value = true;
  try {
    await emit('approve', { reason: reason.value });
    closeModal();
  } finally {
    isSubmitting.value = false;
  }
};

const handleReject = async () => {
  if (!reason.value.trim()) {
    alert('Please provide a reason for your decision');
    return;
  }
  
  isSubmitting.value = true;
  try {
    await emit('reject', { reason: reason.value });
    closeModal();
  } finally {
    isSubmitting.value = false;
  }
};

// Reset the form when the modal is opened
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    reason.value = '';
  }
});
</script>
