<template>
    <!-- Transaction Details -->
    <div v-if="reportDecision?.report?.reported_transaction" class="bg-gray-50 p-4 rounded-md">
        <h4 class="text-sm font-medium text-gray-500 mb-3">Transaction Details</h4>
        <div class="grid grid-cols-1 gap-x-4 gap-y-3 sm:grid-cols-2">
            <div>
                <dt class="text-xs font-medium text-gray-500">Transaction ID</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ reportDecision.report.reported_transaction.pk }}</dd>
            </div>
            <div>
                <dt class="text-xs font-medium text-gray-500">Product</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ reportDecision.report.reported_transaction.product_name }}</dd>
            </div>
            <div>
                <dt class="text-xs font-medium text-gray-500">Amount</dt>
                <dd class="mt-1 text-sm text-gray-900">
                    {{ Intl.NumberFormat().format(reportDecision.report.reported_transaction.total_amount) }} {{ reportDecision.report.reported_transaction.currency }}
                </dd>
            </div>
            <div>
                <dt class="text-xs font-medium text-gray-500">Connects</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ Intl.NumberFormat().format(reportDecision.report.reported_transaction.connects) }}</dd>
            </div>
            <div>
                <dt class="text-xs font-medium text-gray-500">Payment Method</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ reportDecision.report.reported_transaction.method }}</dd>
            </div>
            <div>
                <dt class="text-xs font-medium text-gray-500">Status</dt>
                <dd class="mt-1">
                <span 
                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                    :class="{
                    'bg-green-100 text-green-800': reportDecision.report.reported_transaction.approved,
                    'bg-yellow-100 text-yellow-800': !reportDecision.report.reported_transaction.approved
                    }"
                >
                    {{ reportDecision.report.reported_transaction.status }}
                </span>
                </dd>
            </div>
            <div class="sm:col-span-2">
                <dt class="text-xs font-medium text-gray-500">Created</dt>
                <dd class="mt-1 text-sm text-gray-900">
                    {{ reportDecision.report.reported_transaction.formatted_created_at }} ({{ reportDecision.report.reported_transaction.time_ago }})
                </dd>
            </div>
            <div v-if="reportDecision.report.reported_transaction.screenshot_url" class="sm:col-span-2">
                <dt class="text-xs font-medium text-gray-500 mb-1">Payment Proof</dt>
                <dd class="mt-1">
                <img 
                    :src="reportDecision.report.reported_transaction.screenshot_url" 
                    alt="Payment proof" 
                    class="h-40 w-auto object-contain border rounded-md"
                    @click="openImage(reportDecision.report.reported_transaction.screenshot_url)"
                />
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