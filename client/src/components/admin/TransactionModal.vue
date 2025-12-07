<template>
  <TransitionRoot as="template" :show="isOpen">
    <Dialog as="div" class="relative z-10" @close="closeModal">
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

      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
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
              class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-2xl sm:p-6"
            >
              <div class="absolute right-0 top-0 pr-4 pt-4">
                <button
                  type="button"
                  class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none"
                  @click="closeModal"
                >
                  <span class="sr-only">Close</span>
                  <X class="h-6 w-6 cursor-pointer" aria-hidden="true" />
                </button>
              </div>

              <div class="sm:flex sm:items-start">
                <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
                  <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                    Transaction Details
                  </DialogTitle>
                  
                  <div class="mt-4 space-y-4">
                    <!-- Screenshot -->
                    <div>
                      <h4 class="text-sm font-medium text-gray-500">Payment Proof</h4>
                      <div class="mt-1">
                        <img 
                          :src="transaction.screenshot_url" 
                          :alt="'Payment proof for ' + transaction.id"
                          class="max-w-full h-auto rounded-lg border border-gray-200"
                        />
                      </div>
                    </div>

                    <!-- Transaction Details -->
                    <div class="grid grid-cols-2 gap-4">
                      <div>
                        <h4 class="text-sm font-medium text-gray-500">Method</h4>
                        <p class="mt-1 text-sm text-gray-900">{{ transaction.method }}</p>
                      </div>
                      <div>
                        <h4 class="text-sm font-medium text-gray-500">Amount</h4>
                        <p class="mt-1 text-sm text-gray-900">
                          {{ Intl.NumberFormat().format(transaction.total_amount) }} {{ transaction.currency }}
                        </p>
                      </div>
                      <div>
                        <h4 class="text-sm font-medium text-gray-500">Connects</h4>
                        <p class="mt-1 text-sm text-gray-900">{{ Intl.NumberFormat().format(transaction.connects) }}</p>
                      </div>
                      <div>
                        <h4 class="text-sm font-medium text-gray-500">Date</h4>
                        <p class="mt-1 text-sm text-gray-900">{{ transaction.formatted_created_at }}</p>
                      </div>
                      <div class="col-span-2">
                        <h4 class="text-sm font-medium text-gray-500">Status</h4>
                        <span 
                          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                          :class="{
                            'bg-yellow-100 text-yellow-800': transaction.status === 'pending',
                            'bg-green-100 text-green-800': transaction.status === 'completed',
                            'bg-red-100 text-red-800': transaction.status === 'rejected'
                          }"
                        >
                          {{ transaction.status }}
                        </span>
                      </div>
                    </div>

                    <!-- Transaction ID Input -->
                    <div v-if="transaction.status === 'pending'">
                      <label for="transactionId" class="block text-sm font-medium text-gray-700">
                        Transaction ID
                      </label>
                      <input
                        type="text"
                        id="transactionId"
                        v-model="transactionId"
                        class="mt-1 px-4 py-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm placeholder-gray-500"
                        placeholder="Enter transaction ID"
                      />
                    </div>

                    <!-- Rejection Reason -->
                    <div v-if="showRejectReason">
                      <label for="rejectReason" class="block text-sm font-medium text-gray-700">
                        Reason for Rejection
                      </label>
                      <textarea
                        id="rejectReason"
                        v-model="rejectReason"
                        rows="3"
                        class="mt-1 px-4 py-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm placeholder-gray-500"
                        placeholder="Please provide a reason for rejection"
                      />
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
                <button
                  v-if="transaction.status === 'pending'"
                  type="button"
                  class="inline-flex w-full justify-center rounded-md border border-transparent px-4 py-2 text-base font-medium text-white shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 sm:col-start-1 sm:text-sm cursor-pointer"
                  @click="toggleRejectReason"
                  :class="[showRejectReason ? 'bg-gray-500' : 'bg-red-600 focus:ring-red-500 hover:bg-red-700']"
                  :disabled="isLoading"
                >
                  {{ showRejectReason ? 'Cancel' : 'Reject' }}
                </button>
                <button
                  v-else
                  type="button"
                  class="inline-flex w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:col-start-1 sm:mt-0 sm:text-sm"
                  @click="closeModal"
                  :disabled="isLoading"
                >
                  Close
                </button>
                
                <button
                  v-if="transaction.status === 'pending'"
                  type="button"
                  class="mt-3 inline-flex w-full justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:col-start-2 sm:mt-0 sm:text-sm"
                  :class="[canApprove ? 'cursor-pointer' : 'opacity-50 cursor-not-allowed']"
                  @click="handleApprove"
                  :disabled="!canApprove || isLoading"
                >
                  <span v-if="isLoading" class="flex items-center">
                    <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                  </span>
                  <span v-else>Approve</span>
                </button>
                
                <button
                  v-if="showRejectReason"
                  type="button"
                  class="mt-3 inline-flex w-full justify-center rounded-md border border-transparent bg-red-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 sm:col-start-2 sm:mt-0 sm:text-sm"
                  :class="[rejectReason.trim() ? 'cursor-pointer' : 'opacity-50 cursor-not-allowed']"
                  @click="handleReject"
                  :disabled="!rejectReason.trim() || isLoading"
                >
                  <span v-if="isLoading" class="flex items-center">
                    <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                  </span>
                  <span v-else>Confirm Rejection</span>
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
import { ref, computed } from 'vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { X } from 'lucide-vue-next';
import { useUserStore } from '@/stores/user';
import { message } from 'ant-design-vue';
import { useAdminStore } from '@/stores/admin';

