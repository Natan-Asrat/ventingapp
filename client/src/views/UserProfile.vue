<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Desktop Navigation -->
    <desktop-top-nav 
      :user-initials="userInitials"
      @logout="handleLogout"
    />
    
    <!-- Mobile Top Navigation -->
    <mobile-top-nav 
      :user-initials="userInitials"
      :user-name="currentUser?.name || 'User'"
      @logout="handleLogout"
    />
    
    <!-- Main Content -->
    <div class="pt-16 pb-16 md:pt-0 md:pb-0">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <!-- Loading State -->
        <div v-if="profileStore.loading" class="text-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500 mx-auto"></div>
          <p class="mt-2 text-sm text-gray-500">Loading profile...</p>
        </div>

        <!-- Profile Content -->
        <div v-else class="flex flex-col md:flex-row gap-6">
          <!-- Left Column - User Profile -->
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
                      <div v-if="profileStore?.profile?.profile_picture" class="h-24 w-24 rounded-full overflow-hidden bg-gray-200">
                        <img :src="profileStore?.profile?.profile_picture" :alt="profileStore?.profile?.name" class="h-full w-full object-cover">
                      </div>
                      <div v-else class="h-24 w-24 rounded-full bg-indigo-100 flex items-center justify-center">
                        <span class="text-3xl font-medium text-indigo-600">{{ userInitials }}</span>
                      </div>
                    </div>
                    <div class="flex-1">
                      <h2 class="text-2xl font-semibold text-gray-900">{{ profileStore?.profile?.name || 'User' }}</h2>
                      <p class="text-sm text-gray-500">@{{ profileStore?.profile?.username }}</p>
                      <p class="mt-1 text-sm text-gray-500">Joined {{ profileStore?.profile?.formatted_date_joined }}</p>
                    </div>
                  </div>
                  
                  <!-- User Stats -->
                  <div class="grid grid-cols-3 gap-4 text-center border-t border-gray-200 pt-4">
                    <div>
                      <p class="text-sm font-medium text-gray-500">Posts</p>
                      <p class="text-lg font-semibold text-gray-900">{{ profileStore.postCount }}</p>
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-500">Followers</p>
                      <p class="text-lg font-semibold text-gray-900">{{ profileStore?.profile?.followers || 0 }}</p>
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-500">Likes</p>
                      <p class="text-lg font-semibold text-gray-900">{{ profileStore?.profile?.post_likes || 0 }}</p>
                    </div>
                  </div>
                <div class="space-y-2">
                    <button
                        v-if="!isCurrentUser"
                        @click="handleProfileFollowClick"
                        class="w-full py-2 px-4 rounded-md shadow-sm text-sm font-medium transition-colors"
                        :class="{
                            // Connected
                            'bg-green-100 text-green-700 hover:bg-green-200 cursor-pointer': profileStore.profile.connected,

                            // Pending
                            'bg-yellow-100 text-yellow-700 hover:bg-yellow-200 cursor-pointer': profileStore.profile.pending_connection && !profileStore.profile.rejected_connection,

                            // Rejected
                            'bg-red-100 text-red-700 cursor-not-allowed': profileStore.profile.rejected_connection,

                            // Default (not connected)
                            'bg-gray-100 text-gray-700 hover:bg-gray-200 cursor-pointer':
                            (!profileStore.profile.connected &&
                            !profileStore.profile.pending_connection &&
                            !profileStore.profile.rejected_connection) ||
                            profileStore.profile.removed_connection,

                            // Disabled state
                            'disabled:opacity-50 disabled:cursor-not-allowed': 
                            profileStore.profile.rejected_connection || profileStore.profile.banned_connection
                        }"
                        :disabled="profileStore.profile.rejected_connection || profileStore.profile.banned_connection"
                    >
                        <template v-if="profileStore.profile.connected">
                            Following
                        </template>

                        <template v-else-if="profileStore.profile.pending_connection">
                            Pending
                        </template>

                        <template v-else-if="profileStore.profile.banned_connection">
                            Banned
                        </template>

                        <template v-else-if="profileStore.profile.rejected_connection">
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
          
          <!-- Right Column - User Posts -->
          <div class="w-full md:w-2/3">
            <div class="bg-white shadow sm:rounded-lg overflow-hidden">
                <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
                    <h3 class="text-lg leading-6 font-medium text-gray-900">Posts</h3>
                </div>
                <FeedList :user_id="profileStore.profileId" />
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Mobile Bottom Navigation -->
    <mobile-bottom-nav :user-initials="userInitials" />
    <ConnectionModal 
      v-if="showConnectionsModal" 
      @close="showConnectionsModal = false" 
      @connection-updated="handleConnectionsUpdated"
      :show="showConnectionsModal" 
      :connections="connections"
      :loadingConnections="loadingConnections"
    />
    <ConnectionRequestModal
      v-if="profileStore.showConnectionProfileModal"
      :is-open="profileStore.showConnectionProfileModal"
      :user-name="profileStore.selectedUserForConnection?.posted_by?.name || 'this user'"
      @close="profileStore.closeConnectionProfileModal"
      @confirm="profileStore.confirmConnectionRequest"
    />
    
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { useOtherProfilePostStore } from '@/stores/profile';
import { X } from 'lucide-vue-next';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import api from '@/api/axios';
import { message } from 'ant-design-vue';
import FeedList from '@/components/feed/FeedList.vue';
import ConnectionModal from '@/components/feed/ConnectionsModal.vue';
import ConnectionRequestModal from '@/components/feed/ConnectionRequestModal.vue';

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();
const profileStore = useOtherProfilePostStore();

