<template>
    <div class="space-y-4">
        <div v-if="historyStore.loading.connections" class="flex flex-col items-center justify-center py-12">
            <div class="animate-spin rounded-full h-8 w-8 border-[3px] border-violet-100 border-t-violet-500 mb-3"></div>
            <span class="text-xs font-medium text-zinc-400">Loading connections...</span>
        </div>
        
        <div v-else-if="historyStore.connections.length === 0" class="text-center py-16">
            <div class="w-16 h-16 bg-zinc-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-zinc-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
            </div>
            <p class="text-zinc-500 font-medium">No connections found.</p>
        </div>
        
        <div class="space-y-4">
            <div v-for="connection in historyStore.connections" :key="connection.id" class="bg-white border border-zinc-200 rounded-2xl p-5 hover:border-violet-200 hover:shadow-sm transition-all duration-200">
                <div class="flex flex-col sm:flex-row sm:items-center gap-4">
                    <!-- Profile Section -->
                    <div class="flex items-center flex-1 min-w-0">
                        <!-- Profile Picture -->
                        <div class="relative">
                            <div 
                                v-if="connectionStore.getOtherUser(connection, userStore.user)?.profile_picture" 
                                class="flex-shrink-0 h-12 w-12 rounded-full overflow-hidden ring-2 ring-zinc-100"
                            >
                                <img 
                                    :src="connectionStore.getOtherUser(connection, userStore.user)?.profile_picture" 
                                    :alt="connectionStore.getOtherUser(connection, userStore.user)?.name || 'User'"
                                    class="h-full w-full object-cover"
                                />
                            </div>
                            <div v-else class="flex-shrink-0 h-12 w-12 rounded-full bg-violet-100 flex items-center justify-center ring-2 ring-zinc-100">
                                <span class="text-lg font-bold text-violet-600">
                                    {{ connectionStore.getOtherUser(connection, userStore.user)?.name ? connectionStore.getOtherUser(connection, userStore.user)?.name.charAt(0).toUpperCase() : 'U' }}
                                </span>
                            </div>
                        </div>
                        
                        <!-- User Info -->
                        <div class="ml-4 min-w-0">
                            <p class="text-base font-bold text-zinc-900 truncate">
                                {{ connectionStore.getOtherUser(connection, userStore.user)?.name || connectionStore.getOtherUser(connection, userStore.user)?.username || 'Unknown User' }}
                            </p>
                            <p class="text-xs text-zinc-500 font-medium mt-0.5">
                                Connected {{ connection.formatted_created_at }}
                            </p>
                        </div>
                    </div>
                    
                    <!-- Status and Actions -->
                    <div class="flex items-center justify-between sm:justify-end gap-3 mt-2 sm:mt-0">
                        <div class="flex-shrink-0 flex items-center gap-2">
                            <span
                                v-if="connection.banned"
                                class="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-bold uppercase tracking-wide"
                            >
                                Banned
                            </span>
                            <button
                                v-else-if="isNotInitiator(connection) && (!connection.removed || (connection.reconnection_requested_by && connection.reconnection_requested_by !== userStore.user.id))"
                                @click="historyStore.reportUser(connection)"
                                class="whitespace-nowrap inline-flex items-center px-3 py-1 rounded-full text-xs font-bold text-rose-600 bg-rose-50 border border-rose-100 hover:bg-rose-100 focus:outline-none transition-colors cursor-pointer uppercase tracking-wide"
                            >
                                Report
                            </button>
                        </div>
                        
                        <span
                            class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide"
                            :class="{
                            'bg-emerald-100 text-emerald-700': !connection.removed && !connection.reconnection_requested_by,
                            'bg-amber-100 text-amber-700': connection.reconnection_requested_by && !connection.reconnection_rejected,
                            'bg-rose-100 text-rose-700': connection.rejected || connection.reconnection_rejected,
                            'bg-zinc-100 text-zinc-600': connection.removed
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
            
            <!-- Load More Button -->
            <div v-if="historyStore.connectionsNextUrl" class="flex justify-center mt-8 pb-4">
                <button
                    @click="historyStore.loadMoreConnections"
                    :disabled="historyStore.loading.moreConnections"
                     class="px-6 py-2.5 cursor-pointer border border-zinc-200 rounded-full text-sm font-semibold text-zinc-600 bg-white hover:bg-zinc-50 hover:text-violet-600 hover:border-violet-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-50 transition-all shadow-sm"
                >
                    <span v-if="historyStore.loading.moreConnections" class="flex items-center">
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
import { useUserStore } from '@/stores/user';
import { useConnectionStore } from '@/stores/connection';
import { useHistoryStore } from '@/stores/history';
import ConnectionMessage from '@/components/ConnectionMessage.vue';
const historyStore = useHistoryStore();
const userStore = useUserStore();
const connectionStore = useConnectionStore();

// Check if current user is not the initiator of the connection
const isNotInitiator = (connection) => {
  if (!userStore.user) return false;
  return connection.initiating_user.id !== userStore.user.id;
};

// Get connection status text
const getConnectionStatusText = (connection) => {
  if (connection.removed) return 'Removed';
  if (connection.rejected) return 'Rejected';
  
  if (connection.reconnection_requested_by) {
    if (connection.reconnection_rejected) return 'Rejected';
    return connection.reconnection_requested_by === userStore.user.id 
      ? 'Requested' 
      : 'Pending';
  }
  
  return 'Connected';
};

// Handle accept/reject connection
const handleAction = async (connection, action) => {
  const success = await (action === 'accept' 
    ? connectionStore.handleAcceptConnection(connection)
    : connectionStore.handleRejectConnection(connection)
  );
  
  if (success) {
    historyStore.setConnectionByAction(connection, action);
  }
};
</script>