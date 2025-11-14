import { isNullOrUndef } from '@/utils'

class Storage {
  constructor(option) {
    this.storage = option.storage // 传入的存储对象，可以是 `sessionStorage` 或 `localStorage`
    this.prefixKey = option.prefixKey // 用于前缀化存储的 key，以防止 key 冲突
  }

  getKey(key) {
    return `${this.prefixKey}${key}`.toUpperCase()
  }

  set(key, value, expire) {
    const stringData = JSON.stringify({
      value,
      time: Date.now(),
      expire: !isNullOrUndef(expire) ? new Date().getTime() + expire * 1000 : null,
    })
    this.storage.setItem(this.getKey(key), stringData) // 将数据存入 localStorage 或 sessionStorage，存储的键是 getKey(key) 生成的带前缀的键
  }

  get(key) {
    const { value } = this.getItem(key, {})
    return value
  }

  getItem(key, def = null) {
    const val = this.storage.getItem(this.getKey(key))
    if (!val) return def
    try {
      const data = JSON.parse(val)
      const { value, time, expire } = data
      if (isNullOrUndef(expire) || expire > new Date().getTime()) {
        return { value, time }
      }
      this.remove(key)
      return def
    } catch (error) {
      this.remove(key)
      return def
    }
  }

  remove(key) {
    this.storage.removeItem(this.getKey(key))
  }

  clear() {
    this.storage.clear()
  }
}

export function createStorage({ prefixKey = '', storage = sessionStorage }) {
  return new Storage({ prefixKey, storage })
}
