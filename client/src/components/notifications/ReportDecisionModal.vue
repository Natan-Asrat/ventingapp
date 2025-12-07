<template>
  <TransitionRoot as="template" :show="isOpen">
    <Dialog as="div" class="relative z-50">
      <TransitionChild
        as="template"
        enter="ease-out duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-gray-500/75 transition-opacity" />
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
            <DialogPanel class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-2xl sm:p-6">
              <!-- Close button -->
              <div class="absolute top-0 right-0 pt-4 pr-4">
                <button
                  type="button"
                  class="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  @click="closeModal"
                >
                  <span class="sr-only">Close</span>
                  <X class="h-6 w-6 cursor-pointer" />
                </button>
              </div>

              <!-- Modal content -->
              <div class="sm:flex sm:items-start">
                <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
                  <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                    Report Decision Details
                  </DialogTitle>
                  
                  <div class="mt-4 space-y-4">
                    <!-- Report Reason -->
                    <div v-if="reportDecision?.report?.reason" class="bg-white border border-gray-200 p-4 rounded-md">
                      <h4 class="text-sm font-medium text-gray-500 mb-2">Report Reason</h4>
                      <p class="text-sm text-gray-800">{{ reportDecision.report.reason }}</p>
                    </div>

                    <ReportDecisionDetail :report-decision="reportDecision" />
                    <ReportDecisionPost :report-decision="reportDecision" />
                    <ReportDecisionTransaction :report-decision="reportDecision" />
                    <ReportDecisionConnection :report-decision="reportDecision" />
                    <ReportDecisionMessage :report-decision="reportDecision" />

                    <!-- Close Button -->
                    <div class="mt-5 sm:mt-6">
                      <button
                        type="button"
                        class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:text-sm cursor-pointer"
                        @click="closeModal"
                      >
                        Close
                      </button>
                    </div>

                  </div>
                </div>
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