<template>
  <div v-if="connection.message" class="mt-2">
    <div class="text-xs font-medium text-gray-500 mb-1">
      {{ connection.reconnection_requested_by ? 'Reconnection Request' : 'Connection Request' }}
      <span v-if="showRequestedBy" class="text-xs font-normal text-gray-400 ml-1">
        ({{ requestedByText }})
      </span>
    </div>
    <div class="text-sm text-gray-600 bg-gray-50 p-2 rounded">
      "{{ connection.message }}"
    </div>
    
    <div v-if="isCurrentUserRequester" class="mt-2 text-sm text-gray-600">
      <p>You sent a reconnection request {{ connection.formatted_created_at }}</p>
      <p class="text-yellow-600 mt-1">Waiting for approval...</p>
    </div>
    
    <div v-else-if="isReconnectionRequested" class="mt-2 text-sm text-gray-600">
      <p>{{ requestedByText }} {{ connection.formatted_created_at }}</p>
      <div v-if="!connection.reconnection_rejected" class="flex space-x-2 mt-2">
        <button 
          @click="$emit('action', { connection, type: 'accept' })"
          class="flex-1 flex items-center justify-center px-3 py-1.5 bg-green-100 text-green-700 rounded-md hover:bg-green-200 transition-colors cursor-pointer text-sm"
          :disabled="processing"
        >
          <Check v-if="!processing" :size="16" class="mr-1.5" />
          <Loader2 v-else class="w-4 h-4 animate-spin mr-1.5" />
          Accept
        </button>
        <button 
          @click="$emit('action', { connection, type: 'reject' })"
          class="flex-1 flex items-center justify-center px-3 py-1.5 bg-red-100 text-red-700 rounded-md hover:bg-red-200 transition-colors cursor-pointer text-sm"
          :disabled="processing"
        >
          <X v-if="!processing" :size="16" class="mr-1.5" />
          <Loader2 v-else class="w-4 h-4 animate-spin mr-1.5" />
          Reject
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useUserStore } from '@/stores/user';
import { useConnectionStore } from '@/stores/connection';
import { Check, X, Loader2 } from 'lucide-vue-next';

const props = defineProps({
  connection: {
    type: Object,
    required: true
  },
  processing: {
    type: Boolean,
    default: false
  },
  showRequestedBy: {
    type: Boolean,
    default: true
  }
});

const emit = defineEmits(['action']);

const userStore = useUserStore();
const connectionStore = useConnectionStore();

const isCurrentUserRequester = computed(() => {
  return props.connection.reconnection_requested_by === userStore.user?.id;
});

const isReconnectionRequested = computed(() => {
  return !!props.connection.reconnection_requested_by;
});

const requestedByText = computed(() => {
  if (!props.connection.reconnection_requested_by) return '';
  
  if (isCurrentUserRequester.value) {
    return 'You sent a reconnection request';
  }
  
  const otherUser = connectionStore.getOtherUser(props.connection, userStore.user);
  return `Reconnection request sent by @${otherUser?.username || 'user'}`;
});
</script>
