import { defineStore } from 'pinia'

export const useProjectStore = defineStore('projectStore', {
  state: () => ({
    projectName: ''  // 保存项目名称
  }),
  actions: {
    setProjectName(name) {
      this.projectName = name
      sessionStorage.setItem('projectName', name)  // 存储到 sessionStorage
    },
    loadProjectName() {
      const name = sessionStorage.getItem('projectName')
      console.log("Current project name:", name)
      if (name) {
        this.projectName = name
      }
      return name
    },
    clearProjectName() {
      this.projectName = ''
      sessionStorage.removeItem('projectName')  // 从 sessionStorage 清除
    }
  }
})
