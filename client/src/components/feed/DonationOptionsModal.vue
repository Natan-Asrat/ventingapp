<template>
  <div v-if="show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" @click.self="close">
    <div class="bg-white rounded-lg w-full max-w-2xl overflow-hidden">
      <!-- Header -->
      <div class="p-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900 text-center">Donation Options</h3>
      </div>
      
      <!-- Payment Methods List -->
      <div class="divide-y divide-gray-200 max-h-[60vh] overflow-y-auto">
        <div v-for="(method, index) in paymentMethods" :key="index" class="p-4">
          <div class="flex items-start justify-between">
            <div class="flex-1 min-w-0">
              <div v-if="method.method" class="flex items-center">
                <h4 class="text-base font-medium text-gray-900">{{ method.method }}</h4>
                <button 
                  @click="toggleEditMode(index)"
                  class="ml-2 p-1 text-gray-400 hover:text-indigo-600 rounded-full hover:bg-gray-100"
                  :title="editingIndex === index ? 'Cancel' : 'Edit'"
                >
                  <Pencil v-if="editingIndex !== index" class="h-4 w-4" />
                  <X v-else class="h-4 w-4" />
                </button>
              </div>
              
              <!-- View Mode -->
              <div v-if="editingIndex !== index" class="mt-2 space-y-2">
                <div class="flex items-center">
                  <span class="text-sm text-gray-500 w-24">Account:</span>
                  <span class="text-sm text-gray-900 font-mono">{{ method.account }}</span>
                </div>
                <div v-if="method.nameOnAccount" class="flex items-center">
                  <span class="text-sm text-gray-500 w-24">Name:</span>
                  <span class="text-sm text-gray-900">{{ method.nameOnAccount }}</span>
                </div>
              </div>
              
              <!-- Edit Mode -->
              <div v-else class="mt-3 space-y-3">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Platform/Bank Name</label>
                  <input
                    v-model="editingMethod.method"
                    type="text"
                    class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                    placeholder="e.g., PayPal, Chase, Binance"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Account Details</label>
                  <input
                    v-model="editingMethod.account"
                    type="text"
                    class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                    placeholder="Email, account number, or wallet address"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Name on Account</label>
                  <input
                    v-model="editingMethod.nameOnAccount"
                    type="text"
                    class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                    placeholder="Name as it appears on your account"
                  />
                </div>
                <div class="flex justify-end space-x-2 pt-2">
                  <button
                    type="button"
                    @click="cancelEdit"
                    class="px-3 py-1.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    @click="savePaymentMethod(index)"
                    :disabled="!isValidMethod"
                    class="px-3 py-1.5 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Save
                  </button>
                </div>
              </div>
            </div>
            <button
              v-if="editingIndex !== index"
              @click="removePaymentMethod(index)"
              class="ml-4 p-1 text-gray-400 hover:text-red-600 rounded-full hover:bg-gray-100"
              title="Remove payment method"
            >
              <Trash2 class="h-4 w-4" />
            </button>
          </div>
        </div>
        
        <!-- Add New Payment Method -->
        <div class="p-4 border-t border-gray-200">
          <button
            @click="addNewPaymentMethod"
            class="w-full flex items-center justify-center px-4 py-2 border border-dashed border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <Plus class="h-4 w-4 mr-2" />
            Add Payment Method
          </button>
        </div>
      </div>
      
      <!-- Footer -->
      <div class="p-4 bg-gray-50 border-t border-gray-200 flex justify-end">
        <button
          @click="close"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Done
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { Pencil, X, Plus, Trash2 } from 'lucide-vue-next';
import { message } from 'ant-design-vue';
import api from '@/api/axios';

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  paymentInfoList: {
    type: Array,
    default: () => []
  },
  postId: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['close', 'update:payment-info-list']);

// Local state
const paymentMethods = ref([...props.paymentInfoList]);
const editingIndex = ref(-1);
const editingMethod = ref({
  method: '',
  account: '',
  nameOnAccount: ''
});

// Computed
const isValidMethod = computed(() => {
  return (
    editingMethod.value.method.trim() !== '' &&
    editingMethod.value.account.trim() !== '' &&
    editingMethod.value.nameOnAccount.trim() !== ''
  );
});

// Watch for changes in props
watch(() => props.paymentInfoList, (newVal) => {
  paymentMethods.value = [...newVal];
}, { deep: true });

// Methods
const toggleEditMode = (index) => {
  console.log("toggle index", index);
  if (editingIndex.value === index) {
    editingIndex.value = -1;
  } else {
    editingIndex.value = index;
    editingMethod.value = { ...paymentMethods.value[index] };
  }
};

const addNewPaymentMethod = () => {
  console.log("add new payment method");
  console.trace();
  // If already in edit mode, cancel it
  if (editingIndex.value !== -1) {
    editingIndex.value = -1;
  }
  
  // Reset the form
  editingMethod.value = {
    method: '',
    account: '',
    nameOnAccount: ''
  };
  
  // Add a new empty method and start editing it
  paymentMethods.value.push({ ...editingMethod.value });
  editingIndex.value = paymentMethods.value.length - 1;
};

const savePaymentMethod = async (index) => {
  try {
    const methodData = { ...editingMethod.value };
    let response;
    
    if (methodData.pk) {
      // Update existing payment method
      response = await api.put(
        `/post/payment_info/${methodData.pk}/`,
        {
          method: methodData.method,
          account: methodData.account,
          nameOnAccount: methodData.nameOnAccount
        }
      );
    } else {
      // Create new payment method
      response = await api.post(
        `/post/posts/${props.postId}/add_payment_info/`,
        {
          method: methodData.method,
          account: methodData.account,
          nameOnAccount: methodData.nameOnAccount
        }
      );
    }
    
    // Update local state with server response
    paymentMethods.value[index] = response.data;
    emit('update:payment-info-list', [...paymentMethods.value]);
    editingIndex.value = -1;
    message.success(`Payment method ${methodData.pk ? 'updated' : 'added'} successfully`);
  } catch (error) {
    console.error('Error saving payment method:', error);
    message.error(error.response?.data?.detail || 'Failed to save payment method');
  }
};

const removePaymentMethod = async (index) => {
  try {
    const methodToDelete = paymentMethods.value[index];
    
    // If the payment method has a pk, delete it from the server
    if (methodToDelete.pk) {
      await api.delete(`/post/payment_info/${methodToDelete.pk}/`);
    }
    
    // Remove from local state
    paymentMethods.value.splice(index, 1);
    emit('update:payment-info-list', [...paymentMethods.value]);
    
    // If we were editing the removed method, reset editing state
    if (editingIndex.value === index) {
      editingIndex.value = -1;
    } else if (editingIndex.value > index) {
      // Adjust the editing index if needed
      editingIndex.value--;
    }
    
    // Emit the updated list to the parent
    emit('update:payment-info-list', [...paymentMethods.value]);
    
    message.success('Payment method removed');
  } catch (error) {
    console.error('Error removing payment method:', error);
    message.error('Failed to remove payment method');
  }
};

const cancelEdit = () => {
  // If this was a new payment method that wasn't saved, remove it
  if (editingIndex.value === paymentMethods.value.length - 1 && 
      !paymentMethods.value[editingIndex.value].method &&
      !paymentMethods.value[editingIndex.value].account) {
    paymentMethods.value.pop();
  }
  editingIndex.value = -1;
};

const close = () => {
  // Reset any pending edits
  if (editingIndex.value !== -1) {
    cancelEdit();
  }
  emit('close');
};
</script>
