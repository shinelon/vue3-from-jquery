<script setup>
// 第 9 章：用户详情页。从 URL 的 :id 取参数，请求该用户
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getUserById } from '../api/user'
import { ElMessage } from 'element-plus'

const route = useRoute()       // 读：拿当前路由的参数
const router = useRouter()     // 跳：用 router.back() 返回

const user = ref(null)
const loading = ref(false)

const roleMap = { admin: '管理员', editor: '编辑', viewer: '访客' }

onMounted(async () => {
  loading.value = true
  try {
    user.value = await getUserById(route.params.id)   // route.params.id 是 URL 里的 :id
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="page" v-loading="loading">
    <div class="head">
      <el-button @click="router.back()">← 返回</el-button>
      <span class="title">用户详情</span>
    </div>

    <el-descriptions v-if="user" :column="1" border style="margin-top: 16px">
      <el-descriptions-item label="ID">{{ user.id }}</el-descriptions-item>
      <el-descriptions-item label="姓名">{{ user.name }}</el-descriptions-item>
      <el-descriptions-item label="邮箱">{{ user.email }}</el-descriptions-item>
      <el-descriptions-item label="手机">{{ user.phone }}</el-descriptions-item>
      <el-descriptions-item label="角色">{{ roleMap[user.role] || user.role }}</el-descriptions-item>
      <el-descriptions-item label="状态">
        <el-tag :type="user.status === 1 ? 'success' : 'info'">
          {{ user.status === 1 ? '启用' : '禁用' }}
        </el-tag>
      </el-descriptions-item>
    </el-descriptions>
  </div>
</template>

<style scoped>
.page { padding: 16px; }
.head { display: flex; align-items: center; gap: 12px; }
.title { font-size: 16px; font-weight: 600; }
</style>
