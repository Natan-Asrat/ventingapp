<template>
  <div class="min-h-screen bg-gray-50">
    <DesktopTopNav />
    <MobileTopNav />
    
    <!-- Main Content -->
    <div class="pt-16 pb-16 md:pt-0 md:pb-0">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="bg-white shadow sm:rounded-lg overflow-hidden">
          <div class="px-4 py-5 sm:px-6 border-b border-gray-200 flex items-center">
            <MessageSquare class="h-5 w-5 text-indigo-600 mr-2" />
            <div>
              <h3 class="text-lg leading-6 font-medium text-gray-900">Are you sad?</h3>
            </div>
          </div>
          
          <form @submit.prevent="newPostStore.submitPost" class="px-4 py-5 sm:p-6">
            <div class="space-y-6">
              <NewPostDescription />
              <NewPostImageUpload />
              <NewPostDonations />

              <div class="flex justify-end pt-4">
                <button
                  type="submit"
                  class="w-full md:w-auto inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  :class="{'cursor-pointer': !newPostStore.isLoading, 'cursor-not-allowed': newPostStore.isLoading}"
                  :disabled="newPostStore.isLoading"
                >
                  <Send v-if="!newPostStore.isLoading" class="-ml-1 mr-2 h-4 w-4" />
                  <span v-else class="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></span>
                  {{ newPostStore.isLoading ? 'Posting...' : 'Post' }}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <MobileBottomNav />
    
    <!-- Payment Method Modal -->
    <PaymentMethodModal 
      :isOpen="newPostStore.isPaymentModalOpen"
      :initialData="newPostStore.newPaymentInfo"
      @close="newPostStore.setIsPaymentModalOpen(false)"
      @save="newPostStore.addPaymentMethod"
    />
  </div>
</template>

<script setup>
import { MessageSquare, Send } from 'lucide-vue-next';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import PaymentMethodModal from '@/components/PaymentMethodModal.vue';
import { useNewPostStore } from '@/stores/new_post';
import NewPostDescription from '@/components/new_post/NewPostDescription.vue';
import NewPostImageUpload from '@/components/new_post/NewPostImageUpload.vue';
import NewPostDonations from '@/components/new_post/NewPostDonations.vue';
const newPostStore = useNewPostStore();
</script>