<template>
    <!-- Appeal Section -->
    <div v-if="reportDecision?.report?.about_user == userStore.user.id" class="sm:col-span-2 pt-4 border-t border-zinc-100 mt-2">
        <div v-if="notificationStore.isLoadingAppeals" class="flex items-center space-x-2 text-sm text-zinc-500 py-2">
             <div class="animate-spin h-4 w-4 border-2 border-violet-500 border-t-transparent rounded-full"></div>
             <span>Loading appeal information...</span>
        </div>
        <template v-else>
            <!-- Show existing appeal if any -->
            <div v-if="notificationStore.existingAppeals.length > 0" class="space-y-4">
                <div v-for="appeal in notificationStore.existingAppeals" :key="appeal.id" class="border border-zinc-200 rounded-xl p-5 bg-white shadow-sm">
                    <div class="flex justify-between items-start mb-3">
                        <div class="flex items-center gap-2">
                            <div class="bg-violet-100 p-1.5 rounded-lg">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-violet-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
                                </svg>
                            </div>
                            <h4 class="text-sm font-bold text-zinc-900">Your Appeal</h4>
                        </div>
                        <span 
                            class="px-2.5 py-0.5 text-[10px] font-bold rounded-full uppercase tracking-wide"
                            :class="{
                                'bg-amber-100 text-amber-700': !appeal.decisions?.length,
                                'bg-emerald-100 text-emerald-700': appeal.decisions?.some(d => d.approved),
                                'bg-rose-100 text-rose-700': appeal.decisions?.some(d => d.rejected)
                            }"
                        >
                            {{ !appeal.decisions?.length ? 'Pending Review' : 
                            appeal.decisions.some(d => d.approved) ? 'Approved' : 'Rejected' }}
                        </span>
                    </div>
                    
                    <div class="bg-zinc-50 rounded-lg p-3 border border-zinc-100">
                        <p class="text-sm text-zinc-700 leading-relaxed">{{ appeal.message }}</p>
                    </div>

                    <div v-if="appeal.decisions?.length > 0" class="mt-4 pt-4 border-t border-zinc-100">
                        <h5 class="text-xs font-bold text-zinc-400 uppercase tracking-wide mb-2">Admin Decision</h5>
                        <div class="bg-zinc-50 rounded-lg p-3 border border-zinc-100">
                             <p class="text-sm text-zinc-800 font-medium">{{ appeal.decisions[0].reason || 'No specific reason provided.' }}</p>
                        </div>
                        <p class="text-xs text-zinc-400 mt-2 font-medium flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Decided {{ appeal.decisions[0].created_since }}
                        </p>
                    </div>
                    
                    <div class="mt-3 flex justify-end">
                        <p class="text-xs text-zinc-400 font-medium">
                            Submitted {{ appeal.created_since }}
                        </p>
                    </div>
                </div>
            </div>
            
            <!-- Show appeal form if no existing appeals -->
            <template v-else>
                <div v-if="reportDecision?.from_appeal" class="py-2">
                    <button
                        class="text-sm font-semibold text-zinc-600 hover:text-zinc-900 focus:outline-none cursor-pointer flex items-center transition-colors"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
                        </svg>
                        Reply to your previous Appeal
                    </button>
                </div>
                <div v-else-if="!notificationStore.showAppealForm" class="py-2">
                    <button
                        @click="notificationStore.setShowAppealForm(true)"
                        class="text-sm font-semibold text-violet-600 hover:text-violet-700 focus:outline-none cursor-pointer flex items-center transition-colors hover:bg-violet-50 px-3 py-2 rounded-lg -ml-3"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                        </svg>
                        Appeal this Decision
                    </button>
                </div>
                <div v-else class="space-y-3 bg-zinc-50 p-4 rounded-xl border border-zinc-100 mt-2">
                    <div>
                        <label for="appeal-message" class="block text-xs font-bold text-zinc-700 uppercase tracking-wide mb-2">Appeal Message</label>
                        <textarea
                            id="appeal-message"
                            :value="notificationStore.appealMessage"
                            @input="e => notificationStore.setAppealMessage(e.target.value)"
                            rows="4"
                            class="block w-full rounded-xl border-zinc-200 bg-white shadow-sm focus:border-violet-500 focus:ring-violet-500/20 sm:text-sm p-3 placeholder-zinc-400 transition-all resize-none"
                            placeholder="Please explain why you believe this decision should be reconsidered..."
                        ></textarea>
                    </div>
                    <div class="flex items-center justify-end space-x-3 pt-1">
                        <button
                            @click="notificationStore.setShowAppealForm(false)"
                            class="inline-flex items-center px-4 py-2 border border-zinc-300 text-sm font-medium rounded-full text-zinc-700 bg-white hover:bg-zinc-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-zinc-500 transition-colors cursor-pointer shadow-sm"
                        >
                            Cancel
                        </button>
                        <button
                            @click="notificationStore.submitAppeal(reportDecision.id)"
                            :disabled="notificationStore.isSubmittingAppeal || !notificationStore.appealMessage"
                            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-full text-white bg-zinc-900 hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer shadow-sm"
                        >
                            <span v-if="notificationStore.isSubmittingAppeal" class="flex items-center">
                                <span class="animate-spin h-4 w-4 border-2 border-white/30 border-t-white mr-2 rounded-full"></span>
                                Submitting...
                            </span>
                            <span v-else>Submit Appeal</span>
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