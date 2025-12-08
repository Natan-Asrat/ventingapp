<template>
  <div v-if="connection.message" class="mt-4 border-t border-zinc-100 pt-3">
    <div v-if="connection.reconnection_requested_by" class="flex items-center text-xs font-semibold text-zinc-500 mb-2 uppercase tracking-wide">
      <span class="bg-zinc-100 px-2 py-0.5 rounded text-zinc-600 mr-2">
         {{ connection.reconnection_requested_by ? 'Reconnection Request' : 'Connection Request' }}
      </span>
      <span v-if="showRequestedBy" class="text-zinc-400 font-medium normal-case">
        {{ requestedByText }}
      </span>
    </div>
    
    <div class="relative bg-zinc-50 p-4 rounded-xl border border-zinc-100/50">
        <svg class="absolute top-4 left-3 w-4 h-4 text-zinc-300" fill="currentColor" viewBox="0 0 24 24"><path d="M14.017 21L14.017 18C14.017 16.8954 13.1216 16 12.017 16H9C9 14.8954 9.89543 14 11 14C11.5523 14 12 13.5523 12 13V7C12 6.44772 11.5523 6 11 6C10.4477 6 10 6.44772 10 7V13C10 13.5523 10.4477 14 11 14V14C11 15.1046 10.1046 16 9 16H6C4.89543 16 4 16.8954 4 18V21" /></svg>
        <p class="text-sm text-zinc-700 leading-relaxed italic pl-6">
            "{{ connection.message }}"
        </p>
    </div>
    
    <div v-if="isCurrentUserRequester" class="mt-3 flex items-center justify-between text-xs font-medium">
      <p class="text-zinc-400">Sent {{ connection.formatted_created_at }}</p>
      <span class="text-amber-600 bg-amber-50 px-2 py-0.5 rounded-full border border-amber-100">Waiting for approval</span>
    </div>
    
    <div v-else-if="isReconnectionRequested" class="mt-3">
      <p class="text-xs text-zinc-400 font-medium mb-3">{{ requestedByText }} • {{ connection.formatted_created_at }}</p>
      <div v-if="!connection.reconnection_rejected" class="flex space-x-3">
        <button 
          @click="$emit('action', { connection, type: 'accept' })"
          class="flex-1 flex items-center justify-center px-4 py-2 bg-zinc-900 text-white rounded-full hover:bg-emerald-600 shadow-sm hover:shadow-md transition-all cursor-pointer text-xs font-bold uppercase tracking-wide"
          :disabled="processing"
        >
          <Check v-if="!processing" :size="14" class="mr-1.5 stroke-[3]" />
          <Loader2 v-else class="w-3.5 h-3.5 animate-spin mr-1.5" />
          Accept
        </button>
        <button 
          @click="$emit('action', { connection, type: 'reject' })"
          class="flex-1 flex items-center justify-center px-4 py-2 bg-white border border-zinc-200 text-zinc-700 rounded-full hover:bg-rose-50 hover:text-rose-600 hover:border-rose-200 transition-all cursor-pointer text-xs font-bold uppercase tracking-wide"
          :disabled="processing"
        >
          <X v-if="!processing" :size="14" class="mr-1.5 stroke-[3]" />
          <Loader2 v-else class="w-3.5 h-3.5 animate-spin mr-1.5" />
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
    return 'You sent a request';
  }
  
  const otherUser = connectionStore.getOtherUser(props.connection, userStore.user);
  return `Request by @${otherUser?.username || 'user'}`;
});
</script>