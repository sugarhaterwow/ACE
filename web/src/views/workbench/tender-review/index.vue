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

import { h, ref, onMounted, onBeforeUnmount } from 'vue'
import { NButton, useDialog, useMessage, useNotification } from 'naive-ui'

import ProjectSetup from './ProjectSetup.vue'
import Upload from './Upload.vue'
import ReviewProfile from './ReviewProfile.vue'
import EditSubmit from './EditSubmit/index.vue'
import api from '@/api'
import { onBeforeRouteLeave } from 'vue-router'


onMounted(() => {
  window.addEventListener('beforeunload', handleBeforeUnload)
})


onBeforeUnmount(() => {
  window.removeEventListener('beforeunload', handleBeforeUnload)
})

function handleBeforeUnload(e: BeforeUnloadEvent) {
  // 如果有未保存的修改，就提示
  if (1) {
    e.preventDefault()
    e.returnValue = ''   // Chrome/Firefox 必须设置 returnValue 才会触发提示
  }
}



onBeforeRouteLeave((to, from, next) => {
  if (1) {
    // 有未保存修改 → 弹窗确认
    dialog.warning({
      title: 'Unsaved changes',
      content: 'You have unsaved changes. Are you sure you want to leave?',
      positiveText: 'Leave',
      negativeText: 'Stay',
      onPositiveClick: () => {
        // 用户点击“离开” → 执行函数
        api.deleteProject(projectName.value)
        next()
      },
      onNegativeClick: () => next(false) // 取消跳转
    })
  } else {
    next()
  }
})


const dialog = useDialog()
const message = useMessage()
const notification = useNotification()

// 总步骤数
const stepCount = 4
// 初始步骤：第一步
const currentStep = ref(0)
// 保存每一次独立job的任务名
const projectName = ref<string>('')
// 保存上传步骤的文件
const uploadFile = ref<File | null>(null)
// 第一步和第二步出现Next Page按钮的标志
const stepSuccess = ref({
  projectSetup: false,
  upload: false,
})
// 第三步的子组件实例
const reviewProfileRef = ref()



// 回到前一步骤
const goPrev = () => {
  if (currentStep.value > 0) currentStep.value -= 1
}
// 前往下一步骤
const goNext = () => {
  if (currentStep.value < steps.length - 1) currentStep.value += 1
}


const prevPage = () => {
  if (currentStep.value === 0) return // 已经是第一页了

  const idx = currentStep.value
  goPrev()
}

const nextPage = () => {
  if (currentStep.value === 2) { 
    return 
  }
  const idx = currentStep.value
  
  // 已保存且有新改动 → 直接继续
  goNext()
    
}

// 最后一步统一提交：
// 情况 1：初始为空 + 没修改 → 提示 "No changes made on this page. Please fill in required fields before submitting."
// 情况 2：没修改 + 必填项都有值 → 弹窗确认 "No changes made. Submit already saved configuration?"
// 情况 3：修改了但没保存 → 弹窗确认 "You have unsaved changes. Proceed without saving current configuration?"
// 情况 4：修改并保存过 → 直接提交后端已保存的配置。


const submitAll = () => {
  const comp = reviewProfileRef.value
  console.log(comp)
  if (!comp) return
  const tempForm = comp.getTempForm()
  const isModified = comp.isModified //是否修改
  const hasRequired = comp.validate() // 所有必填项都填写
  const hasSaved = comp.hasSaved // 是否保存
  console.log("修改：", isModified, "必填：", hasRequired, "保存：", hasSaved)

  if (!hasRequired) {
    // 情况 1
    message.warning("Please fill in required fields before submitting.")
    return
  }
  else {
    if (!isModified) {
      // 没修改没保存/没修改保存了：提示页面没变化，是否提交已保存的配置？
      dialog.warning({
        title: "No changes detected",
        content: "No changes made on this page. Do you want to submit the already saved configuration?",
        positiveText: "Confirm",
        negativeText: "Cancel",
        onPositiveClick: () => {
          api.submitJob(tempForm)
          message.success("Submitted successfully!")
          goNext()
        }
      })
      return
    }

        
    if (!hasSaved && isModified) {
      // 保存了没修改：提示页面没变化，是否提交已保存的配置？
      dialog.warning({
        title: "Unsaved changes",
        content: "You have unsaved changes. Proceed without saving current configuration?",
        positiveText: "Confirm",
        negativeText: "Cancel",
        onPositiveClick: () => {
          api.submitJob(tempForm)
          message.success("Submitted successfully!")
          goNext()
        }
      })
      return
    }
    
    if (hasSaved && isModified) {
      // 保存了并且有修改：直接提交
      dialog.success({
        title: "Ready to submit",
        content: "You have saved and modified configuration. Submit now?",
        positiveText: "Submit",
        negativeText: "Cancel",
        onPositiveClick: () => {
          api.submitJob(tempForm)
          message.success("Submitted successfully!")
          goNext()
        }
      })
      return
    }
  
  }
}


// 步骤定义
const steps = [
  {
    title: 'ProjectSetup',
    component: () =>
      h(ProjectSetup, {
        projectName: projectName.value,
        'onUpdate:projectName': (v: string) => (projectName.value = v),
        hasSuccess: stepSuccess.value.projectSetup,
        'onUpdate:hasSuccess': (v: boolean) => (stepSuccess.value.projectSetup = v)
      }),
    footer: () =>
      h('div', { style: 'display:flex;justify-content:space-between;padding:0 16px;' }, [
        h('div'),
        stepSuccess.value.projectSetup
          ? h(NButton, { type: 'primary', ghost: true, onClick: nextPage }, { default: () => 'Next Page' })
          : null
      ])

  },
  {
    title: 'Document Upload',
    component: () =>
      h(Upload, {
        projectName: projectName.value,
        file: uploadFile.value,
        hasSuccess: stepSuccess.value.upload,
        'onUpdate:file': (f: any) => (uploadFile.value = f),
        'onUpdate:hasSuccess': (v: boolean) => {
          console.log("upload button",v)
          stepSuccess.value.upload = v
          }
      }),
    footer: () =>
      h('div', { style: 'display:flex;justify-content:space-between;padding:0 16px;' }, [
        h('div'),
        stepSuccess.value.upload
          ? h(NButton, { type: 'primary', ghost: true, onClick: nextPage }, { default: () => 'Next Page' })
          : null
      ])
  },
  {
    title: 'Review Profile',
    component: () =>
      h(ReviewProfile, {
        ref: reviewProfileRef  // 父组件定义的 ref，用来拿子组件实例
        // form: stepStore.stepStates[currentStep.value].form, 
        
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
      h(EditSubmit)
  }
]


</script>

 