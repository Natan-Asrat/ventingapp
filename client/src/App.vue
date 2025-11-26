<script setup>
import { RouterView, useRoute } from 'vue-router';
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import api from '@/api/axios';
import CelebrationModal from '@/components/transaction/CelebrationModal.vue';
import { useUserStore } from '@/stores/user';
const route = useRoute();
const showCelebration = ref(false);
const recentTransaction = ref(null);
const userStore = useUserStore();

const checkForSuccess = async () => {
  console.log("checking for success")
    try {
      const response = await api.get('/transaction/transactions/recent_success/');
      console.log("recent success", response.data)
      if (response.data && response.data.connects) {
        recentTransaction.value = response.data;
        showCelebration.value = true;
        userStore.checkAuth();
      }
    } catch (error) {
      console.error('Error fetching recent transaction:', error);
    }
};

// Check when route changes
watch(() => route.query, () => {
  setTimeout(() => {
    checkForSuccess();
  }, 1000);
}, { immediate: true });
watch(
  () => route.query,
  () => {
   console.log("checkingg")
  }
);
const handleVisibilityChange = () => {
  if (!document.hidden) {
    // User has returned to the tab
    console.log('User returned to the page!');
    checkForSuccess();
    // Example: force full reload (bypass SPA cache)
    // window.location.reload();

    // Or call any function to refresh your data
    // refreshData();
  }
};

onMounted(() => {
  document.addEventListener('visibilitychange', handleVisibilityChange);
});

onBeforeUnmount(() => {
  document.removeEventListener('visibilitychange', handleVisibilityChange);
});
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Global notification container -->
    <div id="notification-container"></div>
    
    <!-- Main content -->
    <main class="min-h-screen">
      <RouterView v-slot="{ Component }">
        <transition 
          enter-active-class="transition-opacity duration-200 ease-out"
          leave-active-class="transition-opacity duration-150 ease-in"
          enter-from-class="opacity-0"
          leave-to-class="opacity-0"
        >
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>

    <!-- Celebration Modal -->
    <CelebrationModal 
      :is-open="showCelebration" 
      :transaction="recentTransaction"
      @close="showCelebration = false"
    />
  </div>
</template>

