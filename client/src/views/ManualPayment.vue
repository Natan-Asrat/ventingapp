<template>
  <div class="min-h-screen bg-gray-50">
    <DesktopTopNav />    
    <MobileTopNav />
    
    <!-- Main Content -->
    <div class="pt-16 pb-16 md:pt-0 md:pb-0">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="text-center mb-8">
          <h1 class="text-2xl font-bold text-gray-900">Manual Payment Options</h1>
          <p class="mt-2 text-sm text-gray-600">Choose your preferred payment method and follow the instructions</p>
          <button
            @click="supportStore.open()"
            class="mt-4 w-full cursor-pointer text-center text-sm text-gray-500 hover:text-indigo-600 hover:underline focus:outline-none"
          >
            Contact Support
          </button>
        </div>

        <div v-if="manualPaymentStore.loading" class="flex justify-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>

        <div v-else class="space-y-4">
          <div 
            v-for="option in manualPaymentStore.paymentOptions" 
            :key="option.pk"
            class="bg-white overflow-hidden shadow rounded-lg border border-gray-200 hover:shadow-md transition-shadow duration-200 cursor-pointer"
            @click="openPaymentModal(option)"
          >
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-16 w-16 flex items-center justify-center mr-4">
                  <img 
                    v-if="option.logo_url" 
                    :src="option.logo_url" 
                    :alt="option.method" 
                    class="max-h-full max-w-full object-contain"
                  >
                  <div v-else class="h-full w-full flex items-center justify-center bg-gray-100 rounded">
                    <span class="text-gray-400 text-xs">No logo</span>
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <h3 class="text-lg font-medium text-gray-900">{{ option.method }}</h3>
                  <p class="mt-1 text-sm text-gray-500">{{ option.currency }} - {{ option.account }}</p>
                </div>
                <div class="ml-4">
                  <ChevronRight class="h-5 w-5 text-gray-400" />
                </div>
              </div>
            </div>
          </div>

          <div v-if="manualPaymentStore.paymentOptions.length === 0" class="text-center py-12">
            <p class="text-gray-500">No payment options available at the moment.</p>
          </div>
        </div>
      </div>
    </div>
    
    <MobileBottomNav />    
    <PaymentModal 
      :is-open="isModalOpen" 
      :payment-option="selectedOption"
      @close="closeModal"
      @submit="handlePaymentSubmit"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import PaymentModal from '@/components/payment/PaymentModal.vue';
import { message } from 'ant-design-vue';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import { useSupportStore } from '@/stores/support';
import { useManualPaymentStore } from '@/stores/manual_payment';
import { ChevronRight } from 'lucide-vue-next';
const manualPaymentStore = useManualPaymentStore();
const supportStore = useSupportStore();
const isModalOpen = ref(false);
const selectedOption = ref(null);


const openPaymentModal = (option) => {
  selectedOption.value = option;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  selectedOption.value = null;
};

const handlePaymentSubmit = async (formData) => {
  try {
    const response = await manualPaymentStore.submitManualPayment(formData, selectedOption.value.pk)
    
    // Handle successful submission
    closeModal();
    // Show success message
    message.success('Payment submitted successfully! It will be reviewed shortly.');
  } catch (error) {
    console.error('Error submitting payment:', error);
    // Show error message to user
    const errorMessage = error.response?.data?.error || 'Failed to submit payment. Please try again.';
    message.error(errorMessage);
  }
};

onMounted(async () => {
  await manualPaymentStore.fetchPaymentOptions();
});
</script>
