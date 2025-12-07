<template>            
    <div class="space-y-4">
        <div v-if="historyStore.loading.usage" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
        
        <div v-else-if="historyStore.usages.length === 0" class="text-center py-12 text-gray-500">
            No usage history found.
        </div>
        
        <div v-else class="space-y-4">
            <div v-for="usage in historyStore.usages" :key="usage.id" class="border rounded-lg overflow-hidden">
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
                                <div 
                                    v-if="usage.connection.connected_user?.profile_picture" 
                                    class="h-8 w-8 rounded-full overflow-hidden mr-2"
                                >
                                    <img 
                                        :src="usage.connection.connected_user.profile_picture" 
                                        :alt="usage.connection.connected_user.name" 
                                        class="h-full w-full object-cover"
                                    >
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
            <div v-if="historyStore.usagesNextUrl" class="flex justify-center mt-6">
                <button
                    @click="historyStore.loadMoreUsages"
                    :disabled="historyStore.loading.moreUsages"
                    class="px-4 py-2 cursor-pointer border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                    <span v-if="historyStore.loading.moreUsages">Loading...</span>
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