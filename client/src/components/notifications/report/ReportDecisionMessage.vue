<template>
    <!-- Message Details -->
    <div
        v-if="reportDecision?.report?.reported_message"
        class="border-t border-gray-200 pt-4"
    >
        <h4 class="text-sm font-medium text-gray-500 mb-2">Reported Message</h4>

        <div class="space-y-4 text-left">
            <!-- Message Header -->
            <div class="flex items-start space-x-3">
                
                <!-- Sender Avatar -->
                <div
                    v-if="reportDecision.report.reported_message.user?.profile_picture"
                    class="h-10 w-10 rounded-full overflow-hidden flex-shrink-0"
                >
                    <img
                        :src="reportDecision.report.reported_message.user.profile_picture"
                        :alt="reportDecision.report.reported_message.user?.name"
                        class="h-full w-full object-cover"
                    />
                </div>

                <div
                    v-else
                    class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-sm text-gray-600 flex-shrink-0"
                >
                    {{ reportDecision.report.reported_message.user?.name
                        ? reportDecision.report.reported_message.user.name.charAt(0).toUpperCase()
                        : 'U'
                    }}
                </div>

                <!-- Sender Info -->
                <div class="flex-1 min-w-0">
                    <div class="flex items-center space-x-2">
                        <span class="text-sm font-medium text-gray-900 truncate">
                        {{ reportDecision.report.reported_message.user?.name || 'Unknown User' }}
                        </span>
                        <span class="text-xs text-gray-500">
                        @{{ reportDecision.report.reported_message.user?.username || 'user' }}
                        </span>
                    </div>

                    <!-- Main Message Content -->
                    <div
                        v-if="reportDecision.report.reported_message.message"
                        class="text-sm text-gray-800"
                    >
                        {{ reportDecision.report.reported_message.message }}
                    </div>
                </div>
            </div>

            <!-- Message Content -->
            <div class="pl-13 -mt-2 space-y-3">

                <!-- Reply To -->
                <div
                    v-if="reportDecision.report.reported_message.reply_to"
                    class="bg-gray-50 rounded-lg p-2 text-xs border border-gray-100"
                >
                    <div class="flex items-center text-gray-500 mb-1">
                        <Reply class="h-3 w-3 mr-1" />
                        <span>
                        Replying to @{{ reportDecision.report.reported_message.reply_to.user?.username || 'user' }}
                        </span>
                    </div>
                    <p class="text-gray-700 truncate">
                        {{ reportDecision.report.reported_message.reply_to.message || 'No message content' }}
                    </p>
                </div>

                <!-- Forwarded From -->
                <div
                    v-if="reportDecision.report.reported_message.forwarded_from"
                    class="bg-blue-50 rounded-lg p-2 text-xs border border-blue-100"
                >
                    <div class="flex items-center text-blue-600 mb-1">
                        <Forward class="h-3 w-3 mr-1" />
                        <span>
                        Forwarded from @{{ reportDecision.report.reported_message.forwarded_from.user?.username || 'user' }}
                        </span>
                    </div>
                    <p class="text-gray-700">
                        {{ reportDecision.report.reported_message.forwarded_from.message || 'No message content' }}
                    </p>
                </div>

                <!-- Shared Post -->
                <div
                    v-if="reportDecision.report.reported_message.shared_post"
                    class="border border-gray-200 rounded-lg overflow-hidden"
                >
                    <div class="p-3 bg-gray-50 border-b border-gray-100">
                        <div class="flex items-center space-x-2">
                            <FileText class="h-4 w-4 text-gray-500" />
                            <span class="text-xs font-medium text-gray-700">Shared Post</span>
                        </div>
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
                                class="h-6 w-6 rounded-full bg-gray-200 flex items-center justify-center text-xs text-gray-600"
                            >
                                {{
                                reportDecision.report.reported_message.shared_post.posted_by?.name
                                    ? reportDecision.report.reported_message.shared_post.posted_by.name.charAt(0).toUpperCase()
                                    : 'U'
                                }}
                            </div>

                            <span class="text-xs font-medium">
                                {{ reportDecision.report.reported_message.shared_post.posted_by?.name || 'User' }}
                            </span>
                        </div>

                        <!-- Description -->
                        <ShowMore :text="reportDecision.report.reported_message.shared_post.description" />

                        <!-- Post Image -->
                        <div v-if="reportDecision.report.reported_message.shared_post.image_url" class="mt-3 rounded-lg overflow-hidden">
                            <img 
                                :src="reportDecision.report.reported_message.shared_post.image_url" 
                                :alt="'Post by ' + (reportDecision.report.reported_message.shared_post.posted_by?.username || 'user')" 
                                class="w-full h-auto object-cover cursor-zoom-in"
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
                    class="text-sm text-gray-500 italic"
                >
                    No message content
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