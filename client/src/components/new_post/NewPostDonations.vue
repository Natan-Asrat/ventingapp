<template>
    <div class="pt-6 border-t border-zinc-100">
        <div class="flex items-center justify-between">
            <div class="flex items-start space-x-3">
                 <div class="p-2 bg-amber-50 rounded-lg">
                    <Wallet class="h-5 w-5 text-amber-500" />
                 </div>
                <div>
                    <h4 class="text-sm font-bold text-zinc-900">
                        Accept Donations
                    </h4>
                    <p class="text-xs text-zinc-500 mt-0.5">Let others support your story</p>
                </div>
            </div>
            <button
                type="button"
                :class="[newPostStore.receiveDonations ? 'bg-violet-600' : 'bg-zinc-200']"
                class="relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500"
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
                        <X class="h-3 w-3 text-zinc-400" />
                    </span>
                    <span
                        :class="[newPostStore.receiveDonations ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100']"
                        class="absolute inset-0 h-full w-full flex items-center justify-center transition-opacity"
                        aria-hidden="true"
                    >
                        <Check class="h-3 w-3 text-violet-600" />
                    </span>
                </span>
            </button>
        </div>

        <!-- Payment Info Section (Conditional) -->
        <transition
             enter-active-class="transition ease-out duration-200"
             enter-from-class="transform opacity-0 -translate-y-2"
             enter-to-class="transform opacity-100 translate-y-0"
             leave-active-class="transition ease-in duration-150"
             leave-from-class="transform opacity-100 translate-y-0"
             leave-to-class="transform opacity-0 -translate-y-2"
        >
            <div v-if="newPostStore.receiveDonations" class="mt-6 space-y-4 bg-zinc-50/50 rounded-xl p-4 border border-zinc-100">
                <div class="flex items-center justify-between">
                    <h5 class="text-xs font-bold text-zinc-500 uppercase tracking-wide">
                        Payment Methods
                    </h5>
                    <button
                        type="button"
                        @click="newPostStore.setIsPaymentModalOpen(true)"
                        class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-semibold rounded-full text-violet-700 bg-violet-100 hover:bg-violet-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 cursor-pointer transition-colors"
                    >
                        <Plus class="h-3 w-3 mr-1" />
                        Add Method
                    </button>
                </div>
                
                <!-- Payment Methods List -->
                <div v-if="newPostStore.post.payment_info.length > 0" class="space-y-3">
                    <div v-for="(payment, index) in newPostStore.post.payment_info" :key="index" class="flex items-center justify-between p-3 bg-white rounded-xl border border-zinc-200 hover:border-violet-200 transition-colors shadow-sm">
                        <div class="flex-1 min-w-0">
                            <div class="flex items-center">
                                <p class="text-sm font-bold text-zinc-900 truncate">{{ payment.method }}</p>
                            </div>
                            <div class="mt-0.5">
                                <p class="text-xs text-zinc-500 font-mono bg-zinc-50 inline-block px-1.5 py-0.5 rounded border border-zinc-100">{{ payment.account }}</p>
                            </div>
                            <p v-if="payment.nameOnAccount" class="text-xs text-zinc-400 truncate mt-0.5">{{ payment.nameOnAccount }}</p>
                        </div>
                        <button
                            type="button"
                            @click="newPostStore.removePaymentMethod(index)"
                            class="ml-3 p-1.5 rounded-full text-zinc-400 hover:text-rose-600 hover:bg-rose-50 cursor-pointer transition-colors"
                            title="Remove payment method"
                        >
                            <X class="h-4 w-4" />
                        </button>
                    </div>
                </div>
                <div v-else class="text-center py-6 border-2 border-dashed border-zinc-200 rounded-xl">
                    <p class="text-sm text-zinc-500 font-medium">No payment methods added yet.</p>
                </div>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { Plus, X, Check, Wallet } from 'lucide-vue-next';
import { useNewPostStore } from '@/stores/new_post';
const newPostStore = useNewPostStore();
</script>