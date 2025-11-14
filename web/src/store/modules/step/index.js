// src/stores/stepStore.js
import { defineStore } from 'pinia'

export const useStepStore = defineStore('stepStore', {
  state: () => ({
    stepStates: [
      { updated: false, saved: false, form: { uploadedFiles: []} },
      { updated: false, saved: false, form: {} },
    ]
  }),
  actions: {
    saveStep(idx, formData) {
      if (idx < 0 || idx >= this.stepStates.length) return false
    
      const oldForm = this.stepStates[idx].form || {}
      const newForm = JSON.parse(JSON.stringify(formData))

      console.log("former form:", JSON.stringify(oldForm))
      console.log("now form:", JSON.stringify(formData) )
    
      const isEqual = JSON.stringify(oldForm) === JSON.stringify(newForm)
    
      this.stepStates[idx].form = newForm
      this.stepStates[idx].saved = true
      this.stepStates[idx].updated = !isEqual   // 统一判断
      console.log("按保存键保存：", this.stepStates[idx].saved)
      console.log("按保存键更新：", this.stepStates[idx].updated)
      localStorage.setItem(`tenderReviewSteps:${idx}`, JSON.stringify(newForm))
      return true
    },
    loadFromLocal() {
      for (let i = 0; i < this.stepStates.length; i++) {
        const raw = localStorage.getItem(`tenderReviewSteps:${i}`)
        if (raw) {
          this.stepStates[i].form = JSON.parse(raw)
          
        }
      }
    },
    submitAll() {
      const allData = []
      for (let i = 0; i < this.stepStates.length; i++) {
        const raw = localStorage.getItem(`tenderReviewSteps:${i}`)
        allData.push(raw ? JSON.parse(raw) : {})
      }

      console.log('Submitted data:', allData)
      // TODO: 这里替换成你的 API 请求

      // 清空本地存储和状态
      for (let i = 0; i < this.stepStates.length; i++) {
        // localStorage.removeItem(`tenderReviewSteps:${i}`)
        this.stepStates[i].updated = false
        this.stepStates[i].saved = false
        // 保留原来的 form，不做修改

      }
    }
  }
})
