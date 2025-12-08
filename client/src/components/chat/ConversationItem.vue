<template>
    <li 
        class="py-3 px-3 rounded-xl hover:bg-zinc-50 cursor-pointer transition-all duration-200 group border border-transparent hover:border-zinc-100"
        @click="$emit('select-conversation', conversation)"
    >
        <div class="flex items-center">
            <div class="flex-shrink-0 mr-4 relative">
                <!-- Avatar Logic -->
                <div v-if="conversation.is_group || conversation.name" class="h-12 w-12 rounded-full overflow-hidden bg-violet-100 flex items-center justify-center ring-2 ring-white shadow-sm">
                    <img 
                        v-if="conversation.logo" 
                        :src="conversation.logo" 
                        :alt="conversation.name || 'Group'"
                        class="h-full w-full object-cover"
                    >
                    <span v-else class="text-violet-600 font-bold text-lg">
                        {{ conversation.name ? conversation.name.charAt(0).toUpperCase() : 'G' }}
                    </span>
                </div>
                
                <div 
                    v-else-if="conversation.other_user_list?.length > 0 && conversation.other_user_list[0]?.user?.profile_picture" 
                    class="h-12 w-12 rounded-full overflow-hidden ring-2 ring-white shadow-sm"
                >
                    <img 
                        :src="conversation.other_user_list[0].user.profile_picture" 
                        :alt="conversation.other_user_list[0].user.name"
                        class="h-full w-full object-cover"
                    >
                </div>
                
                <div v-else class="h-12 w-12 rounded-full bg-zinc-100 flex items-center justify-center text-zinc-400 font-bold text-lg ring-2 ring-white shadow-sm">
                    {{ 
                    conversation.other_user_list?.length > 0 ? 
                    conversation.other_user_list[0].user.name.charAt(0).toUpperCase() : 'U'
                    }}
                </div>
                
                <!-- Online Status (Optional - if available) -->
                <!-- <span class="absolute bottom-0 right-0 block h-3 w-3 rounded-full bg-emerald-400 ring-2 ring-white"></span> -->
            </div>
            
            <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-0.5">
                    <p class="text-sm font-semibold truncate transition-colors group-hover:text-violet-700" 
                       :class="conversation.new_messages_count > 0 ? 'text-zinc-900' : 'text-zinc-800'">
                        {{ 
                            conversation.name || 
                            (conversation.other_user_list?.length > 0 ? 
                            conversation.other_user_list[0].user.name : 
                            'New Chat')
                        }}
                    </p>
                    <p v-if="conversation.last_message_list.length > 0" class="text-xs text-zinc-400 font-medium whitespace-nowrap ml-2">
                        {{ conversation.last_message_list[0].created_since }}
                    </p>
                </div>
                <div class="flex justify-between items-center">
                    <p :class="['text-xs truncate pr-2', conversation.new_messages_count > 0 ? 'font-semibold text-zinc-800' : 'text-zinc-500 group-hover:text-zinc-600']">
                        <span v-if="conversation.last_message_list?.[0]?.user?.id === userStore.user?.id" class="text-zinc-400">You: </span>
                        {{ conversation.last_message || 'Start a conversation' }}
                    </p>
                    <span v-if="conversation.new_messages_count > 0" class="bg-violet-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-sm flex-shrink-0 min-w-[1.25rem] text-center">
                        {{ conversation.new_messages_count > 99 ? '99+' : conversation.new_messages_count }}
                    </span>
                </div>
            </div>
            
            <!-- Context Menu Trigger -->
            <div class="ml-2 relative">
                <DropdownMenu>
                    <template #trigger>
                        <div class="p-1.5 rounded-full text-zinc-300 hover:text-violet-600 hover:bg-violet-50 transition-colors">
                            <EllipsisVertical class="h-5 w-5"/>
                        </div>
                    </template>
                    
                    <div class="py-1">
                        <button 
                            v-if="conversation.my_membership_list[0]?.category !== 'primary'"
                            @click.stop="chatStore.moveConversation(conversation, 'primary')"
                            class="flex cursor-pointer w-full items-center px-4 py-2 text-xs font-medium text-zinc-700 hover:bg-violet-50 hover:text-violet-700 transition-colors"
                        >
                            <ArrowRight class="mr-2 h-3.5 w-3.5" />
                            <span>Move to Primary</span>
                            <Check v-if="conversation.my_membership_list[0]?.category === 'primary'" class="ml-auto h-3.5 w-3.5 text-violet-600" />
                        </button>
                        <button 
                            v-if="conversation.my_membership_list[0]?.category !== 'secondary'"
                            @click.stop="chatStore.moveConversation(conversation, 'secondary')"
                            class="flex cursor-pointer w-full items-center px-4 py-2 text-xs font-medium text-zinc-700 hover:bg-violet-50 hover:text-violet-700 transition-colors"
                        >
                            <ArrowRight class="mr-2 h-3.5 w-3.5" />
                            <span>Move to Secondary</span>
                            <Check v-if="conversation.my_membership_list[0]?.category === 'secondary'" class="ml-auto h-3.5 w-3.5 text-violet-600" />
                        </button>
                        <div class="h-px bg-zinc-100 my-1"></div>
                        <button 
                            @click.stop="chatStore.archiveConversation(conversation)"
                            class="flex cursor-pointer w-full items-center px-4 py-2 text-xs font-medium text-rose-600 hover:bg-rose-50 transition-colors"
                        >
                            <Archive class="mr-2 h-3.5 w-3.5" />
                            <span>Archive</span>
                        </button>
                    </div>
                </DropdownMenu>
            </div>
        </div>
    </li>
</template>

<script setup>
import { EllipsisVertical, Archive, ArrowRight, Check } from 'lucide-vue-next';
import DropdownMenu from '@/components/common/DropdownMenu.vue';
import { useChatStore } from '@/stores/chat';
import { useUserStore } from '@/stores/user';

const chatStore = useChatStore();
const userStore = useUserStore();

defineProps({
    conversation: {
        type: Object,
        required: true
    }
})
</script>