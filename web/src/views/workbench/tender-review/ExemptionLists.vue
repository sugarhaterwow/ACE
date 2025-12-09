<template>
  <div v-if="pageConfig">
    <div v-for="(step, idx) in pageConfig.steps" :key="idx" class="card-wrapper">
      <n-card 
        :title="step.title" 
        size="large" 
        embedded
      >
        <p style="color: #555; margin-bottom: 20px">
          {{ step.description }}
        </p>
      
        <!-- 如果是 Checklist 模块 -->
        <CrudTable
          v-show="step.tableColumns && columns.length > 0"
          ref="tableRef"
          :columns="columns"
          :get-data="() => fetchTableData(...selectedTable)"
          @onDataChange="handleDataChange"  
          @onChecked="handleSelectionChange"
          v-model:checked-row-keys="checkedRowKeys"              
        >
          <template #queryBar>
            <QueryBarItem label-width="40">
              <div class="flex gap-20">
                <!-- 遍历 step.modules 里的 components -->
                <div
                  v-for="(comp, i) in step.modules[0].components"
                  :key="i"
                  class="flex flex-col"
                  style="width: 250px"
                >
                  <span class="text-gray-700 mb-10 text-left">{{ comp.label }}</span>
                  <n-select
                    v-model:value="selectedTable[i]"
                    :options="comp.options"
                    :placeholder="comp.placeholder"
                    clearable
                    style="width: 230px"
                  />
                </div>
              </div>
            </QueryBarItem>
          </template>
        </CrudTable>

        <div v-if="!step.tableColumns">
          <div v-for="(sub, i) in step.modules" :key="i">
            <n-card :title="sub.title" size="medium" embedded>
              <div class="form-grid">
                <div
                  v-for="(input, j) in sub.components"
                  :key="j"
                  class="form-item"
                >
                  <label>
                    {{ input.label }}
                    <span v-if="input.required" class="required">*</span>
                  </label>

                  <n-input
                    v-if="!input.options"
                    v-model:value="localForm[step.title][input.label]"
                    :placeholder="input.placeholder"
                    style="width: 280px"
                  />

                  <n-select
                    v-else
                    v-model:value="localForm[step.title][input.label]"
                    :options="input.options"
                    :placeholder="input.placeholder"
                    style="width: 260px"
                  />
                </div>
              </div>
            </n-card>
          </div>
        </div>
      </n-card>
    </div>
    <div class="actions">
      <n-button type="primary" ghost @click="saveConfig">Save Configuration</n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useMessage } from 'naive-ui'
import api from '@/api'
import { NTag, NDropdown, MessageApi } from 'naive-ui'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import { h, ref, watch, onMounted, nextTick, isEqual } from 'vue'

const message = useMessage()
const pageConfig = ref(null)

// CrudTable 引用
const tableRef = ref([])
// CrudTable 各列类型和名称
const columns = ref([])
// 保存 CrudTable 内部数据
const innerTableData = ref<any[]>([])
// 控制勾选回显
const checkedRowKeys = ref<number[]>([])
const selectedTable = ref<any[]>([])

// 表单核心状态
const localForm = reactive<Record<string, any>>({})        // 当前用户填写的表单
const originalForm = ref<Record<string, any>>({})         // 最原始的表单快照
const hasSaved = ref(false)                                // 标记是否点击过 save 按钮（新增）

// 子组件只负责收集数据，而 saved 和 updated 状态完全由父组件和 store 统一管理
const emit = defineEmits<{
  (e: 'save', value: Record<string, any>): void
}>()

// ======================== 新增核心工具函数 ========================
/** 深对比两个对象是否一致（判断是否修改） */
const isFormEqual = (form1: Record<string, any>, form2: Record<string, any>): boolean => {
  // 处理空对象/undefined 情况
  if (!form1 && !form2) return true
  if (!form1 || !form2) return false
  // 处理数组引用不同但内容相同的情况（表格数据常用）
  const stringify = (obj: any) => JSON.stringify(obj, (key, value) => {
    if (Array.isArray(value)) return value.sort() // 数组排序后对比（避免顺序影响）
    return value
  })
  return stringify(form1) === stringify(form2)
}

/** 判断是否所有必填项已填写（复用 validate 核心逻辑） */
const isAllRequiredFilled = (): boolean => {
  if (!pageConfig.value) return false
  for (const step of pageConfig.value.steps) {
    const stepData = localForm[step.title]
    if (!stepData) continue

    if (step.tableColumns) {
      // 表格步骤：至少有一个组合有选中行
      const hasAnySelection = Object.values(stepData).some(
        (rows: any[]) => Array.isArray(rows) && rows.some(row => row.selected)
      )
      if (!hasAnySelection) return false
    } else {
      // 普通步骤：必填字段非空
      for (const mod of step.modules) {
        for (const comp of mod.components) {
          if (comp.required && !stepData[comp.label]) {
            return false
          }
        }
      }
    }
  }
  return true
}

