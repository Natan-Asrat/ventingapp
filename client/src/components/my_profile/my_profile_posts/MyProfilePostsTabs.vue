<template>
    <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8 px-4" aria-label="Tabs">
            <button
                v-for="tab in myProfileStore.tabs"
                :key="tab.name"
                @click="myProfileStore.activeTab = tab.name"
                :class="[
                    myProfileStore.activeTab === tab.name
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 cursor-pointer',
                    'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2'
                ]"
                :aria-current="myProfileStore.activeTab === tab.name ? 'page' : undefined"
            >
                <component :is="tab.icon" class="h-4 w-4" />
                    {{ tab.name }}
                <span 
                    v-if="tab.count !== undefined"
                    :class="[
                    myProfileStore.activeTab === tab.name ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-900',
                    'ml-2 py-0.5 px-2 rounded-full text-xs font-medium'
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
