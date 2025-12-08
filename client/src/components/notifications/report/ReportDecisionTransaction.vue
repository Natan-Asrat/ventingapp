<template>
    <!-- Transaction Details -->
    <div v-if="reportDecision?.report?.reported_transaction" class="bg-zinc-50 p-5 rounded-xl border border-zinc-100">
        <h4 class="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-4">Reported Transaction</h4>
        <div class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-2">
            <div>
                <dt class="text-xs font-medium text-zinc-500">Transaction ID</dt>
                <dd class="mt-1 text-sm font-mono text-zinc-800 bg-white px-2 py-1 rounded border border-zinc-200 inline-block">{{ reportDecision.report.reported_transaction.pk }}</dd>
            </div>
            <div>
                <dt class="text-xs font-medium text-zinc-500">Product</dt>
                <dd class="mt-1 text-sm font-semibold text-zinc-900">{{ reportDecision.report.reported_transaction.product_name }}</dd>
            </div>
            <div>
                <dt class="text-xs font-medium text-zinc-500">Amount</dt>
                <dd class="mt-1 text-sm font-bold text-zinc-900">
                    {{ Intl.NumberFormat().format(reportDecision.report.reported_transaction.total_amount) }} {{ reportDecision.report.reported_transaction.currency }}
                </dd>
            </div>
            <div>
                <dt class="text-xs font-medium text-zinc-500">Connects</dt>
                <dd class="mt-1 text-sm font-semibold text-zinc-900">{{ Intl.NumberFormat().format(reportDecision.report.reported_transaction.connects) }}</dd>
            </div>
            <div>
                <dt class="text-xs font-medium text-zinc-500">Payment Method</dt>
                <dd class="mt-1 text-sm text-zinc-900">{{ reportDecision.report.reported_transaction.method }}</dd>
            </div>
            <div>
                <dt class="text-xs font-medium text-zinc-500">Status</dt>
                <dd class="mt-1">
                <span 
                    class="px-2.5 py-0.5 inline-flex text-xs font-bold rounded-full uppercase tracking-wide"
                    :class="{
                    'bg-emerald-100 text-emerald-700': reportDecision.report.reported_transaction.approved,
                    'bg-amber-100 text-amber-700': !reportDecision.report.reported_transaction.approved
                    }"
                >
                    {{ reportDecision.report.reported_transaction.status }}
                </span>
                </dd>
            </div>
            <div class="sm:col-span-2">
                <dt class="text-xs font-medium text-zinc-500">Created</dt>
                <dd class="mt-1 text-sm text-zinc-700">
                    {{ reportDecision.report.reported_transaction.formatted_created_at }} <span class="text-zinc-400">({{ reportDecision.report.reported_transaction.time_ago }})</span>
                </dd>
            </div>
            <div v-if="reportDecision.report.reported_transaction.screenshot_url" class="sm:col-span-2 pt-2">
                <dt class="text-xs font-bold text-zinc-500 uppercase tracking-wide mb-2">Payment Proof</dt>
                <dd>
                <div class="rounded-lg overflow-hidden border border-zinc-200 bg-white">
                    <img 
                        :src="reportDecision.report.reported_transaction.screenshot_url" 
                        alt="Payment proof" 
                        class="h-48 w-full object-contain cursor-zoom-in hover:opacity-95 transition-opacity"
                        @click="openImage(reportDecision.report.reported_transaction.screenshot_url)"
                    />
                </div>
                </dd>
            </div>
        </div>
    </div>
</template>

<script setup>
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

const openImage = (url) => {
  window.open(url, '_blank');
};
</script>