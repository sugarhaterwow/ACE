<template>
  <n-card>
    <template #header>
      <div style="background-color: #f0f9ff; padding: 20px 20px; border-radius: 4px;">
        <div style="font-size: 25px; line-height: 1.5; color: #0f172a;">
          {{config.title}}
        </div>
        <div style="font-size: 12px; color: #334155; margin-top: 4px;">
          {{config.description}}
        </div>
      </div>
    </template>

    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px">
      <template v-for="(card, index) in config.cards" :key="index"> 
        <MetricCard
          v-if="!showSkeleton"
          :key="index"
          :mainText="card.title"
          :subNumber="data.metricData[card.key]"
          :subLabel="card.subLabel"
          :icon="card.icon"
          :iconColor="card.iconColor"
          :mainTextStyle="{ fontSize: '18px', fontWeight: '600', color: '#333' }"
          :subNumberStyle="{ fontSize: '18px', fontWeight: 'bold', color: card.iconColor}"
          :subLabelStyle="{ fontSize: '14px', marginLeft: '9px', color: '#888' }"
        />

        <n-card
          v-else
          class="w-full"
          style="border-radius: 12px"
          :content-style="{ padding: '16px' }"
        >
          <div style="display: flex; align-items: center; gap: 12px">
            <n-icon size="50" :color="card.iconColor" v-if="card.icon">
              <component :is="card.icon" />
            </n-icon>

            <div style="flex: 1">
              <div style="font-size: 15px; font-weight: 600; color: #333">
                {{ card.title }}
              </div>

              <div style="margin-top: 10px; display: flex; align-items: baseline; gap: 8px">
                <n-skeleton text :width="80" />
              </div>
            </div>
          </div>
        </n-card>
      </template>
    </div>
    <template #footer>
      <SelectPDF :showSkeleton="showSkeleton" :config="config" :data="data" />
    </template>
  </n-card>
  

</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import {
  ApprovalsApp16Regular,
  ArrowDownload20Filled,
  TabDesktopClock20Regular,
  Document28Regular,
  ColorLine16Regular,
  DismissCircle28Regular,

} from '@vicons/fluent'
import SelectPDF from './SelectPDF.vue'

const activeTab = ref('searchhighlight')
defineProps({
  showSkeleton: Boolean,
  config: Object,
  data: Object
})


</script>

<style>

:host {
  display: block;
  width: 100%;
}

/* 左边 Tabs */
.analysis-tabs {
  flex: 1;
  border-right: 1px solid #e5e7eb;
  overflow-y: auto;
  padding: 16px;
}

</style>