// State
const loading = ref(true);
const user = ref(null);
const isFollowing = ref(false);
const isFollowingLoading = ref(false);

const showConnectionsModal = ref(false);

const connections = ref([]);

const loadingConnections = ref(false);
// Computed
const currentUser = computed(() => userStore.user);
const isCurrentUser = computed(() => {
  return currentUser.value && user.value && currentUser.value.id === user.value.id;
});

const userInitials = computed(() => {
  if (!user.value?.name) return 'U';
  return user.value.name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .substring(0, 2);
});

const handleConnectionsUpdated = async () => {
  await fetchConnections()
  emit('connection-updated')
  showConnectionsModal.value = false;
}

const fetchConnections = async () => {  
  try {
    loadingConnections.value = true;
    const response = await api.get(`/account/users/${profileStore.profileId}/our_connection/`);
    connections.value = response.data;
    showConnectionsModal.value = true;
  } catch (error) {
    console.error('Error fetching connections:', error);
  } finally {
    loadingConnections.value = false;
  }
};

const handleProfileFollowClick = async () => {
  console.log("clicked follow")
  if (profileStore.profile.pending_connection) {
    fetchConnections();
  } else if (!profileStore.profile.rejected_connection) {
    if (profileStore.profile.removed_connection && !profileStore.profile.pending_connection && !profileStore.profile.rejected_connection) {
        profileStore.setShowConnectionProfileModal(true);
    } else {
        await profileStore.handleProfileFollow(false);
        await userStore.checkAuth();
    }
  }
};

const toggleFollow = async () => {
  if (!currentUser.value) {
    router.push('/login');
    return;
  }
  
  try {
    isFollowingLoading.value = true;
    
    if (isFollowing.value) {
      await api.post(`/account/users/${user.value.id}/unfollow/`);
      message.success(`Unfollowed ${user.value.name}`);
    } else {
      await api.post(`/account/users/${user.value.id}/follow/`);
      message.success(`Following ${user.value.name}`);
    }
    
    // Toggle follow state
    isFollowing.value = !isFollowing.value;
    
    // Update followers count
    if (user.value) {
      user.value.followers += isFollowing.value ? 1 : -1;
    }
  } catch (err) {
    console.error('Error toggling follow:', err);
    message.error('Failed to update follow status. Please try again.');
  } finally {
    isFollowingLoading.value = false;
  }
};

const handleLogout = () => {
  userStore.logout();
  router.push('/login');
};

const loadProfile = async () => {
  console.log("user id", route.params.userId)
  console.log("username", route.params.username)
  profileStore.resetProfileId();
  if (route.params.userId || route.params.username) {
      profileStore.setLoading(true);
      await profileStore.fetchUserProfile();
      profileStore.setLoading(false);
  } else {
      profileStore.setLoading(false);
  }
  profileStore.startProfilePolling();

}
watch(() => route.params.userId, async (newUserId, oldUserId) => {
  if (newUserId && newUserId !== oldUserId) {
    await loadProfile();
  }
});

// Initial load
onMounted(async () => {
    await loadProfile();
});

onUnmounted(() => {
    profileStore.stopProfilePolling();
});
</script>
