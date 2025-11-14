<template>
  <n-card :title="config.title" size="large" embedded>
    <p v-if="config.description" class="description">
      {{ config.description }}
    </p>

    <div v-for="(module, mIdx) in config.modules" :key="mIdx" class="form-item">
      <n-card :title="module.title" size="medium" embedded>
        <div class="form-input">
          <div v-for="(field, fIdx) in module.components" :key="fIdx" class="form-grid">
            <label class="form-label">
              {{ field.label }}
              <span v-if="field.required" class="required">*</span>
            </label>

            <component
              :is="resolveComponent(field)"
              v-model="form[field.model || `${mIdx}_${fIdx}`]"
              v-bind="getComponentProps(field)"
            />
          </div>
        </div>
      </n-card>
    </div>

    <div class="actions">
      <slot name="actions">
        <n-button type="primary" ghost @click="emitSave">Save</n-button>
      </slot>
    </div>
  </n-card>
</template>


<script setup lang="ts">
import { ref, watch, defineProps, defineEmits, onMounted } from 'vue'
import { useMessage } from 'naive-ui'
import api from '@/api'



const props = defineProps<{
  config: any
  form: Record<string, any>
}>()

const emit = defineEmits<{
  (e: 'save', value: Record<string, any>): void
}>()

function resolveComponent(type: string) {
  switch (type) {
    case 'input':
      return 'n-input'
    case 'textarea':
      return 'n-input'
    case 'number':
      return 'n-input-number'
    case 'select':
      return 'n-select'
    case 'radio':
      return 'n-radio-group'
    case 'checkbox':
      return 'n-checkbox-group'
    case 'switch':
      return 'n-switch'
    case 'date':
      return 'n-date-picker'
    case 'time':
      return 'n-time-picker'
    case 'datetime':
      return 'n-date-picker'
    case 'upload':
      return 'n-upload'
    case 'table':
      return 'n-data-table'
    case 'button':
      return 'n-button'
    case 'divider':
      return 'n-divider'
    case 'text':
      return 'n-text'
    case 'slot':
      return 'slot'
    default:
      return 'div'
  }
}

function getComponentProps(field: any) {
  const props: Record<string, any> = {
    placeholder: field.placeholder || '',
    options: field.options || [],
    type: field.inputType || 'text'
  }
  if (field.type === 'select') {
    props.options = (field.options || []).map((opt: any) =>
      typeof opt === 'string' ? { label: opt, value: opt } : opt
    )
  }
  if (field.type === 'table') {
    props.columns = field.columns || []
    props.data = field.data || []
  }
  return props
}

function validate(): boolean {
  const missing = config.value?.modules
    ?.flatMap((mod: any) => mod.components)
    ?.filter((f: any) => f.required && !localForm.value[f.model])
  if (missing?.length) {
    message.error('Please fill in all required fields.')
    return false
  }
  return true
}

function emitSave() {
  if (!validate()) return
  emit('save', { ...localForm.value })
}

defineExpose({
  validate,
  getForm: () => ({ ...localForm.value })
})


</script>

<style scoped>
.description {
  color: #555;
  margin-bottom: 20px;
}
.actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
}
.form-item {
  display: flex;
  flex-direction: column;
  gap: 40px;
}
.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  margin-bottom: 20px;
}
.form-label {
  font-weight: 500;
}
.required {
  color: red;
  margin-left: 4px;
}
</style>



