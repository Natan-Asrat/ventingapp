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

      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <DialogPanel class="relative transform overflow-hidden rounded-2xl bg-white px-4 pb-6 pt-6 text-left shadow-2xl transition-all sm:my-8 sm:w-full sm:max-w-sm sm:p-6 border border-zinc-100">
              <div>
                <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-violet-100 ring-4 ring-violet-50">
                  <PartyPopper class="h-8 w-8 text-violet-600" />
                </div>
                <div class="mt-5 text-center">
                  <DialogTitle as="h3" class="text-xl font-bold leading-6 text-zinc-900">
                    Congratulations! 🎉
                  </DialogTitle>
                  <div class="mt-3">
                    <p class="text-sm text-zinc-500">
                      <template v-if="transaction">
                        You successfully received <span class="font-bold text-zinc-800">{{ transaction.connects }} connects</span>
                        <template v-if="transaction.subscription_id">
                          for your subscription renewal
                        </template>
                        <br>
                        <span class="text-xs text-zinc-400 mt-2 block font-medium uppercase tracking-wide">
                          {{ transaction.formatted_created_at }}
                        </span>
                      </template>
                      <template v-else>
                          Operation successful!
                      </template>
                    </p>
                  </div>
                </div>
              </div>
              <div class="mt-6">
                <button
                  type="button"
                  class="inline-flex w-full justify-center rounded-full bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-white shadow-lg hover:bg-violet-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-violet-600 cursor-pointer transition-all hover:-translate-y-0.5"
                  @click="closeModal"
                >
                  Continue
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
import { watch } from 'vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { PartyPopper } from 'lucide-vue-next';
import { useTransactionStore } from '@/stores/transaction';
const transactionStore = useTransactionStore();
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  transaction: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['close']);

const closeModal = () => {
  transactionStore.celebrate();
  emit('close');
};

// Close modal when transaction is cleared
watch(() => props.transaction, (newVal) => {
  if (!newVal) {
    emit('close');
  }
});
</script>