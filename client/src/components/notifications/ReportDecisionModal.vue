<template>
  <TransitionRoot as="template" :show="isOpen">
    <Dialog as="div" class="relative z-50">
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
                  class="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  @click="closeModal"
                >
                  <span class="sr-only">Close</span>
                  <X class="h-6 w-6 cursor-pointer" />
                </button>
              </div>

              <!-- Modal content -->
              <div class="sm:flex sm:items-start">
                <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
                  <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                    Report Decision Details
                  </DialogTitle>
                  
                  <div class="mt-4 space-y-4">
                    <!-- Report Reason -->
                    <div v-if="reportDecision?.report?.reason" class="bg-white border border-gray-200 p-4 rounded-md">
                      <h4 class="text-sm font-medium text-gray-500 mb-2">Report Reason</h4>
                      <p class="text-sm text-gray-800">{{ reportDecision.report.reason }}</p>
                    </div>

                    <!-- Decision Details -->
                    <div class="bg-gray-50 p-4 rounded-md">
                      <h4 class="text-sm font-medium text-gray-500 mb-3">Decision Information</h4>
                      <dl class="grid grid-cols-1 gap-x-4 gap-y-3 sm:grid-cols-2">
                        <div>
                          <dt class="text-xs font-medium text-gray-500">Decision Date</dt>
                          <dd class="mt-1 text-sm text-gray-900">
                            {{ reportDecision?.formatted_created_at }} ({{ reportDecision?.created_since }})
                          </dd>
                        </div>
                        <div class="sm:col-span-2">
                          <dt class="text-xs font-medium text-gray-500">Status</dt>
                          <dd class="mt-1">
                            <span 
                              class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                              :class="{
                                'bg-green-100 text-green-800': reportDecision?.approved,
                                'bg-red-100 text-red-800': reportDecision?.rejected,
                                'bg-yellow-100 text-yellow-800': !reportDecision?.approved && !reportDecision?.rejected
                              }"
                            >
                              {{ reportDecision?.approved ? 'Approved' : reportDecision?.rejected ? 'Rejected' : 'Pending' }}
                            </span>
                          </dd>
                        </div>
                        <div v-if="reportDecision?.reason" class="sm:col-span-2">
                          <dt class="text-xs font-medium text-gray-500">Reason</dt>
                          <dd class="mt-1 text-sm text-gray-900">{{ reportDecision.reason }}</dd>
                        </div>
                        <!-- Appeal Section -->
                        <div v-if="reportDecision?.report?.about_user == userStore.user.id" class="sm:col-span-2 pt-3">
                          <div v-if="isLoadingAppeals" class="text-sm text-gray-500">
                            Loading appeal information... 
                          </div>
                          <template v-else>
                            <!-- Show existing appeal if any -->
                            <div v-if="existingAppeals.length > 0" class="space-y-4">
                              <div v-for="appeal in existingAppeals" :key="appeal.id" class="border rounded-md p-4 bg-gray-50">
                                <div class="flex justify-between items-start">
                                  <h4 class="text-sm font-medium text-gray-700">Your Appeal</h4>
                                  <span 
                                    class="px-2 py-1 text-xs font-medium rounded-full"
                                    :class="{
                                      'bg-yellow-100 text-yellow-800': !appeal.decisions?.length,
                                      'bg-green-100 text-green-800': appeal.decisions?.some(d => d.approved),
                                      'bg-red-100 text-red-800': appeal.decisions?.some(d => d.rejected)
                                    }"
                                  >
                                    {{ !appeal.decisions?.length ? 'Pending' : 
                                       appeal.decisions.some(d => d.approved) ? 'Approved' : 'Rejected' }}
                                  </span>
                                </div>
                                <p class="mt-2 text-sm text-gray-600">{{ appeal.message }}</p>
                                <div v-if="appeal.decisions?.length > 0" class="mt-3 pt-3 border-t border-gray-200">
                                  <h5 class="text-xs font-medium text-gray-500 mb-1">Decision</h5>
                                  <p class="text-sm text-gray-700">{{ appeal.decisions[0].reason || 'No reason provided' }}</p>
                                  <p class="text-xs text-gray-500 mt-1">
                                    Decided {{ appeal.decisions[0].created_since }}
                                  </p>
                                </div>
                                <p class="text-xs text-gray-500 mt-3">
                                  Submitted {{ appeal.created_since }}
                                </p>
                              </div>
                            </div>
                            
                            <!-- Show appeal form if no existing appeals -->
                            <template v-else>
                              <div v-if="reportDecision?.from_appeal">
                                <button
                                  class="text-sm text-gray-600 hover:text-gray-800 focus:outline-none cursor-pointer"
                                >
                                  Reply to your previous Appeal
                                </button>
                              </div>
                              <div v-else-if="!showAppealForm">
                                <button
                                  @click="showAppealForm = true"
                                  class="text-sm text-indigo-600 hover:text-indigo-800 focus:outline-none cursor-pointer"
                                >
                                  Submit an Appeal
                                </button>
                              </div>
                              <div v-else class="space-y-2">
                                <label for="appeal-message" class="block text-sm font-medium text-gray-700">Appeal Message</label>
                                <textarea
                                  id="appeal-message"
                                  v-model="appealMessage"
                                  rows="3"
                                  class="mt-1 px-4 py-2 placeholder-gray-500 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                                  placeholder="Please explain why you're appealing this decision..."
                                ></textarea>
                                <div class="flex space-x-2">
                                  <button
                                    @click="submitAppeal"
                                    :disabled="isSubmittingAppeal"
                                    class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                                  >
                                    <span v-if="isSubmittingAppeal">Submitting...</span>
                                    <span v-else>Submit Appeal</span>
                                  </button>
                                  <button
                                    @click="showAppealForm = false"
                                    class="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                  >
                                    Cancel
                                  </button>
                                </div>
                              </div>
                            </template>
                          </template>
                        </div>
                      </dl>
                    </div>

                    <!-- Post Details -->
                    <div v-if="reportDecision?.report?.reported_post" class="bg-white border border-gray-200 rounded-lg overflow-hidden">
                      <div class="p-4 border-b border-gray-200">
                        <h4 class="text-sm font-medium text-gray-500 mb-3">Reported Post</h4>
                        <!-- Post Header -->
                        <div class="flex items-start space-x-3">
                          <div v-if="reportDecision.report.reported_post.posted_by?.profile_picture" class="flex-shrink-0 h-10 w-10 rounded-full overflow-hidden">
                            <img 
                              :src="reportDecision.report.reported_post.posted_by.profile_picture" 
                              :alt="reportDecision.report.reported_post.posted_by.name"
                              class="h-full w-full object-cover"
                            />
                          </div>
                          <div v-else class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-sm text-gray-600">
                            {{ reportDecision.report.reported_post.posted_by?.name ? reportDecision.report.reported_post.posted_by.name.charAt(0).toUpperCase() : 'U' }}
                          </div>
                          <div class="flex-1 min-w-0">
                            <p class="text-sm font-medium text-gray-900 truncate">
                              {{ reportDecision.report.reported_post.posted_by?.name || 'Anonymous' }}
                            </p>
                            <p class="text-xs text-gray-500">
                              {{ reportDecision.report.reported_post.formatted_created_at }}
                            </p>
                          </div>
                        </div>
                        
                        <!-- Post Content -->
                        <div class="mt-3 text-sm text-gray-800">
                          {{ reportDecision.report.reported_post.description }}
                        </div>
                        
                        <!-- Post Image -->
                        <div v-if="reportDecision.report.reported_post.image_url" class="mt-3">
                          <img 
                            :src="reportDecision.report.reported_post.image_url" 
                            alt="Post content"
                            class="max-h-64 w-auto rounded-md cursor-pointer hover:opacity-90 transition-opacity"
                            @click="openImage(reportDecision.report.reported_post.image_url)"
                          />
                        </div>
                        
                        <!-- Post Stats -->
                        <div class="mt-3 flex items-center space-x-4 text-sm text-gray-500">
                          <div class="flex items-center space-x-1">
                            <Heart class="h-4 w-4" :class="{ 'fill-red-500 text-red-500': reportDecision.report.reported_post.liked }" />
                            <span>{{ reportDecision.report.reported_post.likes || 0 }}</span>
                          </div>
                          <div class="flex items-center space-x-1">
                            <MessageCircle class="h-4 w-4" />
                            <span>{{ reportDecision.report.reported_post.comments || 0 }}</span>
                          </div>
                          <div class="flex items-center space-x-1">
                            <Eye class="h-4 w-4" />
                            <span>{{ reportDecision.report.reported_post.views || 0 }}</span>
                          </div>
                        </div>
                        
                        <!-- Payment Info if exists -->
                        <div v-if="reportDecision.report.reported_post.payment_info_list?.length > 0" class="mt-3 pt-3 border-t border-gray-100">
                          <h5 class="text-xs font-medium text-gray-500 mb-2">Payment Information</h5>
                          <div class="space-y-2">
                            <div v-for="(payment, index) in reportDecision.report.reported_post.payment_info_list" :key="index" class="bg-gray-50 p-2 rounded text-xs">
                              <p><span class="font-medium">Method:</span> {{ payment.method }}</p>
                              <p><span class="font-medium">Account:</span> {{ payment.account }}</p>
                              <p v-if="payment.nameOnAccount"><span class="font-medium">Name:</span> {{ payment.nameOnAccount }}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Transaction Details -->
                    <div v-if="reportDecision?.report?.reported_transaction" class="bg-gray-50 p-4 rounded-md">
                      <h4 class="text-sm font-medium text-gray-500 mb-3">Transaction Details</h4>
                      <div class="grid grid-cols-1 gap-x-4 gap-y-3 sm:grid-cols-2">
                        <div>
                          <dt class="text-xs font-medium text-gray-500">Transaction ID</dt>
                          <dd class="mt-1 text-sm text-gray-900">{{ reportDecision.report.reported_transaction.pk }}</dd>
                        </div>
                        <div>
                          <dt class="text-xs font-medium text-gray-500">Product</dt>
                          <dd class="mt-1 text-sm text-gray-900">{{ reportDecision.report.reported_transaction.product_name }}</dd>
                        </div>
                        <div>
                          <dt class="text-xs font-medium text-gray-500">Amount</dt>
                          <dd class="mt-1 text-sm text-gray-900">
                            {{ Intl.NumberFormat().format(reportDecision.report.reported_transaction.total_amount) }} {{ reportDecision.report.reported_transaction.currency }}
                          </dd>
                        </div>
                        <div>
                          <dt class="text-xs font-medium text-gray-500">Connects</dt>
                          <dd class="mt-1 text-sm text-gray-900">{{ Intl.NumberFormat().format(reportDecision.report.reported_transaction.connects) }}</dd>
                        </div>
                        <div>
                          <dt class="text-xs font-medium text-gray-500">Payment Method</dt>
                          <dd class="mt-1 text-sm text-gray-900">{{ reportDecision.report.reported_transaction.method }}</dd>
                        </div>
                        <div>
                          <dt class="text-xs font-medium text-gray-500">Status</dt>
                          <dd class="mt-1">
                            <span 
                              class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                              :class="{
                                'bg-green-100 text-green-800': reportDecision.report.reported_transaction.approved,
                                'bg-yellow-100 text-yellow-800': !reportDecision.report.reported_transaction.approved
                              }"
                            >
                              {{ reportDecision.report.reported_transaction.status }}
                            </span>
                          </dd>
                        </div>
                        <div class="sm:col-span-2">
                          <dt class="text-xs font-medium text-gray-500">Created</dt>
                          <dd class="mt-1 text-sm text-gray-900">
                            {{ reportDecision.report.reported_transaction.formatted_created_at }} ({{ reportDecision.report.reported_transaction.time_ago }})
                          </dd>
                        </div>
                        <div v-if="reportDecision.report.reported_transaction.screenshot_url" class="sm:col-span-2">
                          <dt class="text-xs font-medium text-gray-500 mb-1">Payment Proof</dt>
                          <dd class="mt-1">
                            <img 
                              :src="reportDecision.report.reported_transaction.screenshot_url" 
                              alt="Payment proof" 
                              class="h-40 w-auto object-contain border rounded-md"
                              @click="openImage(reportDecision.report.reported_transaction.screenshot_url)"
                              
                            />
                          </dd>
                        </div>
                      </div>
                    </div>
                    <!-- Connection Details -->
                    <div v-if="reportDecision?.report?.reported_connection" class="bg-white border border-gray-200 rounded-lg overflow-hidden">
                      <div class="p-4 border-b border-gray-200">
                        <h4 class="text-sm font-medium text-gray-500 mb-3">Reported Connection</h4>
                        
                        <!-- Initiating User -->
                        <div class="flex items-start space-x-3 mb-4">
                          <div v-if="reportDecision.report.reported_connection.initiating_user.profile_picture" class="flex-shrink-0 h-10 w-10 rounded-full overflow-hidden">
                            <img 
                              :src="reportDecision.report.reported_connection.initiating_user.profile_picture" 
                              :alt="reportDecision.report.reported_connection.initiating_user.name || 'User'"
                              class="h-full w-full object-cover"
                            />
                          </div>
                          <div v-else class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-sm text-gray-600">
                            {{ (connectionStore.getOtherUser(reportDecision.report.reported_connection, userStore.user)?.name || 'U').charAt(0).toUpperCase() }}
                          </div>
                          <div class="flex-1 min-w-0">
                            <p class="text-sm font-medium text-gray-900">
                              {{ connectionStore.getOtherUser(reportDecision.report.reported_connection, userStore.user)?.name || 'User' }}
                              <span class="text-xs font-normal text-gray-500">
                                @{{ connectionStore.getOtherUser(reportDecision.report.reported_connection, userStore.user)?.username }}
                              </span>
                            </p>
                          </div>
                        </div>
                        
                        <!-- Connection Message Component -->
                        <ConnectionMessage 
                          :connection="reportDecision.report.reported_connection"
                          :processing="false"
                          :show-requested-by="false"
                        />
                      </div>
                    </div>

                    <!-- Close Button -->
                    <div class="mt-5 sm:mt-6">
                      <button
                        type="button"
                        class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:text-sm cursor-pointer"
                        @click="closeModal"
                      >
                        Close
                      </button>
                    </div>

                  </div>
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
import { ref, onMounted  } from 'vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { X, Eye, MessageCircle, Heart } from 'lucide-vue-next';
import { api } from '@/main';
import { message } from 'ant-design-vue';
import { useUserStore } from '@/stores/user';
import { useConnectionStore } from '@/stores/connection';
import ConnectionMessage from '@/components/ConnectionMessage.vue';
const connectionStore = useConnectionStore();
const userStore = useUserStore();
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
  reportDecision: {
    type: Object,
    default: () => ({
      report: {
        reported_transaction: {}
      }
    })
  },
});

