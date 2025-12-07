<template>
  <div class="min-h-screen bg-gray-50">
    <DesktopTopNav />    
    <MobileTopNav />
    
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
          <OtherProfileDetail 
            :post-count="profileStore.postCount"
            :profile="profileStore.profile"
            @follow="handleProfileFollowClick"
          />
          
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
    
    <MobileBottomNav />
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
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { useOtherProfilePostStore } from '@/stores/profile';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import FeedList from '@/components/feed/FeedList.vue';
import ConnectionModal from '@/components/feed/ConnectionsModal.vue';
import ConnectionRequestModal from '@/components/feed/ConnectionRequestModal.vue';
import OtherProfileDetail from '@/components/other_profile/OtherProfileDetail.vue';
import { useConnectionStore } from '@/stores/connection';
const route = useRoute();
const userStore = useUserStore();
const profileStore = useOtherProfilePostStore();
const connectionStore = useConnectionStore();
const showConnectionsModal = ref(false);

const connections = ref([]);

const loadingConnections = ref(false);

const handleConnectionsUpdated = async () => {
  await fetchConnections()
  emit('connection-updated')
  showConnectionsModal.value = false;
}

const fetchConnections = async () => {  
  try {
    loadingConnections.value = true;
    const response = await connectionStore.fetchOurConnections(profileStore.profileId);
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
