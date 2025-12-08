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

      <div class="fixed inset-0 z-10 overflow-y-auto">
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
            <DialogPanel class="relative transform overflow-hidden rounded-2xl bg-white text-left shadow-2xl transition-all sm:my-8 sm:w-full sm:max-w-lg border border-zinc-100">
               <!-- Close Button -->
              <div class="absolute top-4 right-4 z-10">
                <button
                  type="button"
                  class="rounded-full p-1 bg-white/80 text-zinc-400 hover:text-zinc-600 hover:bg-zinc-100 focus:outline-none transition-all cursor-pointer backdrop-blur-sm"
                  @click="$emit('close')"
                >
                  <span class="sr-only">Close</span>
                  <X class="h-5 w-5" aria-hidden="true" />
                </button>
              </div>

              <!-- Header / Logo -->
              <div class="bg-zinc-50 px-6 py-6 border-b border-zinc-100 flex flex-col items-center">
                 <div class="h-16 w-16 bg-white rounded-2xl flex items-center justify-center mb-3 shadow-sm border border-zinc-100 p-2">
                    <img 
                      v-if="paymentOption?.logo_url" 
                      :src="paymentOption?.logo_url" 
                      :alt="paymentOption?.method" 
                      class="max-h-full max-w-full object-contain"
                    >
                    <CreditCard v-else class="h-8 w-8 text-zinc-300" />
                 </div>
                 <DialogTitle as="h3" class="text-xl font-bold leading-6 text-zinc-900 text-center">
                    {{ paymentOption?.method }}
                 </DialogTitle>
                 <p class="text-xs font-medium text-zinc-400 uppercase tracking-wide mt-1">Manual Transfer</p>
              </div>

              <!-- Body -->
              <div class="px-6 py-6 space-y-6">
                 <!-- Account Details Box -->
                 <div class="bg-violet-50/50 rounded-xl p-4 border border-violet-100/50">
                    <h4 class="text-xs font-bold text-violet-600 uppercase tracking-wide mb-3 flex items-center">
                        <Info class="h-3.5 w-3.5 mr-1.5" />
                        Transfer Details
                    </h4>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <span class="text-zinc-500">Account Number:</span>
                            <span class="font-mono font-bold text-zinc-800 select-all">{{ paymentOption?.account }}</span>
                        </div>
                         <div class="flex justify-between">
                            <span class="text-zinc-500">Account Name:</span>
                            <span class="font-bold text-zinc-800 select-all">{{ paymentOption?.nameOnAccount }}</span>
                        </div>
                    </div>
                 </div>

                 <p class="text-sm text-zinc-600 leading-relaxed text-center">
                    Please transfer the exact amount to the account above and upload the screenshot of your transaction below.
                 </p>

                 <!-- Form -->
                 <div class="space-y-5">
                     <div class="grid grid-cols-2 gap-4">
                        <div class="space-y-1.5">
                            <label for="connects" class="block text-xs font-bold text-zinc-700 uppercase tracking-wide">Connects to buy</label>
                            <div class="relative rounded-xl shadow-sm">
                                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                   <Wallet class="h-4 w-4 text-zinc-400" />
                                </div>
                                <input
                                    type="number"
                                    id="connects"
                                    v-model.number="connects"
                                    min="1"
                                    step="1"
                                    class="block w-full rounded-xl border-zinc-200 bg-zinc-50 pl-10 focus:border-violet-500 focus:ring-violet-500/20 sm:text-sm py-2.5 transition-all font-semibold text-zinc-900"
                                    @input="calculateAmount"
                                />
                            </div>
                        </div>

                         <div class="space-y-1.5">
                            <label for="amount" class="block text-xs font-bold text-zinc-700 uppercase tracking-wide">Total Amount ({{ paymentOption?.currency }})</label>
                            <div class="relative rounded-xl shadow-sm">
                                <input
                                    type="text"
                                    id="amount"
                                    :value="formattedAmount"
                                    disabled
                                    class="block w-full rounded-xl border-zinc-200 bg-zinc-100 focus:border-zinc-300 focus:ring-0 sm:text-sm py-2.5 font-bold text-zinc-500 cursor-not-allowed text-center"
                                />
                            </div>
                        </div>
                     </div>

                     <!-- File Upload -->
                     <div class="space-y-2">
                         <label class="block text-xs font-bold text-zinc-700 uppercase tracking-wide">Payment Proof</label>
                         
                         <div v-if="!imagePreview" class="group mt-1 flex justify-center px-6 pt-8 pb-8 border-2 border-zinc-200 border-dashed rounded-xl hover:border-violet-300 hover:bg-violet-50/30 transition-all cursor-pointer" @click="$refs.fileInput.click()">
                             <div class="space-y-2 text-center">
                                 <div class="mx-auto h-12 w-12 text-zinc-300 group-hover:text-violet-500 transition-colors bg-zinc-50 group-hover:bg-white rounded-full flex items-center justify-center">
                                     <Image class="h-6 w-6" />
                                 </div>
                                 <div class="text-sm text-zinc-600">
                                     <span class="font-semibold text-violet-600 hover:text-violet-500">Upload screenshot</span>
                                 </div>
                                 <p class="text-xs text-zinc-400">PNG, JPG up to 20MB</p>
                             </div>
                             <input
                                 ref="fileInput"
                                 type="file"
                                 class="hidden"
                                 accept="image/*"
                                 @change="handleFileUpload"
                             />
                         </div>

                         <div v-else class="relative mt-2 rounded-xl overflow-hidden border border-zinc-200 bg-zinc-50 group">
                             <img :src="imagePreview" alt="Payment proof" class="w-full h-48 object-contain bg-white" />
                             <div class="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors flex items-center justify-center">
                                  <button
                                     type="button"
                                     @click="removeImage"
                                     class="p-2 bg-white text-rose-500 rounded-full shadow-lg hover:bg-rose-50 transform scale-0 group-hover:scale-100 transition-all cursor-pointer"
                                 >
                                     <X class="h-5 w-5" />
                                 </button>
                             </div>
                         </div>
                     </div>
                 </div>
              </div>

              <!-- Footer -->
              <div class="px-6 py-4 bg-zinc-50 border-t border-zinc-100 flex flex-col gap-3">
                 <button
                    type="button"
                    class="w-full inline-flex justify-center items-center px-4 py-3 border border-transparent text-sm font-bold rounded-full shadow-sm text-white bg-zinc-900 hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer"
                    :disabled="!isFormValid"
                    @click="handleSubmit"
                 >
                    Submit Payment
                 </button>
                 <button
                    @click="supportStore.open()"
                    class="w-full text-center text-xs font-medium text-zinc-400 hover:text-violet-600 transition-colors cursor-pointer"
                 >
                    Need help? Contact Support
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
import { ref, computed, watch } from 'vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { X, CreditCard, Wallet, Image, Info } from 'lucide-vue-next';
import { message } from 'ant-design-vue';
import { useSupportStore } from '@/stores/support';
const supportStore = useSupportStore();
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
  paymentOption: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['close', 'submit']);

