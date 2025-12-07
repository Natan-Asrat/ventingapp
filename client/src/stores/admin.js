import { defineStore } from "pinia";
import api from "@/api/axios";

export const useAdminStore = defineStore('admin', () => {
    const getAppeals = async (decision_id) => {
        const response = await api.get(`/report/report-decisions/${decision_id}/appeals/`);
        return response;
    }

    const approveAppeal = async (appeal_id, reason) => {
        await api.post(`/report/appeals/${appeal_id}/approve/`, {
            reason: reason
        });
    }

    const rejectAppeal = async (appeal_id, reason) => {
        await api.post(`/report/appeals/${appeal_id}/reject/`, {
            reason: reason.trim()
        });
    }

    const approveTransaction = async (pk, transaction_id_on_screenshot) => {
        const response = await api.post(`/transaction/transactions/${pk}/approve_transaction/`, {
            transaction_id: transaction_id_on_screenshot,
        });
        return response;
    }

    const rejectTransaction = async (pk, reason) => {
        const response = await api.post(`/transaction/transactions/${pk}/reject_transaction/`, {
            reason: reason.trim(),
        });
        return response;
    }

    const getDashboardStats = async () => {
        const response = await api.get('/analytics/analytics/admin_dashboard/');
        return response;
    }

    const getPendingTransactions = async (page) => {
        const response = await api.get('/transaction/transactions/pending_transactions/', { params: { page } });
        return response;
    }

    const dismissReport = async (report_id) => {
        await api.post(`/report/reports/${report_id}/dismiss/`);
    }

    const restoreReport = async (report_id) => {
        await api.post(`/report/reports/${report_id}/restore/`);
    }

    const approveReport = async (report_id, reason) => {
        await api.post(`/report/reports/${report_id}/approve/`, { reason });
    }

    const rejectReport = async (report_id, reason) => {
        await api.post(`/report/reports/${report_id}/reject/`, { reason });
    }
    
    const getReports = async (params) => {
        const response = await api.get('/report/reports/', { params })
        return response;
    }

    const getUsers = async (params) => {
        const response = await api.get('/account/users/', { params });
        return response;
    }

    const applyUserAction = async (user_id, action) => [
        await api.post(`/account/users/${user_id}/${action}/`)
    ]

    return {
        getAppeals,
        approveAppeal,
        rejectAppeal,
        approveTransaction,
        rejectTransaction,
        getDashboardStats,
        getPendingTransactions,
        dismissReport,
        restoreReport,
        approveReport,
        rejectReport,
        getReports,
        getUsers,
        applyUserAction
    }
})