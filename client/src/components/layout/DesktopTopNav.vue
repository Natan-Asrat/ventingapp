<template>
  <nav class="hidden md:block bg-white/90 backdrop-blur-md border-b border-zinc-100 sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex-shrink-0 flex items-center gap-2 cursor-pointer" @click="$router.push({name: 'Feed'})">
           <div class="w-8 h-8 bg-violet-100 rounded-lg flex items-center justify-center text-violet-600 shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
           </div>
           <h1 class="text-xl font-bold text-zinc-800 tracking-tight">Venting<span class="text-violet-600">App</span></h1>
        </div>
        
        <div class="flex items-center space-x-2 lg:space-x-4">
          <!-- Search Bar -->
          <div class="flex-1 w-64 lg:w-80 px-2">
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search class="h-4 w-4 text-zinc-400 group-focus-within:text-violet-500 transition-colors" />
              </div>
              <input
                type="text"
                v-model="searchQuery"
                @keyup.enter="handleSearch"
                class="block w-full pl-9 pr-8 py-2 border border-zinc-200 rounded-full leading-5 bg-zinc-50/50 placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 focus:bg-white transition-all sm:text-sm"
                placeholder="Find stories or people..."
              />
              <button
                v-if="postStore.isInSearch"
                @click="closeSearch"
                class="absolute cursor-pointer inset-y-0 right-0 pr-3 flex items-center"
              >
                <X class="h-4 w-4 text-zinc-400 hover:text-zinc-600" />
              </button>
            </div>
          </div>

          <div class="flex items-center space-x-1 border-r border-zinc-100 pr-4 mr-1">
             <router-link
                :to="{name: 'Feed'}"
                class="p-2 rounded-full text-zinc-400 hover:text-violet-600 hover:bg-violet-50 transition-all cursor-pointer"
                active-class="text-violet-600 bg-violet-50"
                title="Home"
              >
                <Home class="h-5 w-5" />
              </router-link>
              
              <router-link
                :to="{name: 'Notifications'}"
                class="p-2 rounded-full text-zinc-400 hover:text-violet-600 hover:bg-violet-50 transition-all cursor-pointer relative"
                active-class="text-violet-600 bg-violet-50"
                title="Notifications"
              >
                <Bell class="h-5 w-5" />
              </router-link>
              
              <router-link
                :to="{name: 'History'}"
                class="p-2 rounded-full text-zinc-400 hover:text-violet-600 hover:bg-violet-50 transition-all cursor-pointer"
                active-class="text-violet-600 bg-violet-50"
                title="History"
              >
                <Clock class="h-5 w-5" />
              </router-link>
              
              <router-link
                :to="{name: 'Chat'}"
                class="p-2 rounded-full text-zinc-400 hover:text-violet-600 hover:bg-violet-50 transition-all cursor-pointer"
                active-class="text-violet-600 bg-violet-50"
                title="Messages"
              >
                <MessageCircleMore class="h-5 w-5" />
              </router-link>
          </div>
          
          <router-link
            :to="{name: 'NewPost'}"
            class="flex items-center px-4 py-2 text-sm font-semibold text-white bg-zinc-900 rounded-full hover:bg-violet-600 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300 cursor-pointer"
          >
            <Plus class="h-4 w-4 mr-1.5" />
            New Post
          </router-link>
          
          <!-- Support Button -->
          <button
            @click.stop="supportStore.open()"
            class="p-2 cursor-pointer rounded-full text-zinc-400 hover:text-violet-600 hover:bg-violet-50 transition-all"
            title="Support"
          >
            <Headset class="h-5 w-5" />
          </button>

          <!-- Connects Counter -->
          <div class="relative">
            <button
              @click="openConnectsModal"
              class="flex items-center space-x-1.5 px-3 py-1.5 rounded-full border border-zinc-200 bg-white hover:border-violet-200 hover:shadow-sm transition-all cursor-pointer group"
            >
              <Wallet class="h-4 w-4 text-amber-500 group-hover:scale-110 transition-transform" />
              <span class="text-sm font-semibold text-zinc-600 group-hover:text-zinc-900">{{ currentConnects }}</span>
            </button>
          </div>

          <div class="relative ml-2">
            <button
                @click="toggleProfileMenu"
                class="relative flex items-center p-0.5 rounded-full ring-2 ring-transparent hover:ring-zinc-100 transition-all cursor-pointer"
                id="user-menu"
                aria-expanded="false"
                aria-haspopup="true"
              >
                <div class="relative">
                  <div v-if="profilePicture" class="h-9 w-9 rounded-full overflow-hidden ring-1 ring-zinc-100 shadow-sm">
                    <img :src="profilePicture" alt="Profile" class="h-full w-full object-cover" />
                  </div>
                  <div v-else class="h-9 w-9 rounded-full bg-violet-100 flex items-center justify-center ring-1 ring-zinc-100 shadow-sm">
                    <span class="text-violet-600 font-bold text-sm">{{ userStore.userInitials }}</span>
                  </div>
                  <BadgeCheck 
                    v-if="hasActiveSubscription"
                    class="h-4 w-4 text-white absolute -bottom-1 -right-1 bg-white rounded-full"
                    fill="#7c3aed"
                  />
                </div>
              </button>
            
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
                class="origin-top-right absolute right-0 mt-2 w-56 rounded-xl shadow-xl py-2 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50 divide-y divide-zinc-100"
                role="menu"
                aria-orientation="vertical"
                aria-labelledby="user-menu"
              >
                <div class="px-4 py-3">
                  <p class="text-xs font-medium text-zinc-400">Signed in as</p>
                  <p class="text-sm font-bold text-zinc-900 truncate">{{ userStore.user?.name }}</p>
                </div>
                <div class="py-1">
                  <router-link
                    to="/profile"
                    class="group flex items-center px-4 py-2 text-sm text-zinc-600 hover:bg-violet-50 hover:text-violet-600 transition-colors"
                    role="menuitem"
                  >
                    Your Profile
                  </router-link>
                   <router-link
                    :to="{name: 'History'}"
                    class="group flex items-center px-4 py-2 text-sm text-zinc-600 hover:bg-violet-50 hover:text-violet-600 transition-colors"
                    role="menuitem"
                  >
                    History
                  </router-link>
                </div>
                <div class="py-1">
                  <button
                    @click="handleLogout"
                    class="w-full text-left px-4 py-2 text-sm text-rose-500 hover:bg-rose-50 cursor-pointer transition-colors"
                    role="menuitem"
                  >
                    Sign out
                  </button>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </div>
    <!-- Connects Modal -->
    <ConnectsModal
      :is-open="isConnectsModalOpen"
      :current-connects="currentConnects"
      :connects-data="connectsStore.connectsData"
      :loading="connectsStore.isLoading"
      @close="isConnectsModalOpen = false"
      @purchase="connectsStore.handlePurchaseConnects"
    />
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { Search, X, Home, Wallet, BadgeCheck, Bell, Headset, Clock, MessageCircleMore, Plus } from 'lucide-vue-next';
import { usePostStore } from '@/stores/post';
import { useUserStore } from '@/stores/user';
import { useSupportStore } from '@/stores/support';
import ConnectsModal from '@/components/connects/ConnectsModal.vue';
import { useConnectsStore } from '@/stores/connect';
const userStore = useUserStore();
const connectsStore = useConnectsStore();
const supportStore = useSupportStore();

const profilePicture = computed(() => {
  return userStore.user?.profile_picture;
});

const postStore = usePostStore();
const searchQuery = ref('');

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    postStore.search(searchQuery.value.trim());
  }
};
const closeSearch = () => {
  searchQuery.value = '';
  postStore.closeSearch();
}
const isProfileMenuOpen = ref(false);
const isConnectsModalOpen = ref(false);
const currentConnects = computed(() => userStore?.user?.connects);

const hasActiveSubscription = computed(() => {
  if (!userStore.subscriptions || userStore.subscriptions.length === 0) return false;
  return userStore.subscriptions.some(sub => sub.is_active);
});

const toggleProfileMenu = () => {
  isProfileMenuOpen.value = !isProfileMenuOpen.value;
};

const handleLogout = async () => {
  userStore.logout();
};

// Handle click outside to close the dropdown
const handleClickOutside = (event) => {
  const dropdownElement = document.querySelector('.profile-dropdown');
  if (isProfileMenuOpen.value && dropdownElement && !dropdownElement.contains(event.target)) {
    isProfileMenuOpen.value = false;
  }
};


const openConnectsModal = async () => {
  isConnectsModalOpen.value = true;
  await connectsStore.fetchConnectsData();
};

onMounted(async () => {
  document.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>
