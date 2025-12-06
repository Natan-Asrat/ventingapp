import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { ClipboardList, Archive } from 'lucide-vue-next';
import api from '@/api/axios';
import { message } from 'ant-design-vue';

export const useMyProfileStore = defineStore('myprofile', () => {

    const ACTIVE_TAB = 'Active'
    const ARCHIVED_TAB = 'Archived'
    const tabs = [
        { name: ACTIVE_TAB, icon: ClipboardList, count: computed(() => posts.value.length) },
        { name: ARCHIVED_TAB, icon: Archive, count: computed(() => archivedPosts.value.length) },
    ];
    const activeTab = ref(ACTIVE_TAB);
    const loading = ref(true);
    const loadingMore = ref(false);
    const posts = ref([]);
    const archivedPosts = ref([])
    const activeNextPage = ref(null);
    const archivedNextPage = ref(null);


    const hasNextPage = computed(() => activeTab.value == ACTIVE_TAB ? !!activeNextPage.value : !!archivedNextPage.value);
    const isArchivingId = ref(null);

    const setLoading = (value) => {
        loading.value = value;
    }

    const updateProfilePicture = async (file) => {
        const formData = new FormData();
        formData.append('profile_picture', file);

        const response = await api.patch('/account/users/edit_profile/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response;
    };

    const updateName = async (name) => {
        const response = await api.patch('/account/users/edit_profile/', {
            name: name.trim(),
        });
        return response;
    }

    const filteredPosts = computed(() => {
        if (activeTab.value === ARCHIVED_TAB) {
            return archivedPosts.value;
        }
        return posts.value;
    });

    const fetchUserPosts = async (url = '/post/posts/my_posts/', page = 1) => {
        try {
            const response = await api.get(url);
            
            if (url.includes('page=')) {
            // Append to existing posts for pagination
                posts.value = [...posts.value, ...response.data.results];
            } else {
            // Initial load
                posts.value = response.data.results;
            }
            
            activeNextPage.value = response.data.next;
        } catch (error) {
            console.error('Error fetching user posts:', error);
            message.error('Failed to load your posts. Please try again.');
        }
    };

    const fetchArchivedUserPosts = async (url = '/post/posts/my_archived_posts/') => {
        try {
            const response = await api.get(url);
            
            if (url.includes('page=')) {
            // Append to existing posts for pagination
                archivedPosts.value = [...archivedPosts.value, ...response.data.results];
            } else {
            // Initial load
                archivedPosts.value = response.data.results;
            }
            
            archivedNextPage.value = response.data.next;
        } catch (error) {
            console.error('Error fetching user posts:', error);
            message.error('Failed to load your posts. Please try again.');
        }
    };

    const loadMorePosts = async () => {
        if (
            activeTab.value == ACTIVE_TAB && !activeNextPage.value
            || activeTab.value == ARCHIVED_TAB && !archivedNextPage.value
            ||
            loadingMore.value
        ) return;
        
        loadingMore.value = true;
        try {
            // Extract the path from the full URL
            if(activeTab.value == ACTIVE_TAB) {
                await fetchUserPosts(activeNextPage.value);
            } else {
                await fetchArchivedUserPosts(archivedNextPage.value);
            }
        } catch (error) {
            console.error('Error loading more posts:', error);
            message.error('Failed to load more posts. Please try again.');
        } finally {
            loadingMore.value = false;
        }
    };

    const handlePostUpdate = (updatedPost) => {
        const index = posts.value.findIndex(p => p.id === updatedPost.id);
        if (index !== -1) {
            posts.value.splice(index, 1, updatedPost);
        }
    };

    const archivePost = async (postId) => {
        try {
            isArchivingId.value = postId;
            const response = await api.post(`/post/posts/${postId}/archive/`);
            archivedPosts.value.unshift(response.data);
            posts.value = posts.value.filter(post => post.id !== postId);
            message.success('Post deleted successfully');
        } catch (error) {
            console.error('Error archiving post:', error);
            message.error(error.response?.data?.detail || 'Failed to delete post');
        } finally {
            isArchivingId.value = null;
        }
    };
    const restorePost = async (postId) => {
        try {
            isArchivingId.value = postId;
            const response = await api.post(`/post/posts/${postId}/unarchive/`);
            archivedPosts.value = archivedPosts.value.filter(post => post.id !== postId);
            posts.value.unshift(response.data);
            message.success('Post restored successfully');
        } catch (error) {
            console.error('Error archiving post:', error);
            message.error(error.response?.data?.detail || 'Failed to delete post');
        } finally {
            isArchivingId.value = null;
        }
    };

    return {
        updateProfilePicture,
        updateName,

        activeTab,
        tabs,
        ACTIVE_TAB,
        ARCHIVED_TAB,

        loading,
        loadingMore,
        hasNextPage,
        setLoading,

        loadMorePosts,
        handlePostUpdate,

        posts,
        archivedPosts,
        filteredPosts,

        archivePost,
        restorePost,
        isArchivingId,

        fetchUserPosts,
        fetchArchivedUserPosts
    }
})