<template>
    <!-- Tabs -->
    <div class="border-b border-gray-200">
        <nav class="flex -mb-px" aria-label="Tabs">
            <button
                v-for="tab in historyStore.tabs"
                :key="tab.name"
                @click="historyStore.activeTab = tab.id"
                :class="[
                    historyStore.activeTab === tab.id
                    ? 'border-indigo-500 text-indigo-600'
                    : 'cursor-pointer border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                    'w-1/3 py-4 px-1 text-center border-b-2 font-medium text-sm'
                ]"
            >
                <div class="flex flex-col items-center">
                    <div class="flex items-center">
                        <span>{{ tab.name }}</span>
                        <span 
                            v-if="tab.count > 0"
                            :class="[
                            historyStore.activeTab === tab.id ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-600',
                            'ml-2 py-0.5 px-2 rounded-full text-xs font-medium hidden md:block'
                            ]"
                        >
                            {{ tab.count }}
                        </span>
                    </div>
                    <span 
                        v-if="tab.count > 0"
                        :class="[
                            historyStore.activeTab === tab.id ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-600',
                            'mt-1 py-0.5 px-2 rounded-full text-xs font-medium md:hidden'
                        ]"
                    >
                        {{ tab.count }}
                    </span>
                </div>
            </button>
        </nav>
    </div>
</template>

<script setup>
import { useHistoryStore } from '@/stores/history';
const historyStore = useHistoryStore();
</script>