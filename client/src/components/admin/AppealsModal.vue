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
            <DialogPanel class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-2xl sm:p-6">
              <!-- Close button -->
              <div class="absolute top-0 right-0 pt-4 pr-4">
                <button
                  type="button"
                  class="bg-white cursor-pointer rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  @click="closeModal"
                >
                  <span class="sr-only">Close</span>
                  <X class="h-6 w-6" />
                </button>
              </div>

              <!-- Modal content -->
              <div class="sm:flex sm:items-start">
                <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
                  <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                    Appeals for Decision #{{ decisionId }}
                  </DialogTitle>
                  
                  <div class="mt-4 space-y-4">
                    <div v-if="isLoading" class="flex justify-center py-4">
                      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-500"></div>
                    </div>
                    <div v-else-if="appeals.length === 0" class="text-center py-4 text-gray-500">
                      No appeals found for this decision.
                    </div>
                    <div v-else v-for="appeal in appeals" :key="appeal.id" class="border border-gray-200 rounded-lg p-4">
                      <div class="flex justify-between items-start">
                        <div class="flex-1">
                          <div class="flex items-center justify-between">
                            <div class="flex items-center">
                              <div v-if="appeal.submitted_by?.profile_picture" class="h-8 w-8 rounded-full overflow-hidden mr-2">
                                <img :src="appeal.submitted_by.profile_picture" :alt="appeal.submitted_by.username" class="h-full w-full object-cover">
                              </div>
                              <div class="flex-1 min-w-0">
                                <p class="text-sm font-medium text-gray-900 truncate">
                                  {{ appeal.submitted_by?.name || appeal.submitted_by?.username || 'Unknown User' }}
                                </p>
                                <p class="text-xs text-gray-500 truncate">
                                  @{{ appeal.submitted_by?.username }}
                                </p>
                              </div>
                            </div>
                            <button
                              @click="toggleDecisionForm(appeal.id)"
                              class="inline-flex cursor-pointer items-center px-2.5 py-1 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                            >
                              {{ selectedAppealId === appeal.id ? 'Cancel' : 'Decide' }}
                            </button>
                          </div>
                          <p class="mt-1 text-sm text-gray-600">{{ appeal.message }}</p>
                          <p class="mt-2 text-xs text-gray-500">
                            {{ appeal.created_since }}
                          </p>
                        </div>
                      </div>
                      
                      <!-- Appeal Decisions -->
                      <!-- Decision Form -->
                      <div v-if="selectedAppealId == appeal.id && showDecisionForm" class="mt-4 border-t pt-4">
                        <div class="space-y-4">
                          <div>
                            <label for="decision-reason" class="block text-sm font-medium text-gray-700 mb-1">Reason for decision</label>
                            <textarea
                              id="decision-reason"
                              v-model="decisionReason"
                              rows="3"
                              class="shadow-sm placeholder-gray-500 focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border border-gray-300 rounded-md p-2"
                              placeholder="Enter the reason for your decision"
                            ></textarea>
                          </div>
                          <div class="flex justify-end space-x-3">
                            <button
                              type="button"
                              @click="handleReject"
                              :disabled="isSubmitting"
                              class="inline-flex cursor-pointer items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                            >
                              <span v-if="isSubmitting && selectedAppealId === appeal.id" class="animate-spin mr-2">↻</span>
                              Reject
                            </button>
                            <button
                              type="button"
                              @click="handleApprove"
                              :disabled="isSubmitting"
                              class="inline-flex cursor-pointer items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                            >
                              <span v-if="isSubmitting && selectedAppealId === appeal.id" class="animate-spin mr-2">↻</span>
                              Approve
                            </button>
                          </div>
                        </div>
                      </div>

                      <!-- Existing Decisions -->
                      <div v-if="appeal.decisions && appeal.decisions.length > 0" class="mt-4 border-t pt-4">
                        <h4 class="text-sm font-medium text-gray-700 mb-2">Decisions</h4>
                        <div v-for="decision in appeal.decisions" :key="decision.id" class="mt-2 p-3 rounded-md" 
                          :class="[
                            decision.approved ? 'bg-green-50 border border-green-200' :
                            decision.rejected ? 'bg-red-50 border border-red-200' :
                            'bg-yellow-50 border border-yellow-200'
                      ]">
                          <div class="flex justify-between items-start">
                            <div>
                              <p class="text-sm font-medium">
                                {{ decision.approved === true ? 'Approved' : 
                                   decision.rejected ? 'Rejected' : 'Pending' }}
                              </p>
                              <div class="flex items-center mt-1">
                                <div v-if="decision.decision_maker?.profile_picture" class="h-5 w-5 rounded-full overflow-hidden mr-1">
                                  <img :src="decision.decision_maker.profile_picture" :alt="decision.decision_maker.username" class="h-full w-full object-cover">
                                </div>
                                <p class="text-xs text-gray-500">
                                  {{ decision.decision_maker?.name || decision.decision_maker?.username || 'System' }} • {{ decision.created_since }}
                                </p>
                              </div>

                              <p v-if="decision.reason" class="text-sm text-gray-700 mt-2">{{ decision.reason }}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-5 sm:mt-6">
                <button
                  type="button"
                  class="inline-flex cursor-pointer w-full justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:text-sm"
                  @click="closeModal"
                >
                  Close
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
import { ref, onMounted, watch, computed } from 'vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { X } from 'lucide-vue-next';
import { api } from '@/main';

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  decisionId: {
    type: [String, Number],
    default: null
  }
});

