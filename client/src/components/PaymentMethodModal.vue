<template>
  <TransitionRoot as="template" :show="isOpen">
    <Dialog as="div" class="relative z-50" @close="$emit('close')">
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
            <DialogPanel class="relative transform overflow-hidden rounded-2xl bg-white px-4 pt-5 pb-4 text-left shadow-2xl transition-all sm:my-8 sm:w-full sm:max-w-md sm:p-6 border border-zinc-100">
              <div class="absolute top-0 right-0 hidden pt-4 pr-4 sm:block">
                <button type="button" class="rounded-full bg-white text-zinc-400 hover:text-zinc-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2 cursor-pointer transition-colors hover:bg-zinc-50 p-1" @click="$emit('close')">
                  <span class="sr-only">Close</span>
                  <X class="h-5 w-5" aria-hidden="true" />
                </button>
              </div>
              <form @submit.prevent="handleSubmit">
                <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-violet-100 mb-5">
                  <CreditCard class="h-6 w-6 text-violet-600" aria-hidden="true" />
                </div>
                <div class="text-center sm:text-left">
                  <DialogTitle as="h3" class="text-lg font-bold leading-6 text-zinc-900 text-center">Add Payment Method</DialogTitle>
                  <div class="mt-6 space-y-5">
                    <div class="space-y-1.5">
                      <label for="method" class="block text-xs font-bold text-zinc-700 uppercase tracking-wide">Platform or Bank Name</label>
                      <input
                        type="text"
                        required
                        @invalid="e => e.target.setCustomValidity('This field is required')"
                        @input="e => e.target.setCustomValidity('')"
                        id="method"
                        v-model="paymentData.method"
                        class="block w-full rounded-xl border-zinc-200 bg-zinc-50 shadow-sm focus:border-violet-500 focus:ring-violet-500/20 sm:text-sm p-3 placeholder-zinc-400 transition-all"
                        placeholder="e.g., PayPal, Chase, Binance"
                      />
                    </div>
                    <div class="space-y-1.5">
                      <label for="account" class="block text-xs font-bold text-zinc-700 uppercase tracking-wide">Account Details</label>
                      <input
                        type="text"
                        required
                        @invalid="e => e.target.setCustomValidity('This field is required')"
                        @input="e => e.target.setCustomValidity('')"
                        id="account"
                        v-model="paymentData.account"
                        class="block w-full rounded-xl border-zinc-200 bg-zinc-50 shadow-sm focus:border-violet-500 focus:ring-violet-500/20 sm:text-sm p-3 placeholder-zinc-400 transition-all"
                        placeholder="Email, account number, or wallet address"
                      />
                    </div>
                    <div class="space-y-1.5">
                      <label for="nameOnAccount" class="block text-xs font-bold text-zinc-700 uppercase tracking-wide">Name on Account</label>
                      <input
                        type="text"
                        required
                        @invalid="e => e.target.setCustomValidity('This field is required')"
                        @input="e => e.target.setCustomValidity('')"
                        id="nameOnAccount"
                        v-model="paymentData.nameOnAccount"
                        class="block w-full rounded-xl border-zinc-200 bg-zinc-50 shadow-sm focus:border-violet-500 focus:ring-violet-500/20 sm:text-sm p-3 placeholder-zinc-400 transition-all"
                        placeholder="Name as it appears on your account"
                      />
                    </div>
                  </div>
                </div>
                <div class="mt-8 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
                  <button
                    type="submit"
                    class="inline-flex w-full justify-center rounded-full border border-transparent bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2 sm:col-start-2 transition-all cursor-pointer"
                  >
                    Save Method
                  </button>
                  <button
                    type="button"
                    class="mt-3 inline-flex w-full justify-center rounded-full border border-zinc-300 bg-white px-4 py-2.5 text-sm font-semibold text-zinc-700 shadow-sm hover:bg-zinc-50 focus:outline-none focus:ring-2 focus:ring-zinc-500 focus:ring-offset-2 sm:col-start-1 sm:mt-0 transition-all cursor-pointer"
                    @click="$emit('close')"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, watch } from 'vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { CreditCard, X } from 'lucide-vue-next';


const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  initialData: {
    type: Object,
    default: () => ({
      method: '',
      account: '',
      nameOnAccount: ''
    })
  }
});
const emit = defineEmits(['save', 'close'])
const paymentData = ref({ ...props.initialData });

    // Watch for changes in initialData prop
watch(() => props.initialData, (newVal) => {
  paymentData.value = { ...newVal };
}, { deep: true });

const handleSubmit = () => {
  // HTML5 form validation will handle the required fields
  // If we reach here, the form is valid
  emit('save', { ...paymentData.value });
  emit('close');
};
</script>