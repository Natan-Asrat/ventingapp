<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Desktop Navigation -->
    <desktop-top-nav 
      :user-initials="userInitials"
      @logout="handleLogout"
    />
    
    <!-- Mobile Top Navigation -->
    <mobile-top-nav 
      :user-initials="userInitials"
      user-name="History"
      @logout="handleLogout"
    />
    
    <!-- Main Content -->
    <div class="pt-16 pb-16 md:pt-0 md:pb-0">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="bg-white shadow sm:rounded-lg overflow-hidden">
          <!-- Tabs -->
          <div class="border-b border-gray-200">
            <nav class="flex -mb-px" aria-label="Tabs">
              <button
                v-for="tab in tabs"
                :key="tab.name"
                @click="activeTab = tab.id"
                :class="[
                  activeTab === tab.id
                    ? 'border-indigo-500 text-indigo-600'
                    : 'cursor-pointer border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                  'w-1/3 py-4 px-1 text-center border-b-2 font-medium text-sm'
                ]"
              >
                <div class="flex flex-col items-center">
                  <div class="flex items-center">
                    <span>{{ tab.name }}</span>
                    <span 
                      v-if="tab.count > 0"
                      :class="[
                        activeTab === tab.id ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-600',
                        'ml-2 py-0.5 px-2 rounded-full text-xs font-medium hidden md:block'
                      ]"
                    >
                      {{ tab.count }}
                    </span>
                  </div>
                  <span 
                    v-if="tab.count > 0"
                    :class="[
                      activeTab === tab.id ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-600',
                      'mt-1 py-0.5 px-2 rounded-full text-xs font-medium md:hidden'
                    ]"
                  >
                    {{ tab.count }}
                  </span>
                </div>
              </button>
            </nav>
          </div>

          <!-- Tab Content -->
          <div class="p-4">
            <!-- Transactions Tab -->
            <div v-if="activeTab === 'transactions'" class="space-y-4">
              <div v-if="loading.transactions" class="flex justify-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-500"></div>
              </div>
              
              <div v-else-if="transactions.length === 0" class="text-center py-12 text-gray-500">
                No transactions found.
              </div>
              
              <div v-else class="space-y-4">
                <div v-for="transaction in transactions" :key="transaction.pk" class="border rounded-lg overflow-hidden">
                  <div class="p-4">
                    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start">
                      <div>
                        <h3 class="font-medium text-gray-900">
                          {{ transaction.product_name || 'Transaction' }}
                        </h3>
                        <p class="text-sm text-gray-500">
                          {{ transaction.formatted_created_at }} • {{ transaction.time_ago }}
                        </p>
                      </div>
                      <span 
                        v-if="transaction.status"
                        class="mt-2 sm:mt-0 px-2 py-1 text-xs font-medium rounded-full self-start"
                        :class="{
                          'bg-green-100 text-green-800': transaction.approved,
                          'bg-yellow-100 text-yellow-800': !transaction.approved && !transaction.status.includes('rejected'),
                          'bg-red-100 text-red-800': transaction.status.includes('rejected')
                        }"
                      >
                        {{ transaction.status }}
                      </span>
                      <span 
                        v-else
                        class="mt-2 sm:mt-0 px-2 py-1 text-xs font-medium text-gray-600 bg-gray-100 rounded-full self-start"
                      >
                        Pending
                      </span>
                    </div>
                    
                    <div v-if="transaction.product_name" class="mt-3 pt-3 border-t border-gray-100">
                      <div class="flex items-center justify-between text-sm">
                        <span class="text-gray-500">Connects:</span>
                        <span class="font-medium text-gray-900">
                          {{ transaction.connects || 'N/A' }}
                        </span>
                      </div>
                      <div class="flex items-center justify-between mt-1 text-sm">
                        <span class="text-gray-500">Amount:</span>
                        <span class="font-medium text-gray-900">
                          {{ transaction.total_amount ? `${Number(transaction.total_amount).toLocaleString()} ${(transaction.currency || '').toUpperCase()}` : 'N/A' }}
                        </span>
                      </div>
                      <a 
                        v-if="transaction.screenshot_url" 
                        :href="transaction.screenshot_url" 
                        target="_blank"
                        class="inline-block mt-2 text-indigo-600 hover:text-indigo-800 text-sm font-medium"
                      >
                        View Receipt
                      </a>
                    </div>
                  </div>
                </div>
                
                <!-- Load More Button -->
                <div v-if="transactionsNextUrl" class="flex justify-center mt-6">
                  <button
                    @click="loadMoreTransactions"
                    :disabled="loading.moreTransactions"
                    class="px-4 py-2 cursor-pointer border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                  >
                    <span v-if="loading.moreTransactions">Loading...</span>
                    <span v-else>Load More</span>
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Connections Tab -->
            <div v-else-if="activeTab === 'connections'" class="space-y-4">
              <div v-if="loading.connections" class="flex justify-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-500"></div>
              </div>
              
              <div v-else-if="connections.length === 0" class="text-center py-12 text-gray-500">
                No connections found.
              </div>
              
              <div class="space-y-4">
                <div v-for="connection in connections" :key="connection.id" class="border rounded-lg overflow-hidden">
                  <div class="p-4">
                    <div class="flex flex-col sm:flex-row sm:items-center gap-4">
                      <!-- Profile Section -->
                      <div class="flex items-center flex-1 min-w-0">
                        <!-- Profile Picture -->
                        <div 
                          v-if="connectionStore.getOtherUser(connection, userStore.user)?.profile_picture" 
                          class="flex-shrink-0 h-12 w-12 rounded-full overflow-hidden bg-gray-200"
                        >
                          <img 
                            :src="connectionStore.getOtherUser(connection, userStore.user)?.profile_picture" 
                            :alt="connectionStore.getOtherUser(connection, userStore.user)?.name || 'User'"
                            class="h-full w-full object-cover"
                          />
                        </div>
                        <div v-else class="flex-shrink-0 h-12 w-12 rounded-full bg-indigo-100 flex items-center justify-center">
                          <span class="text-lg font-medium text-indigo-600">
                            {{ connectionStore.getOtherUser(connection, userStore.user)?.name ? connectionStore.getOtherUser(connection, userStore.user)?.name.charAt(0).toUpperCase() : 'U' }}
                          </span>
                        </div>
                        
                        <!-- User Info -->
                        <div class="ml-3 min-w-0">
                          <p class="text-sm font-medium text-gray-900 truncate">
                            {{ connectionStore.getOtherUser(connection, userStore.user)?.name || connectionStore.getOtherUser(connection, userStore.user)?.username || 'Unknown User' }}
                          </p>
                          <p class="text-xs text-gray-500">
                            Connected {{ connection.formatted_created_at }}
                          </p>
                        </div>
                      </div>
                      
                      <!-- Status and Actions -->
                      <div class="flex items-center justify-between sm:justify-end gap-2 mt-2 sm:mt-0">
                        <div class="flex-shrink-0 flex items-center gap-2">
                          <span
                            v-if="connection.banned"
                            class="px-2.5 py-0.5 bg-yellow-100 text-yellow-800 rounded-full text-xs font-medium whitespace-nowrap"
                          >
                            Banned
                          </span>
                          <button
                            v-else-if="isNotInitiator(connection) && (!connection.removed || (connection.reconnection_requested_by && connection.reconnection_requested_by !== userStore.user.id))"
                            @click="reportUser(connection)"
                            class="whitespace-nowrap inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                          >
                            Report
                          </button>
                        </div>
                        
                        <span
                          class="px-2.5 py-0.5 rounded-full text-xs font-medium whitespace-nowrap"
                          :class="{
                            'bg-green-100 text-green-800': !connection.removed && !connection.reconnection_requested_by,
                            'bg-yellow-100 text-yellow-800': connection.reconnection_requested_by && !connection.reconnection_rejected,
                            'bg-red-100 text-red-800': connection.rejected || connection.reconnection_rejected,
                            'bg-gray-100 text-gray-800': connection.removed
                          }"
                        >
                          {{ getConnectionStatusText(connection) }}
                        </span>
                      </div>
                    </div>
                    
                    <ConnectionMessage 
                      :connection="connection" 
                      :processing="connectionStore.processingAction"
                      @action="handleAction($event.connection, $event.type)"
                    />
                  </div>
                </div>
                
                <!-- Load More Button -->
                <div v-if="connectionsNextUrl" class="flex justify-center mt-6">
                  <button
                    @click="loadMoreConnections"
                    :disabled="loading.moreConnections"
                    class="px-4 py-2 cursor-pointer border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                  >
                    <span v-if="loading.moreConnections">Loading...</span>
                    <span v-else>Load More</span>
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Usage Tab -->
            <div v-else-if="activeTab === 'usage'" class="space-y-4">
              <div v-if="loading.usage" class="flex justify-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-500"></div>
              </div>
              
              <div v-else-if="usages.length === 0" class="text-center py-12 text-gray-500">
                No usage history found.
              </div>
              
              <div v-else class="space-y-4">
                <div v-for="usage in usages" :key="usage.id" class="border rounded-lg overflow-hidden">
                  <div class="p-4">
                    <div class="flex flex-col md:flex-row md:justify-between md:items-start">
                      <div>
                        <h3 class="font-medium text-gray-900">
                          {{ usage.connection ? 'Connection' : usage.transaction ? 'Transaction' : 'Connect Usage' }}
                        </h3>
                        <p class="text-sm text-gray-500">
                          {{ new Date(usage.created_at).toLocaleDateString() }} • 
                          {{ new Date(usage.created_at).toLocaleTimeString() }}
                        </p>
                      </div>
                      <div class="mt-2 md:mt-0">
                        <span 
                          class="px-2 py-1 text-xs font-medium rounded-full"
                          :class="{
                            'bg-green-100 text-green-800': (usage.connectsAfter - usage.connectsBefore) > 0,
                            'bg-red-100 text-red-800': (usage.connectsAfter - usage.connectsBefore) < 0,
                            'bg-gray-100 text-gray-800': (usage.connectsAfter - usage.connectsBefore) === 0
                          }"
                        >
                          {{ (usage.connectsAfter - usage.connectsBefore) < 0 ? '-' : '' }}{{ Math.abs(usage.connectsAfter - usage.connectsBefore) }}
                          {{ Math.abs(usage.connectsAfter - usage.connectsBefore) === 1 ? 'Connect' : 'Connects' }}
                        </span>
                      </div>
                    </div>
                    
                    <div class="mt-2 text-sm">
                      <p>
                        <span class="font-medium">Before:</span> {{ usage.connectsBefore }} Connects •
                        <span class="font-medium">After:</span> {{ usage.connectsAfter }} Connects
                      </p>
                      <div v-if="usage.connection && usage.connection?.connected_user" class="mt-2 p-2 bg-gray-50 rounded-md">
                        <p class="font-medium text-gray-700">Connection Details:</p>
                        <div class="flex items-center mt-1">
                          <div v-if="usage.connection.connected_user?.profile_picture" 
                               class="h-8 w-8 rounded-full overflow-hidden mr-2">
                            <img :src="usage.connection.connected_user.profile_picture" 
                                 :alt="usage.connection.connected_user.name" 
                                 class="h-full w-full object-cover">
                          </div>
                          <div v-else class="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center mr-2">
                            <span class="text-sm text-indigo-600">
                              {{ usage.connection.connected_user?.name?.charAt(0) || 'U' }}
                            </span>
                          </div>
                          <div>
                            <p class="text-sm font-medium text-gray-900">
                              {{ usage.connection.connected_user?.name || 'User' }}
                              <span class="text-xs text-gray-500">@{{ usage.connection.connected_user?.username }}</span>
                            </p>
                            <p class="text-xs text-gray-500">
                              {{ usage.connection.formatted_created_at }}
                            </p>
                          </div>
                        </div>
                      </div>
                      <div v-else-if="usage.transaction" class="mt-2 p-2 bg-gray-50 rounded-md">
                        <p class="font-medium text-gray-700">Transaction Details:</p>
                        <div class="mt-2">
                          <template v-if="!usage.transaction.product_name && !usage.transaction.status">
                            <p class="text-sm text-gray-500">Transaction not fulfilled</p>
                          </template>
                          <template v-else>
                            <div class="flex items-center justify-between">
                              <span class="text-sm text-gray-500">Product:</span>
                              <span class="text-sm font-medium text-gray-900">
                                {{ usage.transaction.product_name || 'N/A' }}
                              </span>
                            </div>
                            <div class="flex items-center justify-between mt-1">
                              <span class="text-sm text-gray-500">Status:</span>
                              <span 
                                v-if="usage.transaction.status"
                                class="px-2 py-0.5 text-xs font-medium rounded-full"
                                :class="{
                                  'bg-green-100 text-green-800': usage.transaction.approved,
                                  'bg-yellow-100 text-yellow-800': !usage.transaction.approved && usage.transaction.status && !usage.transaction.status.includes('rejected'),
                                  'bg-red-100 text-red-800': usage.transaction.status && usage.transaction.status.includes('rejected')
                                }"
                              >
                                {{ usage.transaction.status }}
                              </span>
                              <span v-else class="text-sm text-gray-500">Pending</span>
                            </div>
                            <div v-if="usage.transaction.total_amount !== null" class="flex items-center justify-between mt-1">
                              <span class="text-sm text-gray-500">Amount:</span>
                              <span class="text-sm font-medium text-gray-900">
                                {{ Number(usage.transaction.total_amount).toLocaleString() }} {{ (usage.transaction.currency || '').toUpperCase() }}
                              </span>
                            </div>
                          </template>
                          <div v-if="usage.transaction.screenshot_url" class="mt-2">
                            <a 
                              :href="usage.transaction.screenshot_url" 
                              target="_blank"
                              class="text-indigo-600 hover:text-indigo-800 text-sm font-medium"
                            >
                              View Receipt
                            </a>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Load More Button -->
                <div v-if="usagesNextUrl" class="flex justify-center mt-6">
                  <button
                    @click="loadMoreUsages"
                    :disabled="loading.moreUsages"
                    class="px-4 py-2 cursor-pointer border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                  >
                    <span v-if="loading.moreUsages">Loading...</span>
                    <span v-else>Load More</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Mobile Bottom Navigation -->
    <mobile-bottom-nav :user-initials="userInitials" />
    
    <!-- Report Modal -->
    <ReportModal 
      v-if="reportModalOpen" 
      :is-open="reportModalOpen" 
      @close="reportModalOpen = false"
      @submit="handleReport"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { Flag } from 'lucide-vue-next';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { useConnectionStore } from '@/stores/connection';
