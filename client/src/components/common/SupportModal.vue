<template>
  <TransitionRoot appear :show="isOpen" as="template">
    <Dialog as="div" class="relative z-50" @close="closeModal">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/25" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
              <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900 flex justify-between items-center">
                <span>Support Contacts</span>
                <button
                  @click="closeModal"
                  class="text-gray-400 cursor-pointer hover:text-gray-500"
                >
                  <X class="h-5 w-5" />
                </button>
              </DialogTitle>

              <div v-if="isLoading" class="flex justify-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
              </div>

              <div v-else-if="error" class="mt-4 text-red-600 text-sm">
                {{ error }}
              </div>

              <div v-else class="mt-4 space-y-4">
                <div v-if="supportContacts.length === 0" class="text-gray-500 text-center py-4">
                  No support contacts available at the moment.
                </div>
                <div v-else>
                  <div v-for="contact in supportContacts" :key="contact.id" class="border border-gray-200 rounded-lg p-4">
                    <h4 class="font-medium text-gray-900">{{ contact.name }}</h4>
                    <div class="mt-2 space-y-1 text-sm text-gray-600">
                      <div v-if="contact.email" class="flex items-center">
                        <Mail class="h-4 w-4 mr-2 text-gray-400 flex-shrink-0" />
                        <a :href="'mailto:' + contact.email" class="hover:text-indigo-600 break-all">{{ contact.email }}</a>
                      </div>
                      <div v-if="contact.phone" class="flex items-center">
                        <Phone class="h-4 w-4 mr-2 text-gray-400 flex-shrink-0" />
                        <a :href="'tel:' + contact.phone" class="hover:text-indigo-600">{{ contact.phone }}</a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-6 flex justify-end">
                <button
                  type="button"
                  class="inline-flex cursor-pointer justify-center rounded-md border border-transparent bg-indigo-100 px-4 py-2 text-sm font-medium text-indigo-900 hover:bg-indigo-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2"
                  @click="closeModal"
                >
                  Close
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { X, Mail, Phone } from 'lucide-vue-next';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { useSupportStore } from '@/stores/support';
const supportStore = useSupportStore();
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
});

const emit = defineEmits(['close']);

const supportContacts = ref([]);
const isLoading = ref(false);
const error = ref(null);

const closeModal = () => {
  emit('close');
};

const fetchSupportContacts = async () => {
  if (!props.isOpen) return;
  
  isLoading.value = true;
  error.value = null;
  
  try {
    const response = await supportStore.fetchContacts();
    supportContacts.value = response.data;
  } catch (err) {
    console.error('Error fetching support contacts:', err);
    error.value = 'Failed to load support contacts. Please try again later.';
    
    // Fallback to default contacts if API fails
    supportContacts.value = [
      {
        id: 1,
        name: 'Admin 1',
        email: 'adminemail@gmail.com',
        phone: '1234455666',
      },
      {
        id: 2,
        name: 'Support',
        email: 'supportemail1@gmail.com',
        phone: '1001001001',
      }
    ];
  } finally {
    isLoading.value = false;
  }
};

// Fetch contacts when modal is opened
onMounted(() => {
  if (props.isOpen) {
    fetchSupportContacts();
  }
});

</script>
