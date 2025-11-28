<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-xl font-semibold text-gray-900">Pending Transactions</h2>
      <button 
        @click="refreshTransactions" 
        class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer"
        :disabled="isLoading"
      >
        <svg v-if="isRefreshing" class="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <svg v-else class="-ml-1 mr-2 h-4 w-4 text-gray-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        Refresh
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading && transactions.length === 0" class="bg-white shadow overflow-hidden sm:rounded-lg p-6 text-center">
      <div class="flex justify-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>
      <p class="mt-2 text-sm text-gray-500">Loading transactions...</p>
    </div>

    <!-- Empty state -->
    <div v-else-if="!isLoading && transactions.length === 0" class="bg-white shadow overflow-hidden sm:rounded-lg p-6 text-center">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No pending transactions</h3>
      <p class="mt-1 text-sm text-gray-500">Get started by approving or rejecting transactions as they come in.</p>
    </div>

    <!-- Transactions list -->
    <div v-else class="bg-white shadow overflow-hidden sm:rounded-md">
      <ul role="list" class="divide-y divide-gray-200">
        <li v-for="transaction in transactions" :key="transaction.id">
          <div class="px-4 py-4 sm:px-6">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center">
                    <svg class="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-indigo-600 truncate">
                    {{ transaction.method }}
                  </p>
                  <p class="text-sm text-gray-500">
                    {{ Intl.NumberFormat().format(transaction.connects) }} connects • {{ Intl.NumberFormat().format(transaction.total_amount) }} {{ transaction.currency }}
                  </p>
                </div>
              </div>
              <div class="ml-2 flex-shrink-0 flex">
                <div class="text-right mr-4">
                  <p class="text-xs text-gray-500">{{ transaction.time_ago }}</p>
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" 
                    :class="{
                      'bg-yellow-100 text-yellow-800': transaction.status === 'pending',
                      'bg-green-100 text-green-800': transaction.status === 'completed',
                      'bg-red-100 text-red-800': transaction.status === 'rejected'
                    }">
                    {{ transaction.status }}
                  </span>
                </div>
                <button
                  @click="openTransactionModal(transaction)"
                  class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer"
                >
                  View Details
                </button>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <!-- Transaction Modal -->
    <TransactionModal
      v-if="isModalOpen"
      :is-open="isModalOpen"
      :transaction="selectedTransaction"
      @close="closeModal"
      @update:transaction="updateTransaction"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { api } from '@/main';
import { message } from 'ant-design-vue';
import TransactionModal from '@/components/admin/TransactionModal.vue';

const transactions = ref([]);
const isLoading = ref(true);
const isRefreshing = ref(false);
const isModalOpen = ref(false);
const selectedTransaction = ref(null);

const fetchTransactions = async () => {
  try {
    const response = await api.get('/transaction/transactions/pending_transactions/');
    transactions.value = response.data;
  } catch (error) {
    console.error('Error fetching transactions:', error);
    message.error('Failed to load transactions. Please try again.');
  } finally {
    isLoading.value = false;
    isRefreshing.value = false;
  }
};

const refreshTransactions = () => {
  isRefreshing.value = true;
  fetchTransactions();
};

const openTransactionModal = (transaction) => {
  selectedTransaction.value = { ...transaction };
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  selectedTransaction.value = null;
};

const updateTransaction = (updatedTransaction) => {
  const index = transactions.value.findIndex(t => t.id === updatedTransaction.id);
  if (index !== -1) {
    transactions.value[index] = updatedTransaction;
    // Remove from the list if it's no longer pending
    if (updatedTransaction.status !== 'pending') {
      transactions.value.splice(index, 1);
    }
  }
};

onMounted(() => {
  fetchTransactions();
});
</script>
