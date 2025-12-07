<template>
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
                :class="[newPostStore.receiveDonations ? 'bg-indigo-600' : 'bg-gray-200']"
                class="relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                role="switch"
                aria-checked="false"
                @click="newPostStore.toggleReceiveDonations()"
            >
                <span
                    :class="[newPostStore.receiveDonations ? 'translate-x-5' : 'translate-x-0']"
                    class="pointer-events-none relative inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200"
                >
                    <span
                        :class="[newPostStore.receiveDonations ? 'opacity-0 ease-out duration-100' : 'opacity-100 ease-in duration-200']"
                        class="absolute inset-0 h-full w-full flex items-center justify-center transition-opacity"
                        aria-hidden="true"
                    >
                        <X class="h-3 w-3 text-gray-400" />
                    </span>
                    <span
                        :class="[newPostStore.receiveDonations ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100']"
                        class="absolute inset-0 h-full w-full flex items-center justify-center transition-opacity"
                        aria-hidden="true"
                    >
                        <Check class="h-3 w-3 text-indigo-600" />
                    </span>
                </span>
            </button>
        </div>

        <!-- Payment Info Section (Conditional) -->
        <div v-if="newPostStore.receiveDonations" class="mt-4 space-y-4">
            <div class="flex items-center justify-between">
                <h5 class="text-sm font-medium text-gray-700">
                    Payment Methods
                </h5>
                <button
                    type="button"
                    @click="newPostStore.setIsPaymentModalOpen(true)"
                    class="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer"
                >
                    <Plus class="h-3 w-3 mr-1" />
                    Add Method
                </button>
            </div>
            
            <!-- Payment Methods List -->
            <div v-if="newPostStore.post.payment_info.length > 0" class="space-y-2">
                <div v-for="(payment, index) in newPostStore.post.payment_info" :key="index" class="flex items-center justify-between p-3 bg-gray-50 rounded-md border border-gray-200">
                    <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900 truncate">{{ payment.method }}</p>
                        <p class="text-xs text-gray-500 truncate">{{ payment.account }}</p>
                        <p v-if="payment.nameOnAccount" class="text-xs text-gray-500 truncate">{{ payment.nameOnAccount }}</p>
                    </div>
                    <button
                        type="button"
                        @click="newPostStore.removePaymentMethod(index)"
                        class="ml-2 text-red-600 hover:text-red-800 cursor-pointer"
                        title="Remove payment method"
                    >
                        <X class="h-4 w-4" />
                    </button>
                </div>
            </div>
            <p v-else class="text-sm text-gray-500 italic">No payment methods added. Click 'Add Method' to add one.</p>
        </div>
    </div>
</template>

<script setup>
import { Plus, X, Check } from 'lucide-vue-next';
import { useNewPostStore } from '@/stores/new_post';
const newPostStore = useNewPostStore();
</script>