<template>
  <div>
    <nav class="md:hidden bg-white shadow-sm fixed top-0 left-0 right-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <div class="flex-shrink-0 flex items-center">
          <h1 class="text-xl font-bold text-indigo-600">VentingApp</h1>
        </div>
        
        <!-- Search and Actions -->
        <div class="flex items-center space-x-2">
          <!-- Search Icon (only visible when search is not active) -->
          <button 
            v-if="!showSearch"
            @click="toggleSearch"
            class="p-2 rounded-full text-gray-600 hover:text-indigo-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <Search class="h-5 w-5" />
          </button>
          
          <!-- Search Input (full width when active) -->
          <div v-if="showSearchorInSearch" class="absolute left-0 right-0 top-0 h-16 bg-white flex items-center px-4 z-50">
            <div class="relative w-full">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search class="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                v-model="searchQuery"
                @keyup.enter="handleSearch"
                class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Search..."
                ref="searchInput"
              />
              <button
                @click="closeSearch"
                class="absolute cursor-pointer inset-y-0 right-0 pr-3 flex items-center"
              >
                <X class="h-5 w-5 text-gray-400 hover:text-gray-500" />
              </button>
            </div>
          </div>
          <button
            @click="openConnectsModal"
            class="flex items-center space-x-1 px-3 py-1.5 rounded-full border border-gray-200 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-500 cursor-pointer"
          >
            <Wallet class="h-5 w-5 text-amber-600" />
            <span class="text-sm font-medium text-gray-700">{{ currentConnects }}</span>
          </button>

          <router-link
            :to="{name: 'Chat'}"
            class="p-2 rounded-full text-gray-600 hover:text-indigo-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <MessageCircleMore class="h-5 w-5" />
          </router-link>

          <!-- Support Button -->
          <button
            @click.stop="supportStore.open()"
            class="p-2 rounded-full text-gray-600 hover:text-indigo-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <Headset class="h-5 w-5" />
          </button>

          <!-- Mobile menu button -->
          <div class="flex items-center" :class="{ 'ml-2': showSearch }">
          <button
            @click="isMenuOpen = !isMenuOpen"
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-indigo-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
            aria-expanded="false"
          >
            <span class="sr-only">Open main menu</span>
            <!-- Hamburger icon -->
             <Menu class="h-6 w-6 block" :class="{ 'hidden': isMenuOpen, 'block': !isMenuOpen }"/>

            <!-- Close icon -->
             <X class="h-6 w-6" :class="{ 'block': isMenuOpen, 'hidden': !isMenuOpen }"/>
          </button>
        </div>
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
              <span class="text-indigo-600 font-medium">{{ userStore.userInitials }}</span>
            </div>
          </div>
          <div class="ml-3">
            <div class="text-base font-medium text-gray-800">{{ userStore?.user?.name || 'User' }}</div>
            <div class="text-sm font-medium text-gray-500">View profile</div>
          </div>
        </div>
      </div>
    </div>
  </nav>
  
  <!-- Connects Modal -->
  <ConnectsModal
    :is-open="isConnectsModalOpen"
    :current-connects="currentConnects"
    :connects-data="connectsStore.connectsData"
    :loading="connectsStore.isLoading"
    @close="isConnectsModalOpen = false"
    @purchase="connectsStore.handlePurchaseConnects"
  />
  
  
  <!-- Overlay when menu is open -->
  <div 
    v-if="isMenuOpen" 
    class="fixed inset-0 bg-black/50 z-40"
    @click="closeMenu"
  ></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { useSupportStore } from '@/stores/support';
import { usePostStore } from '@/stores/post';
import { Wallet, Headset, Menu, X, MessageCircleMore, Search } from 'lucide-vue-next';
import ConnectsModal from '@/components/connects/ConnectsModal.vue';
import { useConnectsStore } from '@/stores/connect';
const router = useRouter();
const userStore = useUserStore();
const postStore = usePostStore();
const supportStore = useSupportStore();
const connectsStore = useConnectsStore();
const isMenuOpen = ref(false);
const showSearch = ref(false);
const searchQuery = ref('');
const showSearchorInSearch = computed (() => showSearch.value || postStore.isInSearch)

const toggleSearch = () => {
  showSearch.value = !showSearch.value;
  if (!showSearch.value) {
    searchQuery.value = '';
  }
};

const closeSearch = () => {
  searchQuery.value = '';
  showSearch.value = false;
  postStore.closeSearch();
}

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    postStore.search(searchQuery.value.trim());
    showSearch.value = false;
  }
};

const isConnectsModalOpen = ref(false);
const currentConnects = computed(() => userStore?.user?.connects || 0);


const closeMenu = () => {
  isMenuOpen.value = false;
};

const handleLogout = async () => {
  userStore.logout();
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

const openConnectsModal = async () => {
  isConnectsModalOpen.value = true;
  await connectsStore.fetchConnectsData();
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  document.addEventListener('keydown', handleEscape);
  connectsStore.fetchConnectsData();
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
  document.removeEventListener('keydown', handleEscape);
});
</script>
