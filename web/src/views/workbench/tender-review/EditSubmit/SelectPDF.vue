<template>
  <div class="workspace">
    <!-- 顶部选择器 -->
    <div class="module-selector">
      <button
        v-for="m in config.modules"
        :key="m.value"
        :class="{ active: m.value === activeModule }"
        @click="activeModule = m.value"
      >
        {{ m.label }}
      </button>
    </div>

    <!-- 主体布局 -->
    <div class="main">
      <!-- 左侧内容 -->
      <div class="left">
        <template v-if="showSkeleton">
            <n-skeleton
              v-for="n in 10"
              :key="n"
              text
              :repeat="3"
              style="margin-bottom: 16px; border-radius: 8px"
            />
          </template>

          <!-- 否则显示 ResultCard -->
          <template v-else>
            <ResultCard
              v-for="(item, idx) in currentModuleData"
              :key="idx"
              v-bind="item"
              :active-module="activeModule"
              @go-to-page="goToPage"
            />
          </template>
      </div>

      <!-- 右侧预览区 -->
      <div class="right bg-white border rounded-lg">
        <template v-if="showSkeleton">
          <!-- 顶部工具栏骨架 -->
          <div class="flex items-center justify-between px-4 py-2 border-b bg-gray-50">
            <n-skeleton text style="width: 60%; height: 20px;" />
            <n-skeleton text style="width: 80px; height: 20px;" />
          </div>

          <!-- 骨架页滚动容器 -->
          <div class="scroll-area p-4 space-y-6">
            <div
              v-for="(page, idx) in skeletonPages"
              :key="idx"
              :ref="el => pageRefs[idx] = el"
              class="page-skeleton"
            >
              <n-skeleton text style="width: 40%; height: 16px; margin-bottom: 12px;" />
              <n-skeleton text :repeat="5" style="margin-bottom: 8px;" />
              <n-skeleton style="width: 100%; height: 200px; border-radius: 4px; margin: 12px 0;" />
              <n-skeleton text :repeat="3" style="margin-bottom: 8px;" />
            </div>
          </div>
        </template>

        <template v-else>
          
          

          <div class="p-4 flex justify-center items-center">
            <img :src="imageSrc" alt="Content Image" class="max-w-full rounded-lg" />
          </div>

        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, toRefs } from 'vue'
import { NSkeleton } from 'naive-ui'

import { computed } from 'vue'

const imageSrc = computed(() => {
  switch (activeModule.value) {
    case 'search_highlight':
      return '/show.jpg'
    case 'clause_alignment':
      return '/show1.jpg'
    case 'issues':
      return '/show2.jpg'
    default:
      return '/show.jpg'
  }
})

const props = defineProps<{
  showSkeleton: boolean
  config: {
    modules: { label: string; value: string }[]
  }
  data: Record<string, any>
}>()

const {showSkeleton, config, data} = toRefs(props)

const activeModule = ref(config.value.modules[0]?.value || '')

const moduleData = computed(() => {
  const result: Record<string, any> = {}
  config.value.modules.forEach((mod) => {
    result[mod.value] = data.value?.[mod.value] || []
  })
  return result
})

const currentModuleData = computed(() => moduleData.value[activeModule.value] || [])

const skeletonPages = [1, 2, 3, 4, 5] // 模拟5页骨架屏
const pageRefs = ref([])

// 当前展开的卡片索引, 默认展开第一张卡片
const expandedIndex = ref(0)


function handleShowPdf(pdfname) {
  console.log('Selected PDF:', pdfname)
  // 你可以在这里显示 PDF、跳转页面、或更新状态
}

const pdfUrl = '/EUSFTA_Chap_6.pdf' // ✅ 写死的 PDF 路径
const selectedPdf = ref('')
const currentPage = ref(1)


function goToPage(pageNum) {
  nextTick(() => {
    const target = pageRefs.value[pageNum - 1]
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  })
}
</script>

<style scoped>
.workspace {
  display: flex;
  gap: 8px; /* 按钮之间的间距 */
  flex-direction: column;
  height: 100vh; /* 占满视口高度，保证滚动生效 */
}

.module-selector {
  display: flex;
  gap: 8px;
  padding: 10px 0;
  background: #fff; /* 白底 */
  border-bottom: 1px solid #ddd; /* 底部分隔线 */
  margin-bottom: 2px;
}

.module-selector button {
  flex: 1; /* 按钮平分容器宽度 */
  padding: 12px 0;
  font-size: 16px;
  font-weight: 500;
  border: none;
  border-radius: 6px;
  background: #e5e7eb;
  color: #1f2937;
  cursor: pointer;
  transition: all 0.2s ease;
}

.module-selector button:hover {
  background: #f3f4f6; /* hover 时浅灰 */
}

.module-selector button.active {
  background: #0b1f4d; /* 蓝色高亮 */
  color: white;
  border-color: #0b1f4d;
}

.main {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 16px;
  flex: 1;
  padding: 8px;
  overflow: hidden; /* 防止双滚动条 */
}

.left {
  display: flex;
  flex-direction: column;
  overflow-y: auto; /* 左侧列表可滚动 */
}

.right {
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 右侧整体不溢出 */
}

.right .scroll-area {
  flex: 1;
  overflow-y: auto; /* 右侧骨架屏可滚动 */
}

.page-skeleton {
  border-bottom: 1px solid #eee;
  padding-bottom: 20px;
}

.pdf-placeholder {
  display: flex;
  justify-content: center;   /* 水平居中 */
  align-items: center;       /* 垂直居中 */
  height: 100%;              /* 占满右侧高度 */
  color: #888;
  font-size: 16px;
  text-align: center;
}
</style>

