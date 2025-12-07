<template>
    <div 
        class="bg-white rounded-lg shadow overflow-hidden border-l-4"
        :class="{
            'border-indigo-500': !notification.viewed,
            'border-transparent': notification.viewed,
            'opacity-75': notification.viewed
        }"
    >
        <div class="p-4">
            <div class="flex items-start">
                <div class="flex-shrink-0 pt-0.5">
                    <div class="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center">
                        <CircleQuestionMark v-if="!notification.viewed" class="h-5 w-5 text-indigo-600" />
                        <CircleCheckBig v-else class="h-5 w-5 text-gray-400" />
                    </div>
                </div>
                <div class="ml-3 flex-1">
                    <div class="flex items-center justify-between">
                        <p class="text-sm font-medium text-gray-900">
                            {{ notification.title }}
                        </p>
                        <p class="text-xs text-gray-500">
                            {{ notification.created_since }}
                        </p>
                    </div>
                    <p class="mt-1 text-sm text-gray-600">
                        {{ notification.message }}
                    </p>
                    
                    <!-- Report decision actions -->
                    <div v-if="notification.report_decision" class="mt-3 flex space-x-3">
                        <button
                            @click="notificationStore.openReportModal(notification.report_decision)"
                            class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer"
                        >
                            View Report
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useNotificationStore } from '@/stores/notifications';
import { CircleQuestionMark, CircleCheckBig} from 'lucide-vue-next';
const notificationStore = useNotificationStore();

defineProps({
    notification: {
        type: Object,
        required: true
    }
})
</script>
