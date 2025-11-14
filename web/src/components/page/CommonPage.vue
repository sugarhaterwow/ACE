<template>
  <AppPage :show-footer="showFooter">
    <header v-if="showHeader" mb-15 min-h-45 flex items-center justify-between px-15>
      <slot v-if="$slots.header" name="header" />
      <template v-else>
        <div class="flex flex-col">
          <h1 class="text-30 font-bold text-hex-333 mb-3 dark:text-hex-ccc">
            {{ title || route.meta?.title }}
          </h1>
          <p v-if="subTitle" class="text-14 text-gray-500 mt-1">
            {{ subTitle }}
          </p>
        </div>
        <slot name="action" />
      </template>
    </header>

    <n-card flex-1 rounded-10>
      <slot />
    </n-card>
  </AppPage>
</template>

<script setup>
defineProps({
  showFooter: {
    type: Boolean,
    default: false,
  },
  showHeader: {
    type: Boolean,
    default: true,
  },
  title: {
    type: String,
    default: undefined,
  },
  subTitle: {
    type: String,
    default: undefined,
  }
})
const route = useRoute()
</script>
