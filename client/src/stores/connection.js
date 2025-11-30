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
    return {
        handleAcceptConnection,
        handleRejectConnection,
        processingAction,
        getOtherUser
    }
});