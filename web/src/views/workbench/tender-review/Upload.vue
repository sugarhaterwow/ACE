<template>
  <n-card 
    title="Upload Tender Document" 
    size="large" 
    embedded 
    style="width: 100%; box-sizing: border-box; overflow-x: hidden;"
  >
    <p style="color: #555; margin-bottom: 20px">
      Upload and configure your tender document for AI-powered analysis
    </p>

    <!-- Upload Area -->
    <n-upload
      multiple
      directory-dnd
      :default-upload="false"
      :on-change="handleFileChange"
      :show-file-list="false"
      accept=".pdf,.doc,.docx"
      style="border: 2px dashed #ccc; background-color: #eef2ff; padding: 30px; text-align: center; border-radius: 8px;"
    >
      <div>
        <!-- 图标行 -->
        <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 10px;">

          <n-icon :size="50" color="#0073e6">
              <DocumentTextOutline />
            </n-icon>

            <n-icon :size="50" color="#0073e6">
              <DocumentAttachOutline />
            </n-icon>

            <n-icon :size="50" color="#0073e6">
              <DocumentOutline />
            </n-icon>
        </div>
        <p>
          Drag and drop your files here or
          <span style="color: #0073e6; cursor: pointer;"> Select a file </span>
        </p>
        <n-button style="margin-top: 10px;"> Select files </n-button>
      </div>
    </n-upload>

    <div class="upload-settings" style="margin-top: 24px">
      <p style="font-size: 12px; color: #777; margin-bottom: 10px;">
        Supported formats: PDF, DOC, DOCX, files up to 100 MB / 1000 pages each
      </p>

      <!-- Flex container: select on left, button on right -->
      <div style="display: flex; justify-content: flex-end; align-items: center; gap: 10px;">
        <!-- <n-select -->
        <!--   v-model:value="selectedFolder" -->
        <!--   :options="folderOptions" -->
        <!--   style="width: 200px;" -->
        <!-- /> -->

        <n-button
          type="primary"
          style="background-color: #0050b3; color: #fff; border-color: #0050b3;"
          @click="handleFileUpload"
        >
          Upload Files
        </n-button>
      </div>
    </div>

    <!-- Uploaded Files List -->
    <div style="margin-top: 20px;">
      <h3 style="margin-bottom: 10px;">Uploaded Files</h3>
      <div style="display: flex; flex-direction: column; gap: 16px;">
        <div
          v-for="file in uploadedFiles"
          :key="file.name"
          style="border: 1px solid #ccc; border-radius: 8px; padding: 16px; background: #f9f9f9;"
        >
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
              <strong>{{ file.name }}</strong>
              <p style="font-size: 12px; color: #666;">{{ file.size }} KB</p>
            </div>

            <div style="display: flex; align-items: center; gap: 10px;">
              <n-progress
                v-if="file.status === 'uploading'"
                type="line"
                :percentage="file.progress"
                style="width: 120px;"
              />

              <n-button
                v-if="file.status === 'success'"
                type="success"
                size="small"
                @click="downloadFile(file)"
              >
                Download
              </n-button>

              <n-button
                v-if="file.status === 'error'"
                type="error"
                size="small"
                @click="retryUpload(file)"
              >
                Retry
              </n-button>

              <n-button
                type="error"
                size="small"
                @click="handleFileDelete(file)"
              >
                Delete
              </n-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    
    
  </n-card>
</template>

<script setup lang="ts">
import { h, ref, watch, computed } from "vue"
import { useMessage } from "naive-ui"
import { DocumentTextOutline, DocumentAttachOutline, DocumentOutline } from "@vicons/ionicons5"
import api from '@/api'

// 获取父组件传过来的三个变量：项目名、已上传的文件和Next Page是否出现的标志
const props = defineProps({
  projectName: String,
  file: {
    type: Array,
    default: () => []
  },
  hasSuccess: Boolean
})

// 当父组件传来的两个变量变化，要告诉父组件以修改它的值
const emit = defineEmits(['update:file', 'update:hasSuccess'])
// 本地副本：上传的文件
const uploadedFiles = ref([...(props.file ?? [])])
const message = useMessage()


// 文件选择处理（每新增一个文件都会调用一次这个函数。）：只处理新增文件
const handleFileChange = ({ file }) => {
  // 判断是否已存在同名文件
  if (!uploadedFiles.value.some(
    existing =>
      existing.name === file.name
  )) {
      uploadedFiles.value.push({
        name: file.name,
        size: (file.file?.size / 1024).toFixed(2), // KB
        raw: file.file,                            // 原始 File 对象
        progress: 0,                               // 初始进度
        status: "pending"                          // 初始状态
      })
  } else {
    message.warning(`File "${file.name}" already exists and will be skipped.`)
  }
}


