<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Sidebar -->
    <div class="fixed inset-y-0 left-0 w-64 bg-indigo-800 text-white">
      <div class="p-4 border-b border-indigo-700">
        <h1 class="text-xl font-bold">Admin Dashboard</h1>
      </div>
      <nav class="mt-4">
        <div v-for="item in navItems" :key="item.name">
          <RouterLink 
            v-if="!item.children"
            :to="item.to"
            class="flex items-center px-4 py-3 text-sm font-medium text-indigo-200 hover:bg-indigo-700 hover:text-white"
            :class="{ 'bg-indigo-900': $route.path === item.to }"
          >
            <component :is="item.icon" class="h-5 w-5 mr-3" />
            {{ item.name }}
          </RouterLink>
          
          <!-- Dropdown for Reports -->
          <div v-else class="relative">
            <button 
              @click="toggleDropdown(item.name)"
              class="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-indigo-200 hover:bg-indigo-700 hover:text-white"
              :class="{ 'bg-indigo-900': isDropdownOpen(item.name) }"
            >
              <div class="flex items-center">
                <component :is="item.icon" class="h-5 w-5 mr-3" />
                {{ item.name }}
              </div>
              <ChevronDownIcon 
                class="h-4 w-4 transition-transform duration-200"
                :class="{ 'transform rotate-180': isDropdownOpen(item.name) }" 
              />
            </button>
            
            <transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div 
                v-if="isDropdownOpen(item.name)"
                class="ml-8 mt-1 space-y-1"
              >
                <RouterLink
                  v-for="child in item.children"
                  :key="child.name"
                  :to="child.to"
                  class="block px-4 py-2 text-sm text-indigo-200 hover:bg-indigo-700 hover:text-white rounded"
                  :class="{ 'bg-indigo-900': $route.path === child.to }"
                >
                  {{ child.name }}
                </RouterLink>
              </div>
            </transition>
          </div>
        </div>
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
import { ref, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { 
  HomeIcon, 
  UsersIcon, 
  CreditCardIcon, 
  SettingsIcon, 
  LogOutIcon,
  AlertCircleIcon,
  ChevronDownIcon
} from 'lucide-vue-next';

const router = useRouter();
const userStore = useUserStore();

const route = useRoute();
const openDropdowns = ref([]);

const navItems = [
  { name: 'Dashboard', to: '/admin', icon: HomeIcon },
  { name: 'Pending Payments', to: '/admin/payments', icon: CreditCardIcon },
  { name: 'Users', to: '/admin/users', icon: UsersIcon },
  { 
    name: 'Reports', 
    to: '/admin/reports', 
    icon: AlertCircleIcon,
    children: [
      { name: 'All Reports', to: '/admin/reports' },
      { name: 'Message Reports', to: '/admin/reports/message' },
      { name: 'Post Reports', to: '/admin/reports/post' },
      { name: 'Transaction Reports', to: '/admin/reports/transaction' },
      { name: 'Connection Reports', to: '/admin/reports/connection' },
      { name: 'Conversation Reports', to: '/admin/reports/conversation' }
    ]
  },
  { name: 'Settings', to: '/admin/settings', icon: SettingsIcon },
];

const toggleDropdown = (name) => {
  const index = openDropdowns.value.indexOf(name);
  if (index === -1) {
    openDropdowns.value.push(name);
  } else {
    openDropdowns.value.splice(index, 1);
  }
};

const isDropdownOpen = (name) => {
  return openDropdowns.value.includes(name);
};
watch(
  () => route.path,
  (newPath) => {
    navItems.forEach(item => {
      if (item.children) {
        const shouldOpen = item.children.some(child => 
          newPath.startsWith(child.to)
        );

        if (shouldOpen) {
          if (!openDropdowns.value.includes(item.name)) {
            openDropdowns.value.push(item.name);
          }
        } else {
          const index = openDropdowns.value.indexOf(item.name);
          if (index !== -1) {
            openDropdowns.value.splice(index, 1);
          }
        }
      }
    });
  },
  { immediate: true }
);

const handleLogout = async () => {
  try {
    await userStore.logout();
    router.push('/login');
  } catch (error) {
    console.error('Logout error:', error);
  }
};
</script>