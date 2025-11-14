<template>
  <CommonPage v-if="pageConfig" show-footer :title="pageConfig.title">
    <n-card style="margin-bottom: 16px">
      <n-tabs type="line" animated v-model:value="activeTab">
        <n-tab-pane
          v-for="tab in pageConfig.tabs"
          :key="tab.name"
          :name="tab.name"
          :tab="tab.label"
        >
          <component :is="componentMap[tab.component]" :config="tab.config"/>
        </n-tab-pane>
      </n-tabs>
    </n-card>
  </CommonPage>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '@/api'
import Users from './Users.vue'
import RolesPermissions from './RolesPermissions.vue'

const pageConfig = ref(null)
// 控制当前选中的标签页
const activeTab = ref('')

// 组件映射表
const componentMap = {
  Users,
  RolesPermissions,
}

// 页面挂载时触发表格搜索
onMounted(async () => {
  try {
    const configRes = await api.getPageConfig('user-management')
    pageConfig.value = configRes.data
    activeTab.value = configRes.data.tabs?.[0]?.name || ''
    
  } catch (err) {
    console.error('加载数据失败', err)
  }
})


</script>

<style scoped>
/* 可自定义标签页样式 */
.card-tabs .n-tabs-nav--bar-type {
  padding-left: 4px;
}
</style>
