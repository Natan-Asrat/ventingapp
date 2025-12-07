<template>
    <li 
        class="py-4 hover:bg-gray-50 px-2 rounded-lg cursor-pointer"
        @click="$emit('select-conversation', conversation)"
    >
        <div class="flex items-center">
            <div class="flex-shrink-0 mr-4">
            <!-- Show conversation logo for groups or when explicitly showing conversation details -->
                <div v-if="conversation.is_group || conversation.name" class="h-10 w-10 rounded-full overflow-hidden bg-indigo-100 flex items-center justify-center">
                    <img 
                        v-if="conversation.logo" 
                        :src="conversation.logo" 
                        :alt="conversation.name || 'Group'"
                        class="h-full w-full object-cover"
                    >
                    <span v-else class="text-indigo-600 font-medium">
                        {{ conversation.name ? conversation.name.charAt(0).toUpperCase() : 'G' }}
                    </span>
                </div>
                <!-- Show user profile picture for direct messages -->
                <div 
                    v-else-if="conversation.other_user_list?.length > 0 && conversation.other_user_list[0]?.user?.profile_picture" 
                    class="h-10 w-10 rounded-full overflow-hidden"
                >
                    <img 
                        :src="conversation.other_user_list[0].user.profile_picture" 
                        :alt="conversation.other_user_list[0].user.name"
                        class="h-full w-full object-cover"
                    >
                </div>
                <!-- Fallback to user initial -->
                <div v-else class="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-medium">
                    {{ 
                    conversation.other_user_list?.length > 0 ? 
                    conversation.other_user_list[0].user.name.charAt(0).toUpperCase() : 'U'
                    }}
                </div>
            </div>
            <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between">
                    <p :class="['text-sm truncate', conversation.new_messages_count > 0 ? 'font-bold text-gray-900' : 'font-light text-gray-900']">
                        {{ 
                            conversation.name || 
                            (conversation.other_user_list?.length > 0 ? 
                            conversation.other_user_list[0].user.name : 
                            'New Chat')
                        }}
                    </p>
                </div>
                <p :class="['text-sm truncate', conversation.new_messages_count > 0 ? 'font-medium text-gray-900' : 'text-gray-500']">
                    {{ conversation.last_message || 'No messages yet' }}
                </p>
            </div>
            <div class="flex flex-col items-end">
                <p v-if="conversation.last_message_list.length > 0" class="text-xs text-gray-500">
                    {{ conversation.last_message_list[0].created_since }}
                </p>
                <span v-if="conversation.new_messages_count > 0" class="bg-indigo-600 text-white text-xs font-medium px-2 py-0.5 rounded-full ml-2">
                    {{ conversation.new_messages_count > 99 ? '99+' : conversation.new_messages_count }}
                </span>
            </div>
            <DropdownMenu>
                <template #trigger>
                    <EllipsisVertical class="h-8 py-2 w-8 text-gray-500 cursor-pointer"/>
                </template>
                <button 
                    v-if="conversation.my_membership_list[0]?.category !== 'primary'"
                    @click.stop="chatStore.moveConversation(conversation, 'primary')"
                    class="flex cursor-pointer w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                    <ArrowRight class="mr-2 h-4 w-4" />
                    <span>Move to Primary</span>
                    <Check v-if="conversation.my_membership_list[0]?.category === 'primary'" class="ml-auto h-4 w-4 text-indigo-600" />
                </button>
                <button 
                    v-if="conversation.my_membership_list[0]?.category !== 'secondary'"
                    @click.stop="chatStore.moveConversation(conversation, 'secondary')"
                    class="flex cursor-pointer w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                    <ArrowRight class="mr-2 h-4 w-4" />
                    <span>Move to Secondary</span>
                    <Check v-if="conversation.my_membership_list[0]?.category === 'secondary'" class="ml-auto h-4 w-4 text-indigo-600" />
                </button>
                <button 
                    @click.stop="chatStore.archiveConversation(conversation)"
                    class="flex cursor-pointer w-full items-center px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
                >
                    <Archive class="mr-2 h-4 w-4" />
                    <span>Archive</span>
                </button>
            </DropdownMenu>
        </div>
    </li>
</template>

<script setup>
import { EllipsisVertical, Archive, ArrowRight, Check } from 'lucide-vue-next';
import DropdownMenu from '@/components/common/DropdownMenu.vue';
import { useChatStore } from '@/stores/chat';

const chatStore = useChatStore();
defineProps({
    conversation: {
        type: Object,
        required: true
    }
})
</script>