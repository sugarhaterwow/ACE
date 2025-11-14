<template>
  <div v-if="pageConfig">
    <n-card :title="pageConfig.title" size="large" embedded>
      <p style="color: #555; margin-bottom: 20px">
        {{pageConfig.description}}
      </p>
      

      <CrudTable
        ref="tableRef"
        :columns="columns"
        :get-data="() => fetchTableData(selectedChecklist, selectedProfile)"
        @onDataChange="handleDataChange"  
        @onChecked="handleSelectionChange"
        v-model:checked-row-keys="checkedRowKeys"               
      >
        <template #queryBar>
          <QueryBarItem label-width="40">
            <div class="flex gap-20">
              <div class="flex flex-col" style="width: 250px">
                <span class="text-gray-700 mb-10 text-left">Select Checklist</span>
                <NSelect
                  v-model:value="selectedChecklist"
                  :options="pageConfig.optionsA"
                  :placeholder="pageConfig.selectA"
                  clearable
                  style="width: 230px"
                />
              </div>

              <div class="flex flex-col" style="width: 200px">
                <span class="text-gray-700 mb-10 text-left">Select Criteria Profile</span>
                <NSelect
                  v-model:value="selectedProfile"
                  :options="pageConfig.optionsB"
                  :placeholder="pageConfig.selectB"
                  clearable
                  style="width: 180px"
                />
              </div>
            </div>
          </QueryBarItem>
        </template>
      </CrudTable>

      <!-- Buttons -->
      <div class="actions">
        <div style="display: flex; justify-content: flex-end; width: 100%;">
          <n-button type="primary" ghost @click="saveConfig">Save Configuration</n-button>
        </div>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { h, ref, onMounted, watch, defineProps, defineEmits, computed } from 'vue'
import { NTag, NDropdown } from 'naive-ui'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import { useMessage } from 'naive-ui'
import api from '@/api'

const message = useMessage()

interface StepForm {
  [key: string]: any[]   // key = checklist::profile, value = rows
}

// 本地表单：存储所有 checklist/profile 对应的数据
const localForm = ref<Record<string, any[]>>({})

function getFormKey(checklist: string, profile: string) {
  return `${checklist || ''}::${profile || ''}`
}


// 子组件只负责收集数据，而 saved 和 updated 状态完全由父组件和 store 统一管理
const props = defineProps<{ form: StepForm }>()
const emit = defineEmits<{
  (e: 'save', value: StepForm): void
}>()


// CrudTable 引用
const tableRef = ref<InstanceType<typeof CrudTable> | null>(null)

// 保存 CrudTable 内部数据
const innerTableData = ref<any[]>([])
// 控制勾选回显
const checkedRowKeys = ref<number[]>([])

const selectedChecklist = ref(null)
const selectedProfile = ref(null)

// 定义响应式变量
const pageConfig = ref(null)
const columns = ref([])

// 根据配置生成 columns
function createDynamicColumns(configColumns: any[], syncLocalForm: Function) {
  return configColumns.map((col) => {
    const column: any = {
      title: col.title,
      key: col.key,
      align: col.align || 'center',
      width: col.width,
      type: col.type,
      ellipsis: col.ellipsis === true ? { tooltip: true } : col.ellipsis
    }

    switch (col.key) {
      case 'search_entities':
        column.render = (row: any) => {
          const dropdownOptions = [
            ...row.removed_entities.map((entity: string) => ({ label: entity, key: entity })),
            { type: 'divider' },
            { label: 'Restore All', key: '__restore_all__', style: 'color: green; font-weight: bold;' }
          ]

          return h(
            'div',
            { style: 'display: flex; flex-wrap: wrap; gap: 6px; align-items: center;' },
            [
              ...row.search_entities.map((entity: string, index: number) =>
                h(
                  NTag,
                  {
                    closable: true,
                    onClose: () => {
                      row.search_entities.splice(index, 1)
                      row.removed_entities.push(entity)
                      
                    }
                  },
                  { default: () => entity }
                )
              ),
              row.removed_entities.length
                ? h(
                    NDropdown,
                    {
                      options: dropdownOptions,
                      trigger: 'click',
                      onSelect: (key: string) => {
                        if (key === '__restore_all__') {
                          row.search_entities.push(...row.removed_entities)
                          row.removed_entities = []
                        } else {
                          const idx = row.removed_entities.indexOf(key)
                          if (idx !== -1) {
                            row.removed_entities.splice(idx, 1)
                            row.search_entities.push(key)
                          }
                        }
                        
                      }
                    },
                    {
                      default: () =>
                        h(
                          NTag,
                          { style: 'cursor: pointer; background: #f0f0f0; color: #333;' },
                          { default: () => '...' }
                        )
                    }
                  )
                : null
            ]
          )
        }
        break

      default:
        // 其他列不需要自定义 render
        break
    }

    return column
  })
}

