import { defineStore } from 'pinia';
import api from '@/api/axios';

export const useTransactionStore = defineStore('transaction', () => {
    const celebrate = () => {
        api.post('/transaction/transactions/celebrated/')
    }

    const getRecentSuccess = async () => {
        const response = await api.get('/transaction/transactions/recent_success/');
        return response;
    }

    return {
        celebrate,
        getRecentSuccess
    }
})