<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Sidebar -->
    <div class="fixed inset-y-0 left-0 w-64 bg-indigo-800 text-white">
      <div class="p-4 border-b border-indigo-700">
        <h1 class="text-xl font-bold">Admin Dashboard</h1>
      </div>
      <nav class="mt-4">
        <RouterLink 
          v-for="item in navItems" 
          :key="item.name"
          :to="item.to"
          class="flex items-center px-4 py-3 text-sm font-medium text-indigo-200 hover:bg-indigo-700 hover:text-white"
          :class="{ 'bg-indigo-900': $route.path === item.to }"
        >
          <component :is="item.icon" class="h-5 w-5 mr-3" />
          {{ item.name }}
        </RouterLink>
      </nav>
    </div>

    <!-- Main content -->
    <div class="pl-64">
      <!-- Top header -->
      <header class="bg-white shadow-sm">
        <div class="flex justify-between items-center px-6 py-4">
          <h2 class="text-lg font-medium text-gray-900">{{ $route.meta.title || 'Dashboard' }}</h2>
          <div class="flex items-center">
            <span class="text-sm text-gray-600 mr-4">
              {{ userStore.user?.email }}
            </span>
            <button 
              @click="handleLogout"
              class="text-sm text-gray-600 hover:text-gray-900"
            >
              Sign out
            </button>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <main class="p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { 
  HomeIcon, 
  UsersIcon, 
  CreditCardIcon, 
  SettingsIcon, 
  LogOutIcon,
  AlertCircleIcon
} from 'lucide-vue-next';

const router = useRouter();
const userStore = useUserStore();

const navItems = [
  { name: 'Dashboard', to: '/admin', icon: HomeIcon },
  { name: 'Pending Payments', to: '/admin/payments', icon: CreditCardIcon },
  { name: 'Users', to: '/admin/users', icon: UsersIcon },
  { name: 'Reports', to: '/admin/reports', icon: AlertCircleIcon },
  { name: 'Settings', to: '/admin/settings', icon: SettingsIcon },
];

const handleLogout = async () => {
  try {
    await userStore.logout();
    router.push('/login');
  } catch (error) {
    console.error('Logout error:', error);
  }
};
</script>