<template>
    <!-- Profile Search Results -->
    <div 
      v-if="postStore.isInSearch && !postStore.loading && postStore.searchProfileResults?.length > 0" 
      class="px-4 sm:px-6 max-w-2xl lg:max-w-4xl lg:px-8 pt-20 md:pt-6 mx-auto mb-6"
    >
      <div class="bg-white shadow-sm border border-zinc-100/80 rounded-2xl overflow-hidden">
        <div class="px-6 py-4 border-b border-zinc-100 bg-zinc-50/50">
          <h3 class="text-sm font-semibold text-zinc-500 uppercase tracking-wider">People</h3>
        </div>
        
        <div class="divide-y divide-zinc-100">
          <!-- Show first profile by default -->
          <div 
            v-for="(profile, index) in showAllProfiles ? postStore.searchProfileResults : [postStore.searchProfileResults[0]]" 
            :key="profile.id"
            class="p-5 hover:bg-violet-50/50 transition-colors cursor-pointer group"
            @click="$router.push({ name: 'UsernameProfile', params: { username: profile.username } })"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <!-- Profile Picture -->
                <div class="h-12 w-12 rounded-full bg-violet-100 flex items-center justify-center overflow-hidden flex-shrink-0 ring-2 ring-white shadow-sm">
                  <img 
                    v-if="profile.profile_picture" 
                    :src="profile.profile_picture" 
                    :alt="profile.name" 
                    class="h-full w-full object-cover"
                  >
                  <span v-else class="text-lg font-bold text-violet-500">
                    {{ profile.name ? profile.name.charAt(0).toUpperCase() : 'U' }}
                  </span>
                </div>
                
                <!-- User Info -->
                <div class="min-w-0">
                  <div class="flex items-center space-x-2">
                    <h4 class="text-base font-semibold text-zinc-900 truncate group-hover:text-violet-700 transition-colors">
                      {{ profile.name || 'User' }}
                    </h4>
                  </div>
                  <p class="text-sm text-zinc-500 truncate font-medium">@{{ profile.username }}</p>
                  <div class="flex items-center mt-1 space-x-3 text-xs text-zinc-400">
                    <span>{{ profile.followers }} {{ profile.followers === 1 ? 'follower' : 'followers' }}</span>
                    <span class="text-zinc-300">•</span>
                    <span>{{ profile.post_likes }} {{ profile.post_likes === 1 ? 'like' : 'likes' }}</span>
                  </div>
                </div>
              </div>
              
              <!-- View Profile Button -->
              <button 
                class="px-4 py-2 text-xs font-semibold rounded-full bg-white border border-zinc-200 text-zinc-700 group-hover:bg-violet-600 group-hover:text-white group-hover:border-violet-600 transition-all shadow-sm"
              >
                View Profile
              </button>
            </div>
          </div>
        </div>
        
        <!-- Show 'View more profiles' button if there are more than 1 profiles and not showing all -->
        <div 
          v-if="!showAllProfiles && postStore.searchProfileResults.length > 1" 
          class="px-4 py-3 bg-zinc-50/50 border-t border-zinc-100 text-center"
        >
          <button 
            @click="showAllProfiles = true"
            class="text-sm font-medium text-violet-600 hover:text-violet-800 transition-colors cursor-pointer"
          >
            View {{ postStore.searchProfileResults.length - 1 }} more {{ postStore.searchProfileResults.length - 1 === 1 ? 'profile' : 'profiles' }}
          </button>
        </div>
        
        <!-- Load More Button (only show when showing all profiles) -->
        <div 
          v-if="showAllProfiles && postStore.searchProfileHasNextPage" 
          class="px-4 py-4 bg-zinc-50/50 border-t border-zinc-100 text-center"
        >
          <button 
            @click="postStore.loadMoreProfiles()" 
            :disabled="postStore.loadingMoreProfiles"
            class="inline-flex items-center px-5 py-2 border border-transparent text-sm font-medium rounded-full shadow-sm text-white bg-zinc-900 hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer"
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
