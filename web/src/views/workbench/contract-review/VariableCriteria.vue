<template>
  <div v-if="pageConfig">
    <n-card :title="pageConfig.title" size="large" embedded>
      <p style="color: #555; margin-bottom: 20px">
        {{pageConfig.description}}
      </p>
      
        <div v-for="(module, idx) in pageConfig.modules" :key="idx" class="form-item">
          <n-card :title="module.title" size="medium" embedded>
            <div class="form-input">
              <div v-for="(input, i) in module.components" :key="i" class="form-grid">
                <label class="form-label">
                  {{ input.label }}
                  <span v-if="input.required" class="required">*</span>
                </label>

                <!-- 普通输入框 -->
                <n-input
                  v-if="!input.options"
                  v-model:value="localForm[input.model]"
                  :placeholder="input.placeholder"
                  style="width: 300px"
                />

                <n-select
                  v-else
                  v-model:value="localForm[input.model]"
                  :options="input.options.map(opt => ({ label: opt, value: opt }))"
                  :placeholder="input.placeholder"
                  style="width: 300px"
                />

              </div>
            </div>
          </n-card>
        
        </div>

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
import { ref, watch, defineProps, defineEmits, onMounted } from 'vue'
import { useMessage } from 'naive-ui'
import api from '@/api'

// 表格数据
const pageConfig = ref(null)
const message = useMessage()

interface StepForm {
  minimumPeriod?: string
  units?: string
  maxLiability?: number
  insuranceMin?: string
}

// 子组件只负责收集数据，而 saved 和 updated 状态完全由父组件和 store 统一管理
const props = defineProps<{ form: StepForm }>()
const emit = defineEmits<{
  (e: 'save', value: StepForm): void
}>()

// 本地副本
const localForm = ref<StepForm>({ ...(props.form || {}) })

onMounted(async () => {
  try {
    const configRes = await api.getPageConfig('variable-criteria')
    pageConfig.value = configRes.data

    // 自动生成 model 字段
    pageConfig.value.modules.forEach((mod: any) => {
      mod.components.forEach((input: any, index: number) => {
        if (!input.model) {
          input.model = input.label.replace(/\s+/g, '_').toLowerCase() + '_' + index
        }
        localForm.value[input.model] = props.form?.[input.model] ?? ''
      })
    })
  } catch (err) {
    console.error('加载数据失败', err)
  }
})

// 当父组件的 form 发生变化时，把最新的值拷贝到子组件的 localForm，保证显示的数据是最新的
// 保证子组件的本地表单 localForm 始终和父组件传进来的 form 保持一致，避免翻页返回时看不到之前填写的内容
watch(
  () => props.form,
  (newVal) => {
    localForm.value = { ...newVal }
  },
  { immediate: true }
)

// 子组件自己的校验逻辑
function validate(): boolean {
  for (const mod of pageConfig.value.modules) {
    for (const input of mod.components) {
      if (input.required && !localForm.value[input.model]) {
        message.error(`Please fill in: ${input.label}`)
        return false
      }
    }
  }
  return true
}


// 保存按钮逻辑：保存时才同步给父组件
const saveConfig = () => {
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
.actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.form-item {
  display: flex;
  flex-direction: column; /* 每个 module 一行 */
  gap: 50px;              /* module 之间的间距 */
}

.form-input {
  display: flex;
  flex-wrap: wrap;
  gap: 16px 24px;
}

.form-grid {
  flex: 1 1 calc(50% - 24px); /* 每行两个，减去间距 */
  min-width: 280px; /* 防止太窄 */
}

.form-label {
  font-weight: 500;
  text-align: left; /* label右对齐 */
}

rm-label {
  font-weight: 500;
  margin-bottom: 6px;
}

.required {
  color: red; /* 必填项红色 */
  margin-left: 1px;
}
</style>
