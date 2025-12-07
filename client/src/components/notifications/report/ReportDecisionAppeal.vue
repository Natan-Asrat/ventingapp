<template>
    <!-- Appeal Section -->
    <div v-if="reportDecision?.report?.about_user == userStore.user.id" class="sm:col-span-2 pt-3">
        <div v-if="notificationStore.isLoadingAppeals" class="text-sm text-gray-500">
            Loading appeal information... 
        </div>
        <template v-else>
            <!-- Show existing appeal if any -->
            <div v-if="notificationStore.existingAppeals.length > 0" class="space-y-4">
                <div v-for="appeal in notificationStore.existingAppeals" :key="appeal.id" class="border rounded-md p-4 bg-gray-50">
                    <div class="flex justify-between items-start">
                        <h4 class="text-sm font-medium text-gray-700">Your Appeal</h4>
                        <span 
                            class="px-2 py-1 text-xs font-medium rounded-full"
                            :class="{
                                'bg-yellow-100 text-yellow-800': !appeal.decisions?.length,
                                'bg-green-100 text-green-800': appeal.decisions?.some(d => d.approved),
                                'bg-red-100 text-red-800': appeal.decisions?.some(d => d.rejected)
                            }"
                        >
                            {{ !appeal.decisions?.length ? 'Pending' : 
                            appeal.decisions.some(d => d.approved) ? 'Approved' : 'Rejected' }}
                        </span>
                    </div>
                    <p class="mt-2 text-sm text-gray-600">{{ appeal.message }}</p>
                    <div v-if="appeal.decisions?.length > 0" class="mt-3 pt-3 border-t border-gray-200">
                        <h5 class="text-xs font-medium text-gray-500 mb-1">Decision</h5>
                        <p class="text-sm text-gray-700">{{ appeal.decisions[0].reason || 'No reason provided' }}</p>
                        <p class="text-xs text-gray-500 mt-1">
                        Decided {{ appeal.decisions[0].created_since }}
                        </p>
                    </div>
                    <p class="text-xs text-gray-500 mt-3">
                        Submitted {{ appeal.created_since }}
                    </p>
                </div>
            </div>
            
            <!-- Show appeal form if no existing appeals -->
            <template v-else>
                <div v-if="reportDecision?.from_appeal">
                    <button
                        class="text-sm text-gray-600 hover:text-gray-800 focus:outline-none cursor-pointer"
                    >
                        Reply to your previous Appeal
                    </button>
                </div>
                <div v-else-if="!notificationStore.showAppealForm">
                    <button
                        @click="notificationStore.setShowAppealForm(true)"
                        class="text-sm text-indigo-600 hover:text-indigo-800 focus:outline-none cursor-pointer"
                    >
                        Submit an Appeal
                    </button>
                </div>
                <div v-else class="space-y-2">
                    <label for="appeal-message" class="block text-sm font-medium text-gray-700">Appeal Message</label>
                    <textarea
                        id="appeal-message"
                        :value="notificationStore.appealMessage"
                        @input="e => notificationStore.setAppealMessage(e.target.value)"
                        rows="3"
                        class="mt-1 px-4 py-2 placeholder-gray-500 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        placeholder="Please explain why you're appealing this decision..."
                    ></textarea>
                    <div class="flex space-x-2">
                        <button
                            @click="notificationStore.submitAppeal(reportDecision.id)"
                            :disabled="notificationStore.isSubmittingAppeal"
                            class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                        >
                            <span v-if="notificationStore.isSubmittingAppeal">Submitting...</span>
                            <span v-else>Submit Appeal</span>
                        </button>
                        <button
                            @click="notificationStore.setShowAppealForm(false)"
                            class="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            </template>
        </template>
    </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user';
import { useNotificationStore } from '@/stores/notifications';
const notificationStore = useNotificationStore();
const userStore = useUserStore();
const props = defineProps({
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