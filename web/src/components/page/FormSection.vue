<template>
  <n-card size="small" class="mb-4">
    <div class="mb-2">
      <div class="text-base font-bold">{{ title }}</div>
      <div class="text-sm text-gray-500">{{ subtitle }}</div>
    </div>
    <div class="flex flex-wrap gap-4">
      <slot />
    </div>
  </n-card>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  subtitle?: string
}>()
</script>
