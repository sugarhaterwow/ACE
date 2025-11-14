<template>
  <n-card title="Exemption Lists" size="large" embedded>
    <p style="color: #555; margin-bottom: 20px">
      Set predefined exemptions that affect the analysis of each issue
    </p>

    <n-card size="small" class="mb-4">
      <!-- 查看模式 -->
      <div v-if="!isEditing" class="form-row">
        <n-form-item label="Project Type Exemptions" style="flex: 1;">
          <span>{{ form.projectType || 'Standard Commercial' }}</span>
        </n-form-item>
        <n-form-item label="Regional Exemptions" style="flex: 1;">
          <span>{{ form.region || 'Europe' }}</span>
        </n-form-item>
      </div>

      <!-- 编辑模式 -->
      <div v-else class="form-row">
        <n-form-item label="Project Type Exemptions" style="flex: 1;">
          <n-select
            v-model="editForm.projectType"
            :options="projectTypeOptions"
            placeholder="Standard Commercial"
          />
        </n-form-item>
        <n-form-item label="Regional Exemptions" style="flex: 1;">
          <n-select
            v-model="editForm.region"
            :options="regionOptions"
            placeholder="Europe"
          />
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
</template>

<script setup>
import { ref } from "vue"

const isEditing = ref(false)

const form = ref({
  projectType: "Standard Commercial",
  region: "Europe"
})

const editForm = ref({ ...form.value })

const projectTypeOptions = [
  { label: "Standard Commercial", value: "Standard Commercial" },
  { label: "Residential", value: "Residential" },
  { label: "Industrial", value: "Industrial" }
]

const regionOptions = [
  { label: "Europe", value: "Europe" },
  { label: "Asia", value: "Asia" },
  { label: "North America", value: "North America" }
]

const startEdit = () => {
  editForm.value = { ...form.value }
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
}

const saveConfig = () => {
  form.value = { ...editForm.value }
  isEditing.value = false
  console.log("Saving config:", form.value)
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
