<template>
    <!-- Left Column - User Profile -->
    <div class="w-full md:w-1/3">
        <div class="bg-white shadow sm:rounded-lg overflow-hidden sticky top-6">
            <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
                <h3 class="text-lg leading-6 font-medium text-gray-900">Profile Information</h3>
                <p class="mt-1 max-w-2xl text-sm text-gray-500">Your personal details and account information.</p>
            </div>
            <div class="px-4 py-5 sm:p-6">
                <div class="space-y-6">
                    <ProfilePictureAndName />
                    <ProfileDetailAndSubscriptions />
                    <div class="pt-4 border-t border-gray-200">
                        <router-link 
                            to="/home"
                            class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
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
import ProfilePictureAndName from '@/components/my_profile/my_profile_detail/MyProfilePictureAndName.vue';
import ProfileDetailAndSubscriptions from '@/components/my_profile/my_profile_detail/MyProfileDetailAndSubscriptions.vue';
</script>
