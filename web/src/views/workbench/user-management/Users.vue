<template>
  <CommonPage show-footer :title="config.title">

      <!-- 下方：成员表格 -->
      <div class="flex-1">
        
      <!-- 第一行：标题 -->
      <div class="filter-header">
        <span>Filters</span>
      </div>
        <CrudTable
          ref="$table"
          v-model:query-items="queryItems"
          :columns="columns"
          :get-data="fetchTableData"
        >
       <template #queryBar>
          <div class="filter-panel">
        

            <!-- 第二行：输入框 -->
            <div class="filter-inputs">
              <div
                v-for="filter in config.filters.filter(f => f.type === 'input')"
                :key="filter.key"
                class="filter-item"
              >
                <span class="filter-label">{{ filter.title }}</span>
                <NInput
                  v-model:value="queryItems[filter.key]"
                  :placeholder="filter.placeholder"
                  clearable
                />
              </div>
            </div>

            <!-- 第三行：选择框 -->
            <div class="filter-selects">
              <div
                v-for="filter in config.filters.filter(f => f.type === 'select')"
                :key="filter.key"
                class="filter-item"
              >
                <span class="filter-label">{{ filter.title }}</span>
                <NSelect
                  v-model:value="queryItems[filter.key]"
                  :options="filter.options"
                  :placeholder="filter.placeholder"
                  clearable
                />
              </div>
            </div>
          </div>
        </template>
    </CrudTable>

    <NModal v-model:show="showEditModal" preset="dialog" title="Edit Department">
      <div style="margin-bottom: 12px;">
        <strong>Name:</strong> {{ currentRow?.name }}
      </div>
      <div style="margin-bottom: 12px;">
        <strong>Email:</strong> {{ currentRow?.email }}
      </div>
      <div>
        <strong>Department:</strong>
        <NSelect
          v-model:value="currentRow.departments"
          :options="[
            { label: 'Engineering', value: 'Engineering' },
            { label: 'Marketing', value: 'Marketing' },
            { label: 'Sales', value: 'Sales' }
          ]"
          placeholder="Select department"
          style="margin-top: 8px; width: 200px;"
        />
      </div>
      <template #action>
        <NButton type="primary" @click="handleSaveEdit">Save</NButton>
        <NButton @click="showEditModal = false">Cancel</NButton>
      </template>
    </NModal>
  </div>


   
  </CommonPage>
</template>

<script setup lang="ts">
import { h, reactive, ref, onMounted, watch } from 'vue'
import { NButton, NSelect, NInput, NSwitch, NDropdown, NModal, useDialog } from 'naive-ui'
import CrudTable from '@/components/table/CrudTable.vue'
import api from '@/api'


const props = defineProps<{ config: any }>()

const $table = ref<any>(null) // CrudTable 引用
const tableData = ref<any[]>([])   // 初始为空数组


const queryItems = reactive({})
watch(
  () => props.config,
  (newConfig) => {
    if (newConfig?.filters) {
      newConfig.filters.forEach((f) => {
        if (!(f.key in queryItems)) {
          queryItems[f.key] = f.type === 'select' ? null : ''
        }
      })
    }
  },
  { immediate: true }
)


watch(
  () => ({ ...queryItems }), // 深度监听 queryItems 的每个字段
  () => {
    $table.value?.handleSearch()
  },
  { deep: true }
)

const showEditModal = ref(false)
const currentRow = ref<any>(null)
const dialog = useDialog()


async function fetchTableData({ page = 1, pageSize = 10, ...filters }) {
  const res = await api.getUserManagementData('users')
  const allData = res.data || []

  // 可选：根据 filters 做筛选
  let filtered = allData
  if (filters.role) filtered = filtered.filter(m => m.role === filters.role)
  if (filters.departments) filtered = filtered.filter(m => m.departments === filters.departments)
  if (filters.status) filtered = filtered.filter(m => m.status === filters.status)
  if (filters.keyword?.trim()) {
    const kw = filters.keyword.trim().toLowerCase()
    filtered = filtered.filter(m =>
      m.name.toLowerCase().includes(kw) || m.email.toLowerCase().includes(kw)
    )
  }

  const start = (page - 1) * pageSize
  const end = start + pageSize

  return {
    data: filtered.slice(start, end),
    total: filtered.length
  }
}

onMounted(() => {
  $table.value?.handleSearch()
})


// 表格列
const columns = [
  {
    title: 'Name & Email',
    key: 'name',
    align: 'left',
    render: (row: any) =>
      h('div', [
        h('div', { class: 'font-medium' }, row.name),
        h('div', { style: 'color: #6b7280; font-size: 15px;' }, row.email)
      ])
  },
  { title: 'Role', key: 'role', align: 'center' },
  { title: 'Last Active', key: 'lastActive', align: 'center' },
  {
    title: 'Status',
    key: 'status',
    align: 'center',
    render: (row: any) =>
      h(NSwitch, {
        value: row.status === 'active',
        onUpdateValue: (val: boolean) => {
          row.status = val ? 'active' : 'inactive'
        }
      })
  },
  {
  title: 'Actions',
  key: 'actions',
  align: 'center',
  render: (row: any) =>
      h(
        NDropdown,
        {
          options: [
            { label: 'Edit', key: 'edit' },
            { label: 'Remove', key: 'remove' }
          ],
          onSelect: (key: string) => {
            if (key === 'edit') {
              currentRow.value = { ...row }
              showEditModal.value = true
            }
            if (key === 'remove') {
              dialog.warning({
                title: 'Confirm Removal',
                content: `Are you sure you want to remove ${row.name}?`,
                positiveText: 'Remove',
                negativeText: 'Cancel',
                onPositiveClick: () => {
                  const index = tableData.value.findIndex(u => u.email === row.email)
                  if (index !== -1) {
                    tableData.value.splice(index, 1)
                    $table.value?.handleSearch()
                  }
                }
              })
            }
          }
        },
        {
          default: () => h('span', { style: 'cursor: pointer;' }, '⋮')
        }
      )
  }

]

function handleSaveEdit() {
  const updated = currentRow.value
  const target = tableData.value.find(item => item.email === updated.email)
  if (target) {
    target.departments = updated.departments
  }
  showEditModal.value = false
  $table.value?.handleSearch()
}



// 按钮事件
function handleClear() {
  queryItems.role = null
  queryItems.department = null
  queryItems.status = null
  queryItems.keyword = ''
  $table.value?.handleSearch()
}


</script>

<style scoped>
.filter-panel {
  display: flex;
  flex-direction: column;
  gap: 16px; /* 各行之间间距 */
}

/* 第一行：标题 */
.filter-header {
  height: 50px;
  display: flex;
  align-items: center; /* 垂直居中 */
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

/* 第二、三行布局 */
.filter-inputs,
.filter-selects {
  display: flex;
  flex-wrap: nowrap; /* 不换行 */
  gap: 16px;
  align-items: flex-end;
}

.filter-item {
  flex: 1; /* 平均分配宽度 */
  min-width: 200px;
  display: flex;
  flex-direction: column;
}

.filter-label {
  margin-bottom: 6px;
  font-size: 14px;
  color: #555;
}
</style>
