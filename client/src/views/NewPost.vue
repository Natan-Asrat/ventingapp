<template>
  <div class="min-h-screen bg-zinc-50/50 font-sans">
    <DesktopTopNav />
    <MobileTopNav />
    
    <!-- Main Content -->
    <div class="pt-20 pb-20 md:pt-6 md:pb-0 relative z-0">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="bg-white shadow-sm border border-zinc-100 rounded-2xl overflow-hidden">
          <div class="px-6 py-5 border-b border-zinc-100 bg-zinc-50/30 flex items-center">
            <div class="h-10 w-10 bg-violet-100 rounded-full flex items-center justify-center mr-3">
               <MessageSquare class="h-5 w-5 text-violet-600" />
            </div>
            <div>
              <h3 class="text-lg font-bold text-zinc-900 tracking-tight">Share Your Story</h3>
              <p class="text-sm text-zinc-500">What's on your mind today?</p>
            </div>
          </div>
          
          <form @submit.prevent="submit" class="px-6 py-6">
            <div class="space-y-8">
              <NewPostDescription />
              <NewPostImageUpload />
              <NewPostDonations />

              <div class="pt-6 border-t border-zinc-100 flex justify-end">
                <button
                  type="submit"
                  class="w-full md:w-auto inline-flex justify-center items-center px-6 py-3 border border-transparent text-sm font-semibold rounded-full shadow-sm text-white bg-zinc-900 hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-70 disabled:cursor-not-allowed transition-all duration-300"
                  :class="{'cursor-pointer hover:shadow-lg hover:-translate-y-0.5': !newPostStore.isLoading}"
                  :disabled="newPostStore.isLoading"
                >
                  <Send v-if="!newPostStore.isLoading" class="-ml-1 mr-2 h-4 w-4" />
                  <span v-else class="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></span>
                  {{ newPostStore.isLoading ? 'Posting...' : 'Post Story' }}
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
import { useRouter } from 'vue-router';
import NewPostDescription from '@/components/new_post/NewPostDescription.vue';
import NewPostImageUpload from '@/components/new_post/NewPostImageUpload.vue';
import NewPostDonations from '@/components/new_post/NewPostDonations.vue';
const newPostStore = useNewPostStore();
const router = useRouter();
const submit = () => {
  newPostStore.submitPost(router);
}
</script>