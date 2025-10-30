<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Desktop Navigation -->
    <desktop-top-nav 
      :user-initials="userInitials"
      @logout="handleLogout"
    />
    
    <!-- Mobile Top Navigation -->
    <mobile-top-nav 
      :user-initials="userInitials"
      :user-name="userName"
      @logout="handleLogout"
    />
    
    <!-- Main Content -->
    <div class="pt-16 pb-16 md:pt-0 md:pb-0">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="bg-white shadow sm:rounded-lg overflow-hidden">
          <div class="px-4 py-5 sm:px-6 border-b border-gray-200 flex items-center">
            <MessageSquare class="h-5 w-5 text-indigo-600 mr-2" />
            <div>
              <h3 class="text-lg leading-6 font-medium text-gray-900">Are you sad?</h3>
            </div>
          </div>
          
          <form @submit.prevent="submitPost" class="px-4 py-5 sm:p-6">
            <div class="space-y-6">
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
                    v-model="post.description"
                    required
                    @invalid="e => e.target.setCustomValidity('This field is required')"
                    @input="e => e.target.setCustomValidity('')"
                    class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-3 border placeholder-gray-400"
                    placeholder="Tell us everything..."
                  ></textarea>
                </div>
              </div>
              
              <!-- Image Upload -->
              <div>
                <div class="flex items-center justify-between">
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Did you capture it?
                  </label>
                  <span class="text-xs text-gray-500">Optional</span>
                </div>
                <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                  <div class="space-y-1 text-center">
                    <template v-if="!imagePreview">
                      <div @click="boxClicked">
                        <svg
                          class="mx-auto h-12 w-12 text-gray-400"
                          stroke="currentColor"
                          fill="none"
                          viewBox="0 0 48 48"
                          aria-hidden="true"
                        >
                          <path
                            d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          />
                        </svg>
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
                              @change="handleImageUpload"
                            />
                          </label>
                          <p class="pl-1">or drag and drop</p>
                        </div>
                        <p class="text-xs text-gray-500">PNG, JPG, GIF up to 10MB</p>
                      </div>
                    </template>
                    <template v-else>
                      <div class="relative">
                        <img :src="imagePreview" class="max-h-64 mx-auto rounded-md" alt="Preview" />
                        <button
                          type="button"
                          @click="removeImage"
                          class="absolute -top-3 -right-3 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                        >
                          <X class="h-4 w-4" />
                        </button>
                      </div>
                    </template>
                  </div>
                </div>
              </div>
              
              <!-- Donations Toggle -->
              <div class="pt-4 border-t border-gray-200">
                <div class="flex items-center justify-between">
                  <div>
                    <h4 class="text-sm font-medium text-gray-700">
                      Receive Donations
                    </h4>
                    <p class="text-xs text-gray-500">Allow people to support you with payments</p>
                  </div>
                  <button
                    type="button"
                    :class="[receiveDonations ? 'bg-indigo-600' : 'bg-gray-200']"
                    class="relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    role="switch"
                    aria-checked="false"
                    @click="receiveDonations = !receiveDonations"
                  >
                    <span
                      :class="[receiveDonations ? 'translate-x-5' : 'translate-x-0']"
                      class="pointer-events-none relative inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200"
                    >
                      <span
                        :class="[receiveDonations ? 'opacity-0 ease-out duration-100' : 'opacity-100 ease-in duration-200']"
                        class="absolute inset-0 h-full w-full flex items-center justify-center transition-opacity"
                        aria-hidden="true"
                      >
                        <X class="h-3 w-3 text-gray-400" />
                      </span>
                      <span
                        :class="[receiveDonations ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100']"
                        class="absolute inset-0 h-full w-full flex items-center justify-center transition-opacity"
                        aria-hidden="true"
                      >
                        <Check class="h-3 w-3 text-indigo-600" />
                      </span>
                    </span>
                  </button>
                </div>

                <!-- Payment Info Section (Conditional) -->
                <div v-if="receiveDonations" class="mt-4 space-y-4">
                  <div class="flex items-center justify-between">
                    <h5 class="text-sm font-medium text-gray-700">
                      Payment Methods
                    </h5>
                    <button
                      type="button"
                      @click="isPaymentModalOpen = true"
                      class="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      <Plus class="h-3 w-3 mr-1" />
                      Add Method
                    </button>
                  </div>
                  
                  <!-- Payment Methods List -->
                  <div v-if="post.payment_info.length > 0" class="space-y-2">
                    <div v-for="(payment, index) in post.payment_info" :key="index" class="flex items-center justify-between p-3 bg-gray-50 rounded-md border border-gray-200">
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900 truncate">{{ payment.method }}</p>
                        <p class="text-xs text-gray-500 truncate">{{ payment.account }}</p>
                        <p v-if="payment.nameOnAccount" class="text-xs text-gray-500 truncate">{{ payment.nameOnAccount }}</p>
                      </div>
                      <button
                        type="button"
                        @click="removePaymentMethod(index)"
                        class="ml-2 text-red-600 hover:text-red-800"
                        title="Remove payment method"
                      >
                        <X class="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                  <p v-else class="text-sm text-gray-500 italic">No payment methods added. Click 'Add Method' to add one.</p>
                </div>
              </div>

              <div class="flex justify-end pt-4">
                <button
                  type="submit"
                  class="w-full md:w-auto inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  :class="{'cursor-pointer': !isLoading, 'cursor-not-allowed': isLoading}"
                  :disabled="isLoading"
                >
                  <Send v-if="!isLoading" class="-ml-1 mr-2 h-4 w-4" />
                  <span v-else class="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></span>
                  {{ isLoading ? 'Posting...' : 'Post' }}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- Mobile Bottom Navigation -->
    <mobile-bottom-nav :user-initials="userInitials" />
    
    <!-- Payment Method Modal -->
    <PaymentMethodModal 
      :isOpen="isPaymentModalOpen"
      :initialData="newPaymentInfo"
      @close="isPaymentModalOpen = false"
      @save="addPaymentMethod"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api/axios';
