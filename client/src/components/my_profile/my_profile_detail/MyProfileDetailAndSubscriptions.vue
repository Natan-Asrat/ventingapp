<template>
  <div class="pt-2">
    <dl class="space-y-4">
      <div class="flex justify-between py-2 border-b border-zinc-50">
        <dt class="text-sm font-medium text-zinc-500">Email</dt>
        <dd class="text-sm font-semibold text-zinc-900 text-right">{{ user?.email || 'Not provided' }}</dd>
      </div>
      <div v-if="user?.username" class="flex justify-between py-2 border-b border-zinc-50">
        <dt class="text-sm font-medium text-zinc-500">Username</dt>
        <dd class="text-sm font-semibold text-zinc-900 text-right">@{{ user.username }}</dd>
      </div>

      <!-- Subscriptions Section -->
      <div class="pt-4">
        <h3 class="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-4">Active Subscriptions</h3>
        <div v-if="subscriptions.length > 0" class="space-y-3">
          <div v-for="(sub, index) in subscriptions" :key="index" class="bg-zinc-50/50 border border-zinc-200 rounded-xl p-4 hover:border-violet-200 transition-colors">
            <div class="flex justify-between items-start mb-2">
                <div>
                  <h4 class="font-bold text-zinc-900">{{ sub.product_name }}</h4>
                  <p class="text-xs text-zinc-500 font-medium">
                      {{ 
                        Intl.NumberFormat(
                          'en-US', 
                          { 
                            style: 'currency', 
                            currency: 'USD' 
                          }
                        ).format(sub.amount) 
                      }} / {{ formatInterval(sub) }}
                  </p>
                </div>
                <span v-if="sub.is_active" class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-700 uppercase tracking-wide">
                  Active
                </span>
                <span v-else class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-rose-700 uppercase tracking-wide">
                  Inactive
                </span>
            </div>
            <div class="pt-2 border-t border-zinc-200/50 flex items-center justify-between text-xs">
                <p class="flex items-center text-zinc-500">
                  <Calendar class="h-3.5 w-3.5 mr-1.5 opacity-70" />
                  Renews {{ sub.formatted_current_period_end }}
                </p>
                <p class="flex items-center text-violet-600 font-semibold">
                  <Clock class="h-3.5 w-3.5 mr-1.5" />
                  {{ sub.days_left }}
                </p>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-6 bg-zinc-50 rounded-xl border border-dashed border-zinc-200">
             <p class="text-sm text-zinc-500 font-medium">No active subscriptions</p>
        </div>
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
