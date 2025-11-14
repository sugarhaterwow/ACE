

<template>
  <NLayout has-sider wh-full>
    <NLayoutContent>
      <NSpace vertical align="center" size="large" style="margin-top: 80px; min-height: 300px">
        <!-- 图像 -->
        <NImage
          src="https://technopark-slava.ru/wp-content/themes/technopark-slava/img/tech-center.svg"
          alt="Welcome"
          preview-disabled
        />


        <NH2>Intelligent search starts here</NH2>

        <!-- 搜索框 -->
        <NInput
          v-model:value="searchQuery"
          placeholder="Search..."
          clearable
          size="large"
          round
          style="width: 600px"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <TheIcon icon="material-symbols:search" :size="18" class="mr-5" />
          </template>
        </NInput>

        <div v-if="results.length" style="margin-top: 50px; width: 600px; text-align: left">
          <div v-for="(item, index) in results" :key="index" class="result-item">
            {{ item.item || item }}
          </div>
        </div>
        <div v-else style="margin-top: 20px; width: 600px; text-align: center; color: #999">
          {{ msg }}
        </div>
        

      
      </NSpace>
    </NLayoutContent>
  </NLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/store'
import { useI18n } from 'vue-i18n'
import TheIcon from '@/components/icon/TheIcon.vue'
import {
  NLayout,
  NLayoutContent,
  NSpace,
  NImage,
  NH2,
  NInput,
  NIcon
} from 'naive-ui'
import api from '@/api'

const searchQuery = ref('')
const results = ref([])
const msg = ref('')

async function handleSearch() {
  try {
    // axios 默认返回 { data: ... }
    const res = await api.searchDocument({ query: searchQuery.value })
    results.value = res.data || []
    msg.value = res.msg || 'No results found'
    console.log('API 返回的数据:', results.value)
  } catch (err) {
    results.value = []
    msg.value = 'Search failed'
  }
}

const userStore = useUserStore()
</script>
