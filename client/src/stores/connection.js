import { defineStore } from 'pinia';


import { ref } from 'vue';
import { api } from '../main';
export const useConnectionStore = defineStore('connection', () => {
    const processingAction = ref(false);

    const handleAcceptConnection = async (connection) => {
        try {
            processingAction.value = true;
            await api.post(`/account/users/${connection.reconnection_requested_by}/accept_reconnection/`);
            return true;
        } catch (error) {
            console.error('Error accepting connection:', error);
            return false;
        } finally {
            processingAction.value = false;
        }
    };

    const handleRejectConnection = async (connection) => {
        try {
            processingAction.value = true;
            await api.post(`/account/users/${connection.reconnection_requested_by}/reject_reconnection/`);
            return true;
        } catch (error) {
            console.error('Error rejecting connection:', error);
            return false;
        } finally {
            processingAction.value = false;
        }
    };
    const getOtherUser = (connection, currentUser) => {
        if (!currentUser) return null;
        return connection.initiating_user.id === currentUser.id 
            ? connection.connected_user 
            : connection.initiating_user;
    };

    const fetchOurConnections = async (user_id) => {
        if (!user_id) return;
        const response = await api.get(`/account/users/${user_id}/our_connection/`);
        return response;
    };
    return {
        handleAcceptConnection,
        handleRejectConnection,
        processingAction,
        getOtherUser,
        fetchOurConnections
    }
});