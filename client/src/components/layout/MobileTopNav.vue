<template>
  <div>
    <nav class="md:hidden bg-white shadow-sm fixed top-0 left-0 right-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <div class="flex-shrink-0 flex items-center">
          <h1 class="text-xl font-bold text-indigo-600">VentingApp</h1>
        </div>
        
        <!-- Mobile menu button -->
        <div class="flex items-center">
          <button
            @click="isMenuOpen = !isMenuOpen"
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-indigo-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
            aria-expanded="false"
          >
            <span class="sr-only">Open main menu</span>
            <!-- Hamburger icon -->
            <svg
              class="block h-6 w-6"
              :class="{ 'hidden': isMenuOpen, 'block': !isMenuOpen }"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <!-- Close icon -->
            <svg
              class="h-6 w-6"
              :class="{ 'block': isMenuOpen, 'hidden': !isMenuOpen }"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu, toggle classes based on menu state -->
    <div 
      class="md:hidden bg-white shadow-lg absolute top-16 left-0 right-0 transform origin-top transition-transform duration-200 ease-in-out"
      :class="{ 'scale-y-100 opacity-100': isMenuOpen, 'scale-y-0 opacity-0 h-0': !isMenuOpen }"
    >
      <div class="px-2 pt-2 pb-3 space-y-1">
        <router-link
          :to="{name: 'Feed'}"
          @click="closeMenu"
          class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-indigo-600 hover:bg-gray-50"
          active-class="bg-gray-100 text-indigo-600"
        >
          Home
        </router-link>
        
        <router-link
          to="/profile"
          @click="closeMenu"
          class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-indigo-600 hover:bg-gray-50"
          active-class="bg-gray-100 text-indigo-600"
        >
          Profile
        </router-link>
        
        <button
          @click="handleLogout"
          class="w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-indigo-600 hover:bg-gray-50"
        >
          Sign out
        </button>
      </div>
      
      <div class="pt-4 pb-3 border-t border-gray-200">
        <div class="flex items-center px-5">
          <div class="flex-shrink-0">
            <div class="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center">
              <span class="text-indigo-600 font-medium">{{ userInitials }}</span>
            </div>
          </div>
          <div class="ml-3">
            <div class="text-base font-medium text-gray-800">{{ userName || 'User' }}</div>
            <div class="text-sm font-medium text-gray-500">View profile</div>
          </div>
        </div>
      </div>
    </div>
  </nav>
  
  <!-- Overlay when menu is open -->
  <div 
    v-if="isMenuOpen" 
    class="fixed inset-0 bg-black/50 z-40"
    @click="closeMenu"
  ></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';

const props = defineProps({
  userInitials: {
    type: String,
    default: 'ME'
  },
  userName: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['logout']);
const router = useRouter();
const userStore = useUserStore();
const isMenuOpen = ref(false);

const closeMenu = () => {
  isMenuOpen.value = false;
};

const handleLogout = async () => {
  closeMenu();
  try {
    await userStore.logout();
    router.push('/login');
  } catch (error) {
    console.error('Logout error:', error);
  }
};

// Close menu when route changes
router.afterEach(() => {
  closeMenu();
});

// Close menu when clicking outside or pressing Escape
const handleClickOutside = (event) => {
  const menuButton = document.querySelector('[aria-expanded]');
  const menu = document.querySelector('.mobile-menu');
  
  if (isMenuOpen.value && menuButton && !menuButton.contains(event.target) && 
      menu && !menu.contains(event.target)) {
    closeMenu();
  }
};

const handleEscape = (event) => {
  if (event.key === 'Escape' && isMenuOpen.value) {
    closeMenu();
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  document.addEventListener('keydown', handleEscape);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
  document.removeEventListener('keydown', handleEscape);
});
</script>
