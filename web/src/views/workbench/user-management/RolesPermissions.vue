<template>
  <CommonPage show-footer :title="config.title">
    <div class="flex gap-4">
      <!-- Admin -->
      <div class="p-6 border rounded shadow flex-1">
        <h3 style="font-size: 20px; font-weight: 700; margin-bottom: 8px;">
          Admin
        </h3>
        <p style="font-size: 12px; color: #374151; margin-bottom: 8px;">
          Full System access and user management
        </p>
        <p style="font-size: 9px; color: #6B7280; margin-bottom: 12px;">
          1 Admin
        </p>
        <n-button type="primary" size="tiny">View Admin</n-button>
      </div>

      <!-- Reviewer -->
      <div class="p-6 border rounded shadow flex-1">
        <h3 style="font-size: 20px; font-weight: 700; margin-bottom: 8px;">
          Reviewer
        </h3>
        <p style="font-size: 12px; color: #374151; margin-bottom: 8px;">
          Review and comment on analyses
        </p>
        <p style="font-size: 9px; color: #6B7280; margin-bottom: 12px;">
          1 Reviewer
        </p>
        <n-button type="primary" size="tiny">View Reviewer</n-button>
      </div>

      <!-- Viewer -->
      <div class="p-6 border rounded shadow flex-1">
        <h3 style="font-size: 20px; font-weight: 700; margin-bottom: 8px;">
          Viewer
        </h3>
        <p style="font-size: 12px; color: #374151; margin-bottom: 8px;">
          Read-only access to completed analyses
        </p>
        <p style="font-size: 9px; color: #6B7280; margin-bottom: 12px;">
          1 Viewer
        </p>
        <n-button type="primary" size="tiny">View Viewer</n-button>
      </div>
    </div>

    <!-- 权限表格 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="fetchTableData"
    />
  </CommonPage>
</template>

<script setup lang="ts">
import { h, reactive, ref, onMounted } from 'vue'
import { NButton } from 'naive-ui'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import MetricCard from '@/components/MetricCard.vue'


defineProps({
  config: Object
})

// CrudTable 引用
const $table = ref(null)

// 页面挂载后自动搜索
onMounted(() => {
  $table.value?.handleSearch()
})

// 筛选项
const queryItems = reactive({
  checklist: 'construction'
})

// Checklist 选项
const optionsA = [
  { label: 'Construction Checklist', value: 'construction' }
]

// 表格列定义（权限矩阵）
const columns = [
  { title: 'Permission', key: 'permission', align: 'center' },
  {
    title: 'Admin',
    key: 'admin',
    align: 'center',
    render: (row: any) => h('span', row.admin ? '✅' : '❌')
  },
  {
    title: 'Reviewer',
    key: 'reviewer',
    align: 'center',
    render: (row: any) => h('span', row.reviewer ? '✅' : '❌')
  },
  {
    title: 'Viewer',
    key: 'viewer',
    align: 'center',
    render: (row: any) => h('span', row.viewer ? '✅' : '❌')
  }
]

// 模拟 29 条权限数据
const allPermissions = [
  { permission: 'Upload Document', admin: true, reviewer: false, viewer: false },
  { permission: 'Configure Analysis', admin: true, reviewer: true, viewer: false },
  { permission: 'View Results', admin: true, reviewer: true, viewer: true },
  { permission: 'Export Data', admin: true, reviewer: false, viewer: false },
  { permission: 'Manage Users', admin: true, reviewer: false, viewer: false },
  // 生成更多模拟数据
  ...Array.from({ length: 24 }, (_, i) => ({
    permission: `Extra Permission ${i + 6}`,
    admin: Math.random() > 0.2,
    reviewer: Math.random() > 0.5,
    viewer: Math.random() > 0.7
  }))
]

// 获取表格数据（分页）
async function fetchTableData({ page = 1, pageSize = 5 }) {
  const start = (page - 1) * pageSize
  const end = start + pageSize
  return {
    data: allPermissions.slice(start, end),
    total: allPermissions.length
  }
}
</script>

<style scoped>
.grid {
  display: grid;
}
</style>