import { api } from '@/main';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import ReportModal from '@/components/feed/ReportModal.vue';
import ConnectionMessage from '@/components/ConnectionMessage.vue';

const router = useRouter();
const userStore = useUserStore();
const connectionStore = useConnectionStore();

// Report modal state
const reportModalOpen = ref(false);
const selectedConnection = ref(null);
// Tabs
const activeTab = ref('transactions');
const tabs = ref([
  { id: 'transactions', name: 'Transactions', count: 0 },
  { id: 'connections', name: 'Connections', count: 0 },
  { id: 'usage', name: 'Usage', count: 0 },
]);

// User initials for avatar
const userInitials = computed(() => {
  if (!userStore.user?.name) return 'U';
  return userStore.user.name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .substring(0, 2);
});

// Handle logout
const handleLogout = async () => {
  await userStore.logout();
  router.push('/login');
};

// Transactions
const transactions = ref([]);
const transactionsNextUrl = ref(null);
const loading = ref({
  transactions: false,
  moreTransactions: false,
  connections: false,
  moreConnections: false,
  usage: false,
  moreUsages: false
});

// Fetch transactions
const fetchTransactions = async (url = '/transaction/transactions/my_transactions/') => {
  try {
    loading.value.transactions = true;
    const response = await api.get(url);
    if (url.includes('page=')) {
      // Append new transactions if loading more
      transactions.value = [...transactions.value, ...response.data.results];
    } else {
      transactions.value = response.data.results;
    }
    transactionsNextUrl.value = response.data.next;
    tabs.value[0].count = response.data.count;
  } catch (error) {
    console.error('Error fetching transactions:', error);
  } finally {
    loading.value.transactions = false;
    loading.value.moreTransactions = false;
  }
};

