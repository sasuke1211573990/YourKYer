<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { marked } from 'marked'

const question = ref('')
const messages = ref([])

const renderMarkdown = (content) => {
  return marked(content)
}

const sendQuestion = async () => {
  if (!question.value) return
  
  messages.value.push({ type: 'user', content: question.value })
  const currentQuestion = question.value
  question.value = ''
  
  // Create a placeholder for AI response
  const aiMessageIndex = messages.value.push({ type: 'ai', content: '' }) - 1
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ question: currentQuestion })
    })

    if (!response.ok) throw new Error('Network response was not ok')

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      
      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() // Keep incomplete line in buffer

      for (const line of lines) {
        if (!line.trim()) continue
        try {
          const data = JSON.parse(line)
          if (data.type === 'answer') {
            messages.value[aiMessageIndex].content += data.content
          } else if (data.type === 'sources') {
            // Optionally handle sources display
            // For now we might append it or store it separately
            // messages.value[aiMessageIndex].content += '\n\n**参考资料**:\n' + data.content.join('\n')
          } else if (data.type === 'error') {
            messages.value[aiMessageIndex].content += '\n\n' + data.content
          }
        } catch (e) {
          console.error('Error parsing JSON chunk', e)
        }
      }
    }
  } catch (error) {
    messages.value[aiMessageIndex].content += '\n\n[系统提示] 发送失败或网络中断'
    console.error(error)
  }
}
</script>

<template>
  <div class="chat-container">
    <div class="messages">
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.type]">
        <div v-if="msg.type === 'ai'" class="content markdown-body" v-html="renderMarkdown(msg.content)"></div>
        <div v-else class="content">{{ msg.content }}</div>
      </div>
    </div>
    <div class="input-area">
      <el-input
        v-model="question"
        placeholder="请输入您的考研问题..."
        @keyup.enter="sendQuestion"
      >
        <template #append>
          <el-button @click="sendQuestion">发送</el-button>
        </template>
      </el-input>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  height: 80vh;
}
.messages {
  flex: 1;
  overflow-y: auto;
  border: 1px solid #ebeef5;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 4px;
}
.message {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 4px;
  max-width: 80%;
}
.message.user {
  background-color: #ecf5ff;
  align-self: flex-end;
  margin-left: auto;
}
.message.ai {
  background-color: #f0f9eb;
  align-self: flex-start;
  margin-right: auto;
}
.message.error {
  background-color: #fef0f0;
  text-align: center;
  align-self: center;
}
/* Basic Markdown Styles */
:deep(.markdown-body) {
  line-height: 1.6;
}
:deep(.markdown-body h1), :deep(.markdown-body h2), :deep(.markdown-body h3) {
  margin-top: 1em;
  margin-bottom: 0.5em;
  font-weight: bold;
}
:deep(.markdown-body ul), :deep(.markdown-body ol) {
  padding-left: 20px;
  margin-bottom: 1em;
}
:deep(.markdown-body p) {
  margin-bottom: 1em;
}
:deep(.markdown-body code) {
  background-color: #f4f4f5;
  padding: 2px 4px;
  border-radius: 2px;
}
</style>
