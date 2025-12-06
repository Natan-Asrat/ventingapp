<template>
    <div class="flex items-start space-x-4">
        <div class="flex-shrink-0 relative group">
            <div v-if="user?.profile_picture" class="h-24 w-24 rounded-full overflow-hidden bg-gray-200">
                <img :src="user.profile_picture" :alt="user.name" class="h-full w-full object-cover">
            </div>
            <div v-else class="h-24 w-24 rounded-full bg-indigo-100 flex items-center justify-center">
                <span class="text-3xl font-medium text-indigo-600">{{ userInitials }}</span>
            </div>
            <button
                @click="triggerFileInput"
                class="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-white px-3 py-1 rounded-full text-xs font-medium text-indigo-600 shadow-sm border border-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer"
            >
                Change
            </button>
            <input
                ref="fileInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleProfilePictureChange"
            />
        </div>
        <div class="flex-1">
            <div v-if="!isEditingName" class="flex items-center">
                <h2 class="text-2xl font-semibold text-gray-900">{{ user?.name || 'User' }}</h2>
                <button
                    @click="startEditingName"
                    class="ml-2 p-1 cursor-pointer rounded-full text-gray-400 hover:text-indigo-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                    <PencilIcon class="h-4 w-4" />
                </button>
            </div>
            <div v-else class="flex items-center space-x-2">
                <input
                    v-model="editingName"
                    type="text"
                    class="py-2 px-3 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                    @keyup.enter="saveName"
                >
                <button
                    @click="saveName"
                    :disabled="isSaving"
                    :class="{'cursor-pointer': !isSaving}"
                    class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                    <span v-if="isSaving" class="flex items-center">
                        <Loader2 class="animate-spin -ml-1 mr-2 h-3 w-3 text-white" />
                        Saving...
                    </span>
                    <span v-else>Save</span>
                </button>
                <button
                    @click="cancelEditingName"
                    class="p-1 text-gray-400 hover:text-gray-500 focus:outline-none"
                    :disabled="isSaving"
                >
                    <X class="h-4 w-4 cursor-pointer" />
                </button>
            </div>
            <p class="mt-1 text-sm text-gray-500">Member since {{ user?.formatted_date_joined }}</p>
        </div>
    </div>         
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useUserStore } from '@/stores/user';
import { Loader2, PencilIcon, X } from 'lucide-vue-next';
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