const adminStore = useAdminStore();
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
  transaction: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['close', 'update:transaction']);

const userStore = useUserStore();
const isLoading = ref(false);
const transactionId = ref('');
const showRejectReason = ref(false);
const rejectReason = ref('');

const canApprove = computed(() => {
  return transactionId.value.trim().length > 0;
});

const closeModal = () => {
  if (isLoading.value) return;
  resetForm();
  emit('close');
};

const toggleRejectReason = () => {
  if (showRejectReason.value) {
    rejectReason.value = '';
  }
  showRejectReason.value = !showRejectReason.value;
};

const resetForm = () => {
  transactionId.value = '';
  rejectReason.value = '';
  showRejectReason.value = false;
};

const handleApprove = async () => {
  if (!transactionId.value.trim() || isLoading.value) return;
  
  isLoading.value = true;
  
  try {
    const response = await adminStore.approveTransaction(props.transaction.pk, transactionId.value.trim())
    
    message.success('Transaction approved');
    const updatedTransaction = { 
      ...props.transaction, 
      status: 'completed', 
      approved: true,
      rejected: false,
      transaction_id: transactionId.value.trim()
    };
    
    // Emit the updated transaction first
    emit('update:transaction', updatedTransaction);
    
    // Close the modal after a short delay to show the success message
    setTimeout(() => {
      closeModal();
    }, 300);
  } catch (error) {
    console.error('Error approving transaction:', error);
    const errorMessage = error.response?.data?.detail || error.response?.data?.error || 'Failed to approve transaction. Please try again.';
    message.error(errorMessage);
  } finally {
    isLoading.value = false;
  }
};

const handleReject = async () => {
  if (!rejectReason.value.trim() || isLoading.value) return;
  
  isLoading.value = true;
  
  try {
    const response = await adminStore.rejectTransaction(props.transaction.pk, rejectReason.value.trim())
    
    message.success('Transaction rejected');
    const updatedTransaction = { 
      ...props.transaction, 
      status: 'rejected', 
      approved: false,
      rejected: true,
      rejection_reason: rejectReason.value.trim()
    };
    
    // Emit the updated transaction first
    emit('update:transaction', updatedTransaction);
    
    // Close the modal after a short delay to show the success message
    setTimeout(() => {
      closeModal();
    }, 300);
  } catch (error) {
    console.error('Error rejecting transaction:', error);
    const errorMessage = error.response?.data?.detail || error.response?.data?.error || 'Failed to reject transaction. Please try again.';
    message.error(errorMessage);
  } finally {
    isLoading.value = false;
  }
};
</script>
