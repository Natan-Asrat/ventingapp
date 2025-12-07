<template>
    <!-- Image Upload -->
    <div>
        <div class="flex items-center justify-between">
            <label class="block text-sm font-medium text-gray-700 mb-1">
                Did you capture it?
            </label>
            <span class="text-xs text-gray-500">Optional</span>
        </div>
        <div 
            @click="boxClicked" 
            :class="{'cursor-pointer': !newPostStore.imagePreview}"
            class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md"
        >
            <div class="space-y-1 text-center">
                <template v-if="!newPostStore.imagePreview">
                    <div>
                    <Image class="mx-auto h-12 w-12 text-gray-400" />
                    <div class="flex text-sm text-gray-600">
                        <label
                        for="file-upload"
                        class="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500"
                        >
                        <span>Upload Image</span>
                        <input
                            ref="fileInput"
                            id="file-upload"
                            name="file-upload"
                            type="file"
                            class="sr-only"
                            accept="image/*"
                            @change="newPostStore.handleImageUpload"
                        />
                        </label>
                        <p class="pl-1">or drag and drop</p>
                    </div>
                    <p class="text-xs text-gray-500">PNG, JPG, GIF up to 10MB</p>
                    </div>
                </template>
                <template v-else>
                    <div class="relative">
                    <img :src="newPostStore.imagePreview" class="max-h-64 mx-auto rounded-md" alt="Preview" />
                    <button
                        type="button"
                        @click.stop="removeImage"
                        class="absolute -top-3 -right-3 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 cursor-pointer"
                    >
                        <X class="h-4 w-4" />
                    </button>
                    </div>
                </template>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { X, Image } from 'lucide-vue-next';
import { useNewPostStore } from '@/stores/new_post';
const newPostStore = useNewPostStore();

const fileInput = ref(null);

const boxClicked = () => {
  if (newPostStore.imagePreview) return;
  if (fileInput.value) {
    fileInput.value.click();
  }
};
const removeImage = () => {
    newPostStore.setImagePreview(null);
    newPostStore.setPostImage(null);
    if (fileInput.value) {
        fileInput.value.value = '';
    }
};
</script>