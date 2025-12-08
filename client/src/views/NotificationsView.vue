<template>
  <div class="min-h-screen bg-zinc-50/50 font-sans">
    <DesktopTopNav />    
    <MobileTopNav />
    
    <!-- Main Content -->
    <div class="pt-20 pb-20 md:pt-6 md:pb-0 relative z-0">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex justify-between items-center mb-6">
          <div>
            <h1 class="text-2xl font-bold text-zinc-900 tracking-tight">Notifications</h1>
            <p class="text-sm text-zinc-500 mt-1">Updates about your activity and reports</p>
          </div>
          <button 
            @click="markAllAsRead" 
            :disabled="notificationStore.isLoading || notificationStore.notifications.length === 0"
            class="text-sm font-medium text-violet-600 hover:text-violet-800 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-violet-50 px-3 py-1.5 rounded-full transition-colors cursor-pointer"
          >
            Mark all as read
          </button>
        </div>

        <!-- Loading state -->
        <div v-if="notificationStore.isLoading && notificationStore.notifications.length === 0" class="flex flex-col items-center justify-center py-20">
          <div class="animate-spin rounded-full h-10 w-10 border-[3px] border-violet-100 border-t-violet-500 mb-4"></div>
          <p class="text-sm font-medium text-zinc-400 animate-pulse tracking-wide">Loading updates...</p>
        </div>

        <!-- Empty state -->
        <div v-else-if="!notificationStore.isLoading && notificationStore.notifications.length === 0" class="flex flex-col items-center justify-center py-24 px-6 text-center bg-white rounded-2xl border border-zinc-100 shadow-sm">
          <div class="w-16 h-16 bg-zinc-50 rounded-full flex items-center justify-center mb-4 ring-8 ring-zinc-50/50">
            <Bell class="h-8 w-8 text-zinc-300" />
          </div>
          <h3 class="text-lg font-bold text-zinc-900">All caught up!</h3>
          <p class="mt-1 text-sm text-zinc-500">You don't have any new notifications.</p>
        </div>

        <!-- Notifications list -->
        <div v-else class="space-y-3">
          <NotificationItem 
            v-for="notification in notificationStore.notifications" 
            :key="notification.id"
            :notification="notification"
          />
          <!-- Load More Button -->
          <div v-if="notificationStore.hasNextPage" class="flex justify-center py-8">
            <button 
                @click="notificationStore.loadMore" 
                :disabled="notificationStore.loadingMore"
                class="px-6 py-2.5 bg-white border border-zinc-200 text-zinc-700 font-semibold text-sm rounded-full hover:bg-zinc-50 hover:border-zinc-300 hover:shadow-sm disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer flex items-center"
            >
                <span v-if="notificationStore.loadingMore" class="animate-spin h-4 w-4 border-2 border-zinc-400 border-t-zinc-600 mr-2 rounded-full"></span>
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