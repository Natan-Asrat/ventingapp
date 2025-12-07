import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '@/api/axios';

export const useChatStore = defineStore('chat', () => {
    const categories = ref([]);
    const pagination = ref({
        page: 1,
        hasMore: true,
        loadingMore: false
    });

    const loading = ref(true);
    const conversations = ref([]);

    const setPagination = (value) => {
        pagination.value = value;
    }
    const visibleConversations = ref([]);

    const resetVisibleConversations = () => {
        visibleConversations.value = []
    }

    const addToVisibleConversations = (id) => {
        visibleConversations.value.push(id);
    }

    const removeVisibleConversation = (index) => {
        visibleConversations.value.splice(index, 1);
    }

    let visibleConversationsInterval = null;
    let latestConversationsInterval = null;

    const tabs = ref([
        { id: 'primary', name: 'Primary', unread: 0 },
        { id: 'secondary', name: 'Secondary', unread: 0 },
        { id: 'requests', name: 'Requests', unread: 0 },
        { id: 'archived', name: 'Archived', unread: 0 }
    ]);
    const activeTab = ref('primary');
    const activeTabName = computed(() => {
        const tab = tabs.value.find(t => t.id === activeTab.value);
        return tab ? tab.name : '';
    });
    const setActiveTab = (tabId) => {
        activeTab.value = tabId;
    }

    const fetchCategories = async () => {
        try {
            const response = await api.get('chat/conversations/categories/');
            categories.value = response.data;
            // Initialize tabs with categories
            tabs.value = response.data.map(category => ({
                id: category,
                name: category.charAt(0).toUpperCase() + category.slice(1),
                unread: 0
            }));
        } catch (error) {
            console.error('Error fetching categories:', error);
        }
    };

    const fetchConversations = async (loadMore = false) => {
        if (!activeTab.value) return;
        
        if (loadMore) {
            pagination.value.loadingMore = true;
            pagination.value.page += 1;
        } else {
            loading.value = true;
            pagination.value.page = 1;
            pagination.value.hasMore = true;
        }

        try {
            const response = await api.get(`chat/conversations/?category=${activeTab.value}&page=${pagination.value.page}`);
            const newConversations = response.data.results || [];
            
            if (loadMore) {
                // Merge new conversations with existing ones, avoiding duplicates
                const existingIds = new Set(conversations.value.map(c => c.id));
                const uniqueNewConversations = newConversations.filter(conv => !existingIds.has(conv.id));
                conversations.value = [...conversations.value, ...uniqueNewConversations];
                
                // Check if there are more pages
                pagination.value.hasMore = response.data.next !== null;
            } else {
                conversations.value = newConversations;
                pagination.value.hasMore = response.data.next !== null;
            }
            
            // Re-sort conversations by updated_at
            conversations.value.sort((a, b) => {
            return new Date(b.updated_at) - new Date(a.updated_at);
            });
        } catch (error) {
            console.error('Error fetching conversations:', error);
            if (loadMore) {
                // Revert page increment on error
                pagination.value.page = Math.max(1, pagination.value.page - 1);
            }
        } finally {
            loading.value = false;
            pagination.value.loadingMore = false;
        }
    };

    const updateUnreadCounts = async (conversations) => {
        let counts = {};
        categories.value.forEach(cat => counts[cat] = 0);
        
        const response = await api.get("/chat/conversations/unread_counts/")
        counts = response.data
        
        tabs.value = tabs.value.map(tab => ({
            ...tab,
            unread: counts[tab.id] || 0
        }));
    };

    const sharePost = async (conversation_id, post_id) => {
        const response = await api.post(`/chat/conversations/${conversation_id}/share_post/`, { post_id: post_id });
        return response;
    };

    const fetchVisibleConversations = async () => {
        if (!visibleConversations.value.length) return;

        try {
            const ids = visibleConversations.value.join(',');
            const response = await api.get(`chat/conversations/get_bulk/?id=${ids}`);
            const fetchedConversations = response.data; // array of conversation objects

            // Update conversations in place
            fetchedConversations.forEach((conv) => {
            updateOrAddConversation(conv);
            });
        } catch (error) {
            console.error("Error fetching visible conversations:", error);
        }
    };

    const fetchLatestConversations = async () => {
        if (conversations.value.length === 0) return;
        
        try {
            const latestId = conversations.value[0].id; // Get the most recent conversation ID
            const response = await api.get(`chat/conversations/latest_conversations/?after_id=${latestId}&category=${activeTab.value}`);
            const newConversations = response.data;
            
            if (newConversations.length > 0) {
                // Update or add new conversations
                newConversations.forEach(conv => {
                    updateOrAddConversation(conv);
                });
                
                // Sort conversations by updated_at in descending order
                conversations.value.sort((a, b) => {
                    return new Date(b.updated_at) - new Date(a.updated_at);
                });
            }
        } catch (error) {
            console.error('Error fetching latest conversations:', error);
        }
    };

    const updateOrAddConversation = (newConv) => {
        const index = conversations.value.findIndex(c => c.id === newConv.id);
        if (index !== -1) {
            conversations.value[index] = { ...conversations.value[index], ...newConv };
        } else {
            conversations.value.unshift(newConv);
            conversations.value.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
        }
    };

    const moveConversation = async (conversation, category) => {
        try {
            await api.post(`chat/conversations/${conversation.id}/move_conversation/`, {
                category: category
            });
            
            // Update the local state
            conversations.value = conversations.value.filter(c => c.id !== conversation.id);
            await updateUnreadCounts();
        } catch (error) {
            console.error('Error moving conversation:', error);
        }
    };

    const archiveConversation = async (conversation) => {
        try {
            await api.post(`chat/conversations/${conversation.id}/archive_conversation_for_me/`);
            conversations.value = conversations.value.filter(c => c.id !== conversation.id);
            await updateUnreadCounts();
        } catch (error) {
            console.error('Error archiving conversation:', error);
        }
    };


    const startVisibleConversationsPolling = () => {
        if (visibleConversationsInterval) clearInterval(visibleConversationsInterval);
        if (latestConversationsInterval) clearInterval(latestConversationsInterval);
        
        visibleConversationsInterval = setInterval(fetchVisibleConversations, 5000);
        latestConversationsInterval = setInterval(fetchLatestConversations, 3000);
    };

    const stopVisibleConversationsPolling = () => {
        if (visibleConversationsInterval) clearInterval(visibleConversationsInterval);
        if (latestConversationsInterval) clearInterval(latestConversationsInterval);
    };


    const loadMoreConversations = async () => {
        if (!pagination.value.hasMore || pagination.value.loadingMore) return;
        await fetchConversations(true);
    };


    return {
        activeTab,
        tabs,
        pagination,
        categories,
        visibleConversations,
        activeTabName,

        loading,
        conversations,

        fetchCategories,
        fetchConversations,
        updateUnreadCounts,
        loadMoreConversations,
        archiveConversation,
        moveConversation,
        fetchVisibleConversations,

        startVisibleConversationsPolling,
        stopVisibleConversationsPolling,

        addToVisibleConversations,
        removeVisibleConversation,

        sharePost,
        setPagination,
        setActiveTab,
        resetVisibleConversations
    }
});