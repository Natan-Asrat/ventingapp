<template>
  <TransitionRoot as="template" :show="isOpen">
    <Dialog as="div" class="fixed z-50 inset-0 overflow-y-auto" @close="$emit('close')">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <TransitionChild
          as="template"
          enter="ease-out duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="ease-in duration-200"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <DialogOverlay class="fixed inset-0 bg-gray-500/75 transition-opacity z-40" />
        </TransitionChild>

        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

        <TransitionChild
          as="template"
          enter="ease-out duration-300"
          enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          enter-to="opacity-100 translate-y-0 sm:scale-100"
          leave="ease-in duration-200"
          leave-from="opacity-100 translate-y-0 sm:scale-100"
          leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
        >
          <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6 relative z-50">
            <div class="absolute top-0 right-0 pt-4 pr-4">
              <button
                type="button"
                class="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none"
                @click="$emit('close')"
              >
                <span class="sr-only">Close</span>
                <X class="h-6 w-6 cursor-pointer" aria-hidden="true" />
              </button>
            </div>

            <div>
              <div class="text-center">
                <div class="flex justify-center mb-4">
                  <img 
                    v-if="paymentOption?.logo_url" 
                    :src="paymentOption?.logo_url" 
                    :alt="paymentOption?.method" 
                    class="h-16 object-contain"
                  >
                </div>
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  {{ paymentOption?.method }}
                </h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    Account: {{ paymentOption?.account }}
                  </p>
                  <p class="text-sm text-gray-500">
                    Account Name: {{ paymentOption?.nameOnAccount }}
                  </p>
                </div>

                <div class="mt-6 space-y-4">
                  <div class="border-t border-gray-200 pt-4">
                    <div class="text-sm text-gray-700 mb-4">
                      Please make the payment to the account above and upload the proof of payment below.
                    </div>

                    <div class="space-y-4">
                      <div>
                        <label for="connects" class="block text-sm font-medium text-gray-700">
                          How many connects do you want to buy?
                        </label>
                        <div class="mt-1">
                          <input
                            type="number"
                            id="connects"
                            v-model.number="connects"
                            min="1"
                            step="1"
                            class="block px-4 py-2 w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                            @input="calculateAmount"
                          />
                        </div>
                      </div>

                      <div>
                        <label for="amount" class="block text-sm font-medium text-gray-700">
                          Amount to Pay ({{ paymentOption?.currency }}):
                        </label>
                        <div class="mt-1">
                          <input
                            type="text"
                            id="amount"
                            :value="formattedAmount"
                            disabled
                            class="block px-4 py-2 w-full rounded-md border-gray-300 bg-gray-100 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                          />
                        </div>
                      </div>

                      <div>
                        <label class="block text-sm font-medium text-gray-700">
                          Payment Screenshot
                        </label>
                        <div v-if="!imagePreview" class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                          <label class="w-full cursor-pointer">
                            <input
                              id="file-upload"
                              ref="fileInput"
                              name="file-upload"
                              type="file"
                              class="sr-only"
                              accept="image/*"
                              @change="handleFileUpload"
                            />
                            <div class="space-y-1 text-center">
                              <div class="flex text-sm text-gray-600 justify-center">
                                <span class="relative bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500">
                                  Upload a screenshot
                                </span>
                                <p class="pl-1">or drag and drop</p>
                              </div>
                              <p class="text-xs text-gray-500">
                                PNG, JPG up to 20MB
                              </p>
                            </div>
                          </label>
                        </div>
                        <div v-else class="mt-1">
                          <div class="relative">
                            <img :src="imagePreview" alt="Payment proof" class="max-h-64 w-auto mx-auto rounded-md" />
                            <button
                              type="button"
                              @click="removeImage"
                              class="absolute top-2 right-2 p-1 bg-white rounded-full shadow-md text-gray-500 hover:text-red-500 focus:outline-none"
                            >
                              <X class="h-5 w-5" />
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="mt-5 sm:mt-6">
                    <button
                      type="button"
                      class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                      :disabled="!isFormValid"
                      @click="handleSubmit"
                    >
                      Submit Payment
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { Dialog, DialogOverlay, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { X } from 'lucide-vue-next';
import { message } from 'ant-design-vue';

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
