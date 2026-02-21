<script setup>
import { ref } from 'vue'
import { marked } from 'marked'

const question = ref('')
const messages = ref([])

const sendQuestion = async () => {
  if (!question.value) return
  
  messages.value.push({ type: 'user', content: question.value })
  const currentQuestion = question.value
  question.value = ''
  
  // Add an empty AI message to start streaming into
  const aiMessageIndex = messages.value.push({ type: 'ai', content: '' }) - 1
  
  try {
    const token = localStorage.getItem('token')
    // Use relative path /api/chat via Nginx proxy
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ question: currentQuestion })
    })

    if (!response.ok) {
        throw new Error('Network response was not ok')
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() // Keep the last incomplete line in the buffer

        for (const line of lines) {
            if (!line.trim()) continue
            try {
                const data = JSON.parse(line)
                if (data.type === 'answer') {
                    // Append content to the current AI message
                    messages.value[aiMessageIndex].content += data.content
                } else if (data.type === 'error') {
                     messages.value[aiMessageIndex].content += `\n[Error: ${data.content}]`
                }
            } catch (e) {
                console.error('Error parsing JSON chunk', e)
            }
        }
    }
  } catch (error) {
    messages.value[aiMessageIndex].content += '\n[发送失败，请确保已登录或检查网络]'
    console.error('Fetch error:', error)
  }
}

// Function to render Markdown content
const renderMarkdown = (content) => {
    return marked(content)
}
</script>

<template>
  <div class="chat-container">
    <div class="messages">
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.type]">
        <!-- Use v-html for AI messages to render Markdown -->
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
}
.message.user {
  background-color: #ecf5ff;
  text-align: right;
}
.message.ai {
  background-color: #f0f9eb;
  text-align: left;
}
.message.error {
  background-color: #fef0f0;
  text-align: center;
}
/* Basic Markdown styles */
:deep(.markdown-body) {
    font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif;
    font-size: 16px;
    line-height: 1.5;
    word-wrap: break-word;
}
:deep(.markdown-body p) {
    margin-bottom: 16px;
}
:deep(.markdown-body h1), :deep(.markdown-body h2) {
    border-bottom: 1px solid #eaecef;
    padding-bottom: .3em;
}
</style>
