<template>
  <div class="border-t border-gray-200 pt-4">
    <dl class="divide-y divide-gray-200">
      <div class="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
        <dt class="text-sm font-medium text-gray-500">Email address</dt>
        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ user?.email || 'Not provided' }}</dd>
      </div>
      <div v-if="user?.username" class="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
        <dt class="text-sm font-medium text-gray-500">Username</dt>
        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ user.username }}</dd>
      </div>
      <div class="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
        <dt class="text-sm font-medium text-gray-500">Account created</dt>
        <dd class="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">{{ user?.formatted_date_joined }}</dd>
      </div>
      <!-- Subscriptions Section -->
      <div class="py-4">
        <h3 class="text-sm font-medium text-gray-500 mb-3">Subscriptions</h3>
        <div v-if="subscriptions.length > 0" class="space-y-4">
          <div v-for="(sub, index) in subscriptions" :key="index" class="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
            <div class="flex justify-between items-start">
                <div>
                  <h4 class="font-medium text-gray-900">{{ sub.product_name }}</h4>
                  <p class="text-sm text-gray-500 mt-1">
                      {{ 
                        Intl.NumberFormat(
                          'en-US', 
                          { 
                            style: 'currency', 
                            currency: 'USD' 
                          }
                        ).format(sub.amount) 
                      }} per {{ formatInterval(sub) }}
                  </p>
                </div>
                <span v-if="sub.is_active" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Active
                </span>
                <span v-else class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                  Inactive
                </span>
            </div>
            <div class="mt-3 pt-3 border-t border-gray-100 text-sm text-gray-600">
                <p class="flex items-center">
                  <Calendar class="h-4 w-4 text-gray-400 mr-2" />
                  Renews on {{ sub.formatted_current_period_end }}
                </p>
                <p class="mt-1 flex items-center text-indigo-600">
                  <Clock class="h-4 w-4 text-indigo-400 mr-2" />
                  {{ sub.days_left }}
                </p>
            </div>
          </div>
        </div>
        <p v-else class="text-sm text-gray-500">No active subscriptions</p>
        </div>
    </dl>
  </div>             
</template>

<script setup>
import { computed } from 'vue';
import { useUserStore } from '@/stores/user';
import { Calendar, Clock } from 'lucide-vue-next';

const userStore = useUserStore();
const user = computed(() => userStore.user);

const subscriptions = computed(() => userStore.subscriptions || []);

const formatInterval = (subscription) => {
  if (!subscription) return '';
  const { recurring_interval, recurring_interval_count } = subscription;
  if (!recurring_interval || !recurring_interval_count) return '';
  
  const interval = recurring_interval_count > 1 
    ? `${recurring_interval}s` 
    : recurring_interval;
  
  return recurring_interval_count > 1 
    ? `${recurring_interval_count} ${interval}`
    : interval;
};
</script>
