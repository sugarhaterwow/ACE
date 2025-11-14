/** 重置样式 */
import '@/styles/reset.css'
import 'uno.css'
import '@/styles/global.scss'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { setupRouter } from '@/router'
import { setupStore } from '@/store'
import App from './App.vue'
import { setupDirectives } from './directives'
import { useResize } from '@/utils'
import i18n from '~/i18n'
import naive from 'naive-ui'


async function setupApp() {
  const app = createApp(App)
  // 通过 setupStore 创建并注册 Pinia
  setupStore(app)

  await setupRouter(app)
  setupDirectives(app)
  app.use(useResize)
  app.use(i18n)
  app.use(naive) 
  app.mount('#app')
}

setupApp()
