<template>
    <div class="w-full md:w-1/3">
        <div class="bg-white shadow-sm border border-zinc-100 rounded-2xl sticky top-24 transition-shadow hover:shadow-md max-h-[calc(100vh-8rem)] overflow-y-auto custom-scrollbar">
            <!-- Decorative Header Background -->
            <div class="h-24 bg-gradient-to-r from-violet-50 via-purple-50 to-fuchsia-50 border-b border-zinc-100/50"></div>
            
            <div class="px-6 pb-6 relative">
                <!-- Profile Header -->
                <div class="flex items-end -mt-10 mb-5">
                    <div class="h-20 w-20 rounded-full overflow-hidden ring-4 ring-white shadow-lg bg-white flex-shrink-0 z-10">
                        <img v-if="profile?.profile_picture" :src="profile?.profile_picture" :alt="profile?.name" class="h-full w-full object-cover">
                        <div v-else class="h-full w-full bg-zinc-100 flex items-center justify-center">
                            <span class="text-2xl font-bold text-zinc-400">{{ userInitials }}</span>
                        </div>
                    </div>
                    
                    <div class="ml-4 mb-1 flex-1 min-w-0">
                        <h2 class="text-xl font-bold text-zinc-900 tracking-tight leading-tight truncate">{{ profile?.name || 'User' }}</h2>
                        <p class="text-sm font-medium text-zinc-500 truncate">@{{ profile?.username }}</p>
                    </div>
                </div>

                <div class="flex items-center mb-6 text-xs text-zinc-400 font-medium">
                    <Calendar class="w-3.5 h-3.5 mr-1.5" />
                    Joined {{ profile?.date_joined_since }}
                </div>

                <!-- Stats Grid -->
                <div class="grid grid-cols-3 gap-2 mb-6">
                    <div class="bg-zinc-50 rounded-xl p-3 text-center border border-zinc-100/50 hover:border-violet-100 transition-colors">
                        <p class="text-lg font-bold text-zinc-900">{{ postCount }}</p>
                        <p class="text-[10px] uppercase font-bold text-zinc-400 tracking-wide">Posts</p>
                    </div>
                    <div class="bg-zinc-50 rounded-xl p-3 text-center border border-zinc-100/50 hover:border-violet-100 transition-colors">
                        <p class="text-lg font-bold text-zinc-900">{{ profile?.followers || 0 }}</p>
                        <p class="text-[10px] uppercase font-bold text-zinc-400 tracking-wide">Followers</p>
                    </div>
                    <div class="bg-zinc-50 rounded-xl p-3 text-center border border-zinc-100/50 hover:border-violet-100 transition-colors">
                        <p class="text-lg font-bold text-zinc-900">{{ profile?.post_likes || 0 }}</p>
                        <p class="text-[10px] uppercase font-bold text-zinc-400 tracking-wide">Likes</p>
                    </div>
                </div>
                
                <!-- Actions -->
                <div class="space-y-3 pt-2 border-t border-zinc-50">
                    <button
                        v-if="!isCurrentUser"
                        @click="$emit('follow')"
                        class="w-full py-2.5 px-4 rounded-full shadow-sm text-sm font-semibold transition-all transform active:scale-[0.98] flex items-center justify-center gap-2"
                        :class="buttonClasses"
                        :disabled="profile.rejected_connection || profile.banned_connection"
                    >
                        <component :is="buttonIcon" class="w-4 h-4 stroke-[2.5]" />
                        {{ buttonText }}
                    </button>
                    
                    <router-link 
                        to="/feed"
                        class="flex w-full items-center justify-center px-4 py-2.5 border border-zinc-200 shadow-sm text-sm font-semibold rounded-full text-zinc-700 bg-white hover:bg-zinc-50 hover:border-zinc-300 transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500"
                    >
                        Back to Feed
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useUserStore } from '@/stores/user';
import { Calendar, UserPlus, UserCheck, Clock, UserX, Check } from 'lucide-vue-next';

const userStore = useUserStore();
// Computed
const currentUser = computed(() => userStore.user);

const props = defineProps({
    profile: {
        type: Object,
        required: true
    },
    postCount: {
        type: Number,
        required: true
    }
})

const userInitials = computed(() => {
  if (!props.profile?.name) return 'U';
  return props.profile.name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .substring(0, 2);
});

const isCurrentUser = computed(() => {
  return currentUser.value && props.profile && currentUser.value.id === props.profile.id;
});

const buttonClasses = computed(() => {
    const p = props.profile;
    if (p.connected) return 'bg-emerald-100 text-emerald-700 hover:bg-emerald-200 border border-emerald-200/50';
    if (p.pending_connection) return 'bg-amber-100 text-amber-700 hover:bg-amber-200 border border-amber-200/50';
    if (p.rejected_connection || p.banned_connection) return 'bg-rose-50 text-rose-400 cursor-not-allowed border border-rose-100';
    
    // Default (Not Connected)
    return 'bg-zinc-900 text-white hover:bg-violet-600 hover:shadow-violet-500/20 border border-transparent';
});

const buttonText = computed(() => {
    const p = props.profile;
    if (p.connected) return 'Following';
    if (p.pending_connection) return 'Pending';
    if (p.banned_connection) return 'Banned';
    if (p.rejected_connection) return 'Rejected';
    return 'Follow';
});

const buttonIcon = computed(() => {
    const p = props.profile;
    if (p.connected) return UserCheck;
    if (p.pending_connection) return Clock;
    if (p.banned_connection || p.rejected_connection) return UserX;
    return UserPlus;
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #e4e4e7;
  border-radius: 20px;
}
.custom-scrollbar:hover::-webkit-scrollbar-thumb {
  background-color: #d4d4d8;
}
</style>