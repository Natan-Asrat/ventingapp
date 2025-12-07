<template>
    <div v-if="historyStore.activeTab === 'transactions'" class="space-y-4">
        <div v-if="historyStore.loading.transactions" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
        
        <div v-else-if="historyStore.transactions.length === 0" class="text-center py-12 text-gray-500">
            No transactions found.
        </div>
        
        <div v-else class="space-y-4">
            <div v-for="transaction in historyStore.transactions" :key="transaction.pk" class="border rounded-lg overflow-hidden">
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
            <div v-if="historyStore.transactionsNextUrl" class="flex justify-center mt-6">
                <button
                    @click="historyStore.loadMoreTransactions"
                    :disabled="historyStore.loading.moreTransactions"
                    class="px-4 py-2 cursor-pointer border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                    <span v-if="historyStore.loading.moreTransactions">Loading...</span>
                    <span v-else>Load More</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useHistoryStore } from '@/stores/history';
const historyStore = useHistoryStore();
</script>