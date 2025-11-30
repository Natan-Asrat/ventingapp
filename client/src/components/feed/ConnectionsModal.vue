<template>
  <Dialog :open="show" @close="$emit('close')" class="relative z-50">
    <!-- The backdrop, rendered as a fixed sibling to the panel container -->
    <div class="fixed inset-0 bg-black/50" aria-hidden="true" />

    <!-- Full-screen container to center the panel -->
    <div class="fixed inset-0 flex items-center justify-center p-4">
      <DialogPanel class="w-full max-w-md max-h-[80vh] overflow-hidden bg-white rounded-lg flex flex-col">
        <div class="p-4 border-b border-gray-200 flex justify-between items-center">
          <DialogTitle class="text-lg font-medium">Connection Request</DialogTitle>
          <button 
            @click="$emit('close')" 
            class="text-gray-500 hover:text-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 rounded-md cursor-pointer"
          >
            <span class="sr-only">Close</span>
            <X :size="20" aria-hidden="true" />
          </button>
        </div>
        
        <div class="overflow-y-auto flex-1 p-4">
          <div v-if="loadingConnections" class="flex justify-center py-8">
            <Loader2 class="w-8 h-8 animate-spin text-indigo-600" />
          </div>
          
          <div v-else-if="connections.length === 0" class="text-center py-8 text-gray-500">
            No connection requests found.
          </div>
          
          <div v-else class="space-y-4">
            <div v-for="connection in connections" :key="connection.id" class="border rounded-lg p-4">
              <div class="flex items-center space-x-3 mb-3">
                <div v-if="connection.initiating_user.profile_picture" class="h-12 w-12 rounded-full overflow-hidden">
                  <img :src="connection.initiating_user.profile_picture" :alt="connection.initiating_user.name" class="h-full w-full object-cover">
                </div>
                <div v-else class="h-12 w-12 rounded-full bg-gray-200 flex items-center justify-center text-gray-600 font-medium">
                  {{ connection.initiating_user.name?.charAt(0).toUpperCase() || 'U' }}
                </div>
                <div>
                  <div>
                    <p class="font-medium">{{ connection.initiating_user.name }}</p>
                    <p class="text-sm text-gray-500">@{{ connection.initiating_user.username }}</p>
                  </div>
                </div>
              </div>
              
              <!-- Connection message if exists -->
              <div v-if="connection.message" class="mt-2 p-3 bg-gray-50 rounded-md text-sm text-gray-700">
                <p class="whitespace-pre-line">{{ connection.message }}</p>
              </div>

              <div v-if="connection.reconnection_requested_by === userStore.user?.id" class="mt-2 text-sm text-gray-600">
                <p>You sent a request {{ connection.formatted_created_at }}</p>
                <p class="text-yellow-600 mt-1">Waiting for approval...</p>
              </div>
              
              <div v-else class="mt-2 text-sm text-gray-600">
                <p>Requested {{ connection.formatted_created_at }}</p>
                <div v-if="!connection.reconnection_rejected" class="flex space-x-2 mt-2">
                  <button 
                    @click="handleAcceptConnection(connection)"
                    class="flex-1 flex items-center justify-center px-3 py-1.5 bg-green-100 text-green-700 rounded-md hover:bg-green-200 transition-colors cursor-pointer"
                    :disabled="connectionStore.processingAction"
                  >
                    <Check v-if="!connectionStore.processingAction" :size="16" class="mr-1.5" />
                    <Loader2 v-else class="w-4 h-4 animate-spin mr-1.5" />
                    Accept
                  </button>
                  <button 
                    @click="handleRejectConnection(connection)"
                    class="flex-1 flex items-center justify-center px-3 py-1.5 bg-red-100 text-red-700 rounded-md hover:bg-red-200 transition-colors cursor-pointer"
                    :disabled="connectionStore.processingAction"
                  >
                    <X v-if="!connectionStore.processingAction" :size="16" class="mr-1.5" />
                    <Loader2 v-else class="w-4 h-4 animate-spin mr-1.5" />
                    Reject
                  </button>
                </div>
                <div v-else class="text-red-600 mt-1">
                  Connection rejected
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="p-4 border-t border-gray-200 bg-gray-50">
          <button 
            @click="$emit('close')" 
            class="w-full py-2 px-4 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 transition-colors cursor-pointer"
          >
            Close
          </button>
        </div>
      </DialogPanel>
    </div>
  </Dialog>
</template>
<script setup>
import { ref } from 'vue';
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/vue';
import api from '@/api/axios';
import { Loader2, Check, X } from 'lucide-vue-next';
import { useUserStore } from '@/stores/user';
import { useConnectionStore } from '@/stores/connection';

const connectionStore = useConnectionStore();
const userStore = useUserStore();

defineProps({
    show: {
        type: Boolean,
        required: true
    },
    connections: {
        type: Array,
        required: true
    },
    loadingConnections: {
        type: Boolean,
        required: true
    }
})

const emit = defineEmits(['connection-updated', 'close'])

const handleAcceptConnection = async (connection) => {
    const success = await connectionStore.handleAcceptConnection(connection);
    if(success) emit('connection-updated');
}

const handleRejectConnection = async (connection) => {
    const success = await connectionStore.handleRejectConnection(connection);
    if(success) emit('connection-updated');
}
</script>