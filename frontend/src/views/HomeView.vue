<script setup>
</script>

<template>
  <div class="home-container">
    <h1>欢迎来到AI考研信息问答平台</h1>
    <p>这里有最新的考研资讯和智能AI助您备考。</p>
    <el-button type="primary" @click="$router.push('/chat')">开始智能问答</el-button>
  </div>
</template>

<style scoped>
.home-container {
  text-align: center;
  margin-top: 50px;
}
</style>
