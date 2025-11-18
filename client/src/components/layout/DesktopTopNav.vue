<template>
  <nav class="hidden md:block bg-white shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex-shrink-0 flex items-center">
          <h1 class="text-xl font-bold text-indigo-600">VentingApp</h1>
        </div>
        
        <div class="flex items-center space-x-6">
          <router-link
            :to="{name: 'Feed'}"
            class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-indigo-600 transition-colors"
            active-class="text-indigo-600 border-b-2 border-indigo-600"
          >
            Home
          </router-link>
          
          <router-link
            :to="{name: 'NewPost'}"
            class="flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            New Post
          </router-link>
          
          <div class="relative ml-3">
            <div class="flex items-center space-x-4">
              <button
                @click="toggleProfileMenu"
                class="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer"
                id="user-menu"
                aria-expanded="false"
                aria-haspopup="true"
              >
                <div v-if="profilePicture" class="h-8 w-8 rounded-full overflow-hidden bg-indigo-100">
                  <img :src="profilePicture" alt="Profile" class="h-full w-full object-cover" />
                </div>
                <div v-else class="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center">
                  <span class="text-indigo-600 font-medium">{{ userInitials }}</span>
                </div>
              </button>
            </div>
            
            <transition
              enter-active-class="transition ease-out duration-200"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div 
                v-if="isProfileMenuOpen" 
                class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50"
                role="menu"
                aria-orientation="vertical"
                aria-labelledby="user-menu"
              >
                <router-link
                  to="/profile"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  role="menuitem"
                >
                  Your Profile
                </router-link>
                <button
                  @click="handleLogout"
                  class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                  role="menuitem"
                >
                  Sign out
                </button>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();

const userInitials = computed(() => {
  if (!userStore.user) return 'ME';
  const { first_name, last_name, email } = userStore.user;
  if (first_name && last_name) {
    return `${first_name[0]}${last_name[0]}`.toUpperCase();
  }
  if (first_name) return first_name[0].toUpperCase();
  if (email) return email[0].toUpperCase();
  return 'ME';
});

const profilePicture = computed(() => {
  return userStore.user?.profile_picture;
});

const emit = defineEmits(['logout']);
const router = useRouter();
const isProfileMenuOpen = ref(false);

const toggleProfileMenu = () => {
  isProfileMenuOpen.value = !isProfileMenuOpen.value;
};

const handleLogout = async () => {
  try {
    await userStore.logout();
    router.push('/login');
  } catch (error) {
    console.error('Logout error:', error);
  }
};

// Handle click outside to close the dropdown
const handleClickOutside = (event) => {
  const dropdownElement = document.querySelector('.profile-dropdown');
  if (isProfileMenuOpen.value && dropdownElement && !dropdownElement.contains(event.target)) {
    isProfileMenuOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>
