<template>
  <AppPage v-if="pageConfig" :title="pageConfig.title" show-footer>
    <!-- 概览统计卡片 -->
    <n-card
      :title="pageConfig.cardsTitle"
      size="medium"
      :segmented="true"
      class="mb-15"
      style="border-radius: 12px"
    >
      <template #header-extra>
        <n-date-picker
          v-model:value="range"
          type="daterange"
          clearable
          style="border-radius: 8px"
        />
      </template>

      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px">
        <MetricCard
          v-for="(card, index) in pageConfig.cards"
          :key="index"
          :title="card.title"
          :mainText="card.value"
          :timeUnit="card.timeUnit"
          :description="card.description"
          :icon="card.icon"
          :iconColor="card.iconColor"
          :trend="card.trend"
          :loading="loading"
          :mainTextStyle="{ fontSize: '20px', fontWeight: '600', color: '#333' }"
          :timeUnitStyle="{ fontSize: '20px', fontWeight: '600', color: '#333' }"
          :subNumberStyle="{ fontSize: '18px', fontWeight: 'bold', color: card.iconColor}"
          :subLabelStyle="{ fontSize: '14px', marginLeft: '9px', color: '#888' }"
        />
      </div>

    </n-card>

    <!-- 投标文档表格 -->
    <n-card
      :title="pageConfig.tableTitle"
      size="medium"
      class="mb-20"
      style="border-radius: 12px"
    >
      <template #header-extra>
        <n-button type="primary" style="border-radius: 8px">+ New Analysis</n-button>
      </template>

      <!-- 筛选区域 -->
      <div style="margin-bottom: 16px; display: flex; gap: 10px; flex-wrap: wrap; align-items: center">
        <!-- 搜索框 -->
        <span style="margin-bottom: 4px; font-weight: 500">Search</span>
        <n-input
          v-model:value="searchKeyword"
          placeholder="Search by tender name or client"
          clearable
          style="flex: 1; min-width: 50px; border-radius: 8px"
        />

        <!-- 状态多选 -->
        <span style="margin-bottom: 4px; font-weight: 500">Status</span>
        <n-select
          v-model:value="selectedStatuses"
          multiple
          placeholder="Select Status"
          :options="pageConfig.statusOptions"
          style="flex: 1; min-width: 50px; border-radius: 8px"
        />

        <!-- 日期范围选择器 -->
        <span style="margin-bottom: 4px; font-weight: 500">Date Range</span>
        <n-date-picker
          v-model:value="dateRange"
          type="daterange"
          clearable
          style="flex: 1; min-width: 180px; border-radius: 8px"
        />
      </div>
                                                                                                   
      <!-- 表格 -->
      <n-data-table
        :columns="columns"
        :data="filteredData"
        :pagination="pagination"
        :bordered="false"
        style="border-radius: 8px"
      />
    </n-card>
  </AppPage>
</template>

<script setup lang="ts">
import { ref, h, computed, onMounted } from 'vue'
import { NButton, NDropdown, NIcon } from 'naive-ui'
import api from '@/api'
import { MoreVertical20Regular } from '@vicons/fluent' // 竖着三个点的图标
import MetricCard from '@/components/page/MetricCard.vue'
import {
  ApprovalsApp16Regular,
  
  ArrowDownload20Filled,
  TabDesktopClock20Regular,
  Document28Regular,
  ColorLine16Regular,
  DismissCircle28Regular,

} from '@vicons/fluent'


// 定义响应式变量
const pageConfig = ref(null)
const tableData = ref<any[]>([])   // 初始为空数组

// 生命周期：组件挂载时执行
onMounted(async () => {
  try {
    const configRes = await api.getPageConfig('dashboard')
    const tenderTable = await api.getDashboardData()
    pageConfig.value = configRes.data 
    tableData.value = tenderTable.data 
  } catch (err) {
    console.error('加载数据失败', err)
  }
  
})

// 默认日期范围（统计卡片）
const range = ref<[Date, Date]>([
  new Date('2024-11-08'),
  new Date('2025-03-23'),
])

// 默认筛选日期范围
const dateRange = ref<[Date, Date]>([
  new Date('2024-11-08'),
  new Date('2025-03-23'),
])


const searchKeyword = ref('')
const selectedStatuses = ref<string[]>([])

const filteredData = computed(() => {
  console.log(tableData.value)
  return tableData.value.filter(item => {
    const matchKeyword = item.name.toLowerCase().includes(searchKeyword.value.toLowerCase())

    const matchStatus =
      selectedStatuses.value.length === 0 || selectedStatuses.value.includes(item.status)

    const matchDate =
      !dateRange.value ||
      (
        new Date(item.analysis) >= dateRange.value[0] &&
        new Date(item.analysis) <= dateRange.value[1]
      )

    return matchKeyword && matchStatus && matchDate
  })
})

const columns = [
  { title: 'Tender Name', key: 'name' },
  { title: 'Folder', key: 'folder' },
  { title: 'Client', key: 'client' },
  {
    title: 'Status',
    key: 'status',
    render(row) {
      const statusMap = {
        'Completed': { type: 'success', color: '#18a058' },
        'In Review': { type: 'warning', color: '#f0a020' },
        'Doc Error': { type: 'error', color: '#d03050' },
      }
      const status = statusMap[row.status]
      return h(
        NButton,
        {
          size: 'small',
          strong: true,
          tertiary: true,
          style: `border-radius: 8px; background-color: ${status.color}; color: white`,
        },
        { default: () => row.status }
      )
    },
  },
  { title: 'Issues Found', key: 'issues' },
  { title: 'Analysis', key: 'analysis' },
  {
    title: 'Actions',
    key: 'actions',
    render(row) {
      const options = [
        { label: 'View', key: 'view' },
        { label: 'Delete', key: 'delete' }
      ]
      return h(
        NDropdown,
        {
          options,
          trigger: 'click',
          onSelect: (key: string) => {
            if (key === 'view') {
              // 处理查看逻辑
              console.log('View row:', row)
            } else if (key === 'delete') {
              // 处理删除逻辑
              console.log('Delete row:', row)
            }
          }
        },
        {
          default: () =>
            h(
              NButton,
              {
                quaternary: true,
                circle: true,
                size: 'small'
              },
              {
                icon: () =>
                  h(NIcon, null, { default: () => h(MoreVertical20Regular) })
              }
            )
        }
      )
    }
  }
]

const pagination = {
  pageSize: 4,
  page: 1,
  pageCount: 12,
  showSizePicker: false,
}
</script>
