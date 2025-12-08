<template>            
    <div class="space-y-4">
        <div v-if="historyStore.loading.usage" class="flex flex-col items-center justify-center py-12">
            <div class="animate-spin rounded-full h-8 w-8 border-[3px] border-violet-100 border-t-violet-500 mb-3"></div>
            <span class="text-xs font-medium text-zinc-400">Loading history...</span>
        </div>
        
        <div v-else-if="historyStore.usages.length === 0" class="text-center py-16">
             <div class="w-16 h-16 bg-zinc-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-zinc-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            </div>
            <p class="text-zinc-500 font-medium">No usage history found.</p>
        </div>
        
        <div v-else class="space-y-4">
            <div v-for="usage in historyStore.usages" :key="usage.id" class="bg-white border border-zinc-200 rounded-2xl p-5 hover:border-violet-200 hover:shadow-sm transition-all duration-200">
                <div>
                    <div class="flex flex-col md:flex-row md:justify-between md:items-start gap-3">
                        <div>
                            <h3 class="font-bold text-zinc-900 text-lg">
                                {{ usage.connection ? 'Connection' : usage.transaction ? 'Transaction' : 'Connect Usage' }}
                            </h3>
                            <p class="text-sm text-zinc-500 mt-1 font-medium">
                                {{ new Date(usage.created_at).toLocaleDateString() }} • 
                                {{ new Date(usage.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}
                            </p>
                        </div>
                        <div class="mt-1 md:mt-0">
                            <span 
                                class="px-3 py-1 text-xs font-bold rounded-full uppercase tracking-wide inline-flex items-center"
                                :class="{
                                'bg-emerald-100 text-emerald-700': (usage.connectsAfter - usage.connectsBefore) > 0,
                                'bg-rose-100 text-rose-700': (usage.connectsAfter - usage.connectsBefore) < 0,
                                'bg-zinc-100 text-zinc-700': (usage.connectsAfter - usage.connectsBefore) === 0
                                }"
                            >
                                {{ (usage.connectsAfter - usage.connectsBefore) > 0 ? '+' : '' }}{{ usage.connectsAfter - usage.connectsBefore }}
                                {{ Math.abs(usage.connectsAfter - usage.connectsBefore) === 1 ? 'Connect' : 'Connects' }}
                            </span>
                        </div>
                    </div>
                    
                    <div class="mt-4 pt-3 border-t border-zinc-100">
                        <div class="flex items-center justify-between text-xs text-zinc-500 mb-3 bg-zinc-50 p-2 rounded-lg">
                            <div><span class="font-bold text-zinc-600">Before:</span> {{ usage.connectsBefore }}</div>
                            <div class="h-4 w-px bg-zinc-200"></div>
                            <div><span class="font-bold text-zinc-600">After:</span> {{ usage.connectsAfter }}</div>
                        </div>
                        
                        <div v-if="usage.connection && usage.connection?.connected_user" class="p-3 bg-violet-50/50 rounded-xl border border-violet-100/50">
                            <p class="text-xs font-bold text-violet-600 uppercase tracking-wide mb-2">Connection Details</p>
                            <div class="flex items-center">
                                <div 
                                    v-if="usage.connection.connected_user?.profile_picture" 
                                    class="h-10 w-10 rounded-full overflow-hidden mr-3 ring-2 ring-white"
                                >
                                    <img 
                                        :src="usage.connection.connected_user.profile_picture" 
                                        :alt="usage.connection.connected_user.name" 
                                        class="h-full w-full object-cover"
                                    >
                                </div>
                                <div v-else class="h-10 w-10 rounded-full bg-violet-100 flex items-center justify-center mr-3 ring-2 ring-white">
                                    <span class="text-sm font-bold text-violet-600">
                                        {{ usage.connection.connected_user?.name?.charAt(0) || 'U' }}
                                    </span>
                                </div>
                                <div>
                                    <p class="text-sm font-bold text-zinc-900">
                                        {{ usage.connection.connected_user?.name || 'User' }}
                                    </p>
                                    <p class="text-xs text-zinc-500 font-medium">@{{ usage.connection.connected_user?.username }}</p>
                                </div>
                            </div>
                        </div>
                        <div v-else-if="usage.transaction" class="p-3 bg-amber-50/50 rounded-xl border border-amber-100/50">
                            <p class="text-xs font-bold text-amber-700 uppercase tracking-wide mb-2">Transaction Details</p>
                            <div class="space-y-1">
                                <template v-if="!usage.transaction.product_name && !usage.transaction.status">
                                    <p class="text-sm text-zinc-500 italic">Transaction not fulfilled</p>
                                </template>
                                <template v-else>
                                    <div class="flex items-center justify-between">
                                        <span class="text-sm text-zinc-500">Product:</span>
                                        <span class="text-sm font-bold text-zinc-900">
                                            {{ usage.transaction.product_name || 'N/A' }}
                                        </span>
                                    </div>
                                <div class="flex items-center justify-between">
                                    <span class="text-sm text-zinc-500">Status:</span>
                                    <span 
                                        v-if="usage.transaction.status"
                                        class="px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide rounded-full"
                                        :class="{
                                            'bg-emerald-100 text-emerald-700': usage.transaction.approved,
                                            'bg-amber-100 text-amber-700': !usage.transaction.approved && usage.transaction.status && !usage.transaction.status.includes('rejected'),
                                            'bg-rose-100 text-rose-700': usage.transaction.status && usage.transaction.status.includes('rejected')
                                        }"
                                    >
                                        {{ usage.transaction.status }}
                                    </span>
                                    <span v-else class="text-sm text-zinc-500">Pending</span>
                                </div>
                                <div v-if="usage.transaction.total_amount !== null" class="flex items-center justify-between">
                                    <span class="text-sm text-zinc-500">Amount:</span>
                                    <span class="text-sm font-bold text-zinc-900">
                                        {{ Number(usage.transaction.total_amount).toLocaleString() }} {{ (usage.transaction.currency || '').toUpperCase() }}
                                    </span>
                                </div>
                                </template>
                                <div v-if="usage.transaction.screenshot_url" class="pt-2">
                                <a 
                                    :href="usage.transaction.screenshot_url" 
                                    target="_blank"
                                    class="text-violet-600 hover:text-violet-800 text-sm font-semibold inline-flex items-center"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                    </svg>
                                    View Receipt
                                </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Load More Button -->
            <div v-if="historyStore.usagesNextUrl" class="flex justify-center mt-8 pb-4">
                <button
                    @click="historyStore.loadMoreUsages"
                    :disabled="historyStore.loading.moreUsages"
                     class="px-6 py-2.5 cursor-pointer border border-zinc-200 rounded-full text-sm font-semibold text-zinc-600 bg-white hover:bg-zinc-50 hover:text-violet-600 hover:border-violet-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-50 transition-all shadow-sm"
                >
                    <span v-if="historyStore.loading.moreUsages" class="flex items-center">
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