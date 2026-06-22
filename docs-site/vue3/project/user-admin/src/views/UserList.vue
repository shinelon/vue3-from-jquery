<script setup>
// 第 9 章：在第 8 章基础上加"详情"跳转（router.push）
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsers, deleteUser } from '../api/user'
import UserDialog from '../components/UserDialog.vue'

const router = useRouter()       // 用于跳转

// —— 列表数据 ——
const users = ref([])
const loading = ref(false)
const keyword = ref('')
const currentPage = ref(1)
const pageSize = ref(5)

const roleMap = { admin: '管理员', editor: '编辑', viewer: '访客' }

const filtered = computed(() => {
  const kw = keyword.value.trim().toLowerCase()
  if (!kw) return users.value
  return users.value.filter(
    u => u.name.toLowerCase().includes(kw) || u.email.toLowerCase().includes(kw)
  )
})

const pagedUsers = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filtered.value.slice(start, start + pageSize.value)
})

async function loadData() {
  loading.value = true
  try {
    users.value = await getUsers()
  } catch (e) {
    ElMessage.error('加载失败：' + e.message)
  } finally {
    loading.value = false
  }
}

// —— 删除 ——
async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确定删除「${row.name}」吗？`, '提示', { type: 'warning' })
  } catch {
    return
  }
  try {
    await deleteUser(row.id)
  } catch (e) {
    ElMessage.error('删除失败：' + e.message)
    return
  }
  ElMessage.success('删除成功')
  loadData()
}

// —— 新增 / 编辑弹窗 ——
const dialogVisible = ref(false)
const editing = ref(null)

function handleAdd() {
  editing.value = null
  dialogVisible.value = true
}
function handleEdit(row) {
  editing.value = row
  dialogVisible.value = true
}

// —— 第 9 章：跳详情页 ——
function handleDetail(row) {
  router.push(`/users/${row.id}`)
}

onMounted(loadData)
</script>

<template>
  <div class="page">
    <div class="toolbar">
      <el-input
        v-model="keyword"
        placeholder="搜索姓名 / 邮箱"
        clearable
        style="width: 240px"
        @input="currentPage = 1"
      />
      <el-button @click="loadData">刷新</el-button>
      <el-button type="primary" @click="handleAdd">+ 新增用户</el-button>
    </div>

    <el-table :data="pagedUsers" v-loading="loading" border stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="phone" label="手机" />
      <el-table-column label="角色">
        <template #default="{ row }">
          <el-tag>{{ roleMap[row.role] || row.role }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态">
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'success' : 'info'">
            {{ row.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220">
        <template #default="{ row }">
          <el-button size="small" link type="primary" @click="handleDetail(row)">详情</el-button>
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="filtered.length"
      :page-sizes="[5, 10, 20]"
      layout="total, sizes, prev, pager, next"
      style="margin-top: 16px; justify-content: flex-end"
    />

    <UserDialog v-model="dialogVisible" :editing="editing" @success="loadData" />
  </div>
</template>

<style scoped>
.page { padding: 16px; }
.toolbar { margin-bottom: 16px; display: flex; gap: 8px; }
</style>
