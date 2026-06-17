<script setup>
import { ref } from 'vue'
import UserCard from './components/UserCard.vue'

// 父组件拥有数据
const users = ref([
  { id: 1, name: '张三', email: 'zhangsan@example.com' },
  { id: 2, name: '李四', email: 'lisi@example.com' },
  { id: 3, name: '王五', email: 'wangwu@example.com' }
])

// 删除逻辑只在父组件这一处（单向数据流）
function handleDelete(id) {
  users.value = users.value.filter(u => u.id !== id)
}
</script>

<template>
  <div class="wrap">
    <h1>用户列表 · 组件化 demo</h1>
    <p class="tip">每张卡片是一个 <code>UserCard</code> 组件：props 传数据，emit 报告删除。</p>

    <UserCard
      v-for="u in users"
      :key="u.id"
      :user="u"
      @delete="handleDelete"
    />

    <p v-if="users.length === 0" class="empty">没有用户了</p>
  </div>
</template>

<style scoped>
.wrap {
  font-family: system-ui, sans-serif;
  max-width: 480px;
  margin: 40px auto;
  padding: 0 16px;
  color: #333;
}
h1 { font-size: 20px; }
.tip { color: #888; font-size: 13px; }
code { background: #f4f4f4; padding: 1px 4px; border-radius: 3px; }
.empty { color: #999; }
</style>
