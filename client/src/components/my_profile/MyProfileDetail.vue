<template>
    <!-- Left Column - User Profile -->
    <div class="w-full md:w-1/3">
        <div class="bg-white shadow-sm border border-zinc-100 rounded-2xl sticky top-24 max-h-[calc(100vh-8rem)] overflow-y-auto custom-scrollbar">
            <div class="px-6 py-6 border-b border-zinc-100 bg-zinc-50/30">
                <h3 class="text-lg font-bold text-zinc-900 tracking-tight">Profile Information</h3>
                <p class="mt-1 text-sm text-zinc-500">Your personal details and account settings.</p>
            </div>
            <div class="p-6">
                <div class="space-y-8">
                    <MyProfilePictureAndName />
                    <MyProfileDetailAndSubscriptions />
                    <div class="pt-6 border-t border-zinc-100">
                        <router-link 
                            to="/feed"
                            class="flex w-full items-center justify-center px-4 py-2.5 border border-zinc-200 shadow-sm text-sm font-semibold rounded-full text-zinc-700 bg-white hover:bg-zinc-50 hover:border-zinc-300 transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500"
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
import MyProfilePictureAndName from '@/components/my_profile/my_profile_detail/MyProfilePictureAndName.vue';
import MyProfileDetailAndSubscriptions from '@/components/my_profile/my_profile_detail/MyProfileDetailAndSubscriptions.vue';
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #e4e4e7;
  border-radius: 20px;
}
.custom-scrollbar:hover::-webkit-scrollbar-thumb {
  background-color: #d4d4d8;
}
</style>