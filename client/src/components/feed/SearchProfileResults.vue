<template>

    <!-- Profile Search Results -->
    <div 
      v-if="postStore.isInSearch && !postStore.loading && postStore.searchProfileResults?.length > 0" 
      class="px-4 sm:px-6 max-w-2xl lg:max-w-4xl lg:px-8 pt-20 md:pt-6 mx-auto"
    >
      <div class="bg-white shadow-sm mb-6 rounded-lg overflow-hidden">
        <div class="px-4 py-3 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">Profiles</h3>
        </div>
        
        <div class="divide-y divide-gray-200">
          <!-- Show first profile by default -->
          <div 
            v-for="(profile, index) in showAllProfiles ? postStore.searchProfileResults : [postStore.searchProfileResults[0]]" 
            :key="profile.id"
            class="p-4 hover:bg-gray-50 transition-colors cursor-pointer"
            @click="$router.push({ name: 'UsernameProfile', params: { username: profile.username } })"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <!-- Profile Picture -->
                <div class="h-14 w-14 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden flex-shrink-0">
                  <img 
                    v-if="profile.profile_picture" 
                    :src="profile.profile_picture" 
                    :alt="profile.name" 
                    class="h-full w-full object-cover"
                  >
                  <span v-else class="text-xl font-medium text-gray-500">
                    {{ profile.name ? profile.name.charAt(0).toUpperCase() : 'U' }}
                  </span>
                </div>
                
                <!-- User Info -->
                <div class="min-w-0">
                  <div class="flex items-center space-x-2">
                    <h4 class="text-base font-semibold text-gray-900 truncate">
                      {{ profile.name || 'User' }}
                    </h4>
                  </div>
                  <p class="text-sm text-gray-500 truncate">@{{ profile.username }}</p>
                  <div class="flex items-center mt-1 space-x-4">
                    <span class="text-xs text-gray-500">{{ profile.followers }} {{ profile.followers === 1 ? 'follower' : 'followers' }}</span>
                    <span class="text-xs text-gray-500">•</span>
                    <span class="text-xs text-gray-500">{{ profile.post_likes }} {{ profile.post_likes === 1 ? 'like' : 'likes' }}</span>
                  </div>
                </div>
              </div>
              
              <!-- View Profile Button -->
              <router-link 
                :to="{ name: 'UsernameProfile', params: { username: profile.username } }"
                class="px-4 py-1.5 text-sm font-medium rounded-md bg-indigo-600 text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                View Profile
              </router-link>
            </div>
          </div>
        </div>
        
        <!-- Show 'View more profiles' button if there are more than 1 profiles and not showing all -->
        <div 
          v-if="!showAllProfiles && postStore.searchProfileResults.length > 1" 
          class="px-4 py-3 border-t border-gray-200 text-center"
        >
          <button 
            @click="showAllProfiles = true"
            class="text-sm font-medium text-indigo-600 hover:text-indigo-800"
          >
            View more profiles
          </button>
        </div>
        
        <!-- Load More Button (only show when showing all profiles) -->
        <div 
          v-if="showAllProfiles && postStore.searchProfileHasNextPage" 
          class="px-4 py-3 border-t border-gray-200 text-center"
        >
          <button 
            @click="postStore.loadMoreProfiles()" 
            :disabled="postStore.loadingMoreProfiles"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg v-if="postStore.loadingMoreProfiles" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ postStore.loadingMoreProfiles ? 'Loading...' : 'Load more profiles' }}
          </button>
        </div>
      </div>
    </div>
</template>

<script setup>
import {ref} from 'vue';
import { usePostStore } from '@/stores/post';

const postStore = usePostStore();

// State
const showAllProfiles = ref(false);

</script>
