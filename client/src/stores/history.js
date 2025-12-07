import { defineStore } from "pinia";
import { ref, watch } from 'vue';
import api from '@/api/axios';

export const useHistoryStore = defineStore('history', () => {
    const loading = ref({
        transactions: false,
        moreTransactions: false,
        connections: false,
        moreConnections: false,
        usage: false,
        moreUsages: false
    });
    const setLoadingTransactions = (value) => {
        loading.value.transactions = value;
    }

    const setLoadingConnections = (value) => {
        loading.value.connections = value;
    }

    const setLoadingUsage = (value) => {
        loading.value.usage = value;
    }

    
    const reportModalOpen = ref(false);
    const selectedConnection = ref(null);

    const CONNECTIONS_TAB = 'connections';
    const USAGE_TAB = 'usage';
    const TRANSACTIONS_TAB = 'transactions';
    const tabs = ref([
        { id: TRANSACTIONS_TAB, name: 'Transactions', count: 0 },
        { id: CONNECTIONS_TAB, name: 'Connections', count: 0 },
        { id: USAGE_TAB, name: 'Usage', count: 0 },
    ]);
    const activeTab = ref('transactions');
    const usages = ref([]);
    const usagesNextUrl = ref(null);

    const transactions = ref([]);
    const transactionsNextUrl = ref(null);

    const connections = ref([]);
    const connectionsNextUrl = ref(null);


    const reportUser = (connection) => {
        console.log("report conn", connection)
        selectedConnection.value = connection;
        console.log("report conn", selectedConnection.value)
        reportModalOpen.value = true;
    };

    const setReportModalOpen = (value) => {
        reportModalOpen.value = value;
    }

    const setConnectionByAction = (conn, action) => {
        const index = connections.value.findIndex(c => c.id === conn.id);
        if (index !== -1) {
            if (action === 'accept') {
                
                connections.value[index].reconnection_requested_by = null;
                connections.value[index].reconnection_rejected = false;
            } else {
                connections.value[index].reconnection_rejected = true;
            }
        }
    }

    const submitReport = async (conn_id, reason) => {
        await api.post('/report/reports/report_connection/', {
            connection_id: conn_id,
            reason: reason
        });
    }

    // Fetch transactions
    const fetchTransactions = async (url = '/transaction/transactions/my_transactions/') => {
        try {
            const response = await api.get(url);
            if (url.includes('page=')) {
            // Append new transactions if loading more
                transactions.value = [...transactions.value, ...response.data.results];
            } else {
                transactions.value = response.data.results;
            }
            transactionsNextUrl.value = response.data.next;
            tabs.value[0].count = response.data.count;
        } catch (error) {
            console.error('Error fetching transactions:', error);
        } finally {
            loading.value.transactions = false;
            loading.value.moreTransactions = false;
        }
    };

    const fetchUsages = async (url = '/usage/connect-usages/') => {
        try {
            const response = await api.get(url);
            if (url.includes('page=')) {
                // Append new usages if loading more
                usages.value = [...usages.value, ...response.data.results];
            } else {
                usages.value = response.data.results;
            }
            usagesNextUrl.value = response.data.next;
            tabs.value[2].count = response.data.count;
        } catch (error) {
            console.error('Error fetching usages:', error);
        } finally {
            loading.value.usage = false;
            loading.value.moreUsages = false;
        }
    };


    const fetchMyConnections = async (url = '/account/users/connections/') => {
        try {
            const response = await api.get(url);
            if (url.includes('page=')) {
                // Append new connections if loading more
                connections.value = [...connections.value, ...response.data.results];
            } else {
                connections.value = response.data.results;
            }
            connectionsNextUrl.value = response.data.next;
            tabs.value[1].count = response.data.count;
        } catch (error) {
            console.error('Error fetching connections:', error);
        } finally {
            loading.value.connections = false;
            loading.value.moreConnections = false;
        }
    };

    // Load more connections
    const loadMoreConnections = () => {
        if (!connectionsNextUrl.value) return;
        loading.value.moreConnections = true;
        
        // Use the full URL directly since it's already correct from the API
        fetchMyConnections(connectionsNextUrl.value);
    };


    const loadMoreUsages = () => {
        if (!usagesNextUrl.value) return;
        loading.value.moreUsages = true;
        fetchUsages(usagesNextUrl.value);
    };

    const loadMoreTransactions = () => {
        if (!transactionsNextUrl.value) return;
        loading.value.moreTransactions = true;
        
        // Use the full URL directly since it's already correct from the API
        fetchTransactions(transactionsNextUrl.value);
    };

    watch(activeTab, (newTab) => {
        if (newTab === 'transactions' && transactions.value.length === 0) {
            fetchTransactions();
        } else if (newTab === 'connections' && connections.value.length === 0) {
            fetchMyConnections();
        } else if (newTab === 'usage' && usages.value.length === 0) {
            fetchUsages();
        }
    });

    return {
        tabs,
        activeTab,

        fetchTransactions,
        fetchMyConnections,
        fetchUsages,
        
        loading,
        loadMoreUsages,
        loadMoreTransactions,
        loadMoreConnections,

        usages,
        usagesNextUrl,

        transactions,
        transactionsNextUrl,

        connections,
        connectionsNextUrl,

        setConnectionByAction,
        submitReport,

        USAGE_TAB,
        CONNECTIONS_TAB,
        TRANSACTIONS_TAB,

        setLoadingTransactions,
        setLoadingConnections,
        setLoadingUsage,


        reportModalOpen,
        selectedConnection,

        reportUser,
        setReportModalOpen
    }
})