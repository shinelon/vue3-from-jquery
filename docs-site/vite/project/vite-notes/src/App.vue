<script setup>
import logo from '@/assets/logo.svg'

const title = import.meta.env.VITE_APP_TITLE
</script>

<template>
  <img :src="logo" alt="logo" width="48" />
  <h1>📝 {{ title }}</h1>
  <nav>
    <router-link to="/">首页</router-link> |
    <router-link to="/about">关于</router-link>
  </nav>
  <hr />
  <router-view />
</template>

<style scoped>
body {
  font-family: system-ui, sans-serif;
  max-width: 480px;
  margin: 40px auto;
  color: #333;
}
nav {
  margin: 12px 0;
}
nav a {
  color: #42b883;
  text-decoration: none;
}
</style>
