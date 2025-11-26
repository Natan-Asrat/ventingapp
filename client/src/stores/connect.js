// stores/connects.js
import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/api/axios';

export const useConnectsStore = defineStore('connects', () => {
  const connectsData = ref({});
  const isLoading = ref(false);

  const fetchConnectsData = async () => {
    try {
      isLoading.value = true;
      const response = await api.get('/transaction/transactions/connect_options/');
      connectsData.value = response.data;
    } catch (error) {
      console.error('Error fetching connects data:', error);
    } finally {
      isLoading.value = false;
    }
  };

  const handlePurchaseConnects = async (packageKey) => {
    try {
      const packageData = connectsData.value[packageKey];
      if (!packageData) return;
      isLoading.value = true;

      const response = await api.post('/transaction/transactions/create_order/', {
        product: packageKey,
        current_url: `${window.location.origin}/success`,
      });

      // Open checkout in new tab
      window.open(response.data.checkout_url, '_blank', 'noopener,noreferrer');

    } catch (error) {
      console.error('Error purchasing connects:', error);
    } finally {
      isLoading.value = false;
    }
  };

  return {
    connectsData,
    isLoading,
    fetchConnectsData,
    handlePurchaseConnects,
  };
});
