<script setup lang="ts">
// 顶栏用 Pinia store 管理登录态
import { useUserStore } from './stores/user'
import { ElMessageBox, ElMessage } from 'element-plus'

const userStore = useUserStore() // 一行拿到全局登录态，不用 props

async function handleLogin() {
  const { value } = await ElMessageBox.prompt('请输入用户名', '登录', {
    inputPlaceholder: '如：张三'
  })
  userStore.login({ name: value || '匿名用户' }) // 调 action
  ElMessage.success('登录成功')
}
function handleLogout() {
  userStore.logout()
  ElMessage.success('已登出')
}
</script>

<template>
  <div class="layout">
    <header class="topbar">
      <span>用户管理系统</span>
      <div class="right">
        <span class="user">{{ userStore.displayName }}</span>
        <el-button v-if="!userStore.isLoggedIn" size="small" type="primary" @click="handleLogin">登录</el-button>
        <el-button v-else size="small" @click="handleLogout">登出</el-button>
      </div>
    </header>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style>
* { box-sizing: border-box; }
body { margin: 0; font-family: system-ui, sans-serif; background: #f0f2f5; color: #333; }
.layout { min-height: 100vh; }
.topbar {
  height: 56px;
  background: #001529;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  font-size: 18px;
  font-weight: 600;
}
.topbar .right { display: flex; align-items: center; gap: 12px; font-weight: 400; font-size: 14px; }
.topbar .user { color: #bbb; }
.content {
  max-width: 1100px;
  margin: 24px auto;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
</style>
