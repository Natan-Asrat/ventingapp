<template>
  <div class="space-y-6">
    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-medium text-gray-900">Admin Dashboard</h2>
        <div class="flex items-center space-x-2">
          <span class="inline-flex h-2 w-2 rounded-full" :class="isConnected ? 'bg-green-500' : 'bg-red-500'"></span>
          <span class="text-xs text-gray-500">Auto-updating</span>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-indigo-50 p-4 rounded-lg">
          <h3 class="text-sm font-medium text-indigo-800">Total Users</h3>
          <p class="text-2xl font-bold text-gray-900">
            <template v-if="!isLoading">{{ stats.user_count || 0 }}</template>
            <span v-else class="inline-block h-8 w-12 bg-gray-200 rounded animate-pulse"></span>
          </p>
        </div>
        <div class="bg-green-50 p-4 rounded-lg">
          <h3 class="text-sm font-medium text-green-800">Active Today</h3>
          <p class="text-2xl font-bold text-gray-900">
            <template v-if="!isLoading">{{ stats.daily_active_users || 0 }}</template>
            <span v-else class="inline-block h-8 w-12 bg-gray-200 rounded animate-pulse"></span>
          </p>
        </div>
        <div class="bg-purple-50 p-4 rounded-lg">
          <h3 class="text-sm font-medium text-purple-800">Total Revenue (USD)</h3>
          <p class="text-2xl font-bold text-gray-900">
            <template v-if="!isLoading">${{ Number(stats.total_revenue || 0).toFixed(2) }}</template>
            <span v-else class="inline-block h-8 w-24 bg-gray-200 rounded animate-pulse"></span>
          </p>
        </div>
      </div>
    </div>

    <div class="bg-white shadow rounded-lg p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Recent Activities</h3>
      <div class="text-center py-8 text-gray-500">
        <p>Coming soon</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import api from '@/api/axios';

const isLoading = ref(true);
const isConnected = ref(true);
const pollInterval = ref(null);
const lastUpdated = ref(null);

const stats = ref({
  user_count: 0,
  daily_active_users: 0,
  total_revenue: 0
});

const fetchDashboardStats = async () => {
  try {
    const response = await api.get('/analytics/analytics/admin_dashboard/');
    stats.value = response.data;
    isConnected.value = true;
    lastUpdated.value = new Date();
  } catch (error) {
    console.error('Error fetching dashboard stats:', error);
    isConnected.value = false;
  } finally {
    if (isLoading.value) {
      isLoading.value = false;
    }
  }
};

const startPolling = () => {
  // Initial fetch
  fetchDashboardStats();
  
  // Set up polling every 2 seconds
  pollInterval.value = setInterval(fetchDashboardStats, 2000);
};

onMounted(() => {
  startPolling();
});

onUnmounted(() => {
  // Clear the interval when the component is unmounted
  if (pollInterval.value) {
    clearInterval(pollInterval.value);
  }
});
</script>