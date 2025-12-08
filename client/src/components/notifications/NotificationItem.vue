<template>
    <div 
        class="relative bg-white rounded-xl shadow-sm border transition-all duration-200 overflow-hidden group"
        :class="[
            !notification.viewed 
                ? 'border-violet-200 bg-white shadow-md' 
                : 'border-zinc-100 bg-zinc-50/30 opacity-90 hover:opacity-100 hover:bg-white hover:border-zinc-200'
        ]"
    >
        <div class="absolute left-0 top-0 bottom-0 w-1 bg-violet-500" v-if="!notification.viewed"></div>
        
        <div class="p-4 pl-5">
            <div class="flex items-start gap-4">
                <div class="flex-shrink-0 mt-0.5">
                    <div 
                        class="h-10 w-10 rounded-full flex items-center justify-center ring-2 ring-white shadow-sm"
                        :class="!notification.viewed ? 'bg-violet-100 text-violet-600' : 'bg-zinc-100 text-zinc-400'"
                    >
                        <CircleAlert v-if="notification.report_decision" class="h-5 w-5" />
                        <CircleCheckBig v-else-if="notification.viewed" class="h-5 w-5" />
                        <Bell v-else class="h-5 w-5" />
                    </div>
                </div>
                <div class="flex-1 min-w-0">
                    <div class="flex items-center justify-between mb-1">
                        <p 
                            class="text-sm font-bold truncate pr-2"
                            :class="!notification.viewed ? 'text-zinc-900' : 'text-zinc-700'"
                        >
                            {{ notification.title }}
                        </p>
                        <span 
                            class="text-xs font-medium whitespace-nowrap"
                            :class="!notification.viewed ? 'text-violet-600' : 'text-zinc-400'"
                        >
                            {{ notification.created_since }}
                        </span>
                    </div>

                    <!-- Context Badges (Report Decision specific) -->
                    <div v-if="notification.report_decision" class="flex flex-wrap gap-2 mb-2 mt-1">
                        <span v-if="reportContext" class="inline-flex items-center px-2 py-0.5 rounded-md text-[10px] font-bold bg-zinc-100 text-zinc-600 border border-zinc-200 uppercase tracking-wide">
                            <component :is="reportContext.icon" class="w-3 h-3 mr-1" />
                            {{ reportContext.type }}
                        </span>
                        <span v-if="reportStatus" class="inline-flex items-center px-2 py-0.5 rounded-md text-[10px] font-bold border uppercase tracking-wide" :class="reportStatus.class">
                            {{ reportStatus.label }}
                        </span>
                    </div>

                    <p class="text-sm text-zinc-600 leading-relaxed line-clamp-2">
                        {{ notification.message }}
                    </p>
                    
                    <!-- Report decision actions -->
                    <div v-if="notification.report_decision" class="mt-3 flex space-x-3">
                        <button
                            @click="notificationStore.openReportModal(notification.report_decision)"
                            class="inline-flex items-center px-4 py-1.5 border border-zinc-200 text-xs font-semibold rounded-full text-zinc-700 bg-white hover:bg-zinc-50 hover:border-zinc-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 transition-all cursor-pointer shadow-sm"
                        >
                            View Report Details
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { useNotificationStore } from '@/stores/notifications';
import { CircleCheckBig, Bell, CircleAlert, FileText, Wallet, Users, MessageSquare } from 'lucide-vue-next';
const notificationStore = useNotificationStore();

const props = defineProps({
    notification: {
        type: Object,
        required: true
    }
})

const reportContext = computed(() => {
    if (!props.notification.report_decision?.report) return null;
    
    const report = props.notification.report_decision.report;
    const type = report.report_type;

    if (type === 'post' || report.reported_post) return { type: 'Post', icon: FileText };
    if (type === 'transaction' || report.reported_transaction) return { type: 'Transaction', icon: Wallet };
    if (type === 'connection' || report.reported_connection) return { type: 'Connection', icon: Users };
    if (type === 'message' || report.reported_message) return { type: 'Message', icon: MessageSquare };
    
    return { type: 'Content', icon: FileText };
});

const reportStatus = computed(() => {
    if (!props.notification.report_decision) return null;
    
    const decision = props.notification.report_decision;
    if (decision.approved) return { label: 'Report Approved', class: 'bg-emerald-100 text-emerald-700 border-emerald-200' };
    if (decision.rejected) return { label: 'Report Rejected', class: 'bg-rose-100 text-rose-700 border-rose-200' };
    return { label: 'Pending Review', class: 'bg-amber-100 text-amber-700 border-amber-200' };
});
</script>