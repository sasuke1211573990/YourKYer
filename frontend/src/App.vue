<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">首页</RouterLink> |
        <RouterLink to="/chat">AI问答</RouterLink> |
        <RouterLink to="/login">登录</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
  background-color: #f8f9fa;
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
}

nav {
  width: 100%;
  font-size: 16px;
  text-align: center;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  text-decoration: none;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
  font-weight: bold;
}
</style>
