<template>
    <div v-if="historyStore.activeTab === 'transactions'" class="space-y-4">
        <div v-if="historyStore.loading.transactions" class="flex flex-col items-center justify-center py-12">
            <div class="animate-spin rounded-full h-8 w-8 border-[3px] border-violet-100 border-t-violet-500 mb-3"></div>
            <span class="text-xs font-medium text-zinc-400">Loading transactions...</span>
        </div>
        
        <div v-else-if="historyStore.transactions.length === 0" class="text-center py-16">
            <div class="w-16 h-16 bg-zinc-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-zinc-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                </svg>
            </div>
            <p class="text-zinc-500 font-medium">No transactions found.</p>
        </div>
        
        <div v-else class="space-y-4">
            <div v-for="transaction in historyStore.transactions" :key="transaction.pk" class="bg-white border border-zinc-200 rounded-2xl p-5 hover:border-violet-200 hover:shadow-sm transition-all duration-200">
                <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
                    <div>
                        <h3 class="font-bold text-zinc-900 text-lg">
                            {{ transaction.product_name || 'Transaction' }}
                        </h3>
                        <div class="flex items-center text-sm text-zinc-500 mt-1">
                             <span class="font-medium">{{ transaction.formatted_created_at }}</span>
                             <span class="mx-2 text-zinc-300">•</span>
                             <span>{{ transaction.time_ago }}</span>
                        </div>
                    </div>
                    <span 
                        v-if="transaction.status"
                        class="px-3 py-1 text-xs font-bold uppercase tracking-wide rounded-full self-start"
                        :class="{
                            'bg-emerald-100 text-emerald-700': transaction.approved,
                            'bg-amber-100 text-amber-700': !transaction.approved && !transaction.status.includes('rejected'),
                            'bg-rose-100 text-rose-700': transaction.status.includes('rejected')
                        }"
                    >
                        {{ transaction.status }}
                    </span>
                    <span 
                        v-else
                        class="px-3 py-1 text-xs font-bold uppercase tracking-wide text-zinc-600 bg-zinc-100 rounded-full self-start"
                    >
                        Pending
                    </span>
                </div>
                
                <div v-if="transaction.product_name" class="mt-5 pt-4 border-t border-zinc-100 grid grid-cols-2 gap-4">
                    <div>
                        <p class="text-xs text-zinc-400 font-semibold uppercase tracking-wide mb-1">Connects</p>
                        <p class="font-bold text-zinc-900 text-lg flex items-center">
                            {{ transaction.connects || 'N/A' }}
                        </p>
                    </div>
                    <div>
                        <p class="text-xs text-zinc-400 font-semibold uppercase tracking-wide mb-1">Amount</p>
                        <p class="font-bold text-zinc-900 text-lg">
                            {{ transaction.total_amount ? `${Number(transaction.total_amount).toLocaleString()} ${(transaction.currency || '').toUpperCase()}` : 'N/A' }}
                        </p>
                    </div>
                </div>
                
                <div v-if="transaction.screenshot_url" class="mt-4 pt-2">
                    <a 
                        :href="transaction.screenshot_url" 
                        target="_blank"
                        class="inline-flex items-center text-sm font-semibold text-violet-600 hover:text-violet-800 transition-colors"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        View Receipt
                    </a>
                </div>
            </div>
            
            <!-- Load More Button -->
            <div v-if="historyStore.transactionsNextUrl" class="flex justify-center mt-8 pb-4">
                <button
                    @click="historyStore.loadMoreTransactions"
                    :disabled="historyStore.loading.moreTransactions"
                    class="px-6 py-2.5 cursor-pointer border border-zinc-200 rounded-full text-sm font-semibold text-zinc-600 bg-white hover:bg-zinc-50 hover:text-violet-600 hover:border-violet-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-50 transition-all shadow-sm"
                >
                    <span v-if="historyStore.loading.moreTransactions" class="flex items-center">
                        <div class="animate-spin rounded-full h-4 w-4 border-2 border-zinc-400 border-t-zinc-600 mr-2"></div>
                        Loading...
                    </span>
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