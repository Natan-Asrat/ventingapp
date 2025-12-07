<template>
    <!-- Tabs -->
    <div class="border-b border-gray-200 mb-6">
        <nav class="-mb-px flex space-x-8 overflow-x-auto" aria-label="Tabs">
            <button
                v-for="(tab, index) in chatStore.tabs"
                :key="tab.id"
                @click="$emit('select-tab', tab.id)"
                :class="[
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm',
                chatStore.activeTab === tab.id
                    ? 'border-indigo-500 text-indigo-600'
                    : 'cursor-pointer border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                ]"
                :aria-current="chatStore.activeTab === tab.id ? 'page' : undefined"
            >
                {{ tab.name }}
                <span 
                    v-if="tab.unread > 0"
                    :class="[
                        'ml-2 text-xs font-medium px-2 py-0.5 rounded-full',
                        tab.id === 'archived' 
                        ? 'bg-gray-100 text-gray-600' 
                        : tab.id === 'requests' 
                            ? 'bg-red-100 text-red-600' 
                            : 'bg-indigo-100 text-indigo-600'
                    ]"
                >
                    {{ tab.unread }}
                </span>
            </button>
        </nav>
    </div>
</template>

<script setup>
import { useChatStore } from '@/stores/chat';
const chatStore = useChatStore();
</script>