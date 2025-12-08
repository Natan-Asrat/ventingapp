<template>
  <div class="min-h-screen bg-zinc-50/50 font-sans">
    <DesktopTopNav />
    <MobileTopNav />
    
    <div class="relative z-0">
        <SearchProfileResults />
        <FeedList />
    </div>

    <MobileBottomNav />
  </div>
</template>

<script setup>
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import FeedList from '@/components/feed/FeedList.vue';
import SearchProfileResults from '@/components/feed/SearchProfileResults.vue';
</script>