<template>
  <div class="min-h-screen bg-gray-50">
    <DesktopTopNav />    
    <MobileTopNav />
    
    <!-- Main Content -->
    <div class="pt-16 pb-16 md:pt-0 md:pb-0">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex justify-between items-center mb-8">
          <h1 class="text-2xl font-bold text-gray-900">Notifications</h1>
          <button 
            @click="markAllAsRead" 
            :disabled="notificationStore.isLoading || notificationStore.notifications.length === 0"
            class="text-sm text-indigo-600 hover:text-indigo-800 disabled:opacity-50"
          >
            Mark all as read
          </button>
        </div>

        <!-- Loading state -->
        <div v-if="notificationStore.isLoading && notificationStore.notifications.length === 0" class="text-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p class="mt-2 text-gray-500">Loading notifications...</p>
        </div>

        <!-- Empty state -->
        <div v-else-if="!notificationStore.isLoading && notificationStore.notifications.length === 0" class="text-center py-12">
          <div class="mx-auto h-12 w-12 text-gray-400">
            <Bell />
          </div>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No notifications</h3>
          <p class="mt-1 text-sm text-gray-500">You don't have any notifications yet.</p>
        </div>

        <!-- Notifications list -->
        <div v-else class="space-y-4">
          <NotificationItem 
            v-for="notification in notificationStore.notifications" 
            :key="notification.id"
            :notification="notification"
          />
          <!-- Load More Button -->
          <div v-if="notificationStore.hasNextPage" class="flex justify-center py-4">
            <button 
                @click="notificationStore.loadMore" 
                :disabled="notificationStore.loadingMore"
                class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
                {{ notificationStore.loadingMore ? 'Loading...' : 'Load More' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <MobileBottomNav />
    
    <!-- Report Details Modal -->
    <ReportDecisionModal
      v-if="notificationStore.isModalOpen"
      :is-open="notificationStore.isModalOpen"
      :report-decision="notificationStore.selectedReportDecision"
      @close="notificationStore.closeModal"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import ReportDecisionModal from '@/components/notifications/ReportDecisionModal.vue';
import NotificationItem from '@/components/notifications/NotificationItem.vue';
import { useNotificationStore } from '@/stores/notifications';
import { Bell } from 'lucide-vue-next';

const notificationStore = useNotificationStore();
const markAllAsRead = async () => {
};

onMounted(() => {
  notificationStore.fetchNotifications();
});
</script>
