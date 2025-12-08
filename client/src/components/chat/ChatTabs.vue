<template>
    <!-- Tabs -->
    <div class="border-b border-zinc-100 mb-2">
        <nav class="-mb-px flex space-x-6 overflow-x-auto no-scrollbar px-2" aria-label="Tabs">
            <button
                v-for="(tab, index) in chatStore.tabs"
                :key="tab.id"
                @click="$emit('select-tab', tab.id)"
                :class="[
                'whitespace-nowrap py-3 px-1 border-b-2 font-semibold text-sm transition-colors cursor-pointer flex items-center',
                chatStore.activeTab === tab.id
                    ? 'border-violet-600 text-violet-600'
                    : 'border-transparent text-zinc-500 hover:text-zinc-700 hover:border-zinc-300'
                ]"
                :aria-current="chatStore.activeTab === tab.id ? 'page' : undefined"
            >
                {{ tab.name }}
                <span 
                    v-if="tab.unread > 0"
                    :class="[
                        'ml-2 text-[10px] font-bold px-2 py-0.5 rounded-full',
                        tab.id === 'archived' 
                        ? 'bg-zinc-100 text-zinc-600' 
                        : tab.id === 'requests' 
                            ? 'bg-rose-100 text-rose-600' 
                            : 'bg-violet-100 text-violet-600'
                    ]"
                >
                    {{ tab.unread > 99 ? '99+' : tab.unread }}
                </span>
            </button>
        </nav>
    </div>
</template>

<script setup>
import { useChatStore } from '@/stores/chat';
const chatStore = useChatStore();
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
    display: none;
}
.no-scrollbar {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>