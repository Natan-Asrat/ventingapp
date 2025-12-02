<template>
  <Dialog :open="show" @close="$emit('close')" class="relative z-50">
    <!-- The backdrop, rendered as a fixed sibling to the panel container -->
    <div class="fixed inset-0 bg-black/50" aria-hidden="true" />

    <!-- Full-screen container to center the panel -->
    <div class="fixed inset-0 flex items-center justify-center p-4">
      <DialogPanel class="w-full max-w-md bg-white rounded-lg p-6">
        <div class="text-center">
          <DialogTitle class="text-lg font-medium text-gray-900 mb-2">
            Connect with {{ userName }}
          </DialogTitle>
          
          <div class="mt-2">
            <p class="text-sm text-gray-500">
              <template v-if="!isPending && !isRejected">
                <span v-if="purpose == 'donate'">You need to connect with this user before you can donate to them.</span>
                <span v-else-if="purpose == 'chat'"> You need to connect with this user before you can chat with them.</span>
                <span v-else> You need to connect with this user first.</span>
              </template>
              <template v-else>
                <span v-if="purpose == 'donate'">
                  You have a pending connection request with {{ userName }}. You'll be able to see their donation details once they accept your request.
                </span>
                <span v-else-if="purpose == 'chat'">
                  You have a pending connection request with {{ userName }}. You'll be able to chat with them once they accept your request.
                </span>
                <span v-else>
                  You have a pending connection request with {{ userName }}. You'll be able to continue once they accept your request.
                </span>
              </template>
            </p>
            
            <p class="text-xs text-gray-500 mt-2">
              Connecting with a user will cost you 1 connect.
            </p>
          </div>

          <div class="mt-6 flex flex-col space-y-3">
            <button
              v-if="!isPending && !isRejected"
              type="button"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer"
              @click="handleConnect"
              :disabled="loading"
            >
              <Loader2 v-if="loading" class="w-4 h-4 mr-2 animate-spin" />
              {{ loading ? 'Connecting...' : 'Connect' }}
            </button>
            
            <button
              type="button"
              class="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer"
              @click="$emit('close')"
              :disabled="loading"
            >
              {{ isPending || isRejected ? 'Close' : 'Cancel' }}
            </button>
          </div>
        </div>
      </DialogPanel>
    </div>
  </Dialog>
</template>

<script setup>
import { ref } from 'vue';
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/vue';
import { Loader2 } from 'lucide-vue-next';

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  purpose: {
    type: String,
    required: true
  },
  userName: {
    type: String,
    required: true
  },
  isPending: {
    type: Boolean,
    default: false
  },
  isRejected: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['connect', 'close']);
const loading = ref(false);

const handleConnect = async () => {
  try {
    loading.value = true;
    await emit('connect');
  } finally {
    loading.value = false;
  }
};
</script>
