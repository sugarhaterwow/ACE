


<template>
  <AppPage title="Create a Tender Review job" show-footer>
  
    <n-card
      size="medium"
      :segmented="{ content: true, footer: true }"
      style="border-radius: 12px; margin: 50px auto; width: 95%;"
    >
    
      <!-- 时间轴 -->
      <template #header>
      
        <div style="width: 120%; display: flex; justify-content: center">
          <n-timeline
            horizontal
            style="margin-top: 30px; width: 80%;"
          >
            <n-timeline-item
              v-for="(step, index) in steps"
              :key="index"
              :title="step.title"
              :type="index <= currentStep ? 'info' : 'default'"
              line-type="solid"
              style="flex: 1; display: flex; flex-direction: row; justify-content: left;"
            />
              
          </n-timeline>
        </div>
      </template>


      <!-- 内容区域 -->
      <div style="width: 90%; margin: 20px auto; box-sizing: border-box; height: auto;">
        <component
          :is="steps[currentStep].component"
        />
      </div>

      <!-- 底部区域 -->
      <template #footer>
        <component :is="steps[currentStep].footer" />
      </template>
    </n-card>
    
  </AppPage>
</template>

<script setup lang="ts">

import { h, ref, onMounted } from 'vue'
import { NButton, useDialog, useMessage, useNotification } from 'naive-ui'
import { useRouter } from 'vue-router'

import Upload from './Upload.vue'
import ReviewProfile from './ReviewProfile.vue'

import EditSubmit from './EditSubmit/index.vue'

import { useStepStore } from '@/store/modules/step'

const dialog = useDialog()
const message = useMessage()
const notification = useNotification()

const stepCount = 3
const currentStep = ref(0)
const hasSuccess = ref(false)


const router = useRouter()


// 每个步骤的“是否保存过”标记
const everSavedArr = ref<boolean[]>(Array(stepCount).fill(false))

// 每次进入新页面时，重置该步骤的保存标记
watch(currentStep, (newStep) => {
  everSavedArr.value[newStep] = false
})

// 使用 Pinia store
const stepStore = useStepStore()

// 页面加载时恢复
onMounted(() => {
  stepStore.loadFromLocal()
})

const stepRefs = ref<any[]>([])
// 深比较函数
const deepEqual = (a: any, b: any) => JSON.stringify(a) === JSON.stringify(b)

const goPrev = () => {
  if (currentStep.value > 0) currentStep.value -= 1
}
const goNext = () => {
  if (currentStep.value < steps.length - 1) currentStep.value += 1
}

const tempForms = ref<Record<number, StepForm>>({})

const prevPage = () => {
  if (currentStep.value === 0) return // 已经是第一页了

  const idx = currentStep.value
  const state = stepStore.stepStates[idx]
  const comp = stepRefs.value[idx]

  // 1. 获取子组件当前临时态
  const tempForm = comp?.getTempForm ? comp.getTempForm() : state.form

  if (!everSavedArr.value[idx]) {
    
    // 2. 对比临时态和已保存快照
    const hasDiff = !deepEqual(tempForm, state.form)
    state.updated = hasDiff
    if (hasDiff) state.saved = false

  }

  // 3. 校验必填项
  if (comp && typeof comp.validate === 'function') {
    const valid = comp.validate()
    if (!valid) return
  }

  console.log(state.updated, state.saved)

  // 4. 如果有改动但未保存 → 提示用户
  if (!state.saved && state.updated) {
    // 有未保存的改动 → 必须保存
    dialog.warning({
      title: 'Unsaved changes',
      content: 'You have unsaved changes on this page. Please save before continuing.',
      positiveText: 'Save',
      onPositiveClick: () => {
        const ok = stepStore.saveStep(idx, tempForm)
        if (ok) {
          message.success('Saved successfully!')
          goPrev()
        } else {
          message.error('Save failed!')
        }
      }
    })
    return
  }

  if (!state.saved && !state.updated) {
    // 没有改动 → 可以直接继续
    dialog.warning({
        title: 'No changes detected',
        content: 'There are no new changes on this page. Do you want to continue?',
        positiveText: 'Continue',
        negativeText: 'Cancel',
        onPositiveClick: () => {
          goPrev()
        }
    })
    return
  }

  if (state.saved && !state.updated) {
    // 已保存且没有新改动 → 直接继续
    dialog.warning({
        title: 'No changes detected',
        content: 'There are no new changes on this page. Do you want to continue?',
        positiveText: 'Continue',
        negativeText: 'Cancel',
        onPositiveClick: () => {
          goPrev()
        }
    })
    return
  }

  if (state.saved && state.updated) {
    // 已保存且有新改动 → 直接继续
    goPrev()
    return
  }

}

