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
      <div v-if="loading">
          <div class="fixed z-50 inset-0 bg-zinc-900/20 backdrop-blur-[1px] transition-opacity" />
          <Loader2 class="fixed animate-spin z-50 inset-0 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-16 h-16 text-white flex items-center justify-center drop-shadow-lg" />
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
            <DialogPanel class="relative transform overflow-hidden rounded-2xl bg-white px-4 pb-6 pt-6 text-left shadow-2xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
              <div class="absolute right-0 top-0 pr-4 pt-4">
                <button
                  type="button"
                  class="rounded-full p-1 bg-white text-zinc-400 hover:text-zinc-600 hover:bg-zinc-100 focus:outline-none transition-all cursor-pointer"
                  @click="closeModal"
                >
                  <span class="sr-only">Close</span>
                  <X class="h-6 w-6" aria-hidden="true" />
                </button>
              </div>
              <div class="sm:flex sm:items-start w-full">
                <div class="mt-2 text-center sm:mt-0 sm:text-left w-full">
                  <DialogTitle as="h3" class="text-xl font-bold leading-6 text-zinc-900 text-center mb-6">
                    Wallet
                  </DialogTitle>
                  
                  <div class="bg-gradient-to-br from-amber-50 to-orange-50 rounded-2xl p-6 mb-8 border border-amber-100">
                    <div class="flex flex-col items-center justify-center">
                      <div class="flex items-center justify-center h-14 w-14 rounded-full bg-white shadow-sm ring-4 ring-amber-100 mb-3">
                        <Wallet class="h-7 w-7 text-amber-500" />
                      </div>
                      <p class="text-4xl font-extrabold text-zinc-900 tracking-tight">{{ currentConnects }}</p>
                      <p class="text-sm font-medium text-amber-700/70 mt-1">Available Connects</p>
                    </div>
                  </div>
                    
                  <div class="mt-4">
                      <h4 class="text-sm font-bold text-zinc-800 mb-4 uppercase tracking-wide">Top Up Balance</h4>
                      <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
                        <div 
                          v-for="(item, key) in connectsData" 
                          :key="key"
                          @click="!item.subscribed && purchaseConnects(key)"
                          :class="[
                            'relative rounded-xl border p-4 shadow-sm flex flex-col items-start transition-all duration-200',
                            item.subscribed 
                              ? 'bg-violet-50 border-violet-200 cursor-not-allowed' 
                              : 'bg-white border-zinc-200 hover:border-violet-400 hover:shadow-md hover:-translate-y-0.5 cursor-pointer group'
                          ]"
                        >
                          <div class="flex items-center justify-between w-full mb-3">
                            <div :class="[
                              'h-8 w-8 rounded-full flex items-center justify-center',
                              item.subscribed ? 'bg-violet-100' : 'bg-zinc-100 group-hover:bg-violet-100 transition-colors'
                            ]">
                              <BadgeDollarSign class="h-4 w-4" :class="item.subscribed ? 'text-violet-600' : 'text-zinc-500 group-hover:text-violet-600 transition-colors'" />
                            </div>
                            <div v-if="item.is_sub">
                                <span v-if="item.subscribed" class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-violet-200 text-violet-700 uppercase tracking-wide">
                                  Active
                                </span>
                                <span v-else class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-700 uppercase tracking-wide">
                                  Sub
                                </span>
                            </div>
                          </div>
                          
                          <div class="w-full">
                            <p :class="[
                              'text-lg font-bold',
                              item.subscribed ? 'text-violet-900' : 'text-zinc-900'
                            ]">
                              {{ item.connects }} Connects
                            </p>
                            <div class="flex items-baseline mt-1">
                                <p :class="[
                                    'text-sm font-semibold',
                                    item.subscribed ? 'text-violet-700' : 'text-zinc-600'
                                ]">
                                    ${{ item.price }}{{ item.is_sub ? '/mo' : '' }}
                                </p>
                                <span v-if="item.connects > 1" class="text-xs ml-1.5" :class="item.subscribed ? 'text-violet-400' : 'text-zinc-400'">
                                  (${{ (item.price / item.connects).toFixed(2) }}/ea)
                                </span>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <!-- Pay by Transfer Button -->
                      <div class="mt-8 pt-6 border-t border-zinc-100">
                        <RouterLink
                          :to="{ name: 'ManualPayment' }"
                          class="w-full flex items-center justify-center px-4 py-3 border border-zinc-200 shadow-sm text-sm font-semibold rounded-full text-zinc-700 bg-white hover:bg-zinc-50 hover:border-zinc-300 hover:text-zinc-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-zinc-500 transition-all cursor-pointer"
                        >
                          <Repeat class="h-4 w-4 text-zinc-400 mr-2" />
                          Pay by Bank Transfer
                        </RouterLink>
                        <button
                          @click="supportStore.open()"
                          class="mt-4 w-full cursor-pointer text-center text-xs font-medium text-zinc-400 hover:text-violet-600 hover:underline focus:outline-none transition-colors"
                        >
                          Need help? Contact Support
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
import { defineProps, defineEmits } from 'vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { X, BadgeDollarSign, Wallet, Loader2, Repeat } from 'lucide-vue-next';
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
</script>
