<template>
    <!-- Decision Details -->
    <div class="bg-gray-50 p-4 rounded-md">
        <h4 class="text-sm font-medium text-gray-500 mb-3">Decision Information</h4>
        <dl class="grid grid-cols-1 gap-x-4 gap-y-3 sm:grid-cols-2">
            <div>
                <dt class="text-xs font-medium text-gray-500">Decision Date</dt>
                <dd class="mt-1 text-sm text-gray-900">
                    {{ reportDecision?.formatted_created_at }} ({{ reportDecision?.created_since }})
                </dd>
            </div>
            <div class="sm:col-span-2">
                <dt class="text-xs font-medium text-gray-500">Status</dt>
                <dd class="mt-1">
                <span 
                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                    :class="{
                    'bg-green-100 text-green-800': reportDecision?.approved,
                    'bg-red-100 text-red-800': reportDecision?.rejected,
                    'bg-yellow-100 text-yellow-800': !reportDecision?.approved && !reportDecision?.rejected
                    }"
                >
                    {{ reportDecision?.approved ? 'Approved' : reportDecision?.rejected ? 'Rejected' : 'Pending' }}
                </span>
                </dd>
            </div>
            <div v-if="reportDecision?.reason" class="sm:col-span-2">
                <dt class="text-xs font-medium text-gray-500">Reason</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ reportDecision.reason }}</dd>
            </div>
            <ReportDecisionAppeal :report-decision="reportDecision"/>
        </dl>
    </div>
</template>

<script setup>
import ReportDecisionAppeal from "@/components/notifications/report/ReportDecisionAppeal.vue"
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