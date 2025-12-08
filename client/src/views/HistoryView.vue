<template>
  <div class="min-h-screen bg-zinc-50/50 font-sans">
    <DesktopTopNav />    
    <MobileTopNav />
    
    <!-- Main Content -->
    <div class="pt-20 pb-20 md:pt-6 md:pb-0 relative z-0">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="bg-white shadow-sm border border-zinc-100 rounded-2xl overflow-hidden min-h-[600px]">
          <!-- Tabs -->
          <HistoryTabs />

          <!-- Tab Content -->
          <div class="p-6 bg-zinc-50/30">
            <TransactionsHistory v-if="historyStore.activeTab === historyStore.TRANSACTIONS_TAB" />
            <ConnectionsHistory v-else-if="historyStore.activeTab === historyStore.CONNECTIONS_TAB"/>
            <UsageHistory v-else-if="historyStore.activeTab === historyStore.USAGE_TAB"/>
          </div>
        </div>
      </div>
    </div>
    
    <MobileBottomNav />
    <ReportModal 
      v-if="historyStore.reportModalOpen" 
      :is-open="historyStore.reportModalOpen" 
      @close="historyStore.setReportModalOpen(false)"
      @submit="handleReport"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import DesktopTopNav from '@/components/layout/DesktopTopNav.vue';
import MobileTopNav from '@/components/layout/MobileTopNav.vue';
import MobileBottomNav from '@/components/layout/MobileBottomNav.vue';
import ReportModal from '@/components/feed/ReportModal.vue';
import { useHistoryStore } from '@/stores/history';
import UsageHistory from '@/components/history/UsageHistory.vue';
import ConnectionsHistory from '@/components/history/ConnectionsHistory.vue';
import TransactionsHistory from '@/components/history/TransactionsHistory.vue';
import HistoryTabs from '@/components/history/HistoryTabs.vue';
const historyStore = useHistoryStore();

// Handle report submission
const handleReport = async (reason) => {
  console.log("selected conn", historyStore.selectedConnection)
  if (!historyStore.selectedConnection) return;
  
  try {
    historyStore.submitReport(
      historyStore.selectedConnection?.id, 
      reason
    )
    
    // Close modal and show success message
    historyStore.setReportModalOpen(false)
    alert('Report submitted successfully');
  } catch (error) {
    console.error('Error reporting connection:', error);
    alert(error.response?.data?.error || 'Failed to submit report');
  }
};

// Fetch initial data
onMounted(async () => {
  historyStore.setLoadingTransactions(true);
  await historyStore.fetchTransactions();

  historyStore.setLoadingConnections(true);
  await historyStore.fetchMyConnections();

  historyStore.setLoadingUsage(true);
  await historyStore.fetchUsages();
});
</script>