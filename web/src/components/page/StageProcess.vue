<template>
  <NModal
    v-model:show="visible"
    preset="card"
    title="Analysing Your Document..."
    style="width: 600px"
    :header-style="{ textAlign: 'center' }"
    :closable="currentStage >= 2"
    :maskClosable="currentStage >= 2"
  >
    <div class="text-gray-600 mb-6 text-center">
      Please wait while your document is being processed for analysis.
    </div>


    <div class="progress-container">
      <div v-for="(stage, index) in stages" :key="index" class="stage">
        <!-- 圆点 -->
        <div class="circle" :class="{ completed: index < currentStage, active: index === currentStage }">
          <span v-if="index < currentStage">✔</span>
          <span v-else>{{ index + 1 }}</span>
        </div>

        <!-- 标签 -->
        <div class="label" :class="{ completed: index < currentStage, active: index === currentStage }">
          {{ stage }}
        </div>

        <!-- 连线（保证每个阶段之间都有） -->
        <div v-if="index < stages.length - 1" class="line">
          <div class="line-fill" :style="{ width: connectorFillWidth(index) }" />
        </div>
      </div>
    </div>
  </NModal>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { NModal } from 'naive-ui'

const visible = ref(true)

const stages = [
  'Ingestion',
  'Entity Extraction',
  'Search and Highlight',
  'Clause Alignment'
]

const currentStage = ref(0)   // 当前阶段 index
const stageProgress = ref(0)  // 当前阶段内进度 0~100

// 每条连线的填充宽度
function connectorFillWidth(index) {
  if (index < currentStage.value) return '100%'
  if (index === currentStage.value) return `${stageProgress.value}%`
  return '0%'
}

// 模拟推进
onMounted(() => {
  const timer = setInterval(() => {
    if (currentStage.value < stages.length - 1) {
      if (stageProgress.value < 100) {
        stageProgress.value += 5
      } else {
        stageProgress.value = 0
        currentStage.value++
      }
    } else {
      clearInterval(timer)
      visible.value = false // 可选：完成后关闭
    }
  }, 200)
})
</script>

<style scoped>
.progress-container {
  display: flex;
  align-items: center;
  padding: 20px 0;
}
.stage {
  display: flex;
  align-items: center;
  flex: 1;
}
.circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #ccc;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}
.circle.completed { background: #2d8cf0; }
.circle.active { background: #18a058; }
.label {
  margin-left: 8px;
  font-size: 14px;
  color: #888;
}
.label.completed { color: #2d8cf0; }
.label.active { color: #18a058; }
.line {
  flex: 1;
  height: 4px;
  background: #ccc;
  margin: 0 8px;
  border-radius: 999px;
  overflow: hidden;
}
.line-fill {
  height: 100%;
  background: linear-gradient(90deg, #2d8cf0, #18a058);
  transition: width 0.2s linear;
}
</style>
