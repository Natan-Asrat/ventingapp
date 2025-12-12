<template>
    <div class="flex flex-col items-center text-center space-y-4">
        <div class="relative group">
            <div v-if="user?.profile_picture" class="h-28 w-28 rounded-full overflow-hidden ring-4 ring-white shadow-lg bg-zinc-100">
                <img :src="user.profile_picture" :alt="user.name" class="h-full w-full object-cover">
            </div>
            <div v-else class="h-28 w-28 rounded-full bg-violet-100 flex items-center justify-center ring-4 ring-white shadow-lg">
                <span class="text-3xl font-bold text-violet-600">{{ userInitials }}</span>
            </div>
            <button
                @click="triggerFileInput"
                class="absolute bottom-1 right-1 bg-zinc-900 text-white p-2 rounded-full shadow-md hover:bg-violet-600 transition-all cursor-pointer transform hover:scale-105 border-2 border-white"
                title="Change Profile Picture"
            >
                <Camera class="h-4 w-4" />
            </button>
            <input
                ref="fileInput"
                type="file"
                accept="image/png, image/jpeg"
                class="hidden"
                @change="handleProfilePictureChange"
            />
        </div>
        
        <div class="w-full">
            <div v-if="!isEditingName" class="flex items-center justify-center gap-2 group/name min-h-[40px]">
                <h2 class="text-2xl font-bold text-zinc-900 tracking-tight">{{ user?.name || 'User' }}</h2>
                <button
                    @click="startEditingName"
                    class="p-1.5 rounded-full text-zinc-400 opacity-0 group-hover/name:opacity-100 hover:text-violet-600 hover:bg-violet-50 transition-all cursor-pointer"
                >
                    <PencilIcon class="h-4 w-4" />
                </button>
            </div>
            <div v-else class="flex items-center justify-center space-x-2 w-full max-w-[240px] mx-auto min-h-[40px]">
                <input
                    v-model="editingName"
                    type="text"
                    class="py-1.5 px-3 block w-full rounded-lg border-zinc-300 bg-zinc-50 text-center font-semibold text-zinc-900 shadow-sm focus:border-violet-500 focus:ring-violet-500 sm:text-sm"
                    @keyup.enter="saveName"
                >
                <button
                    @click="saveName"
                    :disabled="isSaving"
                    class="p-2 rounded-full bg-violet-100 text-violet-700 hover:bg-violet-200 cursor-pointer disabled:opacity-50 transition-colors flex-shrink-0"
                >
                    <Check class="h-4 w-4" v-if="!isSaving"/>
                    <Loader2 v-else class="h-4 w-4 animate-spin"/>
                </button>
                <button
                    @click="cancelEditingName"
                    class="p-2 rounded-full text-zinc-400 hover:text-zinc-600 hover:bg-zinc-100 cursor-pointer flex-shrink-0 transition-colors"
                    :disabled="isSaving"
                >
                    <X class="h-4 w-4" />
                </button>
            </div>
            <p class="mt-1 text-sm font-medium text-zinc-500">Member since {{ user?.formatted_date_joined }}</p>
        </div>
    </div>         
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useUserStore } from '@/stores/user';
import { Loader2, PencilIcon, X, Camera, Check } from 'lucide-vue-next';
import { message } from 'ant-design-vue';
import { useMyProfileStore } from '@/stores/my_profile';
const userStore = useUserStore();
const myProfileStore = useMyProfileStore();
const fileInput = ref(null);

// State
const isEditingName = ref(false);
const editingName = ref('');
const isSaving = ref(false);

// Get user data from the store
const user = computed(() => userStore.user);

// Initialize editing name when user data is available
watch(() => user.value?.name, (newName) => {
  if (newName) {
    editingName.value = newName;
  }
}, { immediate: true });

// Methods
const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleProfilePictureChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // Store the current profile picture URL to revert if the update fails
  const previousProfilePicture = user.value?.profile_picture;
  
  // Optimistically update the UI
  const tempProfilePicture = URL.createObjectURL(file);
  userStore.user = { ...user.value, profile_picture: tempProfilePicture };


  try {
    isSaving.value = true;
    const response = await myProfileStore.updateProfilePicture(file);
    // Update with server response data
    userStore.user = { ...user.value, ...response.data };
    message.success('Profile picture updated successfully!');
  } catch (error) {
    console.error('Error updating profile picture:', error);
    // Revert to previous profile picture on error
    userStore.user = { ...user.value, profile_picture: previousProfilePicture };
    message.error('Failed to update profile picture. Please try again.');
  } finally {
    isSaving.value = false;
    // Clean up the object URL to prevent memory leaks
    if (tempProfilePicture) {
      URL.revokeObjectURL(tempProfilePicture);
    }
    // Reset file input
    if (fileInput.value) {
      fileInput.value.value = '';
    }
  }
};
const startEditingName = () => {
  editingName.value = user.value?.name || '';
  isEditingName.value = true;
};

const cancelEditingName = () => {
  isEditingName.value = false;
  editingName.value = user.value?.name || '';
};

const saveName = async () => {
  if (!editingName.value.trim() || editingName.value === user.value?.name) {
    isEditingName.value = false;
    return;
  }

  try {
    isSaving.value = true;
    console.log("editing name",editingName.value )
    const response = await myProfileStore.updateName(editingName.value.trim());
    console.log("name response", response)
    userStore.user = { ...user.value, ...response.data };
    isEditingName.value = false;
    
    message.success('Name updated successfully!');

  } catch (error) {
    console.error('Error updating name:', error);
    message.error('Failed to update name. Please try again.');
  } finally {
    isSaving.value = false;
  }
};

// Format user initials for avatar
const userInitials = computed(() => {
  if (!user.value?.name) return 'U';
  return user.value.name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .substring(0, 2);
});

</script>
