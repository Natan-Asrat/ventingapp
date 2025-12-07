import { defineStore } from "pinia";
import { ref, computed } from 'vue';
import { api } from '@/main';
import { message } from 'ant-design-vue';

export const useNotificationStore = defineStore('notification', () => {
    const notifications = ref([]);
    const isLoading = ref(true);
    const isModalOpen = ref(false);
    const selectedReportDecision = ref(null);
    const isSubmittingAppeal = ref(false);
    const isLoadingAppeals = ref(false);
    const existingAppeals = ref([]);
    const showAppealForm = ref(false);

    const setShowAppealForm = (value) => {
        showAppealForm.value = value;
    };


    const appealMessage = ref('');

    const loadingMore = ref(false);
    const nextPage = ref(null);
    const hasNextPage = computed(() => !!nextPage.value);

    const setAppealMessage = (message) => {
        appealMessage.value = message;
    };
    const fetchNotifications = async (page = 1) => {
        try {
            const response = await api.get('/notification/notifications/', { params: { page } });
            if (page > 1) {
                notifications.value = [...notifications.value, ...response.data.results];
            } else {
                notifications.value = response.data.results;
            }
            nextPage.value = response.data.next;
        } catch (error) {
            console.error('Error fetching notifications:', error);
            message.error('Failed to load notifications');
        } finally {
            isLoading.value = false;
            loadingMore.value = false;
        }
    };
    const openReportModal = (reportDecision) => {
        selectedReportDecision.value = reportDecision;
        isModalOpen.value = true;
        
        if (!reportDecision.viewed) {
            // markAsRead(reportDecision.id);
        }
    };

    const closeModal = () => {
        isModalOpen.value = false;
        selectedReportDecision.value = null;
    };

    const loadMore = () => {
        if (nextPage.value && !loadingMore.value) {
            loadingMore.value = true;
            
            const next = new URL(nextPage.value, window.location.origin);
            const page = next.searchParams.get("page");
            fetchNotifications(page);
        }
    };

    const fetchMyAppeals = async (report_decision_id) => {
        if (!report_decision_id) return;
        
        isLoadingAppeals.value = true;
        try {
            const response = await api.get(`/report/report-decisions/${report_decision_id}/my_appeals/`);
            existingAppeals.value = response.data;
        } catch (error) {
            console.error('Error fetching appeals:', error);
            message.error('Failed to load appeal information');
        } finally {
            isLoadingAppeals.value = false;
        }
    };

    const submitAppeal = async (report_decision_id) => {
        if (!appealMessage.value.trim()) {
            message.warning('Please enter a message for your appeal');
            return;
        }

        try {
            isSubmittingAppeal.value = true;
            await api.post(`/report/report-decisions/${report_decision_id}/submit_appeal/`, {
                message: appealMessage.value
            });
            
            message.success('Appeal submitted successfully');
            showAppealForm.value = false;
            // Refresh the appeals list
            await fetchMyAppeals();
            appealMessage.value = '';
        } catch (error) {
            console.error('Error submitting appeal:', error);
            message.error('Failed to submit appeal. Please try again.');
        } finally {
            isSubmittingAppeal.value = false;
        }
    };
    return {
        isLoading,
        notifications,
        isModalOpen,
        selectedReportDecision,
        hasNextPage,
        loadingMore,
        appealMessage,
        isLoadingAppeals,
        existingAppeals,
        showAppealForm,
        setShowAppealForm,
        fetchNotifications,
        openReportModal,
        closeModal,
        loadMore,
        submitAppeal,
        setAppealMessage,
        fetchMyAppeals
    }
});