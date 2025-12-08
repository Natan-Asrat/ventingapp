<template>
    <!-- Tabs -->
    <div class="border-b border-zinc-100 bg-white sticky top-0 z-10">
        <nav class="flex -mb-px" aria-label="Tabs">
            <button
                v-for="tab in historyStore.tabs"
                :key="tab.name"
                @click="historyStore.activeTab = tab.id"
                :class="[
                    historyStore.activeTab === tab.id
                    ? 'border-violet-600 text-violet-600 bg-violet-50/10'
                    : 'cursor-pointer border-transparent text-zinc-500 hover:text-zinc-700 hover:border-zinc-300 hover:bg-zinc-50',
                    'w-1/3 py-4 px-1 text-center border-b-2 font-semibold text-sm transition-all duration-200'
                ]"
            >
                <div class="flex flex-col items-center justify-center h-full">
                    <div class="flex items-center gap-2">
                        <span>{{ tab.name }}</span>
                        <span 
                            v-if="tab.count > 0"
                            :class="[
                            historyStore.activeTab === tab.id ? 'bg-violet-100 text-violet-700' : 'bg-zinc-100 text-zinc-600',
                            'py-0.5 px-2.5 rounded-full text-xs font-bold hidden md:inline-block transition-colors'
                            ]"
                        >
                            {{ tab.count }}
                        </span>
                    </div>
                    <span 
                        v-if="tab.count > 0"
                        :class="[
                            historyStore.activeTab === tab.id ? 'bg-violet-100 text-violet-700' : 'bg-zinc-100 text-zinc-600',
                            'mt-1.5 py-0.5 px-2 rounded-full text-[10px] font-bold md:hidden transition-colors'
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