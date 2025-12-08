<template>
  <nav class="md:hidden fixed bottom-0 left-0 right-0 bg-white/95 backdrop-blur-lg border-t border-zinc-200 z-50 pb-safe">
    <div class="flex justify-around items-center h-16 px-1">
      <router-link 
        :to="{name: 'Feed'}" 
        class="group flex flex-col items-center justify-center flex-1 h-full pt-1"
        active-class="text-violet-600"
        v-slot="{ isActive }"
      >
        <div class="relative p-1 rounded-xl group-hover:bg-zinc-50 transition-colors" :class="isActive ? 'bg-violet-50' : ''">
           <Home class="h-6 w-6 transition-transform group-active:scale-90" :class="isActive ? 'stroke-[2.5]' : 'text-zinc-400 stroke-[1.5]'" />
        </div>
        <span class="text-[10px] font-medium mt-0.5" :class="isActive ? 'text-violet-600' : 'text-zinc-400'">Home</span>
      </router-link>

      <router-link 
        :to="{name: 'History'}" 
        class="group flex flex-col items-center justify-center flex-1 h-full pt-1"
        active-class="text-violet-600"
        v-slot="{ isActive }"
      >
        <div class="relative p-1 rounded-xl group-hover:bg-zinc-50 transition-colors" :class="isActive ? 'bg-violet-50' : ''">
            <History class="h-6 w-6 transition-transform group-active:scale-90" :class="isActive ? 'stroke-[2.5]' : 'text-zinc-400 stroke-[1.5]'" />
        </div>
        <span class="text-[10px] font-medium mt-0.5" :class="isActive ? 'text-violet-600' : 'text-zinc-400'">History</span>
      </router-link>
      
      <router-link 
        :to="{name: 'NewPost'}" 
        class="group flex flex-col items-center justify-center flex-1 h-full pt-1"
        active-class="text-violet-600"
      >
        <div class="bg-zinc-900 text-white p-3.5 rounded-full -mt-10 shadow-lg shadow-zinc-900/20 group-hover:bg-violet-600 group-hover:scale-105 group-active:scale-95 transition-all duration-300 border-4 border-white cursor-pointer">
          <Plus class="h-6 w-6" />
        </div>
        <span class="text-[10px] font-semibold text-zinc-600 mt-1">New Post</span>
      </router-link>
      
      <router-link 
        :to="{name: 'Notifications'}" 
        class="group flex flex-col items-center justify-center flex-1 h-full pt-1"
        active-class="text-violet-600"
        v-slot="{ isActive }"
      >
        <div class="relative p-1 rounded-xl group-hover:bg-zinc-50 transition-colors" :class="isActive ? 'bg-violet-50' : ''">
            <Bell class="h-6 w-6 transition-transform group-active:scale-90" :class="isActive ? 'stroke-[2.5]' : 'text-zinc-400 stroke-[1.5]'" />
        </div>
        <span class="text-[10px] font-medium mt-0.5" :class="isActive ? 'text-violet-600' : 'text-zinc-400'">Activity</span>
      </router-link>
      
      <div class="flex-1 h-full pt-1">
        <router-link 
          :to="{name: 'Profile'}" 
          class="group flex flex-col items-center justify-center h-full w-full"
          active-class="text-violet-600"
          v-slot="{ isActive }"
        >
          <div class="relative h-7 w-7 flex items-center justify-center rounded-full ring-2 transition-all" :class="isActive ? 'ring-violet-500 ring-offset-2' : 'ring-transparent'">
            <UserIcon v-if="!userStore.user?.profile_picture" class="h-6 w-6" :class="isActive ? 'text-violet-600 fill-current' : 'text-zinc-400 stroke-[1.5]'" />
            <img v-else :src="userStore.user.profile_picture" class="h-full w-full rounded-full object-cover" />

            <BadgeCheck 
              v-if="hasActiveSubscription"
              class="h-3.5 w-3.5 text-white absolute -top-1 -right-1.5 bg-white rounded-full"
              fill="#7c3aed"
            />
          </div>
          <span class="text-[10px] font-medium mt-0.5" :class="isActive ? 'text-violet-600' : 'text-zinc-400'">Me</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { Home, Plus, UserIcon, BadgeCheck, Bell, History } from 'lucide-vue-next';
import { computed } from 'vue';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();

const hasActiveSubscription = computed(() => {
  if (!userStore.subscriptions || userStore.subscriptions.length === 0) return false;
  return userStore.subscriptions.some(sub => sub.is_active);
});
</script>
