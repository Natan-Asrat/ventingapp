<template>
  <nav class="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50">
    <div class="flex justify-around items-center h-16">
      <router-link 
        :to="{name: 'Feed'}" 
        class="flex flex-col items-center justify-center flex-1 h-full text-gray-600 hover:text-indigo-600 transition-colors"
      >
        <Home class="h-6 w-6" />
        <span class="text-xs mt-1">Home</span>
      </router-link>
      
      <router-link 
        :to="{name: 'NewPost'}" 
        class="flex flex-col items-center justify-center flex-1 h-full text-gray-600 hover:text-indigo-600 transition-colors"
      >
        <div class="bg-indigo-600 text-white p-2 rounded-full -mt-8 mb-1 shadow-lg">
          <Plus class="h-6 w-6" />
        </div>
        <span class="text-xs text-gray-600">New Post</span>
      </router-link>
      
      <router-link 
        :to="{name: 'Profile'}" 
        class="flex flex-col items-center justify-center flex-1 h-full text-gray-600 hover:text-indigo-600 transition-colors"
      >
        <div class="h-6 w-6 flex items-center justify-center">
          <UserIcon class="h-6 w-6 text-indigo-600" />
        </div>
        <span class="text-xs mt-1">Profile</span>
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { Home, Plus, UserIcon } from 'lucide-vue-next';
</script>
