import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// 用户登录态 store（组合式写法，和 <script setup> 一致）
// 对照 jQuery：相当于一个"响应式的、可控的"全局变量仓库
export const useUserStore = defineStore('user', () => {
  // —— state：共享数据 ——
  const currentUser = ref(null)

  // —— getters：派生数据（computed）——
  const isLoggedIn  = computed(() => !!currentUser.value)
  const displayName = computed(() => currentUser.value?.name || '未登录')

  // —— actions：修改数据的方法 ——
  function login(user) {
    currentUser.value = user
  }
  function logout() {
    currentUser.value = null
  }

  return { currentUser, isLoggedIn, displayName, login, logout }
})
