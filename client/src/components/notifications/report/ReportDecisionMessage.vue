<template>
    <!-- Message Details -->
    <div
        v-if="reportDecision?.report?.reported_message"
        class="bg-white border border-zinc-200 rounded-xl overflow-hidden shadow-sm mt-4"
    >
        <div class="px-4 py-3 bg-zinc-50 border-b border-zinc-100">
            <h4 class="text-xs font-bold text-zinc-500 uppercase tracking-wide">Reported Message Content</h4>
        </div>

        <div class="p-5">
            <!-- Message Header -->
            <div class="flex items-start space-x-3 mb-4">
                
                <!-- Sender Avatar -->
                <div
                    v-if="reportDecision.report.reported_message.user?.profile_picture"
                    class="h-10 w-10 rounded-full overflow-hidden flex-shrink-0 ring-2 ring-zinc-50"
                >
                    <img
                        :src="reportDecision.report.reported_message.user.profile_picture"
                        :alt="reportDecision.report.reported_message.user?.name"
                        class="h-full w-full object-cover"
                    />
                </div>

                <div
                    v-else
                    class="h-10 w-10 rounded-full bg-violet-100 flex items-center justify-center text-sm font-bold text-violet-600 flex-shrink-0 ring-2 ring-zinc-50"
                >
                    {{ reportDecision.report.reported_message.user?.name
                        ? reportDecision.report.reported_message.user.name.charAt(0).toUpperCase()
                        : 'U'
                    }}
                </div>

                <!-- Sender Info -->
                <div class="flex-1 min-w-0">
                    <div class="flex items-center space-x-2">
                        <span class="text-sm font-bold text-zinc-900 truncate">
                        {{ reportDecision.report.reported_message.user?.name || 'Unknown User' }}
                        </span>
                    </div>
                    <span class="text-xs font-medium text-zinc-500">
                        @{{ reportDecision.report.reported_message.user?.username || 'user' }}
                    </span>
                </div>
            </div>

            <!-- Message Content Block -->
            <div class="space-y-3">
                
                <!-- Main Message Content -->
                <div
                    v-if="reportDecision.report.reported_message.message"
                    class="text-sm text-zinc-800 bg-zinc-50 p-3 rounded-lg border border-zinc-100"
                >
                    {{ reportDecision.report.reported_message.message }}
                </div>

                <!-- Reply To -->
                <div
                    v-if="reportDecision.report.reported_message.reply_to"
                    class="bg-violet-50/50 rounded-xl p-3 text-xs border border-violet-100"
                >
                    <div class="flex items-center text-violet-600 font-semibold mb-1">
                        <Reply class="h-3.5 w-3.5 mr-1.5" />
                        <span>
                        Replying to @{{ reportDecision.report.reported_message.reply_to.user?.username || 'user' }}
                        </span>
                    </div>
                    <p class="text-zinc-600 truncate pl-5 border-l-2 border-violet-200">
                        {{ reportDecision.report.reported_message.reply_to.message || 'No message content' }}
                    </p>
                </div>

                <!-- Forwarded From -->
                <div
                    v-if="reportDecision.report.reported_message.forwarded_from"
                    class="bg-blue-50/50 rounded-xl p-3 text-xs border border-blue-100"
                >
                    <div class="flex items-center text-blue-600 font-semibold mb-1">
                        <Forward class="h-3.5 w-3.5 mr-1.5" />
                        <span>
                        Forwarded from @{{ reportDecision.report.reported_message.forwarded_from.user?.username || 'user' }}
                        </span>
                    </div>
                    <p class="text-zinc-600 pl-5 border-l-2 border-blue-200">
                        {{ reportDecision.report.reported_message.forwarded_from.message || 'No message content' }}
                    </p>
                </div>

                <!-- Shared Post -->
                <div
                    v-if="reportDecision.report.reported_message.shared_post"
                    class="border border-zinc-200 rounded-xl overflow-hidden mt-3"
                >
                    <div class="px-3 py-2 bg-zinc-50 border-b border-zinc-100 flex items-center gap-2">
                        <FileText class="h-3.5 w-3.5 text-zinc-400" />
                        <span class="text-xs font-bold text-zinc-500 uppercase tracking-wide">Shared Post</span>
                    </div>

                    <div class="p-3">
                        <!-- Post Owner -->
                        <div class="flex items-center space-x-2 mb-2">
                            <div
                                v-if="reportDecision.report.reported_message.shared_post.posted_by?.profile_picture"
                                class="h-6 w-6 rounded-full overflow-hidden"
                            >
                                <img
                                    :src="reportDecision.report.reported_message.shared_post.posted_by.profile_picture"
                                    :alt="reportDecision.report.reported_message.shared_post.posted_by?.name"
                                    class="h-full w-full object-cover"
                                />
                            </div>
                            <div
                                v-else
                                class="h-6 w-6 rounded-full bg-zinc-100 flex items-center justify-center text-[10px] font-bold text-zinc-500"
                            >
                                {{
                                reportDecision.report.reported_message.shared_post.posted_by?.name
                                    ? reportDecision.report.reported_message.shared_post.posted_by.name.charAt(0).toUpperCase()
                                    : 'U'
                                }}
                            </div>

                            <span class="text-xs font-bold text-zinc-700">
                                {{ reportDecision.report.reported_message.shared_post.posted_by?.name || 'User' }}
                            </span>
                        </div>

                        <!-- Description -->
                        <div class="text-xs text-zinc-600 mb-2">
                            <ShowMore :text="reportDecision.report.reported_message.shared_post.description" />
                        </div>

                        <!-- Post Image -->
                        <div v-if="reportDecision.report.reported_message.shared_post.image_url" class="rounded-lg overflow-hidden border border-zinc-100">
                            <img 
                                :src="reportDecision.report.reported_message.shared_post.image_url" 
                                :alt="'Post by ' + (reportDecision.report.reported_message.shared_post.posted_by?.username || 'user')" 
                                class="w-full h-auto object-cover cursor-zoom-in max-h-48"
                                @load="$emit('image-loaded')"
                            />
                        </div>
                    </div>
                </div>

                <!-- No Content -->
                <div
                    v-if="!reportDecision.report.reported_message.message &&
                            !reportDecision.report.reported_message.shared_post &&
                            !reportDecision.report.reported_message.reply_to &&
                            !reportDecision.report.reported_message.forwarded_from"
                    class="text-sm text-zinc-400 italic text-center py-2"
                >
                    No message content available
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Reply, Forward, FileText } from 'lucide-vue-next';
import ShowMore from '@/components/ShowMore.vue';
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
</script>