// Load more transactions
const loadMoreTransactions = () => {
  if (!transactionsNextUrl.value) return;
  loading.value.moreTransactions = true;
  
  // Use the full URL directly since it's already correct from the API
  fetchTransactions(transactionsNextUrl.value);
};

// Connections
const connections = ref([]);
const connectionsNextUrl = ref(null);

// Fetch connections
const fetchConnections = async (url = '/account/users/connections/') => {
  try {
    loading.value.connections = true;
    const response = await api.get(url);
    if (url.includes('page=')) {
      // Append new connections if loading more
      connections.value = [...connections.value, ...response.data.results];
    } else {
      connections.value = response.data.results;
    }
    connectionsNextUrl.value = response.data.next;
    tabs.value[1].count = response.data.count;
  } catch (error) {
    console.error('Error fetching connections:', error);
  } finally {
    loading.value.connections = false;
    loading.value.moreConnections = false;
  }
};

// Load more connections
const loadMoreConnections = () => {
  if (!connectionsNextUrl.value) return;
  loading.value.moreConnections = true;
  
  // Use the full URL directly since it's already correct from the API
  fetchConnections(connectionsNextUrl.value);
};

// Check if current user is not the initiator of the connection
const isNotInitiator = (connection) => {
  if (!userStore.user) return false;
  return connection.initiating_user.id !== userStore.user.id;
};

