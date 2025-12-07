import { defineStore } from "pinia";
import api from '@/api/axios';
import { ref } from 'vue';

export const useManualPaymentStore = defineStore('manualpayment', () => {
    const paymentOptions = ref([]);
    const loading = ref(true);

    const fetchPaymentOptions = async () => {
        try {
            const response = await api.get('transaction/transactions/manual_payment_options/');
            paymentOptions.value = response.data;
        } catch (error) {
            console.error('Error fetching payment options:', error);
        } finally {
            loading.value = false;
        }
    };
    const submitManualPayment = async (formData, manual_payment_option_id) => {
        const response = await api.post(`transaction/manual_payments/${manual_payment_option_id}/submit_payment/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response;
    }
    
    return {
        paymentOptions,
        loading,
        fetchPaymentOptions,
        submitManualPayment
    }
})