import { MessageSquare, Send, Plus, X, CreditCard, User, Check } from 'lucide-vue-next';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import PaymentMethodModal from '@/components/PaymentMethodModal.vue';

const router = useRouter();

// Reactive state
const post = ref({
  description: '',
  image: null,
  payment_info: []
});
const isLoading = ref(false);

const receiveDonations = ref(false);
const imagePreview = ref(null);
const isPaymentModalOpen = ref(false);
const fileInput = ref(null);

// User data - would typically come from auth store
const userInitials = ref('ME');
const userName = ref('User');

const newPaymentInfo = ref({
  method: '',
  account: '',
  nameOnAccount: ''
});

// Methods
const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  // Check file size (10MB max)
  if (file.size > 10 * 1024 * 1024) {
    alert('Image size should be less than 10MB');
    return;
  }
  
  // Check file type
  if (!file.type.match('image.*')) {
    alert('Please select an image file (JPEG, PNG, GIF)');
    return;
  }
  
  // Create preview
  const reader = new FileReader();
  reader.onload = (e) => {
    imagePreview.value = e.target.result;
  };
  reader.readAsDataURL(file);
  
  // Store the file
  post.value.image = file;
};

const removeImage = () => {
  imagePreview.value = null;
  post.value.image = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

const submitPost = async () => {
  if (isLoading.value) return;
  
  try {
    isLoading.value = true;
    if(post.value.image != null){
      const formData = new FormData();
      formData.append('description', post.value.description);
      
      if (post.value.image) {
        formData.append('image', post.value.image);
      }
      console.log("form data", formData)
      
      const response = await api.post('/post/posts/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Assuming you're using token-based auth
        },
      });
      if (receiveDonations.value && post.value.payment_info?.length > 0) {
        const payment_added_response = await api.post(`/post/posts/${response.data.id}/bulk_add_payment_info/`, post.value.payment_info, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        console.log('Payment info added: ', payment_added_response.data)

      } else {
        console.log('Post created:', response.data);

      }
    
      router.push('/home'); // Redirect to feed after successful post
    } else {
      const response = await api.post('/post/posts/', post.value, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      console.log('Post created:', response.data);
      router.push('/home'); // Redirect to feed after successful post
    }
  } catch (error) {
    console.error('Error creating post:', error);
    // You might want to show an error message to the user here
    if (error.response) {
      console.error('Error response:', error.response.data);
    }
  } finally {
    isLoading.value = false;
  }
};

const addPaymentMethod = (paymentData) => {
  if (paymentData.method && paymentData.account) {
    post.value.payment_info.push({ ...paymentData });
    resetPaymentForm();
  }
};

const removePaymentMethod = (index) => {
  post.value.payment_info.splice(index, 1);
};

const resetPaymentForm = () => {
  newPaymentInfo.value = {
    method: '',
    account: '',
    nameOnAccount: ''
  };
};

const handleLogout = () => {
  // TODO: Implement logout logic
  console.log('Logout');
  router.push('/login');
};

const boxClicked = () => {
  if (fileInput.value) {
    fileInput.value.click();
  }
};
</script>