// 上传文件
const handleFileUpload = async () => {
  if (uploadedFiles.value.length === 0) {
    message.warning("No files to upload!")
    return
  }

  // 只取出未上传成功的文件
  const pendingFiles = uploadedFiles.value.filter(f => f.status !== "success")

  if (pendingFiles.length === 0) {
    message.info("All files already uploaded successfully, nothing to do.")
    return
  }

  const formData = new FormData()
  formData.append("folder", props.projectName) // 用父组件传来的 projectName

  uploadedFiles.value.forEach(file => {
    formData.append("files", file.raw)
  })

  try {
    message.info("Uploading files...")
    const res = await api.uploadFiles(formData)

    message.success(res.msg)
    console.log("成功上传:", res)

    const successFiles = res.data.success || []
    const failedFiles = res.data.failed || []

    // 更新 uploadedFiles 的状态
    uploadedFiles.value.forEach(f => {
      if (successFiles.includes(f.name)) {
        f.status = "success"
        f.progress = 100
      } else if (failedFiles.includes(f.name)) {
        f.status = "failed"
      }
    })

    // 把上传成功的文件更新到父表单里
    const successfulFiles = uploadedFiles.value.filter(f => f.status === "success")
    emit('update:file', JSON.parse(JSON.stringify(successfulFiles)))

    // 更新 hasSuccess：只要有成功文件就设为 true
    if (successfulFiles.length === 0) {
      emit('update:hasSuccess', false)
      message.warning("You must upload at least one file before proceeding to the next step.")
    } else {
      emit('update:hasSuccess', true)
    }

    if (failedFiles.length > 0) {
      message.error(`Some files failed to upload: ${failedFiles.join(", ")}`)
    } else {
      message.success("All new files uploaded successfully.")
    }
  } catch (err) {
    message.error("Upload failed: " + (err.response?.data?.message || err.message))
    // 全部标记为失败
    uploadedFiles.value.forEach(f => {
      f.status = "failed"
    })

    // 同步失败状态给父组件
    const successfulFiles = uploadedFiles.value.filter(f => f.status === "success")
    emit('update:file', JSON.parse(JSON.stringify(successfulFiles)))
    // 更新 hasSuccess：只要有成功文件就设为 true
    if (successfulFiles.length === 0) {
      emit('update:hasSuccess', false)
      message.warning("You must upload at least one file before proceeding to the next step.")
    } else {
      emit('update:hasSuccess', true)
    }
  }
}

// 删除文件
const handleFileDelete = async (file) => {
  // 在 uploadedFiles 里查找匹配的文件
  const target = uploadedFiles.value.find(
    f => f.name === file.name)
  // 判断状态
  if (!target || target.status !== "success") {
    message.warning(`File "${file.name}" has not been uploaded successfully and cannot be deleted.`)
    return
  }

  // 调用后端删除接口
  try {
    const res = await api.deleteFile(props.projectName, file.name)
    message.success(res.msg)
    console.log("后端删除成功:", res)

    // 删除前端文件列表
    uploadedFiles.value = uploadedFiles.value.filter(
      f => !(f.name === file.name)
    )

    console.log("Delete uploadedFiles:", uploadedFiles.value)

    const successfulFiles = uploadedFiles.value.filter(f => f.status === "success")
    emit('update:file', JSON.parse(JSON.stringify(successfulFiles)))
    

    // 判断是否还有成功文件
    if (successfulFiles.length === 0) {
      emit('update:hasSuccess', false)
      message.warning("You must upload at least one file before proceeding to the next step.")
    } else {
      emit('update:hasSuccess', true)
    }


    // 清理 NaiveUI 内部 fileList
    const upload = document.querySelector('.n-upload')
    if (upload && upload.__vueParentComponent) {
      upload.__vueParentComponent.ctx.fileList = []
    }

  } catch (err) {
    message.error(`Failed to delete file: ${file.name}.`)
    console.error("后端删除错误:", err)
  }
  
}


// 重试上传
const retryUpload = async (file) => {
  await handleFileUpload()
}

// 模拟下载
const downloadFile = (file) => {
  const blob = new Blob(["Dummy content for " + file.name], { type: "application/octet-stream" })
  const link = document.createElement("a")
  link.href = URL.createObjectURL(blob)
  link.download = file.name
  link.click()
  URL.revokeObjectURL(link.href)
}




</script>