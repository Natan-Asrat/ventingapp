<template>
  <div v-if="show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" @click.self="close">
    <div class="bg-white rounded-lg w-full max-w-md overflow-hidden">
      <div class="p-4 border-b border-gray-200 flex justify-between items-center">
        <h3 class="text-lg font-medium text-gray-900">Donation Methods</h3>
        <button @click="close" class="text-gray-400 hover:text-gray-500 cursor-pointer">
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <div class="divide-y divide-gray-200 max-h-[60vh] overflow-y-auto">
        <div v-for="(method, index) in paymentMethods" :key="index" class="p-4">
          <button 
            @click="toggleAccordion(index)"
            class="w-full flex justify-between items-center text-left cursor-pointer"
          >
            <span class="font-medium">{{ method.method }}</span>
            <svg 
              class="h-5 w-5 text-gray-400 transform transition-transform duration-200"
              :class="{ 'rotate-180': activeIndex === index }"
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          
          <div v-if="activeIndex === index" class="mt-3 space-y-3">
            <div @click="copyToClipboard(method.account)" class="bg-gray-50 p-3 rounded-md flex justify-between items-center cursor-pointer">
              <div>
                <p class="text-xs text-gray-500">Account Number</p>
                <p class="font-mono">{{ method.account }}</p>
              </div>
              <button 
                class="text-indigo-600 hover:text-indigo-800 p-1"
                title="Copy to clipboard"
              >
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                </svg>
              </button>
            </div>
            
            <div @click="copyToClipboard(method.nameOnAccount)" v-if="method.nameOnAccount" class="bg-gray-50 p-3 rounded-md flex justify-between items-center cursor-pointer">
              <div>
                <p class="text-xs text-gray-500">Account Name</p>
                <p>{{ method.nameOnAccount }}</p>
              </div>
              <button 
                
                class="text-indigo-600 hover:text-indigo-800 p-1"
                title="Copy to clipboard"
              >
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="p-4 bg-gray-50 border-t border-gray-200">
        <p class="text-sm text-gray-500 text-center">Thank you for your support!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { message } from 'ant-design-vue';

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  paymentMethods: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:modelValue']);

const show = ref(props.modelValue);
const activeIndex = ref(0);

// Watch for changes to the modelValue prop
watch(() => props.modelValue, (newVal) => {
  show.value = newVal;
  if (newVal) {
    activeIndex.value = 0; // Reset to first payment method when opening
  }
});

// Emit update when show changes
watch(show, (newVal) => {
  emit('update:modelValue', newVal);
});

const toggleAccordion = (index) => {
  activeIndex.value = activeIndex.value === index ? null : index;
};

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    message.success('Copied to clipboard!');
  } catch (err) {
    console.error('Failed to copy:', err);
    message.error('Failed to copy to clipboard');
  }
};

const close = () => {
  show.value = false;
};
</script>

<style scoped>
.rotate-180 {
  transform: rotate(180deg);
}
</style>
