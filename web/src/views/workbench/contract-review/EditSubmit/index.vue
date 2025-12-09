<template>
  <div v-if="pageConfig">

    <div class="page-container">
      <AnalysisPage :showSkeleton="showSkeleton" :config="pageConfig" :data="analysisData"/>
    </div>
    
        
    <!-- 悬浮按钮：只在第三阶段以后显示 -->
    <button
      v-if="currentStage >= 2 && !visible"
      class="floating-btn"
      @click="visible = true"
    >
      View Progress
    </button>

    <!-- 弹框 -->
    <NModal
      v-model:show="visible"
      preset="card"
      :title=pageConfig.modal.title
      style="width: 700px"
      :header-style="{ textAlign: 'center' }"
      :closable="currentStage >= 2"
      :maskClosable="currentStage >= 2"
      
    >
      <div class="text-gray-600 mb-6 text-center">
        {{pageConfig.modal.description}}
      </div>

      <!-- 横向步骤条 -->
      <div class="steps">
        <div
          v-for="(stage, index) in stages"
          :key="index"
          class="step"
        >
          <!-- 圆圈 -->
          <div
            class="circle"
            :class="{ completed: index < currentStage, active: index === currentStage }"
          >
            <span v-if="index <= currentStage">✔</span>
            <span v-else>{{ index + 1 }}</span>
          </div>

          <!-- 下方文字 -->
          <div
            class="label"
            :class="{ completed: index < currentStage, active: index === currentStage }"
          >
            {{ stage }}
          </div>

          <!-- 线条 -->
          <div v-if="index < stages.length - 1" class="connector">
            <div
              class="connector-fill"
              :style="{ width: connectorFillWidth(index) }"
            ></div>
          </div>
        </div>
      </div>
      
    </NModal>

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { NModal, NSkeleton } from 'naive-ui'
import AnalysisPage from './AnalysisPage.vue'
import api from '@/api'

const visible = ref(true)
const pageConfig = ref(null)

const stages = ref([])
const currentStage = ref(0)
const stageProgress = ref(0)
const showSkeleton = ref(true)

const analysisData = ref(null)

function connectorFillWidth(index) {
  if (index < currentStage.value) return '100%'
  if (index === currentStage.value) return `${stageProgress.value}%`
  return '0%'
}

watch(currentStage, async (val) => {
  if (val >= 2) {
    showSkeleton.value = false
    visible.value = false
  }
  try {
      const res = await api.getAboutAnalysis()
      analysisData.value = res.data

  } catch (err) {
    console.error('Failed to fetch selected data:', err)
  }
  
  
})

onMounted(async () => {
  try {
    const configRes = await api.getPageConfig('about')
    pageConfig.value = configRes.data
    stages.value = configRes.data.modal.stages 

    const timer = setInterval(() => {
      if (currentStage.value < stages.value.length - 1) {
        if (stageProgress.value < 100) {
          stageProgress.value += 5
        } else {
          stageProgress.value = 0
          currentStage.value++
        }
      } else {
        clearInterval(timer) 
      }
    }, 200)
  } catch (error) {
    console.error('Failed to fetch config:', error)
  }
})

</script>

<style>

.page-container {
  height: 100vh;          /* 占满视口高度 */
  overflow-y: auto;       /* 超出时滚动 */
  padding: 16px;          /* 可选：内边距 */
  box-sizing: border-box; /* 避免滚动条影响布局 */
}

.steps {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin: 30px auto;
  position: relative;
  width: 100%;
}

.step {
  flex: 1;
  text-align: center;
  position: relative;
}

.circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #e5e7eb; /* 灰色背景 */
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin: 0 auto;
  z-index: 2;
  position: relative;
}

.circle.active {
  background: #3b82f6; /* 蓝色 */
  color: #fff;
}

.circle.completed {
  background: #10b981; /* 绿色 */
  color: #fff;
}

.label {
  margin-top: 10px;
  font-size: 13px;
  color: #6b7280;
}

.label.active {
  color: #3b82f6;
  font-weight: bold;
}

.label.completed {
  color: #10b981;
  font-weight: bold;
}

.connector {
  position: absolute;
  top: 18px; /* 让线和圆心对齐 */
  left: 50%;
  width: 100%;
  height: 2px;
  background: #e5e7eb;
  z-index: 1;
}

.connector-fill {
  height: 100%;
  background: #3b82f6;
  transition: width 0.3s ease;
}

/* 悬浮按钮 */
.floating-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 50px;
  padding: 10px 18px;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}
.floating-btn:hover {
  background: #2563eb;
}
</style>
