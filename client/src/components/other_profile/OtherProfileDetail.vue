<template>
    <div class="w-full md:w-1/3">
        <div class="bg-white shadow sm:rounded-lg overflow-hidden sticky top-6">
            <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
                <h3 class="text-lg leading-6 font-medium text-gray-900">Profile Information</h3>
            </div>
            
            <div class="px-4 py-5 sm:p-6">
                <div class="space-y-6">
                    <!-- Profile Picture and Name -->
                    <div class="flex items-start space-x-4">
                        <div class="flex-shrink-0">
                            <div v-if="profile?.profile_picture" class="h-24 w-24 rounded-full overflow-hidden bg-gray-200">
                                <img :src="profile?.profile_picture" :alt="profile?.name" class="h-full w-full object-cover">
                            </div>
                            <div v-else class="h-24 w-24 rounded-full bg-indigo-100 flex items-center justify-center">
                                <span class="text-3xl font-medium text-indigo-600">{{ userInitials }}</span>
                            </div>
                        </div>
                        <div class="flex-1">
                            <h2 class="text-2xl font-semibold text-gray-900">{{ profile?.name || 'User' }}</h2>
                            <p class="text-sm text-gray-500">@{{ profile?.username }}</p>
                            <p class="mt-1 text-sm text-gray-500">Joined {{ profile?.date_joined_since }}</p>
                        </div>
                    </div>
                    
                    <!-- User Stats -->
                    <div class="grid grid-cols-3 gap-4 text-center border-t border-gray-200 pt-4">
                        <div>
                            <p class="text-sm font-medium text-gray-500">Posts</p>
                            <p class="text-lg font-semibold text-gray-900">{{ postCount }}</p>
                        </div>
                        <div>
                            <p class="text-sm font-medium text-gray-500">Followers</p>
                            <p class="text-lg font-semibold text-gray-900">{{ profile?.followers || 0 }}</p>
                        </div>
                        <div>
                            <p class="text-sm font-medium text-gray-500">Likes</p>
                            <p class="text-lg font-semibold text-gray-900">{{ profile?.post_likes || 0 }}</p>
                        </div>
                    </div>
                    <div class="space-y-2">
                        <button
                            v-if="!isCurrentUser"
                            @click="$emit('follow')"
                            class="w-full py-2 px-4 rounded-md shadow-sm text-sm font-medium transition-colors"
                            :class="{
                                // Connected
                                'bg-green-100 text-green-700 hover:bg-green-200 cursor-pointer': profile.connected,

                                // Pending
                                'bg-yellow-100 text-yellow-700 hover:bg-yellow-200 cursor-pointer': profile.pending_connection && !profile.rejected_connection,

                                // Rejected
                                'bg-red-100 text-red-700 cursor-not-allowed': profile.rejected_connection,

                                // Default (not connected)
                                'bg-gray-100 text-gray-700 hover:bg-gray-200 cursor-pointer':
                                (!profile.connected &&
                                !profile.pending_connection &&
                                !profile.rejected_connection) ||
                                profile.removed_connection,

                                // Disabled state
                                'disabled:opacity-50 disabled:cursor-not-allowed': 
                                profile.rejected_connection || profile.banned_connection
                            }"
                            :disabled="profile.rejected_connection || profile.banned_connection"
                        >
                            <template v-if="profile.connected">
                                Following
                            </template>

                            <template v-else-if="profile.pending_connection">
                                Pending
                            </template>

                            <template v-else-if="profile.banned_connection">
                                Banned
                            </template>

                            <template v-else-if="profile.rejected_connection">
                                Rejected
                            </template>

                            <template v-else>
                                Follow
                            </template>
                        </button>
                        <!-- Back to Home Button -->
                        <router-link 
                            to="/home"
                            class="block mt-4 text-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
                        >
                            Back to Feed
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useUserStore } from '@/stores/user';
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
</script>
