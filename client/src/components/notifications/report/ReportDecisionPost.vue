<template>
    <!-- Post Details -->
    <div v-if="reportDecision?.report?.reported_post" class="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <div class="p-4 border-b border-gray-200">
            <h4 class="text-sm font-medium text-gray-500 mb-3">Reported Post</h4>
            <!-- Post Header -->
            <div class="flex items-start space-x-3">
                <div v-if="reportDecision.report.reported_post.posted_by?.profile_picture" class="flex-shrink-0 h-10 w-10 rounded-full overflow-hidden">
                    <img 
                        :src="reportDecision.report.reported_post.posted_by.profile_picture" 
                        :alt="reportDecision.report.reported_post.posted_by.name"
                        class="h-full w-full object-cover"
                    />
                </div>
                <div v-else class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-sm text-gray-600">
                    {{ reportDecision.report.reported_post.posted_by?.name ? reportDecision.report.reported_post.posted_by.name.charAt(0).toUpperCase() : 'U' }}
                </div>
                <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900 truncate">
                        {{ reportDecision.report.reported_post.posted_by?.name || 'Anonymous' }}
                    </p>
                    <p class="text-xs text-gray-500">
                        {{ reportDecision.report.reported_post.formatted_created_at }}
                    </p>
                </div>
            </div>
            
            <!-- Post Content -->
            <div class="mt-3 text-sm text-gray-800">
                {{ reportDecision.report.reported_post.description }}
            </div>
            
            <!-- Post Image -->
            <div v-if="reportDecision.report.reported_post.image_url" class="mt-3">
                <img 
                    :src="reportDecision.report.reported_post.image_url" 
                    alt="Post content"
                    class="max-h-64 w-auto rounded-md cursor-pointer hover:opacity-90 transition-opacity"
                    @click="openImage(reportDecision.report.reported_post.image_url)"
                />
            </div>
            
            <!-- Post Stats -->
            <div class="mt-3 flex items-center space-x-4 text-sm text-gray-500">
                <div class="flex items-center space-x-1">
                    <Heart class="h-4 w-4" :class="{ 'fill-red-500 text-red-500': reportDecision.report.reported_post.liked }" />
                    <span>{{ reportDecision.report.reported_post.likes || 0 }}</span>
                </div>
                <div class="flex items-center space-x-1">
                    <MessageCircle class="h-4 w-4" />
                    <span>{{ reportDecision.report.reported_post.comments || 0 }}</span>
                </div>
                <div class="flex items-center space-x-1">
                    <Eye class="h-4 w-4" />
                    <span>{{ reportDecision.report.reported_post.views || 0 }}</span>
                </div>
            </div>
            
            <!-- Payment Info if exists -->
            <div v-if="reportDecision.report.reported_post.payment_info_list?.length > 0" class="mt-3 pt-3 border-t border-gray-100">
                <h5 class="text-xs font-medium text-gray-500 mb-2">Payment Information</h5>
                <div class="space-y-2">
                    <div v-for="(payment, index) in reportDecision.report.reported_post.payment_info_list" :key="index" class="bg-gray-50 p-2 rounded text-xs">
                        <p><span class="font-medium">Method:</span> {{ payment.method }}</p>
                        <p><span class="font-medium">Account:</span> {{ payment.account }}</p>
                        <p v-if="payment.nameOnAccount"><span class="font-medium">Name:</span> {{ payment.nameOnAccount }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Eye, MessageCircle, Heart } from 'lucide-vue-next';
defineProps({
  reportDecision: {
    type: Object,
    default: () => ({
      report: {
        reported_transaction: {}
      }
    })
  },
});

const openImage = (url) => {
  window.open(url, '_blank');
};
</script>