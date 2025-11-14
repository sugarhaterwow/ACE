<template>
  <transition name="fade-slide" mode="out-in" appear>
    <section class="cus-scroll-y wh-full flex-col bg-[#f5f6fb] p-15 dark:bg-hex-121212">
      <!-- 显示标题 -->
      <h1 v-if="title" class="text-30 font-bold mb-3 text-hex-333 dark:text-hex-ccc">
        {{ title }}
      </h1>

      <!-- 插槽内容 -->
      <slot />

      <!-- 页脚 -->
      <AppFooter v-if="showFooter" mt-15 />

      <!-- 返回顶部按钮 -->
      <n-back-top :bottom="20" />
    </section>
  </transition>
</template>

<script setup>
defineProps({
  showFooter: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: '',
  },
})
</script>
