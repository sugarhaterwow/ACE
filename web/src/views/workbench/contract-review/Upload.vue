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


const emit = defineEmits(['update:hasSuccess'])
const props = defineProps<{ form: { uploadedFiles: any[] } }>()

const message = useMessage()

const uploadedFiles = ref([])

// 同步父组件传入的 form.uploadedFiles（用于刷新回显）
watch(
  () => props.form.uploadedFiles,
  (newVal) => {
    uploadedFiles.value = Array.isArray(newVal) ? [...newVal] : []
  },
  { immediate: true, deep: true }
)


// 监听文件状态变化，更新父组件的 hasSuccess
watch(uploadedFiles, (files) => {
  // ✅ 判断是否有成功文件
  const hasSuccess = files.some(f => f.status === 'success')
  emit('update:hasSuccess', hasSuccess)
  
}, { deep: true, immediate: true })


// 文件选择处理
const handleFileChange = ({ fileList }) => {
  fileList.forEach(f => {
    // 如果已存在同名文件，就跳过
    if (!uploadedFiles.value.some(existing => existing.name === f.name)) {
      uploadedFiles.value.push({
        name: f.name,
        size: (f.file?.size / 1024).toFixed(2),
        raw: f.file,
        progress: 0,
        status: "pending"
      })
    } else {
      message.warning(`File "${f.name}" already exists and will be skipped.`)
    }
  })
}


// 删除文件
const handleFileDelete = (file) => {
  uploadedFiles.value = uploadedFiles.value.filter(f => f.name !== file.name)
  const successfulFiles = uploadedFiles.value.filter(f => f.status === 'success')
  props.form.uploadedFiles = successfulFiles
  localStorage.setItem("tenderReviewSteps:0", JSON.stringify({ uploadedFiles: successfulFiles }))
}

// 上传所有文件
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

  message.info("Uploading files...")
  const successFiles = []
  const failedFiles = []

  for (const file of pendingFiles) {
    await uploadSingleFile(file)
    if (file.status !== "success") {
      failedFiles.push(file.name)
    }
    
  }
  const successfulFiles = uploadedFiles.value.filter(f => f.status === 'success')
props.form.uploadedFiles = successfulFiles
localStorage.setItem("tenderReviewSteps:0", JSON.stringify({uploadedFiles: successfulFiles}))


  if (failedFiles.length > 0) {
    message.error(`Some files failed to upload: ${failedFiles.join(", ")}`)
  } else {
    message.success("All new files uploaded successfully.")
  }
}



// 单个文件上传（带进度）
function uploadSingleFile(file) {
  return new Promise((resolve) => {
    file.status = "uploading"
    file.progress = 0
    let progress = 0

    const interval = setInterval(() => {
      progress += 10
      file.progress = progress

      if (progress >= 100) {
        clearInterval(interval)
        const success = Math.random() > 0.1
        if (success) {
          file.status = "success"
          file.progress = 100
          resolve()
        } else {
          file.status = "error"
          file.progress = 0
          resolve()
        }
      }
    }, 100)
  })
}

// 重试上传
const retryUpload = async (file) => {
  await uploadSingleFile(file)
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