/** 离开页面前校验（供父组件调用，覆盖4种场景） */
const checkBeforeLeave = async (): Promise<boolean> => {
  const isModified = !isFormEqual(localForm, originalForm.value) // 是否修改未保存
  const isRequiredFilled = isAllRequiredFilled()                 // 必填项是否填完
  const isFormEmpty = isFormEqual(localForm, {})                 // 表单是否为空

  // 情况 1：初始为空 + 没修改 → 提示必填项
  if (isFormEmpty && !isModified && !isRequiredFilled) {
    message.error('No changes made on this page. Please fill in required fields before submitting.');
    return false;
  }

  // 情况 2：没修改 + 必填项都有值 → 确认提交已保存配置
  if (!isModified && isRequiredFilled) {
    try {
      const confirmResult = await message.confirm(
        'No changes made. Submit already saved configuration?',
        { type: 'info', positiveText: 'Yes', negativeText: 'No' }
      );
      return confirmResult === 'confirm';
    } catch (err) {
      return false;
    }
  }

  // 情况 3：修改了但没保存 → 确认是否放弃保存
  if (isModified && !hasSaved.value) {
    try {
      const confirmResult = await message.confirm(
        'You have unsaved changes. Proceed without saving current configuration?',
        { type: 'warning', positiveText: 'Proceed', negativeText: 'Cancel' }
      );
      return confirmResult === 'confirm';
    } catch (err) {
      return false;
    }
  }

  // 情况 4：修改并保存过 → 直接允许提交
  if (isModified && hasSaved.value) {
    return true;
  }

  return false;
}
// =================================================================

