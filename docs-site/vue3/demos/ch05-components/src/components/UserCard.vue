<script setup>
// 子组件：接收一个 user（props），点击删除时通过 emit 通知父组件
const props = defineProps({
  user: { type: Object, required: true }
})

// 声明这个组件会向外触发 'delete' 事件
const emit = defineEmits(['delete'])

function remove() {
  emit('delete', props.user.id)   // 把要删的 id 带给父组件
}
</script>

<template>
  <div class="card">
    <div class="avatar">{{ user.name.charAt(0) }}</div>
    <div class="info">
      <h3>{{ user.name }}</h3>
      <p>{{ user.email }}</p>
    </div>
    <button class="del" @click="remove">删除</button>
  </div>
</template>

<style scoped>
.card {
  display: flex;
  align-items: center;
  gap: 12px;
  border: 1px solid #eee;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 12px;
}
.avatar {
  width: 48px; height: 48px;
  border-radius: 50%;
  background: #42b883;
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-weight: bold; font-size: 20px;
}
.info { flex: 1; }
.info h3 { margin: 0 0 4px; font-size: 16px; }
.info p { margin: 0; color: #888; font-size: 13px; }
.del {
  color: #c00;
  border: 1px solid #eee;
  background: #fff;
  padding: 4px 10px;
  cursor: pointer;
}
</style>
