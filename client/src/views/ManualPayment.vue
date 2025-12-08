<template>
  <div class="min-h-screen bg-zinc-50/50 font-sans">
    <DesktopTopNav />    
    <MobileTopNav />
    
    <!-- Main Content -->
    <div class="pt-20 pb-20 md:pt-6 md:pb-0 relative z-0">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="text-center mb-10">
          <div class="inline-flex items-center justify-center p-3 bg-violet-100 rounded-2xl mb-4 text-violet-600 shadow-sm">
             <Wallet class="h-8 w-8" />
          </div>
          <h1 class="text-2xl font-bold text-zinc-900 tracking-tight">Top Up via Transfer</h1>
          <p class="mt-2 text-sm text-zinc-500 max-w-md mx-auto leading-relaxed">Select a payment provider below to view account details and submit your proof of payment.</p>
        </div>

        <div v-if="manualPaymentStore.loading" class="flex flex-col items-center justify-center py-12">
          <div class="animate-spin rounded-full h-10 w-10 border-[3px] border-violet-100 border-t-violet-500 mb-3"></div>
          <span class="text-sm font-medium text-zinc-400 animate-pulse">Loading payment methods...</span>
        </div>

        <div v-else class="space-y-4">
          <div 
            v-for="option in manualPaymentStore.paymentOptions" 
            :key="option.pk"
            class="group bg-white rounded-2xl border border-zinc-200 p-5 hover:border-violet-200 hover:shadow-lg hover:shadow-violet-500/5 transition-all duration-300 cursor-pointer relative overflow-hidden"
            @click="openPaymentModal(option)"
          >
            <!-- Hover effect decoration -->
            <div class="absolute inset-0 bg-gradient-to-r from-violet-50/0 to-violet-50/30 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none"></div>
            
            <div class="relative flex items-center">
              <div class="flex-shrink-0 h-16 w-16 flex items-center justify-center mr-5 bg-zinc-50 rounded-xl border border-zinc-100 p-2 group-hover:bg-white transition-colors">
                <img 
                  v-if="option.logo_url" 
                  :src="option.logo_url" 
                  :alt="option.method" 
                  class="max-h-full max-w-full object-contain"
                >
                <div v-else class="flex flex-col items-center justify-center text-zinc-300">
                  <CreditCard class="h-6 w-6" />
                </div>
              </div>
              <div class="flex-1 min-w-0">
                <h3 class="text-lg font-bold text-zinc-900 group-hover:text-violet-700 transition-colors">{{ option.method }}</h3>
                <p class="text-sm text-zinc-500 font-medium mt-0.5 flex items-center flex-wrap gap-2">
                    <span class="bg-zinc-100 px-1.5 py-0.5 rounded text-xs text-zinc-600 font-mono border border-zinc-200">{{ option.currency }}</span>
                    <span class="truncate">{{ option.account }}</span>
                </p>
              </div>
              <div class="ml-4 flex-shrink-0">
                <div class="h-10 w-10 rounded-full bg-zinc-50 flex items-center justify-center text-zinc-400 group-hover:bg-violet-600 group-hover:text-white transition-all shadow-sm">
                    <ChevronRight class="h-5 w-5 ml-0.5" />
                </div>
              </div>
            </div>
          </div>

          <div v-if="manualPaymentStore.paymentOptions.length === 0" class="text-center py-16 bg-white rounded-2xl border border-zinc-100 border-dashed">
            <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-zinc-50 mb-3">
                <CreditCard class="h-6 w-6 text-zinc-300" />
            </div>
            <p class="text-zinc-500 font-medium">No payment options available.</p>
            <p class="text-zinc-400 text-xs mt-1">Please check back later or contact support.</p>
          </div>
          
          <div class="pt-8 text-center">
             <button
                @click="supportStore.open()"
                class="inline-flex items-center text-sm font-medium text-zinc-500 hover:text-violet-600 transition-colors cursor-pointer group"
            >
                <Headset class="w-4 h-4 mr-2 group-hover:scale-110 transition-transform" />
                Having trouble? Contact Support
            </button>
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
import { ChevronRight, CreditCard, Wallet, Headset } from 'lucide-vue-next';

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