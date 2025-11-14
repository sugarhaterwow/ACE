<template>
  <div
    bg="#fafafc"
    min-h-60
    flex
    items-start
    justify-between
    b-1
    rounded-8
    p-15
    bc-ccc
    dark:bg-black
  >
    <div class="flex-1 flex items-center justify-between gap-4">
      <slot />
    </div>

      <!-- 根据 props 控制按钮是否显示 -->
      <div v-if="showButtons">
        <n-button secondary type="primary" @click="emit('reset')">重置</n-button>
        <n-button ml-20 type="primary" @click="emit('search')">搜索</n-button>
      </div>
    
  </div>
</template>

<script setup>
const props = defineProps({
  showButtons: {
    type: Boolean,
    default: false // 默认不显示按钮
  }
})

const emit = defineEmits(['search', 'reset'])
</script>
