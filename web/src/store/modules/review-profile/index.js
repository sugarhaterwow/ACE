// stores/criteria-profile.ts
import { defineStore } from 'pinia'

export const useCriteriaProfileStore = defineStore('ReviewProfileStore', {
    state: () => ({
        selectedProfile: { updated: false, saved: false, form: {} },
        variableCriteria: { updated: false, saved: false, form: {} },
        exemptionLists: { updated: false, saved: false, form: {} }
  }),
    actions: {
       
        loadFromLocal() {
            const raw1 = localStorage.getItem('selectedProfile')
            const raw2 = localStorage.getItem('variableCriteria')
            const raw3 = localStorage.getItem('exemptionLists')

            if (raw1) this.selectedProfile.form = JSON.parse(raw1)
            if (raw2) this.variableCriteria.form = JSON.parse(raw2)
            if (raw3) this.exemptionLists.form = JSON.parse(raw3)
        },
        saveAll() {
            const raw1 = localStorage.getItem('selectedProfile')
            const raw2 = localStorage.getItem('variableCriteria')
            const raw3 = localStorage.getItem('exemptionLists')

            const allData = [
                raw1 ? JSON.parse(raw1) : {},
                raw2 ? JSON.parse(raw2) : {},
                raw3 ? JSON.parse(raw3) : {}
            ]

            console.log('Submitted data:', allData)
            // TODO: 替换成你的 API 请求

            // 重置状态（保留 form）
            this.selectedProfile.updated = false; this.selectedProfile.saved = false
            this.variableCriteria.updated = false; this.variableCriteria.saved = false
            this.exemptionLists.updated = false; this.exemptionLists.saved = false
        }
    }
    
})