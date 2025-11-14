<template>
  <n-card
    class="w-full" style="border-radius: 12px"
    :content-style="{ padding: '16px' }"
    :header-style="{ fontWeight: '600', fontSize: '16px' }"
    :title="title"
  >
    <!-- 主体内容：图标 + 文字 -->
    <div style="display: flex; align-items: center; gap: 12px">
      <n-icon size="50" :color="iconColor" v-if="icon">
        <component :is="icon" />
      </n-icon>

      <div style="flex: 1">

        <div style="display: flex; align-items: baseline; gap: 6px;">
          <div :style="mainTextStyle">{{ mainText }}</div>
          <div :style="timeUnitStyle">{{ timeUnit }}</div>
        </div>

        <div style="margin-top: 6px; display: flex; align-items: baseline;">
          <span :style="subNumberStyle">
            {{ subNumber }}
          </span>
          <span :style="subLabelStyle"> 
            {{ subLabel }}
          </span>
        </div>

        <div :style="descriptionStyle">
          {{ description }}
        </div>
      </div>

    </div>

    <!-- 底部动态箭头 -->
    <div
      v-if="trend"
      :style="{
        color: trend.color,
        fontSize: '14px',
        display: 'flex',
        alignItems: 'center',
        gap: '4px',
        marginTop: '12px'
      }"
    >
      <span
        :class="['arrow', trend.direction]"
      >
        {{ trend.direction === 'up' ? '▲' : '▼' }}
      </span>
      <span>{{ trend.value }} {{ trend.label }}</span>
    </div>
  </n-card>
</template>

<script setup lang="ts">
import { NIcon } from 'naive-ui'


defineProps<{
  mainText?: string
  timeUnit?: string 
  subNumber?: string | number
  subLabel?: string
  description?: string
  icon?: any
  iconColor?: string
  trend?: {
    value: string
    direction: 'up' | 'down'
    label: string
    color: string
  }
  mainTextStyle?: Record<string, string>
  subNumberStyle?: Record<string, string>
  subLabelStyle?: Record<string, string>
  descriptionStyle?: Record<string, string>
}>()

</script>

<style scoped>
.arrow {
  display: inline-block;
  animation: bounce 1s infinite;
}
.arrow.up {
  animation-name: bounce-up;
}
.arrow.down {
  animation-name: bounce-down;
}

@keyframes bounce-up {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

@keyframes bounce-down {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(3px); }
}
</style>
