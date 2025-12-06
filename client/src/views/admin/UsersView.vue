<template>
  <div class="space-y-6">
    <div class="bg-white shadow rounded-lg p-6">
      <h2 class="text-lg font-medium text-gray-900 mb-6">Users</h2>
      
      <!-- Search and Filter -->
      <div class="mb-6">
        <div class="relative">
          <input
            type="text"
            v-model="searchQuery"
            @input="handleSearch"
            placeholder="Search users..."
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
          />
          <div class="absolute inset-y-0 right-0 flex items-center pr-3">
            <Search class="h-5 w-5 text-gray-400" />
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-red-500 text-center py-8">
        {{ error }}
      </div>

      <!-- Empty State -->
      <div v-else-if="users.length === 0" class="text-center py-8 text-gray-500">
        No users found.
      </div>

      <!-- Users List -->
      <div v-else class="space-y-4">
        <div v-for="user in users" :key="user.id" class="bg-white rounded-lg shadow p-4 flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <img 
              v-if="user.profile_picture" 
              :src="user.profile_picture" 
              :alt="user.name" 
              class="h-12 w-12 rounded-full object-cover"
            />
            <div v-else class="h-12 w-12 rounded-full bg-gray-200 flex items-center justify-center">
              <span class="text-gray-500 text-xl">{{ user.name ? user.name.charAt(0).toUpperCase() : 'U' }}</span>
            </div>
            <div>
              <h3 class="font-medium text-gray-900">{{ user.name || 'Unnamed User' }}</h3>
              <p class="text-sm text-gray-500">@{{ user.username }}</p>
              <p class="text-xs text-gray-400">Joined {{ user.date_joined_since }}</p>
              <div class="flex items-center space-x-2 mt-1">
                <span class="text-xs px-2 py-0.5 rounded-full" 
                      :class="user.banned_connection ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'">
                  {{ user.banned_connection ? 'Banned' : 'Active' }}
                </span>
                <span class="text-xs px-2 py-0.5 bg-blue-100 text-blue-800 rounded-full">
                  {{ user.followers }} {{ user.followers === 1 ? 'follower' : 'followers' }}
                </span>
              </div>
            </div>
          </div>
          <div class="flex space-x-2">
            <router-link 
              :to="`/admin/reports?user=${user.id}`"
              class="px-3 py-1 text-sm text-indigo-600 hover:bg-indigo-50 rounded-md border border-indigo-100"
              title="View Reports"
            >
              Reports
            </router-link>
            <button 
              @click="toggleBan(user)"
              class="px-3 py-1 text-sm rounded-md"
              :class="user.banned_connection ? 'bg-green-100 text-green-800 hover:bg-green-200' : 'bg-red-100 text-red-800 hover:bg-red-200'"
              :title="user.banned_connection ? 'Unban User' : 'Ban User'"
            >
              {{ user.banned_connection ? 'Unban' : 'Ban' }}
            </button>
          </div>
        </div>

        <!-- Load More Button -->
        <div v-if="hasMore" class="flex justify-center mt-6">
          <button
            @click="loadMore"
            :disabled="loadingMore"
            :class="{'cursor-pointer': !loadingMore}"
            class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 flex items-center"
          >
            <span v-if="!loadingMore">Load More</span>
            <span v-else class="flex items-center">
              <Loader2 class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" />
              Loading...
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/api/axios';
import { debounce } from 'lodash';
import { Loader2, Search } from 'lucide-vue-next';

const route = useRoute();
const users = ref([]);
const isLoading = ref(true);
const error = ref(null);
const nextPage = ref(null);
const loadingMore = ref(false);
const searchQuery = ref(route.query.search || '');

const hasMore = computed(() => !!nextPage.value);

const fetchUsers = async (page = 1, search = '') => {
  try {
    const params = { page };
    if (search) {
      params.search = search;
    }

    const response = await api.get('/account/users/', { params });
    
    if (page === 1) {
      users.value = response.data.results;
    } else {
      users.value = [...users.value, ...response.data.results];
    }
    
    nextPage.value = response.data.next;
    error.value = null;
  } catch (err) {
    console.error('Error fetching users:', err);
    error.value = 'Failed to load users. Please try again.';
  } finally {
    isLoading.value = false;
    loadingMore.value = false;
  }
};

const loadMore = () => {
  if (hasMore.value && !loadingMore.value) {
    loadingMore.value = true;
    const page = nextPage.value ? new URL(nextPage.value).searchParams.get('page') : 2;
    fetchUsers(parseInt(page), searchQuery.value);
  }
};

const toggleBan = async (user) => {
  if (!confirm(`Are you sure you want to ${user.banned_connection ? 'unban' : 'ban'} this user?`)) {
    return;
  }

  try {
    const action = user.banned_connection ? 'unban' : 'ban';
    await api.post(`/account/users/${user.id}/${action}/`);
    
    // Update the local state
    user.banned_connection = !user.banned_connection;
  } catch (err) {
    console.error('Error toggling ban status:', err);
    alert('Failed to update user status. Please try again.');
  }
};

const handleSearch = debounce(() => {
  // Update URL without page reload
  const query = { ...route.query };
  if (searchQuery.value) {
    query.search = searchQuery.value;
  } else {
    delete query.search;
  }
  window.history.replaceState({}, '', `${route.path}?${new URLSearchParams(query).toString()}`);
  
  // Reset pagination and fetch with new search term
  isLoading.value = true;
  fetchUsers(1, searchQuery.value);
}, 300);

// Watch for changes in route query
watch(() => route.query.search, (newSearch) => {
  if (newSearch !== searchQuery.value) {
    searchQuery.value = newSearch || '';
    fetchUsers(1, newSearch || '');
  }
});

onMounted(() => {
  fetchUsers(1, searchQuery.value);
});
</script>