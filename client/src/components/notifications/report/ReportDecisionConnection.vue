<template>
    <!-- Connection Details -->
    <div v-if="reportDecision?.report?.reported_connection" class="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <div class="p-4 border-b border-gray-200">
            <h4 class="text-sm font-medium text-gray-500 mb-3">Reported Connection</h4>
            
            <!-- Initiating User -->
            <div class="flex items-start space-x-3 mb-4">
                <div v-if="connectionStore.getOtherUser(reportDecision.report.reported_connection, userStore.user).profile_picture" class="flex-shrink-0 h-10 w-10 rounded-full overflow-hidden">
                    <img 
                        :src="connectionStore.getOtherUser(reportDecision.report.reported_connection, userStore.user).profile_picture" 
                        :alt="connectionStore.getOtherUser(reportDecision.report.reported_connection, userStore.user).name || 'User'"
                        class="h-full w-full object-cover"
                    />
                </div>
                <div v-else class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-sm text-gray-600">
                    {{ (connectionStore.getOtherUser(reportDecision.report.reported_connection, userStore.user)?.name || 'U').charAt(0).toUpperCase() }}
                </div>
                <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900">
                        {{ connectionStore.getOtherUser(reportDecision.report.reported_connection, userStore.user)?.name || 'User' }}
                        <span class="text-xs font-normal text-gray-500">
                        @{{ connectionStore.getOtherUser(reportDecision.report.reported_connection, userStore.user)?.username }}
                        </span>
                    </p>
                </div>
            </div>
            
            <!-- Connection Message Component -->
            <ConnectionMessage 
                :connection="reportDecision.report.reported_connection"
                :processing="false"
                :show-requested-by="false"
            />
        </div>
    </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user';
import { useConnectionStore } from '@/stores/connection';
import ConnectionMessage from '@/components/ConnectionMessage.vue';
const connectionStore = useConnectionStore();
const userStore = useUserStore();
defineProps({
  reportDecision: {
    type: Object,
    default: () => ({
      report: {
        reported_transaction: {}
      }
    })
  },
});
</script>