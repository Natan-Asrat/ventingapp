<script setup>
import { RouterView } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { onMounted } from 'vue';

const userStore = useUserStore();

// Check authentication status when app loads
onMounted(async () => {
  await userStore.checkAuth();
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
  </div>
</template>

