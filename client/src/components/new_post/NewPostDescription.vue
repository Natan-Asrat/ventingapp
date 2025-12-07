<template>
    <!-- Description Field -->
    <div>
        <div class="flex items-center justify-between">
            <label for="description" class="block text-sm font-medium text-gray-700 mb-1">
                What happened? <span class="text-red-500">*</span>
            </label>
            <span class="text-xs text-gray-500">Required</span>
        </div>
        <div class="mt-1">
            <textarea
                id="description"
                name="description"
                rows="4"
                :value="newPostStore.post.description"
                required
                @invalid="e => e.target.setCustomValidity('This field is required')"
                @input="e => {e.target.setCustomValidity(''); newPostStore.setPostDescription(e.target.value)}"
                class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-3 border placeholder-gray-400"
                placeholder="Tell us everything..."
            ></textarea>
        </div>
    </div>
</template>

<script setup>
import { useNewPostStore } from '@/stores/new_post';
const newPostStore = useNewPostStore();
</script>