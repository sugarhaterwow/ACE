<template>
  <n-card
    title="Project Setup"
    size="large"
    embedded
    style="width: 100%; box-sizing: border-box; overflow-x: hidden; padding: 20px 30px 60px;"
  >
    <!-- Title and Project Name Input Area -->
    
      
    <div style="display: flex; flex-direction: column; align-items: center; gap: 35px;">
      <h3 style="margin: 0; color: #333;">Create Project Name</h3>
      
      <n-input
        v-model:value="projectNameLocal"
        placeholder="Enter project name"
        clearable
        style="width: 400px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"
      />
      
      <n-button 
        type="primary" 
        size="large" 
        @click="checkAndCreateProject" 
        style="width: 400px; height: 35px; border-radius: 8px;"
      >
        Create Project
      </n-button>
    </div>

  </n-card>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useMessage } from 'naive-ui'
import api from '@/api'
import { onMounted, onBeforeUnmount } from 'vue'

// 获取父组件传过来的两个变量：项目名和Next Page是否出现的标志
const props = defineProps({
  projectName: String,
  hasSuccess: Boolean
})
// 当父组件传来的两个变量变化，要告诉父组件以修改它的值
const emit = defineEmits(['update:projectName', 'update:hasSuccess'])

// 本地副本：项目名
const projectNameLocal = ref(props.projectName || '')
const message = useMessage()


// 检查项目是否存在并创建
const checkAndCreateProject = async () => {
    try {
        // 发起请求并等待响应
        const projectInfo = await api.createProject({'job_name': projectNameLocal.value});

        console.log("Created project response:", projectInfo);
                     
        // 这里检查返回的 code 字段是否是成功的状态（假设 code 为 201 表示成功）
        if (projectInfo.code === 200) {
            message.success(projectInfo.msg);  // 显示成功信息

            // 更新父组件的两个值
            emit('update:projectName', projectNameLocal.value) 
            emit('update:hasSuccess', true)
            
            console.log("Project created successfully:", projectInfo);
        } else {
            // 如果返回的 code 不是 200，说明出现了问题（例如项目已经存在）
            message.error(projectInfo.msg || 'Unexpected error occurred.');
        }
    } catch (error) {
        // 捕获任何请求错误，打印项目名称并显示错误信息
        console.log("Error while creating project:", projectNameLocal.value);
        message.error('Failed to create project!');  // 处理请求错误
    }
};



</script>
