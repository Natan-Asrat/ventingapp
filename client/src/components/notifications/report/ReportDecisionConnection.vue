<template>
    <!-- Connection Details -->
    <div v-if="reportDecision?.report?.reported_connection" class="bg-white border border-zinc-200 rounded-xl overflow-hidden shadow-sm">
        <div class="px-4 py-3 bg-zinc-50 border-b border-zinc-100">
            <h4 class="text-xs font-bold text-zinc-500 uppercase tracking-wide">Reported Connection</h4>
        </div>
        <div class="p-5">
            <!-- Initiating User -->
            <div class="flex items-center space-x-3 mb-4">
                <div v-if="connectionStore.getOtherUser(reportDecision.report.reported_connection, userStore.user).profile_picture" class="flex-shrink-0 h-12 w-12 rounded-full overflow-hidden ring-2 ring-zinc-50">
                    <img 
                        :src="connectionStore.getOtherUser(reportDecision.report.reported_connection, userStore.user).profile_picture" 
                        :alt="connectionStore.getOtherUser(reportDecision.report.reported_connection, userStore.user).name || 'User'"
                        class="h-full w-full object-cover"
                    />
                </div>
                <div v-else class="h-12 w-12 rounded-full bg-violet-100 flex items-center justify-center text-base font-bold text-violet-600 ring-2 ring-zinc-50">
                    {{ (connectionStore.getOtherUser(reportDecision.report.reported_connection, userStore.user)?.name || 'U').charAt(0).toUpperCase() }}
                </div>
                <div class="flex-1 min-w-0">
                    <p class="text-base font-bold text-zinc-900">
                        {{ connectionStore.getOtherUser(reportDecision.report.reported_connection, userStore.user)?.name || 'User' }}
                    </p>
                    <p class="text-sm font-medium text-zinc-500">
                        @{{ connectionStore.getOtherUser(reportDecision.report.reported_connection, userStore.user)?.username }}
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