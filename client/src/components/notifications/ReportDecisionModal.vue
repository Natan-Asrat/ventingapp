<template>
  <TransitionRoot as="template" :show="isOpen">
    <Dialog as="div" class="relative z-50" @close="closeModal">
      <TransitionChild
        as="template"
        enter="ease-out duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-zinc-900/60 backdrop-blur-sm transition-opacity" />
      </TransitionChild>

      <div class="fixed inset-0 z-50 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center sm:p-0">
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <DialogPanel class="relative transform overflow-hidden rounded-2xl bg-white text-left shadow-2xl transition-all sm:my-8 sm:w-full sm:max-w-2xl border border-zinc-100">
              <!-- Header -->
              <div class="px-6 py-4 border-b border-zinc-100 bg-zinc-50/50 flex justify-between items-center sticky top-0 z-10">
                <DialogTitle as="h3" class="text-lg font-bold leading-6 text-zinc-900">
                  Report Decision Details
                </DialogTitle>
                <button
                  type="button"
                  class="rounded-full p-1 text-zinc-400 hover:text-zinc-600 hover:bg-zinc-100 focus:outline-none transition-all cursor-pointer"
                  @click="closeModal"
                >
                  <span class="sr-only">Close</span>
                  <X class="h-5 w-5" />
                </button>
              </div>

              <!-- Modal content -->
              <div class="px-6 py-6 max-h-[80vh] overflow-y-auto bg-white">
                  <div class="space-y-6">
                    <!-- Report Reason -->
                    <div v-if="reportDecision?.report?.reason" class="bg-amber-50 border border-amber-100 p-4 rounded-xl">
                      <div class="flex items-start">
                         <div class="flex-shrink-0 mr-3 mt-0.5">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-amber-500" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                            </svg>
                         </div>
                         <div>
                            <h4 class="text-sm font-bold text-amber-800 mb-1">Original Report Reason</h4>
                            <p class="text-sm text-amber-700 leading-relaxed">{{ reportDecision.report.reason }}</p>
                         </div>
                      </div>
                    </div>

                    <ReportDecisionDetail :report-decision="reportDecision" />
                    
                    <div class="border-t border-zinc-100 pt-6">
                        <ReportDecisionPost :report-decision="reportDecision" />
                        <ReportDecisionTransaction :report-decision="reportDecision" />
                        <ReportDecisionConnection :report-decision="reportDecision" />
                        <ReportDecisionMessage :report-decision="reportDecision" />
                    </div>
                  </div>
              </div>
              
              <!-- Footer -->
              <div class="px-6 py-4 bg-zinc-50 border-t border-zinc-100 flex justify-end">
                  <button
                    type="button"
                    class="inline-flex justify-center rounded-full border border-zinc-300 bg-white px-5 py-2 text-sm font-semibold text-zinc-700 shadow-sm hover:bg-zinc-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-zinc-500 transition-colors cursor-pointer"
                    @click="closeModal"
                  >
                    Close
                  </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { onMounted  } from 'vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { X } from 'lucide-vue-next';
import { useNotificationStore } from '@/stores/notifications';
import ReportDecisionDetail from '@/components/notifications/report/ReportDecisionDetail.vue';
import ReportDecisionPost from '@/components/notifications/report/ReportDecisionPost.vue';
import ReportDecisionTransaction from '@/components/notifications/report/ReportDecisionTransaction.vue';
import ReportDecisionConnection from '@/components/notifications/report/ReportDecisionConnection.vue';
import ReportDecisionMessage from '@/components/notifications/report/ReportDecisionMessage.vue';
const notificationStore = useNotificationStore();
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
  reportDecision: {
    type: Object,
    default: () => ({
      report: {
        reported_transaction: {}
      }
    })
  },
});

const emit = defineEmits(['close']);

// Fetch appeals when modal opens
onMounted(async () => {
    await notificationStore.fetchMyAppeals(props.reportDecision?.id);
});

const closeModal = () => {
  emit('close');
};
</script>