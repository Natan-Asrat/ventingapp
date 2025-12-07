<template>
    <div class="space-y-4">
        <div v-if="historyStore.loading.connections" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
        
        <div v-else-if="historyStore.connections.length === 0" class="text-center py-12 text-gray-500">
            No connections found.
        </div>
        
        <div class="space-y-4">
            <div v-for="connection in historyStore.connections" :key="connection.id" class="border rounded-lg overflow-hidden">
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
                                    @click="historyStore.reportUser(connection)"
                                    class="whitespace-nowrap inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 cursor-pointer"
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
            <div v-if="historyStore.connectionsNextUrl" class="flex justify-center mt-6">
                <button
                    @click="historyStore.loadMoreConnections"
                    :disabled="historyStore.loading.moreConnections"
                    class="px-4 py-2 cursor-pointer border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                    <span v-if="historyStore.loading.moreConnections">Loading...</span>
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
    if (connection.reconnection_rejected) return 'Reconnection Rejected';
    return connection.reconnection_requested_by === userStore.user.id 
      ? 'Reconnection Requested' 
      : 'Reconnection Pending';
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