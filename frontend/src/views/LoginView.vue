<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const isLogin = ref(true)
const form = ref({
  username: '',
  password: ''
})

const submitForm = async () => {
  if (isLogin.value) {
    await login()
  } else {
    await register()
  }
}

const login = async () => {
  try {
    const formData = new FormData()
    formData.append('username', form.value.username)
    formData.append('password', form.value.password)
    
    // Assuming backend is on port 8000
    const response = await axios.post('http://localhost:8000/token', formData)
    localStorage.setItem('token', response.data.access_token)
    ElMessage.success('登录成功')
    router.push('/chat')
  } catch (error) {
    ElMessage.error('登录失败，请检查用户名和密码')
  }
}

const register = async () => {
  try {
    await axios.post('http://localhost:8000/users/', {
      email: form.value.username,
      password: form.value.password
    })
    ElMessage.success('注册成功，请登录')
    isLogin.value = true
  } catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      ElMessage.error(`注册失败: ${error.response.data.detail}`)
    } else {
      ElMessage.error('注册失败，请稍后重试')
    }
  }
}
</script>

<template>
  <div class="login-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>{{ isLogin ? '用户登录' : '用户注册' }}</span>
          <el-button class="button" text type="primary" @click="isLogin = !isLogin">
            {{ isLogin ? '去注册' : '去登录' }}
          </el-button>
        </div>
      </template>
      <el-form :model="form" label-width="80px">
        <el-form-item label="邮箱">
          <el-input v-model="form.username" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm" style="width: 100%">
            {{ isLogin ? '登录' : '注册' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  margin-top: 100px;
}
.box-card {
  width: 400px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
