<template>
    <!-- Right Column - User Posts -->
    <div class="w-full md:w-2/3">
        <div class="bg-white shadow sm:rounded-lg overflow-hidden">
            <ProfilePostsTabs />
            
            <!-- Loading State -->
            <div v-if="myProfileStore.loading" class="p-6 text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500 mx-auto"></div>
                <p class="mt-2 text-sm text-gray-500">Loading your posts...</p>
            </div>
            
            <!-- Empty State -->
            <div v-else-if="myProfileStore.posts.length === 0 && myProfileStore.archivedPosts.length === 0" class="p-6 text-center">
                <div class="mx-auto h-24 w-24 text-gray-400">
                    <FileText />
                </div>
                <h3 class="mt-2 text-sm font-medium text-gray-900">No posts yet</h3>
                <p class="mt-1 text-sm text-gray-500">Get started by creating your first post.</p>
                <div class="mt-6">
                    <router-link 
                    :to="{ name: 'NewPost' }"
                    class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                    <PlusIcon class="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
                    New Post
                    </router-link>
                </div>
            </div>
            
            <!-- Posts List -->
            <div v-else class="divide-y divide-gray-200">
                <div v-if="myProfileStore.filteredPosts.length === 0" class="p-8 text-center">
                    <p class="text-gray-500">
                    {{ myProfileStore.activeTab === myProfileStore.ARCHIVED_TAB ? 'No archived posts yet' : 'No active posts yet' }}
                    </p>
                </div>
                <MyPostItem 
                    v-else
                    v-for="post in myProfileStore.filteredPosts" 
                    :key="post.id" 
                    :post="post"
                    :isArchiving="myProfileStore.isArchivingId == post.id"
                    @update:post="myProfileStore.handlePostUpdate"
                    @archive="myProfileStore.archivePost(post.id)"
                    @restore="myProfileStore.restorePost(post.id)"
                    class="border-b border-gray-200 last:border-b-0"
                />
            
                <!-- Load More Button -->
                <div v-if="myProfileStore.hasNextPage" class="p-4 text-center">
                    <button
                        @click="myProfileStore.loadMorePosts"
                        :disabled="myProfileStore.loadingMore"
                        :class="{'cursor-pointer': !myProfileStore.loadingMore}"
                        class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                    >
                        <span v-if="myProfileStore.loadingMore" class="flex items-center">
                            <Loader2 class="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-500" />
                            Loading...
                        </span>
                        <span v-else>Load More</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { FileText, Loader2, PlusIcon } from 'lucide-vue-next';
import { useMyProfileStore } from '@/stores/my_profile';

import MyPostItem from '@/components/feed/MyPostItem.vue';
import ProfilePostsTabs from '@/components/my_profile/my_profile_posts/MyProfilePostsTabs.vue';

const myProfileStore = useMyProfileStore();
</script>
