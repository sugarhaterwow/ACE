<template>
  <div v-if="pageConfig">
    <n-card :title="pageConfig.title" size="large" embedded>
      <p style="color: #555; margin-bottom: 20px">
        {{ pageConfig.description }}
      </p>

      <!-- 遍历模块 -->
      <n-card
        v-for="(mod, mIdx) in pageConfig.modules"
        :key="mIdx"
        size="small"
        class="mb-4"
      >
        <h3>{{ mod.title }}</h3>
        
        <div class="form-row">
          <n-form-item
            v-for="(input, idx) in mod.components"
            :key="idx"
            :label="input.label"
            style="flex: 1;"
          >
            <template v-if="isEditing">
              <!-- 根据类型渲染不同控件 -->
              <n-input
                v-if="input.type === 'input'"
                v-model="editForm[input.label]"
                :placeholder="input.placeholder"
                clearable
                style="width: 250px"
              />
              <n-select
                v-else-if="input.type === 'select'"
                v-model="editForm[input.label]"
                :options="input.options"
                :placeholder="input.placeholder"
                clearable
                style="width: 230px"
              />
            </template>
            <template v-else>
              <span>{{ form[input.label] || '-' }}</span>
              
            </template>
          </n-form-item>
        </div>
      </n-card>

      <!-- 按钮 -->
      <div class="actions">
        <div style="display: flex; justify-content: flex-end; width: 100%; gap: 10px;">
          <n-button v-if="!isEditing" type="primary" @click="startEdit">Edit</n-button>
          <template v-else>
            <n-button @click="cancelEdit">Cancel</n-button>
            <n-button type="primary" ghost @click="saveConfig">Save</n-button>
          </template>
        </div>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue"
import { useMessage } from "naive-ui"
import api from "@/api"

const message = useMessage()

// 页面配置
const pageConfig = ref<any>(null)
const isEditing = ref(false)

// 父组件传入的初始表单
const props = defineProps<{
  form?: Record<string, any>
}>()
const emit = defineEmits<{
  (e: "save", value: Record<string, any>): void
}>()

// 当前显示的表单数据
const form = reactive<Record<string, any>>(props.form || {})

// 编辑时的副本
const editForm = reactive<Record<string, any>>({ ...form })

onMounted(async () => {
  try {
    const configRes = await api.getPageConfig("variable-criteria")
    pageConfig.value = configRes.data
    console.log(pageConfig.value)

    pageConfig.value.modules.forEach((mod: any) => {
      mod.components.forEach((input: any) => {
        const key = input.label
        form[key] = props.form?.[key] ?? ""
        editForm[key] = form[key]
      })
    })


  } catch (err) {
    console.error("加载数据失败", err)
  }
})

const startEdit = () => {
  Object.assign(editForm, form)  // 把 form 的值拷贝到 editForm
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
}

const saveConfig = () => {
  try {
    console.log(editForm)   // reactive 对象，直接打印即可

    // 用 Object.assign 把 editForm 的值拷贝到 form
    Object.assign(form, editForm)

    isEditing.value = false
    emit("save", form) // 通知父组件保存
    message.success("Configuration saved successfully!")
  } catch (err) {
    console.error("Error saving config", err)
    message.error("Error saving configuration. Please try again.")
  }
}
</script>

<style scoped>
.mb-4 {
  margin-bottom: 20px;
}
.form-row {
  display: flex;
  gap: 20px;
  margin-top: 10px;
}
.actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
</style>