const emit = defineEmits(['close']);
console.log("userStore.user.id", userStore.user.id);
console.log("reportDecision?.report?.about_user", props.reportDecision?.report?.about_user);
console.log("is same", userStore.user.id == props.reportDecision?.report?.about_user);
const isSubmittingAppeal = ref(false);
const isLoadingAppeals = ref(false);
const showAppealForm = ref(false);
const appealMessage = ref('');
const existingAppeals = ref([]);

const fetchMyAppeals = async () => {
  if (!props.reportDecision?.id) return;
  
  isLoadingAppeals.value = true;
  try {
    const response = await api.get(`/report/report-decisions/${props.reportDecision.id}/my_appeals/`);
    existingAppeals.value = response.data;
  } catch (error) {
    console.error('Error fetching appeals:', error);
    message.error('Failed to load appeal information');
  } finally {
    isLoadingAppeals.value = false;
  }
};

// Fetch appeals when modal opens
onMounted(async () => {
    await fetchMyAppeals();
});

const closeModal = () => {
  emit('close');
};

const openImage = (url) => {
  window.open(url, '_blank');
};

const submitAppeal = async () => {
  if (!appealMessage.value.trim()) {
    message.warning('Please enter a message for your appeal');
    return;
  }

  try {
    isSubmittingAppeal.value = true;
    await api.post(`/report/report-decisions/${props.reportDecision.id}/submit_appeal/`, {
      message: appealMessage.value
    });
    
    message.success('Appeal submitted successfully');
    showAppealForm.value = false;
    // Refresh the appeals list
    await fetchMyAppeals();
    appealMessage.value = '';
  } catch (error) {
    console.error('Error submitting appeal:', error);
    message.error('Failed to submit appeal. Please try again.');
  } finally {
    isSubmittingAppeal.value = false;
  }
};
</script>