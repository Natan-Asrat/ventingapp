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
        <div class="fixed inset-0 bg-zinc-900/60 backdrop-blur-sm transition-opacity" />
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
            <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white text-left align-middle shadow-2xl transition-all border border-zinc-100">
              <div class="px-6 py-4 border-b border-zinc-100 bg-zinc-50/50 flex justify-between items-center">
                <DialogTitle as="h3" class="text-lg font-bold leading-6 text-zinc-900 flex items-center gap-2">
                  <Headset class="h-5 w-5 text-violet-600" />
                  Support Contacts
                </DialogTitle>
                <button
                  @click="closeModal"
                  class="rounded-full p-1 text-zinc-400 hover:text-zinc-600 hover:bg-zinc-100 focus:outline-none transition-all cursor-pointer"
                >
                  <X class="h-5 w-5" />
                </button>
              </div>

              <div class="px-6 py-6">
                <div v-if="isLoading" class="flex flex-col items-center justify-center py-8">
                  <Loader2 class="animate-spin h-8 w-8 text-violet-600 mb-2" />
                  <span class="text-xs font-medium text-zinc-400">Loading contacts...</span>
                </div>

                <div v-else-if="error" class="bg-rose-50 border border-rose-100 rounded-xl p-4 text-center">
                  <p class="text-sm font-medium text-rose-600">{{ error }}</p>
                </div>

                <div v-else class="space-y-4">
                  <div v-if="supportContacts.length === 0" class="text-center py-8 bg-zinc-50 rounded-xl border border-dashed border-zinc-200">
                    <p class="text-zinc-500 text-sm font-medium">No support contacts available at the moment.</p>
                  </div>
                  <div v-else class="space-y-3">
                    <div v-for="contact in supportContacts" :key="contact.id" class="group bg-white border border-zinc-200 hover:border-violet-200 hover:shadow-sm rounded-xl p-4 transition-all duration-200">
                      <h4 class="font-bold text-zinc-900 mb-3 flex items-center">
                        <div class="w-1.5 h-1.5 rounded-full bg-violet-500 mr-2"></div>
                        {{ contact.name }}
                      </h4>
                      <div class="space-y-2 text-sm text-zinc-600">
                        <div v-if="contact.email" class="flex items-center">
                          <div class="w-8 h-8 rounded-full bg-zinc-50 flex items-center justify-center mr-3 text-zinc-400 group-hover:text-violet-600 group-hover:bg-violet-50 transition-colors">
                             <Mail class="h-4 w-4" />
                          </div>
                          <a :href="'mailto:' + contact.email" class="hover:text-violet-600 transition-colors font-medium break-all">{{ contact.email }}</a>
                        </div>
                        <div v-if="contact.phone" class="flex items-center">
                          <div class="w-8 h-8 rounded-full bg-zinc-50 flex items-center justify-center mr-3 text-zinc-400 group-hover:text-violet-600 group-hover:bg-violet-50 transition-colors">
                             <Phone class="h-4 w-4" />
                          </div>
                          <a :href="'tel:' + contact.phone" class="hover:text-violet-600 transition-colors font-medium">{{ contact.phone }}</a>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="px-6 py-4 bg-zinc-50 border-t border-zinc-100 flex justify-end">
                <button
                  type="button"
                  class="inline-flex justify-center rounded-full border border-zinc-300 bg-white px-5 py-2 text-sm font-semibold text-zinc-700 shadow-sm hover:bg-zinc-50 focus:outline-none focus:ring-2 focus:ring-zinc-500 focus:ring-offset-2 transition-all cursor-pointer"
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
import { X, Mail, Phone, Headset, Loader2 } from 'lucide-vue-next';
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
