<template>
    <!-- Image Upload -->
    <div>
        <div class="flex items-center justify-between mb-2">
            <label class="block text-sm font-bold text-zinc-700">
                Image
            </label>
            <span class="text-xs font-medium text-zinc-400 bg-zinc-100 px-2 py-0.5 rounded-full">Optional</span>
        </div>
        <div 
            @click="boxClicked" 
            :class="[
              'mt-1 flex justify-center px-6 pt-10 pb-10 border-2 border-dashed rounded-xl transition-all duration-300',
              !newPostStore.imagePreview 
                ? 'border-zinc-300 hover:border-violet-400 hover:bg-violet-50/30 cursor-pointer group' 
                : 'border-zinc-200 bg-zinc-50'
            ]"
        >
            <div class="space-y-2 text-center">
                <template v-if="!newPostStore.imagePreview">
                    <div class="flex flex-col items-center">
                        <div class="h-12 w-12 bg-zinc-100 rounded-full flex items-center justify-center mb-3 group-hover:bg-violet-100 transition-colors">
                            <Image class="h-6 w-6 text-zinc-400 group-hover:text-violet-600 transition-colors" />
                        </div>
                        <div class="flex text-sm text-zinc-600">
                            <label
                            for="file-upload"
                            class="relative cursor-pointer rounded-md font-semibold text-violet-600 hover:text-violet-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-violet-500"
                            >
                            <span>Upload a file</span>
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
                        <p class="text-xs text-zinc-500">PNG, JPG, GIF up to 10MB</p>
                    </div>
                </template>
                <template v-else>
                    <div class="relative group/preview inline-block">
                        <img :src="newPostStore.imagePreview" class="max-h-80 mx-auto rounded-lg shadow-sm" alt="Preview" />
                        <div class="absolute inset-0 bg-black/0 group-hover/preview:bg-black/10 transition-colors rounded-lg flex items-center justify-center">
                             <button
                                type="button"
                                @click.stop="removeImage"
                                class="bg-white text-rose-500 rounded-full p-2 shadow-lg hover:bg-rose-50 transform scale-0 group-hover/preview:scale-100 transition-all duration-200 cursor-pointer"
                                title="Remove image"
                            >
                                <X class="h-5 w-5" />
                            </button>
                        </div>
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