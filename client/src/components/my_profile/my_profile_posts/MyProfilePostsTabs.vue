<template>
    <div class="border-b border-zinc-100 bg-white sticky top-0 z-10">
        <nav class="-mb-px flex px-6 space-x-8" aria-label="Tabs">
            <button
                v-for="tab in myProfileStore.tabs"
                :key="tab.name"
                @click="myProfileStore.activeTab = tab.name"
                :class="[
                    myProfileStore.activeTab === tab.name
                    ? 'border-violet-600 text-violet-600'
                    : 'border-transparent text-zinc-500 hover:text-zinc-700 hover:border-zinc-300',
                    'whitespace-nowrap py-4 border-b-2 font-semibold text-sm flex items-center gap-2.5 transition-colors cursor-pointer'
                ]"
                :aria-current="myProfileStore.activeTab === tab.name ? 'page' : undefined"
            >
                <component 
                    :is="tab.icon" 
                    class="h-4 w-4" 
                    :class="myProfileStore.activeTab === tab.name ? 'stroke-[2.5]' : ''"
                />
                    {{ tab.name }}
                <span 
                    v-if="tab.count !== undefined"
                    :class="[
                    myProfileStore.activeTab === tab.name ? 'bg-violet-100 text-violet-700' : 'bg-zinc-100 text-zinc-600',
                    'ml-1.5 py-0.5 px-2.5 rounded-full text-xs font-bold transition-colors'
                    ]"
                >
                    {{ tab.count }}
                </span>
            </button>
        </nav>
    </div>
</template>

<script setup>
import { useMyProfileStore } from '@/stores/my_profile';
const myProfileStore = useMyProfileStore(); 
</script>
