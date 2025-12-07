import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '@/api/axios';
import { message } from 'ant-design-vue';

export const useMessageStore = defineStore('message', () => {
    const isSubmittingReport = ref(false);
    const selectedMessageId = ref(null);
    const isReportModalOpen = ref(false); 

    const showReportMenu = ref(false);
    const toggleReportMenu = () => {
        showReportMenu.value = !showReportMenu.value;
    }
    const setShowReportMenu = (value) => {
        showReportMenu.value = value;
    }
    const setSelectedMessageId = (id) => {
        selectedMessageId.value = id;
    }

    const setIsReportModalOpen = (value) => {
        isReportModalOpen.value = value;
    }

    const submitReport = async (reason) => {
        isSubmittingReport.value = true;
        
        try {
            const response = await api.post('report/reports/report_message/', {
                message_id: selectedMessageId.value,
                reason: reason
            });
            
            if (response.data.error) {
                message.error(response.data.error);
            } else {
                message.success('Message reported successfully');
            }
        } catch (error) {
            console.error('Error reporting message:', error);
            const errorMessage = error.response?.data?.error || 'Failed to report message';
            message.error(errorMessage);
        } finally {
            isSubmittingReport.value = false;
            isReportModalOpen.value = false;
        }
    };

    const fetchConversationById = async (id) => {
        const response = await api.get(`chat/conversations/${id}/`);
        return response;
    }

    const fetchMessagesByURL = async (url) => {
        const response = await api.get(url);
        return response;
    }

    const sendMessage = async (text, conversation_id, reply_to) => {
        await api.post(`chat/conversations/${conversation_id}/send_message/`, {
            message: text,
            reply_to: reply_to || null
        });
    }
    const forwardMessage = async (message_id) => {
        api.post(`chat/messages/${message_id}/forward/`);
    }

    const reactToMessage = async (message_id, reaction) => {
        const response = await api.post(`chat/messages/${message_id}/react/`, {
            emoji: reaction
        });
        return response
    }

    const getBulkMessages = async (message_ids) => {
        const response = await api.get(`chat/messages/get_bulk/?id=${message_ids}`);
        return response;
    }

    const getMessagesAfterId = async (conversation_id, message_id) => {
        const response = await api.get(
            `chat/conversations/${conversation_id}/new_messages/?after_id=${message_id}`
        );
        return response;
    }


    return {
        submitReport,
        isSubmittingReport,
        selectedMessageId,
        showReportMenu,
        isReportModalOpen,
        toggleReportMenu,

        setSelectedMessageId,
        setShowReportMenu,
        setIsReportModalOpen,
        fetchConversationById,
        fetchMessagesByURL,
        sendMessage,
        forwardMessage,
        getBulkMessages,
        reactToMessage,
        getMessagesAfterId
    }
})