const connects = ref(1);
const amount = ref(0);
const proofFile = ref(null);
const imagePreview = ref(null);
const fileInput = ref(null);
const isSubmitting = ref(false);

const formattedAmount = computed(() => {
  return amount.value.toFixed(2);
});

const isFormValid = computed(() => {
  return connects.value > 0 && proofFile.value !== null;
});

const calculateAmount = () => {
  if (props.paymentOption) {
    amount.value = connects.value * (props.paymentOption.exchange_rate || 1);
  }
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // Check file size (20MB max)
  if (file.size > 20 * 1024 * 1024) {
    message.error('Image size should be less than 20MB');
    return;
  }
  
  // Check file type (images only)
  if (!file.type.match('image.*')) {
    message.success('Please select an image file (JPEG, PNG)');
    return;
  }
  
  // Create preview
  const reader = new FileReader();
  reader.onload = (e) => {
    imagePreview.value = e.target.result;
  };
  reader.readAsDataURL(file);
  
  // Store the file
  proofFile.value = file;
};

const removeImage = () => {
  imagePreview.value = null;
  proofFile.value = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

const handleSubmit = () => {
  if (!isFormValid.value) return;

  const formData = new FormData();
  formData.append('amount_transferred', amount.value);
  formData.append('connects_to_buy', connects.value);
  formData.append('screenshot', proofFile.value);

  emit('submit', formData);
};

// Reset form when modal is opened/closed
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    connects.value = 1;
    amount.value = props.paymentOption?.exchange_rate || 1;
    proofFile.value = null;
    imagePreview.value = null;
    if (fileInput.value) {
      fileInput.value.value = '';
    }
  }
});

// Calculate amount when payment option changes
watch(() => props.paymentOption, () => {
  calculateAmount();
}, { immediate: true });
</script>