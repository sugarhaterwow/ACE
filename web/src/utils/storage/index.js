import { createStorage } from './storage'

const prefixKey = ''

export const createLocalStorage = function (option = {}) {
  return createStorage({
    prefixKey: option.prefixKey || '',
    storage: localStorage,
  })
}

export const createSessionStorage = function (option = {}) {
  return createStorage({
    prefixKey: option.prefixKey || '',
    storage: sessionStorage,
  })
}

// 创建一个本地永久存储实例
export const lStorage = createLocalStorage({ prefixKey })
// 创建一个会话临时存储实例
export const sStorage = createSessionStorage({ prefixKey })
