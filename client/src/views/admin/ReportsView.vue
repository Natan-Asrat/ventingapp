<template>
  <!-- Appeals Modal Component -->
  <AppealsModal
    v-if="isAppealsModalOpen"
    :is-open="isAppealsModalOpen"
    :decision-id="selectedDecisionId"
    @close="closeAppealsModal"
  />

  <!-- Decision Modal Component -->
  <DecisionModal
    v-if="isDecisionModalOpen"
    :is-open="isDecisionModalOpen"
    :report-id="selectedReportId"
    @close="closeDecisionModal"
    @approve="handleApprove"
    @reject="handleReject"
  />

  <div class="space-y-6">
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-medium text-gray-900 mb-6">Reports</h2>
      
      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500"></div>
      </div>

      <!-- Reports List -->
      <div v-else class="space-y-6">
        <div v-if="reports.length === 0" class="text-center py-8 text-gray-500">
          No reports found
        </div>

        <div v-for="report in reports" :key="report.id" class="border border-gray-200 rounded-lg overflow-hidden">
          <!-- Report Header -->
          <div class="bg-gray-50 px-4 py-3 border-b border-gray-200">
            <div class="flex justify-between items-start">
              <div>
                <h3 class="text-sm font-medium text-gray-900">
                  Report #{{ report.id }} <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium" 
                      :class="{
                        'bg-green-100 text-green-800': report.report_type === 'transaction',
                        'bg-blue-100 text-blue-800': report.report_type === 'post',
                        'bg-purple-100 text-purple-800': report.report_type === 'connection',
                        'bg-gray-100 text-gray-800': !['transaction', 'post', 'connection'].includes(report.report_type)
                      }">
                  {{ capitalize(report.report_type) }}
                </span>
                </h3>
                <p class="text-xs text-gray-500 mt-1">
                  Created {{ report.created_since }} • 
                  <span :class="{
                    'text-green-600': report.active,
                    'text-red-600': !report.active
                  }">
                    {{ report.active ? 'Active' : 'Inactive' }}
                  </span>
                </p>
              </div>
              <div class="flex flex-col space-y-2 items-end">
                <div class="flex space-x-2">
                  <button
                    v-if="!report.concluded && !report.dismissed"
                    @click="openDecisionModal(report.id)"
                    class="inline-flex cursor-pointer items-center px-3 py-1 border border-transparent text-xs font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Decide
                  </button>
                  <button
                    v-if="!report.concluded && !report.dismissed"
                    @click="handleDismiss(report.id)"
                    class="inline-flex cursor-pointer items-center px-3 py-1 border border-gray-300 text-xs font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Dismiss
                  </button>
                  <span 
                    v-if="report.concluded"
                    class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
                  >
                    Decided
                  </span>
                  <span 
                    v-else-if="report.dismissed"
                    class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
                  >
                    Dismissed
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Report Content -->
          <div class="p-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <!-- Report Details -->
              <div class="md:col-span-2 space-y-4">
                <div>
                  <h4 class="text-sm font-medium text-gray-500">Reason</h4>
                  <p class="mt-1 text-sm text-gray-900">{{ report.reason || 'No reason provided' }}</p>
                </div>

                <!-- Transaction Details -->
                <div v-if="report.reported_transaction" class="border-t border-gray-200 pt-4">
                  <h4 class="text-sm font-medium text-gray-500 mb-2">Transaction Details</h4>
                  <div class="grid grid-cols-2 gap-2 text-sm">
                    <div>
                      <span class="text-gray-500">Amount:</span>
                      <span class="ml-2 font-medium">
                        {{ Intl.NumberFormat().format(report.reported_transaction.total_amount) }} {{ report.reported_transaction.currency }}
                      </span>
                    </div>
                    <div>
                      <span class="text-gray-500">Status:</span>
                      <span class="ml-2 font-medium">
                        {{ report.reported_transaction.status }}
                      </span>
                    </div>
                    <div class="col-span-2">
                      <span class="text-gray-500">Created:</span>
                      <span class="ml-2">{{ report.reported_transaction.time_ago }}</span>
                    </div>
                  </div>
                </div>

                <!-- Post Details -->
                <!-- Message Details -->
                <div v-else-if="report.reported_message" class="border-t border-gray-200 pt-4">
                  <h4 class="text-sm font-medium text-gray-500 mb-2">Reported Message</h4>
                  <div class="space-y-4 text-left">
                    <!-- Message Header -->
                    <div class="flex items-start space-x-3">
                      <!-- Sender Avatar -->
                      <div v-if="report.reported_message.user?.profile_picture" class="h-10 w-10 rounded-full overflow-hidden flex-shrink-0">
                        <img 
                          :src="report.reported_message.user.profile_picture" 
                          :alt="report.reported_message.user.name"
                          class="h-full w-full object-cover"
                        />
                      </div>
                      <div v-else class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-sm text-gray-600 flex-shrink-0">
                        {{ report.reported_message.user?.name ? report.reported_message.user.name.charAt(0).toUpperCase() : 'U' }}
                      </div>
                      
                      <!-- Sender Info -->
                      <div class="flex-1 min-w-0">
                        <div class="flex items-center space-x-2">
                          <span class="text-sm font-medium text-gray-900 truncate">
                            {{ report.reported_message.user?.name || 'Unknown User' }}
                          </span>
                          <span class="text-xs text-gray-500">
                            @{{ report.reported_message.user?.username || 'user' }}
                          </span>
                        </div>
                          <!-- Main Message Content -->
                        <div v-if="report.reported_message.message" class="text-sm text-gray-800">
                          {{ report.reported_message.message }}
                        </div>
                      </div>
                    </div>

                    <!-- Message Content -->
                    <div class="pl-13 -mt-2 space-y-3">
                      <!-- Reply To -->
                      <div v-if="report.reported_message.reply_to" class="bg-gray-50 rounded-lg p-2 text-xs border border-gray-100">
                        <div class="flex items-center text-gray-500 mb-1">
                          <Reply class="h-3 w-3 mr-1" />
                          <span>Replying to @{{ report.reported_message.reply_to.user?.username || 'user' }}</span>
                        </div>
                        <p class="text-gray-700 truncate">{{ report.reported_message.reply_to.message || 'No message content' }}</p>
                      </div>

                      <!-- Forwarded From -->
                      <div v-if="report.reported_message.forwarded_from" class="bg-blue-50 rounded-lg p-2 text-xs border border-blue-100">
                        <div class="flex items-center text-blue-600 mb-1">
                          <Forward class="h-3 w-3 mr-1" />
                          <span>Forwarded from @{{ report.reported_message.forwarded_from.user?.username || 'user' }}</span>
                        </div>
                        <p class="text-gray-700">{{ report.reported_message.forwarded_from.message || 'No message content' }}</p>
                      </div>

                      

                      <!-- Shared Post -->
                      <div v-if="report.reported_message.shared_post" class="border border-gray-200 rounded-lg overflow-hidden">
                        <div class="p-3 bg-gray-50 border-b border-gray-100">
                          <div class="flex items-center space-x-2">
                            <FileText class="h-4 w-4 text-gray-500" />
                            <span class="text-xs font-medium text-gray-700">Shared Post</span>
                          </div>
                        </div>
                        <div class="p-3">
                          <div class="flex items-center space-x-2 mb-2">
                            <div v-if="report.reported_message.shared_post.posted_by?.profile_picture" class="h-6 w-6 rounded-full overflow-hidden">
                              <img 
                                :src="report.reported_message.shared_post.posted_by.profile_picture" 
                                :alt="report.reported_message.shared_post.posted_by.name"
                                class="h-full w-full object-cover"
                              />
                            </div>
                            <div v-else class="h-6 w-6 rounded-full bg-gray-200 flex items-center justify-center text-xs text-gray-600">
                              {{ report.reported_message.shared_post.posted_by?.name ? report.reported_message.shared_post.posted_by.name.charAt(0).toUpperCase() : 'U' }}
                            </div>
                            <span class="text-xs font-medium">{{ report.reported_message.shared_post.posted_by?.name || 'User' }}</span>
                          </div>
                          
                          <ShowMore :text="report.reported_message.shared_post.description" />
                          
                          <!-- Post Image -->
                          <div v-if="report.reported_message.shared_post.image_url" class="mt-3 rounded-lg overflow-hidden">
                            <img 
                              :src="report.reported_message.shared_post.image_url" 
                              :alt="'Post by ' + (report.reported_message.shared_post.posted_by?.username || 'user')" 
                              class="w-full h-auto object-cover cursor-zoom-in"
                              @load="$emit('image-loaded')"
                            />
                          </div>
                          
                          <!-- Payment Info -->
                          <div v-if="report.reported_message.shared_post.payment_info_list?.length > 0" class="mt-2 pt-2 border-t border-gray-100">
                            <div v-for="(payment, index) in report.reported_message.shared_post.payment_info_list" :key="index" class="text-xs bg-gray-50 p-2 rounded">
                              <div class="grid grid-cols-2 gap-1">
                                <span class="text-gray-500">Method:</span>
                                <span class="font-medium">{{ payment.method }}</span>
                                <span class="text-gray-500">Account:</span>
                                <span class="font-mono">{{ payment.account }}</span>
                                <span v-if="payment.nameOnAccount" class="text-gray-500">Name:</span>
                                <span v-if="payment.nameOnAccount" class="font-medium">{{ payment.nameOnAccount }}</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- No Content Message -->
                      <div v-if="!report.reported_message.message && !report.reported_message.shared_post" class="text-sm text-gray-500 italic">
                        No message content
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Post Details -->
                <div v-else-if="report.reported_post" class="border-t border-gray-200 pt-4">
                  <h4 class="text-sm font-medium text-gray-500 mb-2">Post Details</h4>
                  <div class="space-y-3">
                    <!-- Post Author -->
                    <div class="flex items-center space-x-2">
                      <div v-if="report.reported_post.posted_by?.profile_picture" class="h-8 w-8 rounded-full overflow-hidden">
                        <img 
                          :src="report.reported_post.posted_by.profile_picture" 
                          :alt="report.reported_post.posted_by.name"
                          class="h-full w-full object-cover"
                        />
                      </div>
                      <div v-else class="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center text-xs text-gray-600">
                        {{ report.reported_post.posted_by?.name ? report.reported_post.posted_by.name.charAt(0).toUpperCase() : 'U' }}
                      </div>
                      <div>
                        <p class="text-sm font-medium">{{ report.reported_post.posted_by?.name || 'Anonymous' }}</p>
                        <p class="text-xs text-gray-500">{{ report.reported_post.formatted_created_at }}</p>
                      </div>
                    </div>

                    <!-- Post Content -->
                    <div class="text-sm text-gray-800">
                      {{ report.reported_post.description }}
                    </div>

                    <!-- Post Image -->
                    <div v-if="report.reported_post.image" class="mt-2">
                      <img 
                        :src="report.reported_post.image" 
                        :alt="'Post by ' + (report.reported_post.posted_by?.name || 'user')"
                        class="max-h-64 w-auto rounded-lg object-cover"
                        @click="openImageModal(report.reported_post.image)"
                        @error="handleImageError"
                      />
                    </div>

                    <!-- Post Stats -->
                    <div class="flex items-center space-x-4 text-xs text-gray-500 pt-2">
                      <div class="flex items-center space-x-1">
                        <Heart class="h-4 w-4" />
                        <span>{{ report.reported_post.likes || 0 }} likes</span>
                      </div>
                      <div class="flex items-center space-x-1">
                        <MessageCircle class="h-4 w-4" />
                        <span>{{ report.reported_post.comments || 0 }} comments</span>
                      </div>
                      <div class="flex items-center space-x-1">
                        <Eye class="h-4 w-4" />
                        <span>{{ report.reported_post.views || 0 }} views</span>
                      </div>
                    </div>

                    <!-- Payment Info if exists -->
                    <div v-if="report.reported_post.payment_info_list?.length > 0" class="mt-2 pt-2 border-t border-gray-100">
                      <h5 class="text-xs font-medium text-gray-500 mb-1">Payment Info:</h5>
                      <div v-for="(payment, index) in report.reported_post.payment_info_list" :key="index" class="text-xs bg-gray-50 p-2 rounded">
                        <div class="grid grid-cols-2 gap-1">
                          <span class="text-gray-500">Method:</span>
                          <span class="font-medium">{{ payment.method }}</span>
                          <span class="text-gray-500">Account:</span>
                          <span class="font-mono">{{ payment.account }}</span>
                          <span v-if="payment.nameOnAccount" class="text-gray-500">Name:</span>
                          <span v-if="payment.nameOnAccount" class="font-medium">{{ payment.nameOnAccount }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Decisions -->
              <div class="border-t border-gray-200 pt-4 md:border-t-0 md:border-l md:pl-4">
                <h4 class="text-sm font-medium text-gray-500 mb-2">Decisions</h4>
                <div v-if="report.decisions && report.decisions.length > 0" class="space-y-3">
                  <div v-for="decision in report.decisions" :key="decision.id" class="text-sm flex flex-col">
                    <div class="flex justify-between items-start">
                      <div>
                        <span class="font-medium">
                          {{ decision.approved ? 'Approved' : decision.rejected ? 'Rejected' : 'Pending' }}
                        </span>
                        <p v-if="decision.reason" class="text-gray-600 text-xs">
                          {{ decision.reason }}
                        </p>
                      </div>
                      <div class="flex items-center space-x-2">
                        <span class="text-xs text-gray-500">{{ decision.created_since }}</span>
                        
                      </div>
                    </div>
                    <button 
                          v-if="decision.has_appeals"
                          @click="openAppealsModal(decision.id)"
                          class="inline-flex mt-2 w-fit cursor-pointer py-2 px-4 items-center px-2 py-1 text-xs font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                          View Appeals
                        </button>
                  </div>
                  
                </div>
                <p v-else class="text-sm text-gray-500">No decisions yet</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { api } from '@/main';
import { MessageCircle, Forward, Eye, Heart, Reply, FileText, User, Image as ImageIcon, AlertCircle } from 'lucide-vue-next';
import AppealsModal from '@/components/admin/AppealsModal.vue';
import DecisionModal from '@/components/admin/DecisionModal.vue';
import ShowMore from '@/components/ShowMore.vue';

const reports = ref([]);
const isLoading = ref(true);
const error = ref(null);

// Modals state
const isAppealsModalOpen = ref(false);
const isDecisionModalOpen = ref(false);
const isImageModalOpen = ref(false);
const selectedImageUrl = ref('');
const selectedDecisionId = ref(null);
const selectedReportId = ref(null);
const decisionReason = ref('');
const isSubmitting = ref(false);

// Modal handlers
const openAppealsModal = (decisionId) => {
  selectedDecisionId.value = decisionId;
  isAppealsModalOpen.value = true;
};

const closeAppealsModal = () => {
  isAppealsModalOpen.value = false;
  selectedDecisionId.value = null;
};

// Image modal handlers
const openImageModal = (imageUrl) => {
  selectedImageUrl.value = imageUrl;
  isImageModalOpen.value = true;
};

const closeImageModal = () => {
  isImageModalOpen.value = false;
  selectedImageUrl.value = '';
};

const handleImageError = (e) => {
  e.target.style.display = 'none';
};

const openDecisionModal = (reportId) => {
  selectedReportId.value = reportId;
  isDecisionModalOpen.value = true;
};

const closeDecisionModal = () => {
  isDecisionModalOpen.value = false;
  selectedReportId.value = null;
  decisionReason.value = '';
};

// API Handlers
const handleDismiss = async (reportId) => {
  if (confirm('Are you sure you want to dismiss this report?')) {
    try {
      await api.post(`/report/reports/${reportId}/dismiss/`);
      await fetchReports(); // Refresh the reports list
    } catch (error) {
      console.error('Error dismissing report:', error);
      alert('Failed to dismiss report. Please try again.');
    }
  }
};

const handleApprove = async ({ reason }) => {
  if (!selectedReportId.value) return;

  try {
    await api.post(`/report/reports/${selectedReportId.value}/approve/`, { reason });
    await fetchReports(); // Refresh the reports list
  } catch (error) {
    console.error('Error approving report:', error);
    alert('Failed to approve report. Please try again.');
    throw error; // Re-throw to let the modal handle the loading state
  }
};

const handleReject = async ({ reason }) => {
  if (!selectedReportId.value) return;

  try {
    await api.post(`/report/reports/${selectedReportId.value}/reject/`, { reason });
    await fetchReports(); // Refresh the reports list
  } catch (error) {
    console.error('Error rejecting report:', error);
    alert('Failed to reject report. Please try again.');
    throw error; // Re-throw to let the modal handle the loading state
  }
};

const fetchReports = async () => {
  try {
    isLoading.value = true;
    const response = await api.get('/report/reports/');
    reports.value = response.data;
  } catch (err) {
    console.error('Error fetching reports:', err);
    error.value = 'Failed to load reports. Please try again later.';
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchReports();
});

// Filter to capitalize first letter
const capitalize = (value) => {
  if (!value) return '';
  return value.charAt(0).toUpperCase() + value.slice(1);
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const options = { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  };
  return new Date(dateString).toLocaleDateString(undefined, options);
};
</script>