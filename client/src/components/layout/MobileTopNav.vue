<template>
  <div>
    <nav class="md:hidden bg-white/90 backdrop-blur-md shadow-sm border-b border-zinc-100 fixed top-0 left-0 right-0 z-50 h-16 transition-all duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full">
      <div class="flex justify-between items-center h-full">
        <div class="flex-shrink-0 flex items-center gap-2 cursor-pointer" @click="$router.push({name: 'Feed'})">
            <div class="w-8 h-8 bg-violet-100 rounded-lg flex items-center justify-center text-violet-600 shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
           </div>
          <h1 class="text-xl font-bold text-zinc-800 tracking-tight">Venting<span class="text-violet-600">App</span></h1>
        </div>
        
        <!-- Search and Actions -->
        <div class="flex items-center space-x-1">
          <!-- Search Icon -->
          <button 
            v-if="!showSearch"
            @click="toggleSearch"
            class="p-2 rounded-full text-zinc-500 hover:text-violet-600 hover:bg-violet-50 cursor-pointer"
          >
            <Search class="h-5 w-5" />
          </button>
          
          <!-- Search Overlay -->
          <div v-if="showSearchorInSearch" class="absolute left-0 right-0 top-0 h-16 bg-white flex items-center px-4 z-50 border-b border-zinc-100 shadow-sm">
            <div class="relative w-full">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search class="h-5 w-5 text-zinc-400" />
              </div>
              <input
                type="text"
                v-model="searchQuery"
                @keyup.enter="handleSearch"
                class="block w-full pl-10 pr-10 py-2 border border-zinc-200 rounded-full leading-5 bg-zinc-50 placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 transition-all sm:text-sm"
                placeholder="Search..."
                ref="searchInput"
              />
              <button
                @click="closeSearch"
                class="absolute cursor-pointer inset-y-0 right-0 pr-3 flex items-center p-2"
              >
                <X class="h-5 w-5 text-zinc-400 hover:text-zinc-600" />
              </button>
            </div>
          </div>

          <button
            @click="openConnectsModal"
            class="flex items-center space-x-1 px-2.5 py-1.5 rounded-full border border-zinc-200 bg-white hover:border-violet-200 cursor-pointer"
          >
            <Wallet class="h-4 w-4 text-amber-500" />
            <span class="text-xs font-bold text-zinc-600">{{ currentConnects }}</span>
          </button>

          <router-link
            :to="{name: 'Chat'}"
            class="p-2 rounded-full text-zinc-500 hover:text-violet-600 hover:bg-violet-50 cursor-pointer"
          >
            <MessageCircleMore class="h-5 w-5" />
          </router-link>

          <!-- Support Button -->
          <button
            @click.stop="supportStore.open()"
            class="p-2 rounded-full text-zinc-500 hover:text-violet-600 hover:bg-violet-50 cursor-pointer"
          >
            <Headset class="h-5 w-5" />
          </button>

          <!-- Mobile menu button -->
          <div class="flex items-center ml-1">
          <button
            @click="isMenuOpen = !isMenuOpen"
            class="inline-flex items-center justify-center p-2 rounded-full text-zinc-700 hover:text-violet-600 hover:bg-violet-50 cursor-pointer transition-colors"
            aria-expanded="false"
          >
            <span class="sr-only">Open main menu</span>
             <Menu class="h-6 w-6 block" :class="{ 'hidden': isMenuOpen, 'block': !isMenuOpen }"/>
             <X class="h-6 w-6" :class="{ 'block': isMenuOpen, 'hidden': !isMenuOpen }"/>
          </button>
        </div>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <div 
      class="md:hidden bg-white shadow-xl rounded-b-2xl border-b border-zinc-100 absolute top-16 left-0 right-0 transform origin-top transition-all duration-300 ease-in-out z-40 overflow-hidden"
      :class="{ 'scale-y-100 opacity-100 max-h-96': isMenuOpen, 'scale-y-0 opacity-0 max-h-0': !isMenuOpen }"
    >
      <div class="px-4 py-3 space-y-2">
        <router-link
          :to="{name: 'Feed'}"
          @click="closeMenu"
          class="block px-4 py-3 rounded-xl text-base font-medium text-zinc-600 hover:text-violet-600 hover:bg-violet-50 transition-colors"
          active-class="bg-violet-50 text-violet-600"
        >
          Home
        </router-link>
        
        <router-link
          to="/profile"
          @click="closeMenu"
          class="block px-4 py-3 rounded-xl text-base font-medium text-zinc-600 hover:text-violet-600 hover:bg-violet-50 transition-colors"
          active-class="bg-violet-50 text-violet-600"
        >
          Your Profile
        </router-link>

        <router-link
          :to="{name: 'History'}"
          @click="closeMenu"
          class="block px-4 py-3 rounded-xl text-base font-medium text-zinc-600 hover:text-violet-600 hover:bg-violet-50 transition-colors"
          active-class="bg-violet-50 text-violet-600"
        >
          History
        </router-link>
        
        <button
          @click="handleLogout"
          class="w-full text-left px-4 py-3 rounded-xl text-base font-medium text-rose-500 hover:bg-rose-50 cursor-pointer transition-colors"
        >
          Sign out
        </button>
      </div>
      
      <div class="px-4 py-4 bg-zinc-50 border-t border-zinc-100">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="h-10 w-10 rounded-full bg-violet-100 flex items-center justify-center shadow-sm">
              <span class="text-violet-600 font-bold">{{ userStore.userInitials }}</span>
            </div>
          </div>
          <div class="ml-3">
            <div class="text-base font-semibold text-zinc-900">{{ userStore?.user?.name || 'User' }}</div>
            <div class="text-sm font-medium text-zinc-500">Signed in</div>
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
  
  
  <!-- Overlay -->
  <div 
    v-if="isMenuOpen" 
    class="fixed inset-0 bg-black/20 backdrop-blur-sm z-30"
    @click="closeMenu"
  ></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { useSupportStore } from '@/stores/support';
import { usePostStore } from '@/stores/post';
import { Wallet, Headset, Menu, X, MessageCircleMore, Search } from 'lucide-vue-next';
import ConnectsModal from '@/components/connects/ConnectsModal.vue';
import { useConnectsStore } from '@/stores/connect';
const router = useRouter();
const route = useRoute();
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
    postStore.search(searchQuery.value.trim(), route, router);
    showSearch.value = false;
  }
};

const isConnectsModalOpen = ref(false);
const currentConnects = computed(() => userStore?.user?.connects || 0);


const closeMenu = () => {
  isMenuOpen.value = false;
};

const handleLogout = async () => {
  userStore.logout(router);
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
