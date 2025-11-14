<template>
  <div
    class="card"
    @click="handleClick"
  >
    <!-- 头部 -->
    <div class="card-header" :class="titleColorClass">
      <span class="card-title">{{ title }}</span>
      <span class="toggle-btn">{{ expanded ? '−' : '+' }}</span>
    </div>

    <!-- 内容 -->
    <div v-if="expanded" class="card-body">
      <div
        v-for="(rec, idx) in records"
        :key="idx"
        class="record-item"
      >
        <n-card
          style="border-radius: 8px; margin-bottom: 12px;"
        >
          <!-- ans -->
          <div class="ans">{{ rec.ans }}</div>
          <!-- detail -->
          <div class="detail" v-if="rec.detail">
            <span>{{ rec.detail }}</span>
            <n-icon
              size="16"
              color="rgba(0,0,0,0.3)"
              class="detail-icon"
              @click.stop="copyToClipboard(rec.detail)"
              style="cursor: pointer;"
              title="Copy to clipboard"
            >
              <Copy />
            </n-icon>
          </div>

          <!-- description -->
          <div class="description" v-if="rec.description">{{ rec.description }}</div>

          <!-- status + page 同一行 -->
          <div class="status-row">
            <div class="status" v-if="typeof rec.status === 'boolean'">
              <n-icon v-if="rec.status" size="18" color="green">
                <CheckmarkCircle />
              </n-icon>
              <n-icon v-else size="18" color="red">
                <Close />
              </n-icon>
              {{ rec.res }}
            </div>
            <div class="pages" v-if="rec.page || rec.others" @click.stop>
              Page: <span class="page-box">{{ rec.page ?? '-' }}</span>
              <label v-if="rec.others && rec.others.length">
                Other Pages:
                <select
                  v-model="selectedOtherPage"
                  @change="goToOtherPage(selectedOtherPage)"
                >
                  <option
                    v-for="(p, i) in rec.others"
                    :key="i"
                    :value="p"
                  >
                    {{ p }}
                  </option>
                </select>
              </label>
            </div>
          </div>
        </n-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { CheckmarkCircle, Close, Copy } from '@vicons/ionicons5'
import { NIcon } from 'naive-ui'

const props = defineProps({
  showSkeleton: Boolean,
  title: String,
  activeModule: String,
  records: { type: Array, default: () => [] }, 
  defaultExpanded: { type: Boolean, default: false },
})


const emits = defineEmits(['go-to-page'])


const expanded = ref(props.defaultExpanded)
function handleClick() {
  emits('go-to-page', props.records.page) // 通知父组件跳转
  expanded.value = !expanded.value
}

const titleColorClass = computed(() => {
  switch (props.activeModule) {
    case 'search_highlight':
      return 'title-search'
    case 'clause_alignment':
      return 'title-alignment'
    case 'issues':
      return 'title-issues'
    default:
      return ''
  }
})

function copyToClipboard(text) {
  if (!text) return
  navigator.clipboard.writeText(text)
    .then(() => {
      // You can use Naive UI's message notification here
      window.$message?.success('Copied to clipboard')
    })
    .catch(err => {
      console.error('Copy failed', err)
      window.$message?.error('Copy failed')
    })
}

</script>

<style scoped>

.card {
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 12px;
  border: 1px solid #ddd;
  cursor: pointer;
  transition: background-color 0.2s;
}
.card-header {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  font-weight: bold;
}
.card-body {
  padding: 12px;
  font-size: 14px;
}
.compliant { background-color: #e6f4f1; }
.non-compliant { background-color: #fff4e5; }
.pending { background-color: #f4f4f4; }
.status {
  margin-top: 8px;
  font-weight: bold;
}
.pages {
  margin-top: 4px;
  font-size: 12px;
  color: #555;
}
.toggle-btn {
  font-size: 18px;
}

.title-search {
  background-color: rgba(77, 163, 255, 0.15); /* 浅蓝透明背景 */
  color: #000;
  font-weight: bold;
  font-size: 1.1em;
  border-left: 6px solid rgba(77, 163, 255, 0.8); /* 左边深色竖条 */
}

.title-alignment {
  background-color: rgba(255, 152, 0, 0.15);
  color: #000;
  font-weight: bold;
  font-size: 1.1em;
  border-left: 6px solid rgba(255, 152, 0, 0.8);
}

.title-issues {
  background-color: rgba(76, 175, 80, 0.15);
  color: #000;
  font-weight: bold;
  font-size: 1.1em;
  border-left: 6px solid rgba(76, 175, 80, 0.8);
}

.ans {
  display: block;       /* 独立一行 */
  font-weight: bold;    /* 加粗 */
  font-size: 1.1em;     /* 稍微放大 */
  margin-bottom: 6px;   /* 与下面内容留点间距 */
}

.ans::before {
  content: "";
  display: inline-block;
  width: 12px;              /* 圆点大小 */
  height: 12px;
  border-radius: 50%;      /* 圆形 */
  background-color: #4da3ff; /* 圆点颜色，可根据状态改 */
  margin-right: 6px;       /* 圆点和文字间距 */
}

.detail {
  display: inline-flex;           /* 让文字和图标在一行 */
  align-items: center;            /* 垂直居中 */
  gap: 9px;               /* 文字和图标间距 */
  background-color: rgba(77, 163, 255, 0.2); /* 浅蓝背景，可选 */
  border-radius: 6px;              /* 圆角 */
  padding: 4px 10px;                /* 内边距 */
}

.detail span {
  font-weight: bold;     /* 加粗文字 */
}

.detail-icon {
  flex-shrink: 0;                   /* 防止图标被压缩 */
}

.status-row {
  display: flex;
  align-items: center; /* 垂直居中 */
}

.status {
  display: flex;
  align-items: center;
  gap: 4px;
}

.pages {
  margin-left: auto;     /* 推到最右边 */
  display: flex;
  align-items: center;
  gap: 12px;
  color: #000;           /* 黑色文字 */
  font-weight: bold;     /* 加粗文字 */
}

.page-box {
  background-color: #4caf50; /* 绿色背景 */
  color: #fff;               /* 白色文字 */
  padding: 2px 8px;          /* 内边距，形成长方形 */
  border: none;              /* 无边框 */
  border-radius: 4px;        /* 可选：圆角 */
  font-weight: bold;         /* 加粗 */
  display: inline-block;     /* 保证背景只包裹文字 */
}

.pages select {
  width: 50px;       /* 固定宽度 */
  font-size: 0.85em;          /* 字体小一点 */
  padding: 2px 6px;           /* 内边距小一点 */
  border: 1px solid #ccc;     /* 默认灰色边框 */
  border-radius: 4px;
  background-color: transparent; /* 无背景色 */
  outline: none;              /* 去掉默认高亮 */
  color: #000;           /* 下拉框文字黑色 */
  font-weight: bold;     /* 下拉框文字加粗 */
}

.pages select:focus {
  border-color: #409eff;      /* 点击时边框变蓝 */
}


 
</style>
