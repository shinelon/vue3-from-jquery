# 第 10 章 · 状态管理 Pinia：登录态（先痛后甜）

前面几章，每个组件的数据都"自己管自己"（组件里的 `ref`）。但有一类数据是**全局的**——比如"当前登录用户"，顶栏要用、列表页要用、详情页也要用。这种数据怎么管？这一章按"**先痛后甜**"的顺序讲：先让你体会痛点，再给你 Pinia 这个工具。

> 📂 本章改动 [`project/user-admin/`](../project/user-admin/)：新增 `src/stores/user.js`，更新 `main.js`、`App.vue`。对应阶段 `ch10-pinia`。

---

## 一、先痛：跨组件共享数据有多麻烦

假设有个"当前登录用户"，**好几个组件都要用**（顶栏显示名字、列表页记录操作人、详情页显示"是否本人"）。

**办法 1：props 一层层传**

```
App（拥有 currentUser）
 ├ 传 props → 顶栏（显示名字）
 ├ 传 props → 列表页 → 再传 props → 表格 → 再传 props → 操作列 ...
 └ 传 props → 详情页
```

组件嵌套一深，数据要在中间每一层"路过"一遍（写一堆没用的 props）。Vue 社区管这叫 **props 钻孔（prop drilling）**——烦、易错、难维护。

**办法 2：全局变量（jQuery 习惯）**

```js
window.currentUser = { name: '张三' }   // 到处都能读
```

能用，但有两个致命问题：
1. **不响应式**：你改了 `window.currentUser`，页面**不会自动更新**（Vue 不知道它变了）；
2. **不可控**：任何地方都能随便改，大型项目里根本追不清"谁改的、什么时候改的"。

**我们需要的是**：一个**全局的、响应式的、集中管理**的地方放共享数据。这就是 **Pinia**。

---

## 二、什么是状态管理 / 为什么是 Pinia

**状态管理**：把跨组件共享的数据，集中放到一个"仓库（store）"里。任何组件都能直接读写这个仓库，数据变了所有用到它的地方自动更新。

**Pinia** 是 Vue 官方的状态管理库（Vuex 的继任者，更简单）。它的好处：

- ✅ **响应式**：改了仓库数据，页面自动更新；
- ✅ **集中管理**：共享数据都在 `stores/` 目录，一目了然；
- ✅ **任意组件直接用**：不用 props 钻孔；
- ✅ **写法和 `<script setup>` 一致**：`ref`/`computed`/函数，你已经会了。

| jQuery 全局变量 | Pinia store |
|---|---|
| `window.xxx` | `useXxxStore()` |
| 不响应式 | 响应式（改了自动更新） |
| 到处乱改 | 集中在 store 的 actions 里改 |

---

## 三、安装与注册

依赖已在脚手架时装好。在入口注册 Pinia：

```js
// src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'       // ← 引入
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.use(createPinia())                     // ← 注册 Pinia
app.mount('#app')
```

---

## 四、定义一个 store

新建 `src/stores/user.js`。用**组合式写法**（和 `<script setup>` 风格一致，你已经会 `ref`/`computed`）：

```js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // —— state：共享的数据 ——
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

  return { currentUser, isLoggedIn, displayName, login, logout }   // 交出去
})
```

看出来了吗？**store 就是把组件里的 `ref`/`computed`/函数，搬到一个独立文件里，再加上 `defineStore` 包一层**。语法你全都会，没有新东西。

- `state` → `ref`（数据）；
- `getters` → `computed`（派生）；
- `actions` → 普通函数（改数据）。

---

## 五、在组件里用 store（后甜！）

任何组件，**直接调用** `useUserStore()` 就能拿到仓库，不用 props：

```vue
<script setup>
import { useUserStore } from './stores/user'

const userStore = useUserStore()      // ← 一行拿到，无论组件嵌套多深

// 读数据（响应式）
userStore.isLoggedIn
userStore.displayName

// 调 action 改数据
userStore.login({ name: '张三' })
</script>

<template>
  <span>{{ userStore.displayName }}</span>
</template>
```

**对比"先痛"那节**：顶栏、列表页、详情页——**每个组件都只要 `useUserStore()` 一行**，再也不用一层层传 props。而且 `currentUser` 一变，所有用到它的地方**自动更新**。这就是"后甜"。

> ⚠️ 解构会丢响应式？用 store 时如果写 `const { displayName } = userStore`，`displayName` 会失去响应式。要么用 `userStore.displayName` 直接访问，要么用 Pinia 提供的 `storeToRefs`：`const { displayName } = storeToRefs(userStore)`（只对 state/getters 解构时需要，actions 可以直接解构）。

---

## 六、登录态实战

把顶栏接上 store：未登录显示"登录"按钮，登录后显示用户名 + 登出。

```vue
<!-- App.vue -->
<script setup>
import { useUserStore } from './stores/user'
import { ElMessageBox, ElMessage } from 'element-plus'

const userStore = useUserStore()

async function handleLogin() {
  const { value } = await ElMessageBox.prompt('请输入用户名', '登录', {
    inputPlaceholder: '如：张三'
  })
  userStore.login({ name: value || '匿名用户' })   // 调 action
  ElMessage.success('登录成功')
}
function handleLogout() {
  userStore.logout()                                 // 调 action
  ElMessage.success('已登出')
}
</script>

<template>
  <header class="topbar">
    <span>用户管理系统</span>
    <div class="right">
      <span class="user">{{ userStore.displayName }}</span>     <!-- getter 自动算 -->
      <el-button v-if="!userStore.isLoggedIn" size="small" type="primary" @click="handleLogin">登录</el-button>
      <el-button v-else size="small" @click="handleLogout">登出</el-button>
    </div>
  </header>
</template>
```

试试：点登录输入名字 → 顶栏立刻显示名字（store 一变，自动更新）；点登出 → 回到"未登录"。**这个 `currentUser` 现在是全局共享的**，列表页、详情页想用，各自 `useUserStore()` 一行就行。

---

## 🏋️ 小练习

1. **列表页用 store**：在 `UserList.vue` 顶部显示"当前操作人：{{ userStore.displayName }}"，体会"任意组件都能直接读 store"。
2. **持久化**：登录后刷新页面，状态会丢（Pinia 默认存内存）。试着在 `login` 里把用户存进 `localStorage`，初始化时读回来（真实项目用 `pinia-plugin-persistedstate` 插件更省事）。

---

## ✅ 本章你应掌握

- [ ] 理解为什么需要状态管理（props 钻孔之痛、全局变量不响应式/不可控）；
- [ ] 会用 `createPinia()` 注册 Pinia；
- [ ] 会用 `defineStore` 定义 store（组合式：`ref`=state、`computed`=getters、函数=actions）；
- [ ] 在任意组件用 `useUserStore()` 直接读写，不用 props 钻孔；
- [ ] 知道解构 store 会丢响应式，需要 `storeToRefs`。

> 🎉 至此，Vue 的核心生态你都用过了一遍：响应式、组件、路由、状态管理、UI 库、接口请求。最后一章，我们把项目**收尾、打包、准备上线**。

下一篇 👉 [第 11 章 · 收尾：loading / 错误 / 打包部署](11-收尾打包部署.md)
