<template>
  <CommonPage v-if="pageConfig" show-footer :title="pageConfig.title">
    <CrudTable
      ref="$table"
      :columns="columns"
      :get-data="fetchTableData"
    >
      <template #queryBar>
        <QueryBarItem label-width="40">
          <div class="flex flex-col" style="width: 250px">
            <span class="text-gray-700 mb-10 text-left">
              {{ pageConfig.queryItems.title }}
            </span>
            <NSelect
              v-model:value="selectedChecklist"
              :options="pageConfig.queryItems.options"
              :placeholder="pageConfig.queryItems.title"
              clearable
              style="width: 230px"
              @update:value="handleChecklistChange"
            />
          </div>
        </QueryBarItem>
      </template>
    </CrudTable>
  </CommonPage>
</template>

<script setup lang="ts">
import { h, ref, onMounted } from 'vue'
import { NTag, NIcon, NPopconfirm } from 'naive-ui'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import { Trash } from '@vicons/ionicons5'
import api from '@/api'
import { useMessage } from 'naive-ui'


// 页面配置和状态
const pageConfig = ref(null)
const selectedChecklist = ref(null)
const columns = ref([])
const tableData = ref<any[]>([])
const $table = ref<any>(null) // CrudTable 引用
const message = useMessage()

// 动态生成表格列
function createDynamicColumns(configColumns: any[]) {
  return configColumns.map((col: any) => {
    const column: any = {
      title: col.title,
      key: col.key,
      align: col.align || 'center',
      ellipsis: col.ellipsis === true ? { tooltip: true } : col.ellipsis
    }

    switch (col.key) {
      case 'search_entities':
        column.render = (row: any) =>
          h(
            'div',
            { style: 'display: flex; flex-wrap: wrap; gap: 6px; justify-content: center;' },
            row.search_entities.map((entity: string) => h(NTag, {}, { default: () => entity }))
          )
        break

      case 'actions':
        column.render = (row: any, rowIndex: number) =>
          h(
            NPopconfirm,
            {
              onPositiveClick: async () => {
                try {
                  await api.deleteReviewItem(row.id)
                  tableData.value.splice(rowIndex, 1) // 更新前端表格
                  message.success('Delete sucessfully!')
                } catch (err) {
                  console.error('删除失败', err)
                  
                }
              },
              positiveText: 'Confirm',
              negativeText: 'Cancel',
              trigger: 'click'
            },
            {
              default: () => h('span', 'Are you sure you want to delete this item?'),
              trigger: () =>
                h('span', { style: 'cursor: pointer;' }, [
                  h(NIcon, { size: 20 }, { default: () => h(Trash, { color: 'red' }) })
                ])
            }
          )
        break
    }

    return column
  })
}

// 页面初始化
onMounted(async () => {
  try {
    const configRes = await api.getPageConfig('review-criteria')
    pageConfig.value = configRes.data
    columns.value = createDynamicColumns(configRes.data.tableColumns || [])
  } catch (err) {
    console.error('加载页面配置失败', err)
  }
})

// 当用户选择 checklist 时刷新表格
function handleChecklistChange() {
  $table.value?.handleSearch() // ✅ 调用 CrudTable 方法刷新
}

// 获取表格数据
async function fetchTableData() {
  try {
    const res = await api.getReviewCriteria({ query: selectedChecklist.value })
    tableData.value = res.data || []
    return {
      data: tableData.value,
      total: tableData.value.length
    }
  } catch (err) {
    console.error('获取表格数据失败', err)
    tableData.value = []
    return { data: [], total: 0 }
  }
}
</script>
