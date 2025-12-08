<template>
    <!-- Right Column - User Posts -->
    <div class="w-full md:w-2/3">
        <div class="bg-white shadow-sm border border-zinc-100 rounded-2xl overflow-hidden min-h-[500px]">
            <MyProfilePostsTabs />
            
            <!-- Loading State -->
            <div v-if="myProfileStore.loading" class="p-12 text-center flex flex-col items-center">
                <div class="animate-spin rounded-full h-10 w-10 border-[3px] border-violet-100 border-t-violet-500 mb-4"></div>
                <p class="text-sm font-medium text-zinc-400 animate-pulse">Loading your stories...</p>
            </div>
            
            <!-- Empty State -->
            <div v-else-if="myProfileStore.posts.length === 0 && myProfileStore.archivedPosts.length === 0" class="p-12 text-center flex flex-col items-center">
                <div class="h-20 w-20 bg-zinc-50 rounded-full flex items-center justify-center mb-4 ring-8 ring-zinc-50/50">
                    <FileText class="h-10 w-10 text-zinc-300" />
                </div>
                <h3 class="text-lg font-bold text-zinc-900">No posts yet</h3>
                <p class="mt-1 text-zinc-500 max-w-sm mx-auto">Share your thoughts, stories, or questions with the community.</p>
                <div class="mt-8">
                    <router-link 
                    :to="{ name: 'NewPost' }"
                    class="inline-flex items-center px-6 py-3 border border-transparent shadow-lg shadow-zinc-900/10 text-sm font-semibold rounded-full text-white bg-zinc-900 hover:bg-violet-600 hover:-translate-y-0.5 transition-all duration-300"
                    >
                    <PlusIcon class="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
                    Create New Post
                    </router-link>
                </div>
            </div>
            
            <!-- Posts List -->
            <div v-else class="bg-zinc-50/30">
                <div v-if="myProfileStore.filteredPosts.length === 0" class="p-12 text-center">
                    <div class="inline-block p-4 rounded-full bg-zinc-100 mb-3">
                        <FolderOpen class="w-8 h-8 text-zinc-400" />
                    </div>
                    <p class="text-zinc-500 font-medium">
                    {{ myProfileStore.activeTab === myProfileStore.ARCHIVED_TAB ? 'Archive is empty' : 'No active posts' }}
                    </p>
                </div>
                
                <div class="space-y-4 p-4 md:p-6">
                    <MyPostItem 
                        v-for="post in myProfileStore.filteredPosts" 
                        :key="post.id" 
                        :post="post"
                        :isArchiving="myProfileStore.isArchivingId == post.id"
                        @update:post="myProfileStore.handlePostUpdate"
                        @archive="myProfileStore.archivePost(post.id)"
                        @restore="myProfileStore.restorePost(post.id)"
                    />
                </div>
            
                <!-- Load More Button -->
                <div v-if="myProfileStore.hasNextPage" class="p-6 text-center">
                    <button
                        @click="myProfileStore.loadMorePosts"
                        :disabled="myProfileStore.loadingMore"
                        class="inline-flex items-center px-6 py-2.5 border border-zinc-200 shadow-sm text-sm font-medium rounded-full text-zinc-700 bg-white hover:bg-zinc-50 hover:border-zinc-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all cursor-pointer"
                    >
                        <span v-if="myProfileStore.loadingMore" class="flex items-center">
                            <Loader2 class="animate-spin -ml-1 mr-2 h-4 w-4 text-zinc-500" />
                            Loading...
                        </span>
                        <span v-else>Load More Stories</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { FileText, Loader2, PlusIcon, FolderOpen } from 'lucide-vue-next';
import { useMyProfileStore } from '@/stores/my_profile';

import MyPostItem from '@/components/feed/MyPostItem.vue';
import MyProfilePostsTabs from '@/components/my_profile/my_profile_posts/MyProfilePostsTabs.vue';

const myProfileStore = useMyProfileStore();
</script>