// Get the other user in a connection


// Get connection status text
const getConnectionStatusText = (connection) => {
  if (connection.removed) return 'Removed';
  if (connection.rejected) return 'Rejected';
  
  if (connection.reconnection_requested_by) {
    if (connection.reconnection_rejected) return 'Reconnection Rejected';
    return connection.reconnection_requested_by === userStore.user.id 
      ? 'Reconnection Requested' 
      : 'Reconnection Pending';
  }
  
  return 'Connected';
};

// Handle user report
const reportUser = (connection) => {
  selectedConnection.value = connection;
  reportModalOpen.value = true;
};

// Handle report submission
const handleReport = async (reason) => {
  if (!selectedConnection.value) return;
  
  try {
    await api.post('/report/reports/report_connection/', {
      connection_id: selectedConnection.value.id,
      reason: reason
    });
    
    // Close modal and show success message
    reportModalOpen.value = false;
    alert('Report submitted successfully');
  } catch (error) {
    console.error('Error reporting connection:', error);
    alert(error.response?.data?.error || 'Failed to submit report');
  }
};

// Handle accept/reject connection
const handleAction = async (connection, action) => {
  const success = await (action === 'accept' 
    ? connectionStore.handleAcceptConnection(connection)
    : connectionStore.handleRejectConnection(connection)
  );
  
  if (success) {
    // Update the connection in the local state to reflect the change
    const index = connections.value.findIndex(c => c.id === connection.id);
    if (index !== -1) {
      if (action === 'accept') {
        connections.value[index].reconnection_requested_by = null;
        connections.value[index].reconnection_rejected = false;
      } else {
        connections.value[index].reconnection_rejected = true;
      }
    }
  }
};