const emit = defineEmits(['close']);

const appeals = ref([]);
const isLoading = ref(false);
const error = ref(null);

// Decision form state
const showDecisionForm = ref(false);
const selectedAppealId = ref(null);
const decisionReason = ref('');
const isSubmitting = ref(false);

// Computed to check if any appeal is being decided
const isDeciding = computed(() => selectedAppealId.value !== null);

const closeModal = () => {
  emit('close');
};

// Fetch appeals when modal is opened and decisionId changes
onMounted(async () => {
  if (props.decisionId) {
    await fetchAppeals(props.decisionId);
  } else {
    appeals.value = [];
  }
});

const fetchAppeals = async (decisionId) => {
  if (!decisionId) return;
  
  isLoading.value = true;
  error.value = null;
  
  try {
    const response = await api.get(`/report/report-decisions/${decisionId}/appeals/`);
    appeals.value = response.data;
  } catch (err) {
    console.error('Error fetching appeals:', err);
    error.value = 'Failed to load appeals. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

const toggleDecisionForm = (appealId) => {
  if (selectedAppealId.value === appealId) {
    // Clicked on the same appeal, toggle the form
    selectedAppealId.value = null;
    showDecisionForm.value = false;
    decisionReason.value = '';
  } else {
    // Clicked on a different appeal, show its form
    selectedAppealId.value = appealId;
    showDecisionForm.value = true;
  }
};

const handleApprove = async () => {
  if (!decisionReason.value.trim()) {
    alert('Please provide a reason for your decision');
    return;
  }

  isSubmitting.value = true;
  try {
    await api.post(`/report/appeals/${selectedAppealId.value}/approve/`, {
      reason: decisionReason.value
    });
    await fetchAppeals(props.decisionId);
    selectedAppealId.value = null;
    showDecisionForm.value = false;
    decisionReason.value = '';
  } catch (error) {
    console.error('Error approving appeal:', error);
    alert('Failed to submit decision. Please try again.');
  } finally {
    isSubmitting.value = false;
  }
};

const handleReject = async () => {
  if (!decisionReason.value.trim()) {
    alert('Please provide a reason for your decision');
    return;
  }

  isSubmitting.value = true;
  try {
    await api.post(`/report/appeals/${selectedAppealId.value}/reject/`, {
      reason: decisionReason.value
    });
    await fetchAppeals(props.decisionId);
    selectedAppealId.value = null;
    showDecisionForm.value = false;
    decisionReason.value = '';
  } catch (error) {
    console.error('Error rejecting appeal:', error);
    alert('Failed to submit decision. Please try again.');
  } finally {
    isSubmitting.value = false;
  }
};
</script>