const nextPage = () => {
  if (currentStep.value === 0) { 
    goNext() 
    return 
  }
  const idx = currentStep.value
  const state = stepStore.stepStates[idx]
  const comp = stepRefs.value[idx]
  // 1. 从子组件拿当前临时态（子组件需 defineExpose({ getTempForm })
  const tempForm = comp?.getTempForm ? comp.getTempForm() : state.form

  if (!everSavedArr.value[idx]) {
    
    // 2. 对比临时态和已保存快照
    const hasDiff = !deepEqual(tempForm, state.form)
    state.updated = hasDiff
    if (hasDiff) state.saved = false

  }

  
  // 3. 校验必填项
      if (comp && typeof comp.validate === 'function') {
        const valid = comp.validate()
        if (!valid) return
      }
  console.log("updated:",state.updated, "saved:", state.saved)
  console.log("现在填写的内容", JSON.stringify(tempForm), "父组件保存的内容", JSON.stringify(state.form))


  // 4. 判断保存状态
  if (!state.saved && state.updated) {
    // 有未保存的改动 → 必须保存
    dialog.warning({
      title: 'Unsaved changes',
      content: 'You have unsaved changes on this page. Please save before continuing.',
      positiveText: 'Save',
      onPositiveClick: () => {
        const ok = stepStore.saveStep(idx, tempForm)
        if (ok) {
          message.success('Saved successfully!')
          goNext()
        } else {
          message.error('Save failed!')
        }
      }
    })
    return
  }

  if (!state.saved && !state.updated) {
    // 没有改动 → 可以直接继续
    dialog.warning({
        title: 'No changes detected',
        content: 'There are no new changes on this page. Do you want to continue?',
        positiveText: 'Continue',
        negativeText: 'Cancel',
        onPositiveClick: () => {
          goNext()
        }
    })
    return
  }

  if (state.saved && !state.updated) {
    // 已保存且没有新改动 → 直接继续
    dialog.warning({
        title: 'No changes detected',
        content: 'There are no new changes on this page. Do you want to continue?',
        positiveText: 'Continue',
        negativeText: 'Cancel',
        onPositiveClick: () => {
          goNext()
        }
    })
    return
  }
  if (state.saved && state.updated) {
    // 已保存且有新改动 → 直接继续
    goNext()
    return
  }
}


// 最后一步统一提交
const submitAll = () => {
  const needCheckSteps = [1]

  const notSavedSteps = needCheckSteps.filter(
    idx => !stepStore.stepStates[idx].saved
  )

  if (notSavedSteps.length > 0) {
    const titles = notSavedSteps.map(idx => steps[idx].title).join(', ')
    message.warning(`The following steps are not saved: ${titles}`)
    return
  }

  // 全部保存了，才允许提交
  stepStore.submitAll()
  message.success('Task submitted, processing started...')

 goNext() 

}

// 步骤定义
const steps = [
  {
    title: 'Document Upload',
    component: () =>
      h(Upload, {
        form: stepStore.stepStates[currentStep.value].form, // 固定第0步
        hasSuccess: hasSuccess.value,
        'onUpdate:hasSuccess': (v: boolean) => (hasSuccess.value = v)
      }),
    footer: () =>
      h('div', { style: 'display:flex;justify-content:space-between;padding:0 16px;' }, [
        h('div'),
        hasSuccess.value
          ? h(NButton, { type: 'primary', ghost: true, onClick: nextPage }, { default: () => 'Next Page' })
          : null
      ])
  },
  {
    title: 'Review Profile',
    component: () =>
      h(ReviewProfile, {
        ref: (el: any) => (stepRefs.value[currentStep.value] = el), 
        form: stepStore.stepStates[currentStep.value].form, 
        onSave: (v: StepForm) => {
          const ok = stepStore.saveStep(currentStep.value, v)
          if (ok) {
            message.success('Saved successfully!')
            everSavedArr.value[currentStep.value] = true
          } else {
            message.error('Save failed!')
          }
        }
      }),
    footer: () =>
      h('div', { style: 'display: flex; justify-content: space-between; padding: 0 16px;' }, [
        h(NButton, { type: 'primary', ghost: true, onClick: prevPage }, { default: () => 'Back' }),
        h(NButton, { type: 'primary', ghost: true, onClick: submitAll }, { default: () => 'Submit Job' })
      ])
  },
  {
    title: 'Edit Submit',
    component: () =>
      h(EditSubmit, {
        
        
        onSave: (v: StepForm) => {
          const ok = stepStore.saveStep(currentStep.value, v)
          if (ok) {
            message.success('Saved successfully!')
            everSavedArr.value[currentStep.value] = true
          } else {
            message.error('Save failed!')
          }
        }
      })
  }
]


</script>

