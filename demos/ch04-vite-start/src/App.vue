<script setup>
// 用 <script setup> 重写第 1 章的 Todo。
// 逻辑和 CDN 版完全一样，只是不用 createApp / setup() / return 了。
import { ref } from 'vue'

const text = ref('')
const todos = ref([
  { id: 1, text: '学会 <script setup>' },
  { id: 2, text: '把 CDN 项目升级到 Vite' }
])

function add() {
  if (!text.value.trim()) return
  todos.value.push({ id: Date.now(), text: text.value.trim() })
  text.value = ''
}

function remove(id) {
  todos.value = todos.value.filter(t => t.id !== id)
}
</script>

<template>
  <div class="wrap">
    <h1>Todo · Vite + &lt;script setup&gt; 版</h1>

    <input v-model="text" placeholder="输入任务，回车提交" @keyup.enter="add" />
    <button @click="add">添加</button>

    <ul>
      <li v-for="t in todos" :key="t.id">
        <span>{{ t.text }}</span>
        <button class="del" @click="remove(t.id)">删除</button>
      </li>
    </ul>

    <p class="count">共 {{ todos.length }} 条</p>
  </div>
</template>

<style scoped>
/* scoped：样式只作用于本组件 */
.wrap {
  font-family: system-ui, sans-serif;
  max-width: 480px;
  margin: 40px auto;
  padding: 0 16px;
  color: #333;
}
h1 { font-size: 20px; }
input { padding: 6px 10px; font-size: 14px; }
button { padding: 6px 12px; font-size: 14px; cursor: pointer; }
ul { list-style: none; padding: 0; }
li {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
li .del { font-size: 12px; color: #c00; }
.count { color: #888; font-size: 13px; }
</style>
