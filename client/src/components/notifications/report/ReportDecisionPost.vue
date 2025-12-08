<template>
    <!-- Post Details -->
    <div v-if="reportDecision?.report?.reported_post" class="bg-white border border-zinc-200 rounded-xl overflow-hidden shadow-sm">
        <div class="px-4 py-3 bg-zinc-50 border-b border-zinc-100">
             <h4 class="text-xs font-bold text-zinc-500 uppercase tracking-wide">Reported Post Content</h4>
        </div>
        <div class="p-5">
            <!-- Post Header -->
            <div class="flex items-center space-x-3 mb-4">
                <div v-if="reportDecision.report.reported_post.posted_by?.profile_picture" class="flex-shrink-0 h-10 w-10 rounded-full overflow-hidden ring-2 ring-zinc-50">
                    <img 
                        :src="reportDecision.report.reported_post.posted_by.profile_picture" 
                        :alt="reportDecision.report.reported_post.posted_by.name"
                        class="h-full w-full object-cover"
                    />
                </div>
                <div v-else class="h-10 w-10 rounded-full bg-zinc-100 flex items-center justify-center text-sm font-bold text-zinc-400 ring-2 ring-zinc-50">
                    {{ reportDecision.report.reported_post.posted_by?.name ? reportDecision.report.reported_post.posted_by.name.charAt(0).toUpperCase() : 'U' }}
                </div>
                <div class="flex-1 min-w-0">
                    <p class="text-sm font-bold text-zinc-900 truncate">
                        {{ reportDecision.report.reported_post.posted_by?.name || 'Anonymous' }}
                    </p>
                    <p class="text-xs text-zinc-500 font-medium">
                        {{ reportDecision.report.reported_post.formatted_created_at }}
                    </p>
                </div>
            </div>
            
            <!-- Post Content -->
            <div class="text-sm text-zinc-700 leading-relaxed mb-4">
                {{ reportDecision.report.reported_post.description }}
            </div>
            
            <!-- Post Image -->
            <div v-if="reportDecision.report.reported_post.image_url" class="mb-4 rounded-lg overflow-hidden border border-zinc-100 bg-zinc-50">
                <img 
                    :src="reportDecision.report.reported_post.image_url" 
                    alt="Post content"
                    class="w-full h-auto object-cover max-h-64 cursor-zoom-in hover:opacity-95 transition-opacity"
                    @click="openImage(reportDecision.report.reported_post.image_url)"
                />
            </div>
            
            <!-- Post Stats -->
            <div class="flex items-center space-x-6 text-xs font-medium text-zinc-400 pt-2 border-t border-zinc-50">
                <div class="flex items-center space-x-1.5">
                    <Heart class="h-4 w-4" :class="{ 'fill-rose-500 text-rose-500': reportDecision.report.reported_post.liked }" />
                    <span>{{ reportDecision.report.reported_post.likes || 0 }}</span>
                </div>
                <div class="flex items-center space-x-1.5">
                    <MessageCircle class="h-4 w-4" />
                    <span>{{ reportDecision.report.reported_post.comments || 0 }}</span>
                </div>
                <div class="flex items-center space-x-1.5">
                    <Eye class="h-4 w-4" />
                    <span>{{ reportDecision.report.reported_post.views || 0 }}</span>
                </div>
            </div>
            
            <!-- Payment Info if exists -->
            <div v-if="reportDecision.report.reported_post.payment_info_list?.length > 0" class="mt-4 pt-3 border-t border-zinc-100">
                <h5 class="text-xs font-bold text-zinc-400 uppercase tracking-wide mb-2">Payment Information</h5>
                <div class="space-y-2">
                    <div v-for="(payment, index) in reportDecision.report.reported_post.payment_info_list" :key="index" class="bg-zinc-50 p-2.5 rounded-lg border border-zinc-100 text-xs text-zinc-600">
                        <div class="flex justify-between mb-1">
                            <span class="font-bold text-zinc-700">{{ payment.method }}</span>
                        </div>
                        <p class="font-mono bg-white px-1.5 py-0.5 rounded border border-zinc-100 inline-block mb-1">{{ payment.account }}</p>
                        <p v-if="payment.nameOnAccount" class="text-zinc-500 italic">{{ payment.nameOnAccount }}</p>
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