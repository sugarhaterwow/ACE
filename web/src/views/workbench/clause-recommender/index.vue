<template>
    <CommonPage v-if="pageConfig" show-footer :title="pageConfig.title" :sub-title="pageConfig.subtitle">
       <div class="mb-16">
        <div class="flex flex-col w-full">
          <span class="text-[20px] mb-[10px] block text-gray-640" >Enter search text</span>
          <NInput
            v-model:value="queryText"
            type="textarea"
            rows="3"
            placeholder="Type your text here..."
            style="width: 100%"
            class="mt-4 w-full"
          />
          <div class="flex justify-end gap-20 mt-20">
            <NButton @click="clearInput" size="large">Clear</NButton>
            <NButton type="primary" @click="submitInput" size="large">Recommend</NButton>
          </div>
        </div>
      </div>

        <CrudTable
            ref="$table"
            :columns="columns"
            :get-data="fetchTableData"
        >
        </CrudTable>
      


    </CommonPage>

    
    
</template>

<script setup lang="ts">
import { h, reactive, ref, onMounted } from 'vue'
import { NTag, NButton, NIcon, NPopconfirm, NSwitch } from 'naive-ui'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import { Trash } from '@vicons/ionicons5' 
import api from '@/api'
import { useMessage } from 'naive-ui'

// 表格数据
const pageConfig = ref(null)
const queryText = ref('')
const columns = ref([])
const $table = ref<any>(null) // CrudTable 引用
const message = useMessage()



onMounted(async () => {
  try {
    const configRes = await api.getPageConfig('clause-recommender')
    pageConfig.value = configRes.data 
    columns.value = createDynamicColumns(configRes.data.tableColumns || [])
    
  } catch (err) {
    console.error('加载数据失败', err)
  }
})

// 清空输入
function clearInput() {
  queryText.value = ''
}

async function fetchTableData() {
  try {
    const res = await api.getRecommendations({ query: queryText.value })
    return {
      data: res.data || [],
      total: res.data?.length || 0  // 如果没有分页，返回长度即可
    }
  } catch (err) {
    console.error('获取表格数据失败', err)
    return {
      data: [],
      total: 0
    }
  }
}


function submitInput() {
  if (!queryText.value.trim()) {
    window.$message.warning('Enter content to get recommendations!')
    return
  }
  $table.value?.handleSearch()
}



</script>
