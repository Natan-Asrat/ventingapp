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
        <div class="fixed inset-0 bg-gray-500/75 transition-opacity" />
      </TransitionChild>
      <div v-if="loading">
          <div class="fixed z-100 inset-0 bg-gray-500/75 transition-opacity" />
          <Loader2 class="fixed animate-spin z-100 inset-0 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-16 h-16 text-white flex items-center justify-center" />
      </div>


      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <DialogPanel class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
              <div class="absolute right-0 top-0 pr-4 pt-4">
                <button
                  type="button"
                  class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none cursor-pointer"
                  @click="closeModal"
                >
                  <span class="sr-only">Close</span>
                  <X class="h-6 w-6" aria-hidden="true" />
                </button>
              </div>
              <div class="sm:flex sm:items-start">
                <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
                  <DialogTitle as="h3" class="text-base font-semibold leading-6 text-gray-900">
                    Your Connects
                  </DialogTitle>
                  <div class="mt-4">
                    <div class="flex items-center justify-center mb-6">
                      <div class="flex items-center justify-center h-16 w-16 rounded-full bg-amber-100">
                        <Wallet class="h-8 w-8 text-amber-600" />
                      </div>
                      <div class="ml-4">
                        <p class="text-3xl font-bold text-gray-900">{{ currentConnects }}</p>
                        <p class="text-sm text-gray-500">Available connects</p>
                      </div>
                    </div>
                    
                    <div class="mt-8">
                      <h4 class="text-sm font-medium text-gray-900 mb-4">Buy More Connects</h4>
                      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                        <div 
                          v-for="(item, key) in connectsData" 
                          :key="key"
                          @click="!item.subscribed && purchaseConnects(key)"
                          :class="[
                            'relative rounded-lg border px-6 py-8 shadow-sm flex items-center space-x-3 transition-colors',
                            item.subscribed 
                              ? 'bg-indigo-50 border-indigo-200 cursor-not-allowed' 
                              : 'bg-white border-gray-300 hover:border-indigo-500 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500 cursor-pointer'
                          ]"
                        >
                          <div class="flex-shrink-0">
                            <div :class="[
                              'h-10 w-10 rounded-full flex items-center justify-center',
                              item.subscribed ? 'bg-indigo-100' : 'bg-amber-100'
                            ]">
                              <BadgeDollarSign class="h-5 w-5" :class="item.subscribed ? 'text-indigo-600' : 'text-amber-600'" />
                            </div>
                          </div>
                          <div class="flex-1 min-w-0">
                            <div class="focus:outline-none">
                              <p :class="[
                                'text-sm font-medium',
                                item.subscribed ? 'text-indigo-600' : 'text-gray-900'
                              ]">
                                {{ item.connects }} Connects{{ item.is_sub ? '/mo' : '' }}
                                <span v-if="item.subscribed" class="text-xs text-indigo-400 ml-1">(active)</span>
                              </p>
                              <p :class="[
                                'text-sm',
                                item.subscribed ? 'text-indigo-500' : 'text-gray-500'
                              ]">
                                ${{ item.price }}{{ item.is_sub ? '/mo' : '' }}
                                <span v-if="item.connects > 1" class="text-xs ml-1" :class="item.subscribed ? 'text-indigo-300' : 'text-gray-400'">
                                  (${{ (item.price / item.connects).toFixed(2) }}/connect)
                                </span>
                              </p>
                            </div>
                          </div>
                          <div v-if="item.is_sub" class="absolute top-1 right-1">
                            <span v-if="item.subscribed" class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-indigo-100 text-indigo-700">
                              Subscribed
                            </span>
                            <span v-else class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                              Subscribe
                            </span>
                          </div>
                        </div>
                      </div>
                      
                      <!-- Pay by Transfer Button -->
                      <div class="mt-6 pt-6 border-t border-gray-200">
                        <RouterLink
                          :to="{ name: 'ManualPayment' }"
                          class="w-full flex items-center justify-center px-4 py-3 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer"
                        >
                          <svg class="h-5 w-5 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                          </svg>
                          Or Pay by Bank Transfer
                        </RouterLink>
                        <button
                          @click="supportStore.open()"
                          class="mt-4 w-full cursor-pointer text-center text-sm text-gray-500 hover:text-indigo-600 hover:underline focus:outline-none"
                        >
                          Contact Support
                        </button>
                      </div>
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
import { ref, defineProps, defineEmits } from 'vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { X, BadgeDollarSign, Wallet, Loader2 } from 'lucide-vue-next';
import { RouterLink } from 'vue-router';
import { useSupportStore } from '@/stores/support';
const supportStore = useSupportStore(); 
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  currentConnects: {
    type: Number,
    default: 0
  },
  connectsData: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close', 'purchase', 'transfer']);

const closeModal = () => {
  emit('close');
};

const purchaseConnects = (packageKey) => {
  emit('purchase', packageKey);
};

const handleTransferPayment = () => {
  emit('transfer');
};
</script>