// 根据配置生成 columns
function createDynamicColumns(configColumns: any[]) {
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

function getFormKey(...args: any[]) {
  console.log("调用了FormKey:", args.filter(Boolean).join('::'))
  return args.filter(Boolean).join('::')
}

async function fetchTableData(...values: any[]) {
  if (!values || values.length === 0) {
    return { data: [], total: 0 }
  }
  
  // 调用接口，传入整个 selectedTable 数组
  const res = await api.getChecklist({ values })

  // 格式化返回的数据，保证有 search_entities / removed_entities 字段
  const rows = res.data.map((item: any) => ({
    ...item,
    removed_entities: item.removed_entities || [],   // 兼容接口无该字段
    search_entities: item.search_entities || [],
    selected: item.selected || false
  }))

  // 保存到内存表格数据
  innerTableData.value = rows
  
  // 用组合值生成唯一 key
  const key = getFormKey(...values)
  console.log("在fetchDataTable", key)
  const tableStepTitle = pageConfig.value.steps[0]?.title
  
  // 如果 localForm 已经有保存过的数据 → 回显
  if (localForm[tableStepTitle]?.[key]?.length) {
    const saved = localForm[tableStepTitle][key]
    checkedRowKeys.value = saved.map((item: any) => item.id)

    // 恢复 search_entities / removed_entities / selected 状态
    rows.forEach(row => {
      const match = saved.find((s: any) => s.id === row.id)
      if (match) {
        row.search_entities = [...match.search_entities]
        row.removed_entities = [...match.removed_entities]
        row.selected = match.selected
      }
    })
  } else {
    // 默认全选
    checkedRowKeys.value = rows.map((r: any) => r.id)
    rows.forEach(row => row.selected = true) // 标记为选中
    localForm[tableStepTitle][key] = [...rows]
  }
  console.log("返回的数据：", rows)
  return { data: rows, total: rows.length }
}

onMounted(async () => {
  const configRes = await api.getPageConfig('review-profile')
  pageConfig.value = configRes.data
  columns.value = createDynamicColumns(configRes.data.steps[0].tableColumns || [])

  // 初始化 localForm 结构
  for (const step of pageConfig.value.steps) {
    if (!localForm[step.title]) {
      localForm[step.title] = {}
    }
  }
  
  const comps = pageConfig.value.steps[0].modules[0].components
  const optionGroups = comps.map((c: any) => c.options || [])
  // 生成所有组合
  const allCombos = optionGroups.reduce(
    (acc: any[][], group: any[]) =>
      acc.flatMap(prev => group.map(opt => [...prev, opt])),
    [[]]
  )

  console.log("allCombos values:", allCombos.map(combo => combo.map(opt => opt.value)))

  // 初始化所有组合的表格数据
  for (const [stepIndex, step] of pageConfig.value.steps.entries()) {
    if (stepIndex === 0) {
      for (const combo of allCombos) {
        const values = combo.map((opt: any) => opt.value)
        const { data } = await fetchTableData(...values)
        const formKey = getFormKey(...values)
        
        // 过滤掉空的 key
        if (formKey && formKey.trim() !== '') {
          localForm[step.title][formKey] = data
          console.log('values:', values, 'formKey:', formKey, 'data:', data)
        } else {
          console.warn('跳过空 formKey, values:', values)
        } 
      }
    } else {
      // 初始化普通步骤的表单字段
      for (const mod of step.modules) {
        for (const comp of mod.components) {
          localForm[step.title][comp.label] = comp.value || null
        }
      }
    }
  }

  // 初始化原始快照（深拷贝，避免引用关联）
  selectedTable.value = allCombos[0].map((opt: any) => opt.value)
  originalForm.value = JSON.parse(JSON.stringify(localForm))
  hasSaved.value = false // 初始标记为未保存（新增）
})

function handleSelectionChange(keys: number[]) {
  // 更新选中行 id
  checkedRowKeys.value = keys

  const key = getFormKey(...selectedTable.value)
  const stepTitle = pageConfig.value.steps[0].title

  // 更新每一行的 selected 状态
  innerTableData.value.forEach(row => {
    row.selected = keys.includes(row.id)
  })

  // 保存完整的表格数据（包含选中和未选中行）
  localForm[stepTitle][key] = [...innerTableData.value]

  console.log("在handleSelectionChange:", key, localForm[stepTitle][key])
}

// 核心修改：在 onDataChange 时做回显
const handleDataChange = (rows: any[]) => {
  innerTableData.value = rows
  const key = getFormKey(...selectedTable.value)
  const stepTitle = pageConfig.value.steps[0].title
  const saved = localForm[stepTitle][key]

  if (saved && saved.length) {
    // 回显行修改
    rows.forEach(row => {
      const match = saved.find(item => item.id === row.id)
      if (match) {
        row.search_entities = [...match.search_entities]
        row.removed_entities = [...match.removed_entities]
        row.selected = match.selected   // ✅ 恢复选中状态
      }
    })

    // 回显勾选状态
    checkedRowKeys.value = saved.filter(item => item.selected).map(item => item.id)
  } else {
    // 初始化勾选状态
    checkedRowKeys.value = rows.filter(r => r.selected).map(r => r.id)
  }

  // 保证 localForm 跟随更新（保存完整数据）
  localForm[stepTitle][key] = [...rows]

  console.log("在handleDataChange:", key, localForm[stepTitle][key])
}

// 修改 watch 中的调用
watch(selectedTable, async (newVal) => {
  if (newVal.length > 0) {
    await nextTick()
    console.log('Table ref:', tableRef.value)
    
    // 因为 tableRef 是数组，需要取第一个元素
    if (tableRef.value && tableRef.value[0] && tableRef.value[0].handleSearch) {
      await tableRef.value[0].handleSearch()
    } else {
      console.warn('Table ref or handleSearch method not available:', tableRef.value)
    }
  }
}, { deep: true })

function validate(): boolean {
  // 遍历所有 step
  for (const step of pageConfig.value.steps) {
    const stepData = localForm[step.title]

    if (!stepData) continue

    if (step.tableColumns) {
      // 表格 step：至少有一个组合有选中行
      const hasAnySelection = Object.values(stepData).some(
        (rows: any[]) => Array.isArray(rows) && rows.some(row => row.selected)
      )
      if (!hasAnySelection) {
        message.error(`Please select at least one item in ${step.title}!`)
        return false
      }
    } else {
      // 普通 step：检查必填字段
      for (const mod of step.modules) {
        for (const comp of mod.components) {
          if (comp.required && !stepData[comp.label]) {
            message.error(`Please fill in ${comp.label} in ${step.title}!`)
            return false
          }
        }
      }
    }
  }

  return true
}

// 改造 saveConfig：标记保存状态+更新原始快照
const saveConfig = () => {
  console.log('Saving config:', localForm)
  if (!validate()) return
  const currentForm = JSON.parse(JSON.stringify(localForm)) // 深拷贝当前表单
  emit('save', currentForm)   // 通知父组件保存
  originalForm.value = currentForm // 更新原始快照为当前保存的表单（新增）
  hasSaved.value = true // 标记为已保存（新增）
  message.success('Configuration saved successfully!') // 新增保存成功提示
}

// 暴露方法给父组件（新增 checkBeforeLeave）
defineExpose({ 
  validate,
  getTempForm: () => ({ ...localForm }),
  checkBeforeLeave // 关键：父组件 prev/submit 时调用
})
</script>

<style scoped>
.card-wrapper {
  margin-bottom: 20px; /* 控制统一间距 */
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 每行两个 */
  gap: 20px 24px; /* 行间距、列间距 */
  margin-top: 16px;
}

.form-item {
  display: flex;
  flex-direction: column;
}

.form-item label {
  font-weight: 500;
  margin-bottom: 6px;
  color: #333;
}

.form-item .required {
  color: red;
  margin-left: 4px;
}

.actions {
  display: flex;
  justify-content: flex-end; /* 靠右对齐 */
  margin-top: 20px;          /* 可选：增加上边距 */
}
</style>