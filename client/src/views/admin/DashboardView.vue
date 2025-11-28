<template>
  <div class="space-y-6">
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-medium text-gray-900 mb-4">Admin Dashboard</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-indigo-50 p-4 rounded-lg">
          <h3 class="text-sm font-medium text-indigo-800">Total Users</h3>
          <p class="text-2xl font-bold text-gray-900">{{ stats.totalUsers || 'Loading...' }}</p>
        </div>
        <div class="bg-green-50 p-4 rounded-lg">
          <h3 class="text-sm font-medium text-green-800">Active Today</h3>
          <p class="text-2xl font-bold text-gray-900">{{ stats.activeToday || 'Loading...' }}</p>
        </div>
        <div class="bg-purple-50 p-4 rounded-lg">
          <h3 class="text-sm font-medium text-purple-800">Total Revenue</h3>
          <p class="text-2xl font-bold text-gray-900">${{ stats.totalRevenue || '0.00' }}</p>
        </div>
      </div>
    </div>

    <div class="bg-white shadow rounded-lg p-6">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-medium text-gray-900">Recent Activity</h3>
        <button class="text-sm text-indigo-600 hover:text-indigo-800">View All</button>
      </div>
      <div class="space-y-4">
        <div v-for="(activity, index) in recentActivities" :key="index" class="border-b border-gray-100 pb-4 last:border-0 last:pb-0">
          <p class="text-sm text-gray-600">{{ activity.message }}</p>
          <p class="text-xs text-gray-400 mt-1">{{ activity.time }}</p>
        </div>
        <div v-if="recentActivities.length === 0" class="text-center py-4 text-gray-500">
          No recent activity
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const stats = ref({
  totalUsers: 0,
  activeToday: 0,
  totalRevenue: 0
});

const recentActivities = ref([
  // This would come from an API in a real app
  { message: 'New user registered: johndoe@example.com', time: '2 minutes ago' },
  { message: 'Payment received from Jane Smith', time: '1 hour ago' },
  { message: 'System update completed', time: '3 hours ago' },
]);

// In a real app, you would fetch this data from your API
onMounted(() => {
  // Simulate API call
  setTimeout(() => {
    stats.value = {
      totalUsers: 1242,
      activeToday: 342,
      totalRevenue: 12450.75
    };
  }, 1000);
});
</script>
