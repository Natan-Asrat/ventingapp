<template>
    <!-- Decision Details -->
    <div class="bg-zinc-50 p-5 rounded-xl border border-zinc-100">
        <h4 class="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-4">Decision Information</h4>
        <dl class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-2">
            <div>
                <dt class="text-xs font-medium text-zinc-500">Decision Date</dt>
                <dd class="mt-1 text-sm font-semibold text-zinc-900">
                    {{ reportDecision?.formatted_created_at }} <span class="text-zinc-400 font-normal">({{ reportDecision?.created_since }})</span>
                </dd>
            </div>
            <div class="sm:col-span-2">
                <dt class="text-xs font-medium text-zinc-500 mb-1">Status</dt>
                <dd>
                <span 
                    class="px-3 py-1 inline-flex text-xs font-bold rounded-full uppercase tracking-wide"
                    :class="{
                    'bg-emerald-100 text-emerald-700': reportDecision?.approved,
                    'bg-rose-100 text-rose-700': reportDecision?.rejected,
                    'bg-amber-100 text-amber-700': !reportDecision?.approved && !reportDecision?.rejected
                    }"
                >
                    {{ reportDecision?.approved ? 'Approved' : reportDecision?.rejected ? 'Rejected' : 'Pending' }}
                </span>
                </dd>
            </div>
            <div v-if="reportDecision?.reason" class="sm:col-span-2">
                <dt class="text-xs font-medium text-zinc-500">Decision Reasoning</dt>
                <dd class="mt-1 text-sm text-zinc-800 bg-white p-3 rounded-lg border border-zinc-200">{{ reportDecision.reason }}</dd>
            </div>
            <div class="sm:col-span-2 pt-2">
                 <ReportDecisionAppeal :report-decision="reportDecision"/>
            </div>
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