
<template>
  <div v-if="pageConfig">
    <n-card :title=pageConfig.title size="large" embedded>
      <p style="color: #555; margin-bottom: 20px">
        {{pageConfig.description}}
      </p>

      <!-- Installation Period -->
      <n-card size="small" class="mb-4">
        
        <div class="form-row">
          <n-form-item label="Project Type Exemptions" style="width: 250px;">
            <n-select
              :value="localForm.projectType"
              :options="projectTypeOptions"
              placeholder="Standard Commercial"
              @update:value="val => updateField('projectType', val)"
            />
          </n-form-item>
          <n-form-item label="Regional Exemptions" style="width: 250px;">
            <n-select
              :value="localForm.region"
              :options="regionOptions"
              placeholder="Europe"
              @update:value="val => updateField('region', val)"
            />
          </n-form-item>
        </div>
      </n-card>
      

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
import { ref, watch } from 'vue'
import { useMessage } from 'naive-ui'
import api from '@/api'

const message = useMessage()

const pageConfig = ref(null)
const msg = ref('')

onMounted(async () => {
  const configRes = await api.getPageConfig('exemption-lists')
  pageConfig.value = configRes.data

  pageConfig.value.modules.forEach((mod: any) => {
    mod.components.forEach((input: any, index: number) => {
      if (!input.model) {
        input.model = input.label.replace(/\s+/g, '_').toLowerCase() + '_' + index
      }
      // 初始化 localForm
      localForm.value[input.model] = props.form?.[input.model] ?? ''
    })
  })
})

interface ExemptionForm {
  projectType: string
  region: string
}

// 子组件只负责收集数据，而 saved 和 updated 状态完全由父组件和 store 统一管理
const props = defineProps<{ form: ExemptionForm }>()
const emit = defineEmits<{
  (e: 'save', value: ExemptionForm): void
}>()

// 本地副本
const localForm = ref<ExemptionForm>({ ...(props.form || { projectType: '', region: '' }) })

// 当父组件的 form 发生变化时，把最新的值拷贝到子组件的 localForm，保证显示的数据是最新的
// 保证子组件的本地表单 localForm 始终和父组件传进来的 form 保持一致，避免翻页返回时看不到之前填写的内容
watch(
  () => props.form,
  (newVal) => {
    localForm.value = { ...newVal }
  },
  { immediate: true }
)

const projectTypeOptions = [
  { label: 'Standard Commercial', value: 'Standard Commercial' },
  { label: 'Residential', value: 'Residential' }
]

const regionOptions = [
  { label: 'Europe', value: 'Europe' },
  { label: 'Asia', value: 'Asia' }
]

// 更新字段
function updateField<K extends keyof ExemptionForm>(key: K, val: ExemptionForm[K]) {
  localForm.value = { ...localForm.value, [key]: val }
}

// 校验
function validate(): boolean {
  const { projectType, region } = localForm.value
  if (!projectType || !region) {
    message.error('Please select both project type and region!')
    return false
  }
  return true
}

const saveConfig = () => {
  console.log('Saving config:', localForm.value)
  if (!validate()) return
  
  emit('save', { ...localForm.value })   // 通知父组件保存
}

// 暴露 validate 给父组件
defineExpose({ 
  validate,
  getTempForm: () => ({ ...localForm.value })
})

</script>



<style scoped>
.mb-4 {
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  gap: 80px;
  margin-top: 10px;
}

.actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
</style>
