<template>
  <CommonPage v-if="pageConfig" show-footer :title=pageConfig.title>
  <CrudTable
    ref="$table"
    :tableTitle="pageConfig.tableTitle"
    v-model:query-items="queryItems"
    :columns="columns"
    :get-data="() => fetchTableData(selectedProfile)"
    @onDataChange="handleDataChange"  
    @onChecked="handleSelectionChange"
    v-model:checked-row-keys="checkedRowKeys"      
  >
    <template #queryBar>
      <div class="flex justify-between items-end w-full mb-16">
        <!-- 左侧 -->
        <div class="flex flex-col" style="width: 250px">
          <span class="mb-8 text-gray-700">{{ pageConfig.queryItems.title }}</span>
          <n-select
            v-model:value="selectedProfile"
            :options="pageConfig.queryItems.options"
            :placeholder="pageConfig.queryItems.placeholder"
            clearable
            style="width: 230px"
          />
        </div>

        <!-- 右侧 -->
        <div class="flex gap-10 self-end">
          <n-button type="primary" @click="handleSave">Save</n-button>
          <n-button type="primary" @click="goToCreate">+ Create Criteria Profile</n-button>
        </div>
      </div>
    </template>

  </CrudTable>

    
  <div style="display: flex; flex-direction: column; gap: 24px;">

    <VariableCriteria :form="criteriaStore.variableCriteria?.form || {}" />

    <ExemptionLists />
  </div>

  <n-drawer v-model:show="showDrawer" placement="right" width="80%">
    <CommonPage show-footer :title=pageConfig.createItems.title>

    
    
    <div class="form-container">
    <div
      v-for="(module, mIdx) in pageConfig.modules"
      :key="mIdx"
      class="form-module"
    >
      <n-card :title="module.title" size="medium" embedded>
        <p class="module-description">{{ module.description }}</p>

        <div class="form-grid">
          <div
            v-for="(comp, cIdx) in module.components"
            :key="cIdx"
            class="form-field"
          >
            <label class="form-label">
              {{ comp.label }}
              <span v-if="comp.required" class="required">*</span>
            </label>

            <!-- 输入框组件 -->
            <n-input
              v-if="comp.type === 'input'"
              v-model:value="formValues[mIdx][comp.model || comp.label]"
              :placeholder="comp.placeholder"
              style="width: 300px"
            />

            <!-- 下拉选择组件 -->
            <n-select
              v-else-if="comp.type === 'select'"
              v-model:value="formValues[mIdx][comp.model || comp.label]"
              :options="normalizeOptions(comp.options)"
              :placeholder="comp.placeholder"
              style="width: 300px"
            />

            <!-- 其他类型可扩展 -->
            <div v-else class="unsupported">
              Unsupported type: {{ comp.type }}
            </div>
          </div>
        </div>
      </n-card>
    </div>

    <n-button type="primary" class="mt-4" @click="handleSubmit">Submit</n-button>
  </div>
  </CommonPage>
</n-drawer>


    


  

    
  </CommonPage>
</template>

