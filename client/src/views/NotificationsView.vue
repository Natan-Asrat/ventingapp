<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Desktop Navigation -->
    <desktop-top-nav 
      :user-initials="userInitials"
      @logout="handleLogout"
    />
    
    <!-- Mobile Top Navigation -->
    <mobile-top-nav 
      :user-initials="userInitials"
      :user-name="userName"
      @logout="handleLogout"
    />
    
    <!-- Main Content -->
    <div class="pt-16 pb-16 md:pt-0 md:pb-0">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex justify-between items-center mb-8">
          <h1 class="text-2xl font-bold text-gray-900">Notifications</h1>
          <button 
            @click="markAllAsRead" 
            :disabled="isLoading || notifications.length === 0"
            class="text-sm text-indigo-600 hover:text-indigo-800 disabled:opacity-50"
          >
            Mark all as read
          </button>
        </div>

        <!-- Loading state -->
        <div v-if="isLoading && notifications.length === 0" class="text-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p class="mt-2 text-gray-500">Loading notifications...</p>
        </div>

        <!-- Empty state -->
        <div v-else-if="!isLoading && notifications.length === 0" class="text-center py-12">
          <div class="mx-auto h-12 w-12 text-gray-400">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </div>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No notifications</h3>
          <p class="mt-1 text-sm text-gray-500">You don't have any notifications yet.</p>
        </div>

        <!-- Notifications list -->
        <div v-else class="space-y-4">
          <div 
            v-for="notification in notifications" 
            :key="notification.id"
            class="bg-white rounded-lg shadow overflow-hidden border-l-4"
            :class="{
              'border-indigo-500': !notification.viewed,
              'border-transparent': notification.viewed,
              'opacity-75': notification.viewed
            }"
          >
            <div class="p-4">
              <div class="flex items-start">
                <div class="flex-shrink-0 pt-0.5">
                  <div class="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center">
                    <svg v-if="!notification.viewed" class="h-5 w-5 text-indigo-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="h-5 w-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                    </svg>
                  </div>
                </div>
                <div class="ml-3 flex-1">
                  <div class="flex items-center justify-between">
                    <p class="text-sm font-medium text-gray-900">
                      {{ notification.title }}
                    </p>
                    <p class="text-xs text-gray-500">
                      {{ notification.created_since }}
                    </p>
                  </div>
                  <p class="mt-1 text-sm text-gray-600">
                    {{ notification.message }}
                  </p>
                  
                  <!-- Report decision actions -->
                  <div v-if="notification.report_decision" class="mt-3 flex space-x-3">
                    <button
                      @click="openReportModal(notification.report_decision)"
                      class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer"
                    >
                      View Report
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Mobile Bottom Navigation -->
    <mobile-bottom-nav :user-initials="userInitials" />
    
    <!-- Report Details Modal -->
    <ReportDecisionModal
      v-if="isModalOpen"
      :is-open="isModalOpen"
      :report-decision="selectedReportDecision"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import { api } from '@/main';
import { message } from 'ant-design-vue';
import ReportDecisionModal from '@/components/notifications/ReportDecisionModal.vue';

const router = useRouter();
const userStore = useUserStore();

const notifications = ref([]);
const isLoading = ref(true);
const isModalOpen = ref(false);
const selectedReportDecision = ref(null);

const userInitials = computed(() => {
  if (!userStore.user) return '';
  const name = userStore.user.name || userStore.user.email;
  return name
    .split(' ')
    .map(part => part[0])
    .join('')
    .toUpperCase()
    .substring(0, 2);
});

const userName = computed(() => {
  return userStore.user?.name || userStore.user?.email || '';
});

const handleLogout = async () => {
  await userStore.logout();
  router.push('/login');
};

const fetchNotifications = async () => {
  try {
    const response = await api.get('/notification/notifications/');
    notifications.value = response.data;
  } catch (error) {
    console.error('Error fetching notifications:', error);
    message.error('Failed to load notifications');
  } finally {
    isLoading.value = false;
  }
};

const markAsRead = async (notificationId) => {
  // try {
  //   await api.patch(`/notification/notifications/${notificationId}/`, { viewed: true });
  //   const index = notifications.value.findIndex(n => n.id === notificationId);
  //   if (index !== -1) {
  //     notifications.value[index].viewed = true;
  //   }
  // } catch (error) {
  //   console.error('Error marking notification as read:', error);
  // }
};

const markAllAsRead = async () => {
  try {
    await api.post('/notification/notifications/mark_all_as_read/');
    notifications.value = notifications.value.map(n => ({ ...n, viewed: true }));
    message.success('All notifications marked as read');
  } catch (error) {
    console.error('Error marking all notifications as read:', error);
    message.error('Failed to mark all as read');
  }
};

const openReportModal = (reportDecision) => {
  selectedReportDecision.value = reportDecision;
  isModalOpen.value = true;
  
  // Mark as read when opening the report
  if (!reportDecision.viewed) {
    markAsRead(reportDecision.id);
  }
};

const closeModal = () => {
  isModalOpen.value = false;
  selectedReportDecision.value = null;
};

onMounted(() => {
  fetchNotifications();
});
</script>