// Usage
const usages = ref([]);
const usagesNextUrl = ref(null);

// Fetch usages
const fetchUsages = async (url = '/usage/connect-usages/') => {
  try {
    loading.value.usage = true;
    const response = await api.get(url);
    if (url.includes('page=')) {
      // Append new usages if loading more
      usages.value = [...usages.value, ...response.data.results];
    } else {
      usages.value = response.data.results;
    }
    usagesNextUrl.value = response.data.next;
    tabs.value[2].count = response.data.count;
  } catch (error) {
    console.error('Error fetching usages:', error);
  } finally {
    loading.value.usage = false;
    loading.value.moreUsages = false;
  }
};

// Load more usages
const loadMoreUsages = () => {
  if (!usagesNextUrl.value) return;
  loading.value.moreUsages = true;
  fetchUsages(usagesNextUrl.value);
};

// Watch for tab changes
watch(activeTab, (newTab) => {
  if (newTab === 'transactions' && transactions.value.length === 0) {
    fetchTransactions();
  } else if (newTab === 'connections' && connections.value.length === 0) {
    fetchConnections();
  } else if (newTab === 'usage' && usages.value.length === 0) {
    fetchUsages();
  }
});

// Fetch initial data
onMounted(() => {
  fetchTransactions();
  fetchConnections();
  fetchUsages();
});
</script>

<style scoped>
/* Add any custom styles here */
</style>