<script setup lang="ts">
import { h, reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { NTag, NDropdown, NButton, NSpace, NInput, NSelect, NDrawer, useDialog, useMessage } from 'naive-ui'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import VariableCriteria from './VariableCriteria.vue'
import ExemptionLists from './ExemptionLists.vue'
import { useCriteriaProfileStore } from '@/store/modules/review-profile'
import api from '@/api'

const tableData = ref<any[]>([])
// CrudTable 引用
const $table = ref<any>(null) // CrudTable 引用
const message = useMessage()
const showDrawer = ref(false)
const createForm = reactive({})
const criteriaStore = useCriteriaProfileStore()

// 筛选项
const selectedProfile = ref(null)
// 表格列定义
const columns = ref([])
// 页面配置
const pageConfig = ref(null)

function createDynamicColumns(configColumns: any[]) {
  return [
    { type: 'selection', width: 60, align: 'center' }, // 最左侧选择列
    ...configColumns.map((col: any) => {
      const column: any = {
        title: col.title,
        key: col.key,
        align: col.align || 'center',
        ellipsis: col.ellipsis === true ? { tooltip: true } : col.ellipsis
      }

      if (col.key === 'search_entities') {
        column.render = (row: any) => {
          if (!row.removed_entities) row.removed_entities = []

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
      }

      return column
    })
  ]
}

const formValues = ref<Record<string, any>>({})

// 保存 CrudTable 内部数据
const innerTableData = ref<any[]>([])
// 控制勾选回显
const checkedRowKeys = ref<number[]>([])

// 页面挂载时触发表格搜索

onMounted(async () => {
  try {
    const configRes = await api.getPageConfig('criteria-profile')
    pageConfig.value = configRes.data
    columns.value = createDynamicColumns(configRes.data.tableColumns || [])

    // 遍历模块
    for (const mod of configRes.data.modules) {
      formValues.value[mod.title] = {}

      for (const comp of mod.components) {
        if (comp.options && Array.isArray(comp.options)) {
          for (const opt of comp.options) {
            const key = opt.value || opt.label
            const { data } = await fetchTableData(key)
            formValues.value[mod.title][key] = [...data]
          }
        } else {
          const key = comp.model || comp.label
          const { data } = await fetchTableData(key)
          formValues.value[mod.title][key] = [...data]
        }
      }
    }

    console.log(formValues.value)
    selectedProfile.value = configRes.data.modules[0].components[0].options[0].value
  } catch (err) {
    console.error('加载数据失败', err)
  }
})


watch(selectedProfile, async (newProfile) => {
  if (newProfile) {
    await fetchTableData(newProfile)
    console.log('Selected profile:', newProfile)
    $table.value?.handleSearch()
  }
})

const handleSelectionChange = (keys: number[]) => {
  checkedRowKeys.value = keys
  const selected = innerTableData.value.filter(row => keys.includes(row.id))
  formValues.value[pageConfig.value.modules[0].title][selectedProfilerofile] = selected
}

// 核心修改：在 onDataChange 时做回显
const handleDataChange = (rows: any[]) => {
  innerTableData.value = rows

  
  const saved =  formValues.value[pageConfig.value.modules[0].title][selectedProfile]
  

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
   formValues.value[pageConfig.value.modules[0].title][selectedProfile] = rows.filter(r => checkedRowKeys.value.includes(r.id))
  
}


// 处理 options 格式（支持字符串数组或对象数组）
function normalizeOptions(options: any[]) {
  return options.map(opt =>
    typeof opt === 'string' ? { label: opt, value: opt } : opt
  )
}

async function handleSubmit() {
  const result: Record<string, any> = {}

  // 校验必填字段
  for (let idx = 0; idx < pageConfig.value.modules.length; idx++) {
    const mod = pageConfig.value.modules[idx]
    const moduleData = formValues.value[mod.title]
    const moduleResult: Record<string, any> = {}

    for (const comp of mod.components) {
      const key = comp.model || comp.label
      const value = moduleData[key]

      if (comp.required && !value) {
        message.warning(`Please fill in "${comp.label}" in "${mod.title}"`)
        return
      }

      moduleResult[key] = value
    }

    result[mod.title] = moduleResult
  }

  try {
    // 提交到后端
    // await api.submitCriteriaProfile(result)

    message.success('Submitted successfully!')
    showDrawer.value = false // 关闭抽屉
  } catch (err) {
    console.error('提交失败', err)
    message.error('Submission failed.')
  }
}

// 获取数据
async function fetchTableData(criteriaprofile: string) {
  
  const res = await api.getCriteriaProfile({ query: criteriaprofile })
  
  const rows = res.data.map(item => ({
    ...item,
    removed_entities: []
  }))


  innerTableData.value = rows

  if (formValues.value[pageConfig.value.modules[0].title][criteriaprofile]?.length) {
    // 回显
    const saved = formValues.value[pageConfig.value.modules[0].title][criteriaprofile]
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
    formValues.value[pageConfig.value.modules[0].title][criteriaprofile] = [...rows]
  }

  return { data: rows, total: rows.length }
  
}



async function handleSave() {
  const moduleTitle = pageConfig.value.modules[0].title
  const moduleForm = formValues.value[moduleTitle]

  // 检查每个 key 是否都有值
  const allKeysHaveValue = Object.keys(moduleForm).every(key => {
    const val = moduleForm[key]
    // 判断空值逻辑，可以根据需要调整
    return val !== null && val !== undefined && val !== '' && !(Array.isArray(val) && val.length === 0)
  })

  if (!allKeysHaveValue) {
    message.warning('Please select at least one item to save.')
    return
  }

  try {
    // 这里保存的是整个 formValues[moduleTitle]
    // await api.saveSelectedItems(moduleForm)
    message.success('Saved successfully!')
  } catch (err) {
    console.error('保存失败', err)
    message.error('Save failed.')
  }
}




// 点击 Create 跳转页面
const goToCreate = () => {
  showDrawer.value = true
}

</script>