onMounted(async () => {
  try {
    // 1. 拉取页面配置
    const configRes = await api.getPageConfig('analysis-checklist')
    pageConfig.value = configRes.data
    columns.value = createDynamicColumns(configRes.data.tableColumns || [])

    // 2. 判断父组件是否传了已有 form
    const hasForm = props.form && Object.keys(props.form).length > 0

    if (hasForm) {
      // 父组件传入已有 form，直接用
      localForm.value = { ...props.form }
    } else {
      // 遍历所有 checklist/profile 组合，初始化为全选
      for (const checklistOpt of configRes.data.optionsA || []) {
        for (const profileOpt of configRes.data.optionsB || []) {
          const checklist = checklistOpt.value
          const profile = profileOpt.value
          const { data } = await fetchTableData(checklist, profile)

          const key = getFormKey(checklist, profile)
          localForm.value[key] = [...data]   // 默认全选
        }
      }
    }
    
    console.log(localForm.value)
    // 默认选中第一个组合
    const firstChecklist = configRes.data.optionsA?.[0]?.value
    const firstProfile = configRes.data.optionsB?.[0]?.value
    selectedChecklist.value = firstChecklist
    selectedProfile.value = firstProfile

    // 回显第一个组合的数据
    await fetchTableData(firstChecklist, firstProfile)
    checkedRowKeys.value = localForm.value[getFormKey(firstChecklist, firstProfile)].map(r => r.id)
    tableRef.value?.handleSearch()

  } catch (err) {
    console.error('加载数据失败', err)
  }
})

watch([selectedChecklist, selectedProfile], async ([newChecklist, newProfile]) => {
  if (newChecklist && newProfile) {
    await fetchTableData(newChecklist, newProfile)
    
    tableRef.value?.handleSearch()
  }
})



const handleSelectionChange = (keys: number[]) => {
  checkedRowKeys.value = keys
  const selected = innerTableData.value.filter(row => keys.includes(row.id))
  const key = getFormKey(selectedChecklist.value, selectedProfile.value)
  localForm.value[key] = selected
}

function syncLocalForm() {
  const key = getFormKey(selectedChecklist.value, selectedProfile.value)
  localForm.value[key] = innerTableData.value.filter(row =>
    checkedRowKeys.value.includes(row.id)
  )
}

// 核心修改：在 onDataChange 时做回显
const handleDataChange = (rows: any[]) => {
  innerTableData.value = rows

  const key = getFormKey(selectedChecklist.value, selectedProfile.value)
  const saved = localForm.value[key]

  if (saved && saved.length) {
    // 回显行修改
    rows.forEach(row => {
      const match = saved.find(item => item.id === row.id)
      if (match) {
        row.search_entities = [...match.search_entities]
        row.removed_entities = [...match.removed_entities]
      }
    })

    // 回显勾选状态
    checkedRowKeys.value = saved.map(item => item.id)
  }

  // 保证 localForm 跟随更新
  localForm.value[key] = rows.filter(r => checkedRowKeys.value.includes(r.id))
  
}



// 校验逻辑
function validate(): boolean {
  const hasAnySelection = Object.values(localForm.value).some(
    (rows: any[]) => rows && rows.length > 0
  )

  if (!hasAnySelection) {
    message.error('Please select at least one item from the table!')
    return false
  }
  return true
}


// 保存逻辑
function saveConfig() {
  if (!validate()) return
  console.log(localForm.value)
  emit('save', { ...localForm.value })
}


// 获取数据
async function fetchTableData(checklist: string, criteriaprofile: string) {
  
  const res = await api.getChecklist({ checklist, criteriaprofile })
  
  const rows = res.data.map(item => ({
    ...item,
    removed_entities: []
  }))


  innerTableData.value = rows

  const key = getFormKey(checklist, criteriaprofile)

  if (localForm.value[key]?.length) {
    // 回显
    const saved = localForm.value[key]
    checkedRowKeys.value = saved.map(item => item.id)

    // 恢复 search_entities/removed_entities
    rows.forEach(row => {
      const match = saved.find(s => s.id === row.id)
      if (match) {
        row.search_entities = [...match.search_entities]
        row.removed_entities = [...match.removed_entities]
      }
    })
  } else {
    // 默认全选
    checkedRowKeys.value = rows.map(r => r.id)
    localForm.value[key] = [...rows]
  }

  return { data: rows, total: rows.length }
  
}


// 暴露 validate 给父组件
defineExpose({ 
  validate,
  getTempForm: () => ({ ...localForm.value })
})


</script>

<style scoped>
.actions {
  display: flex;
  justify-content: space-between;
  margin-top: 40px;
}
</style>







