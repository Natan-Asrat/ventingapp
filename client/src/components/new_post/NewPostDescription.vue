<template>
    <!-- Description Field -->
    <div>
        <div class="flex items-center justify-between mb-2">
            <label for="description" class="block text-sm font-bold text-zinc-700">
                Description <span class="text-rose-500">*</span>
            </label>
        </div>
        <div class="relative">
            <textarea
                id="description"
                name="description"
                rows="6"
                :value="newPostStore.post.description"
                required
                maxlength="63206"
                @invalid="e => e.target.setCustomValidity('This field is required')"
                @input="e => {e.target.setCustomValidity(''); newPostStore.setPostDescription(e.target.value)}"
                class="block w-full rounded-xl border-zinc-200 bg-zinc-50 shadow-sm focus:border-violet-500 focus:ring-violet-500/20 sm:text-sm p-4 placeholder-zinc-400 transition-all resize-y"
                placeholder="Tell us everything..."
            ></textarea>
        </div>
    </div>
</template>

<script setup>
import { useNewPostStore } from '@/stores/new_post';
const newPostStore = useNewPostStore();
</script>