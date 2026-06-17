import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// 当前登录者（演示用，只需要一个名字）
interface SessionUser {
  name: string
}

// 用户登录态 store（组合式写法，和 <script setup> 一致）
// 对照 JS 版：类型基本全自动推断，你只要给 ref 和函数参数标上类型就行
export const useUserStore = defineStore('user', () => {
  // —— state：共享数据 ——明确告诉它「要么是个登录者，要么是 null」
  const currentUser = ref<SessionUser | null>(null)

  // —— getters：派生数据，类型由 TS 自动推断 ——
  const isLoggedIn = computed(() => !!currentUser.value)
  const displayName = computed(() => currentUser.value?.name || '未登录')

  // —— actions：修改数据的方法，参数标类型 ——
  function login(user: SessionUser) {
    currentUser.value = user
  }
  function logout() {
    currentUser.value = null
  }

  return { currentUser, isLoggedIn, displayName, login, logout }
})
