<template>
  <div v-if="show" class="fixed inset-0 bg-zinc-900/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 transition-opacity" @click.self="close">
    <div class="bg-white rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl transform transition-all border border-zinc-100">
      <!-- Header -->
      <div class="px-6 py-5 border-b border-zinc-100 bg-zinc-50/50 flex justify-between items-center">
        <h3 class="text-lg font-bold text-zinc-900">Donation Options</h3>
         <button @click="close" class="p-1 rounded-full text-zinc-400 hover:text-zinc-600 hover:bg-zinc-100 transition-all cursor-pointer">
            <X class="h-5 w-5" />
        </button>
      </div>
      
      <!-- Payment Methods List -->
      <div class="divide-y divide-zinc-100 max-h-[60vh] overflow-y-auto bg-white">
        <div v-for="(method, index) in paymentMethods" :key="index" class="p-5 hover:bg-zinc-50/30 transition-colors">
          <div class="flex items-start justify-between">
            <div class="flex-1 min-w-0">
              <div v-if="method.method" class="flex items-center">
                <h4 class="text-base font-bold text-zinc-900">{{ method.method }}</h4>
                <button 
                  v-if="!archived"
                  @click="toggleEditMode(index)"
                  class="ml-2 p-1.5 text-zinc-400 hover:text-violet-600 rounded-full hover:bg-violet-50 transition-colors cursor-pointer"
                  :title="editingIndex === index ? 'Cancel' : 'Edit'"
                >
                  <Pencil v-if="editingIndex !== index" class="h-3.5 w-3.5" />
                  <X v-else class="h-3.5 w-3.5" />
                </button>
              </div>
              
              <!-- View Mode -->
              <div v-if="editingIndex !== index" class="mt-2 space-y-1.5">
                <div class="flex items-start">
                  <span class="text-xs font-semibold text-zinc-400 uppercase tracking-wide w-20 pt-0.5">Account</span>
                  <span class="text-sm text-zinc-700 font-mono bg-zinc-50 px-2 py-0.5 rounded border border-zinc-100">{{ method.account }}</span>
                </div>
                <div v-if="method.nameOnAccount" class="flex items-start">
                  <span class="text-xs font-semibold text-zinc-400 uppercase tracking-wide w-20 pt-0.5">Name</span>
                  <span class="text-sm text-zinc-700 font-medium">{{ method.nameOnAccount }}</span>
                </div>
              </div>
              
              <!-- Edit Mode -->
              <div v-else class="mt-4 space-y-4 bg-zinc-50 p-4 rounded-xl border border-zinc-100">
                <div>
                  <label class="block text-xs font-bold text-zinc-700 mb-1.5 uppercase tracking-wide">Platform/Bank Name</label>
                  <input
                    v-model="editingMethod.method"
                    type="text"
                    class="block w-full rounded-lg border-zinc-200 bg-white shadow-sm focus:border-violet-500 focus:ring-violet-500 sm:text-sm p-2.5"
                    placeholder="e.g., PayPal, Chase, Binance"
                  />
                </div>
                <div>
                  <label class="block text-xs font-bold text-zinc-700 mb-1.5 uppercase tracking-wide">Account Details</label>
                  <input
                    v-model="editingMethod.account"
                    type="text"
                    class="block w-full rounded-lg border-zinc-200 bg-white shadow-sm focus:border-violet-500 focus:ring-violet-500 sm:text-sm p-2.5"
                    placeholder="Email, account number, or wallet address"
                  />
                </div>
                <div>
                  <label class="block text-xs font-bold text-zinc-700 mb-1.5 uppercase tracking-wide">Name on Account</label>
                  <input
                    v-model="editingMethod.nameOnAccount"
                    type="text"
                    class="block w-full rounded-lg border-zinc-200 bg-white shadow-sm focus:border-violet-500 focus:ring-violet-500 sm:text-sm p-2.5"
                    placeholder="Name as it appears on your account"
                  />
                </div>
                <div class="flex justify-end space-x-3 pt-2">
                  <button
                    type="button"
                    @click="cancelEdit"
                    class="px-4 py-2 text-sm font-medium text-zinc-700 bg-white border border-zinc-300 rounded-full shadow-sm hover:bg-zinc-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-zinc-500 cursor-pointer"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    @click="savePaymentMethod(index)"
                    :disabled="!isValidMethod"
                    class="px-4 py-2 text-sm font-medium text-white bg-zinc-900 border border-transparent rounded-full shadow-sm hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                  >
                    Save Changes
                  </button>
                </div>
              </div>
            </div>
            <button
              v-if="editingIndex !== index && !archived"
              @click="removePaymentMethod(index)"
              class="ml-4 p-2 text-zinc-400 hover:text-rose-600 rounded-full hover:bg-rose-50 transition-colors cursor-pointer self-start"
              title="Remove payment method"
            >
              <Trash2 class="h-4 w-4" />
            </button>
          </div>
        </div>
        
        <!-- Add New Payment Method -->
        <div v-if="!archived" class="p-5 border-t border-zinc-100 bg-zinc-50/30">
          <button
            @click="addNewPaymentMethod"
            class="w-full flex items-center justify-center px-4 py-3 border border-dashed border-zinc-300 rounded-xl text-sm font-medium text-zinc-600 bg-white hover:bg-zinc-50 hover:border-violet-300 hover:text-violet-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 cursor-pointer transition-all"
          >
            <Plus class="h-5 w-5 mr-2" />
            Add Payment Method
          </button>
        </div>
        <div v-else-if="paymentMethods.length === 0" class="p-8 text-center bg-zinc-50/30">
           <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-zinc-100 mb-3">
             <Wallet class="h-6 w-6 text-zinc-300" />
           </div>
          <p class="text-sm font-medium text-zinc-500">No payment methods added.</p>
        </div>
      </div>
      
      <!-- Footer -->
      <div class="p-4 bg-zinc-50 border-t border-zinc-100 flex justify-end">
        <button
          @click="close"
          class="px-5 py-2 text-sm font-medium text-white bg-zinc-900 border border-transparent rounded-full shadow-sm hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 cursor-pointer transition-colors"
        >
          {{archived ? "Close" : "Done"}}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { Pencil, X, Plus, Trash2, Wallet } from 'lucide-vue-next';
import { message } from 'ant-design-vue';
import { usePostStore } from '@/stores/post';
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
  },
  archived: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close', 'update:payment-info-list']);
const postStore = usePostStore();
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
      const data = {
        method: methodData.method,
        account: methodData.account,
        nameOnAccount: methodData.nameOnAccount
      }
      response = await postStore.updatePaymentMethod(methodData.pk, data);
    } else {
      const data = {
        method: methodData.method,
        account: methodData.account,
        nameOnAccount: methodData.nameOnAccount
      }
      response = await postStore.addPaymentMethod(props.postId, data);
      // Create new payment method
      
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
      await postStore.removePaymentMethod(methodToDelete.pk)
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
