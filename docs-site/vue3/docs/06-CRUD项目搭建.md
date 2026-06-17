# 第 6 章 · CRUD 项目搭建：脚手架 + Element Plus + json-server

从这一章起，我们用前面学的全部知识，**从零搭一个 CRUD 用户管理系统**——这是 jQuery 程序员最熟悉的"表格 + 表单 + 增删改查"场景。

本章只做一件事：**把项目骨架搭起来、跑通"前端 ↔ 后端"的完整链路**。功能（列表、表单）后面几章逐步加。

> 📂 配套项目在 [`project/user-admin/`](../project/user-admin/)。本章对应阶段 `ch06-init`（脚手架 + Element Plus + json-server）。
>
> ⚠️ **关于配套代码（重要）**：磁盘上的 `project/user-admin/` 是**全书完成后的最终成品**，而本章起是"逐步搭建"的叙事。所以磁盘里的文件会比本章讲的"多"一些（已含后续章节加的功能）。本章贴的代码是"做到本章时"的中间态，照着敲即可；想看最终全貌，直接读磁盘文件。

---

## 一、项目总览

最终我们要做出这样一个后台：

- **列表页**：用 Element Plus 的表格展示用户，支持搜索、分页；
- **新增/编辑**：点按钮弹窗表单，带校验，提交到后端；
- **删除**：行内删除，带确认；
- **多页面**：用 Vue Router（列表页 / 详情页）；
- **登录态**：用 Pinia 存当前用户。

技术栈：**Vue3 + Vite + Element Plus + axios + json-server**（假后端）。

本章先搭骨架，让这个空壳能跑、能连通后端。

---

## 二、创建项目

```bash
npm create vue@latest user-admin
```

选项这样选：

```
TypeScript:    No          ← 纯 JS
JSX Support:   No
Vue Router:    Yes         ← 第 9 章用
Pinia:         Yes         ← 第 10 章用
Vitest:        No
E2E Testing:   No
ESLint:        No
Prettier:      No
```

```bash
cd user-admin
npm install      # 装基础依赖
```

> Router 和 Pinia 虽然这章装了，但**它们的用法分别在第 9、10 章讲**。现在先搭架子，能跑就行。

---

## 三、安装三件套

在项目目录里执行：

```bash
# UI 组件库（表格/表单/弹窗都靠它，省掉 CSS）
npm install element-plus

# HTTP 请求库（对照 $.ajax）
npm install axios

# 假后端（一条命令起 REST API，开发用，放进 devDependencies）
npm install -D json-server@0.17
```

> ⚠️ **`json-server` 一定要装 `@0.17` 这个经典版本**。新版（1.x）命令和 API 都变了，本教程按 0.17 写。`-D` 表示它是开发依赖（上线不需要假后端）。

---

## 四、配置 Vite 代理（解决跨域——jQuery 老哥的常见痛点）

前端跑在 `localhost:5173`，后端跑在 `localhost:3000`，**端口不同会跨域**。jQuery 时代你可能被 `Access-Control-Allow-Origin` 报错折磨过。

开发阶段最优雅的解法是 **Vite 代理**：让前端用 `/api/xxx` 请求，Vite 自动转发到 `localhost:3000/xxx`，**浏览器以为没跨域**。

修改 `vite.config.js`：

```js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',   // json-server 的地址
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')  // /api/users → /users
      }
    }
  }
})
```

---

## 五、封装 axios（对照 `$.ajax`）

新建 `src/api/request.js`，统一配置 axios：

```js
import axios from 'axios'

// 创建一个实例，统一配置
const request = axios.create({
  baseURL: '/api',        // 走 Vite 代理 → http://localhost:3000
  timeout: 10000          // 10 秒超时
})

// 响应拦截器：统一取出后端返回的数据，省得每次 res.data
request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('请求出错：', error.message)
    return Promise.reject(error)
  }
)

export default request
```

再建 `src/api/user.js`，把"用户相关接口"集中管理：

```js
import request from './request'

// 获取用户列表（对应 GET /api/users）
export function getUsers(params) {
  return request.get('/users', { params })
}
```

| jQuery | Vue（axios 封装） |
|---|---|
| 到处写 `$.ajax({ url, type, data, success })` | 统一一个 `request`，接口分文件管理 |
| 每次手动取 `res.data` | 拦截器自动取出 |
| 跨域手动处理后端 CORS | Vite 代理开发期自动解决 |

> 💡 把接口集中到 `src/api/` 是好习惯：接口多了不会乱，换后端地址只改一处。

---

## 六、准备假后端 `db.json`

在项目根目录建 `db.json`，json-server 会把它当成"数据库"：

```json
{
  "users": [
    { "id": 1, "name": "张三", "email": "zhangsan@example.com", "phone": "13800000001", "role": "admin", "status": 1 },
    { "id": 2, "name": "李四", "email": "lisi@example.com", "phone": "13800000002", "role": "editor", "status": 1 }
    // ... 多放几条，方便后面分页
  ]
}
```

> 完整数据见 [`project/user-admin/db.json`](../project/user-admin/db.json)。

json-server 会自动生成 REST 接口：

| 操作 | HTTP 方法 | URL |
|---|---|---|
| 查列表 | GET | `/users` |
| 查单个 | GET | `/users/1` |
| 新增 | POST | `/users` |
| 修改 | PUT/PATCH | `/users/1` |
| 删除 | DELETE | `/users/1` |

**你一行后端代码都不用写**，CRUD 全有了。

---

## 七、注册 Element Plus + 验证联通

修改 `src/main.js`，全局注册 Element Plus：

```js
import { createApp } from 'vue'
import ElementPlus from 'element-plus'         // 引入组件库
import 'element-plus/dist/index.css'           // 引入样式（别忘了！）
import App from './App.vue'

const app = createApp(App)
app.use(ElementPlus)                            // 全局注册
app.mount('#app')
```

> 💡 这里用的是**全量注册**（最简单）。真实项目会用"按需引入"减小打包体积，但入门阶段全量最省心，先跑通再说。

把 `src/App.vue` 改成"联通测试页"，请求一次接口验证全链路：

```vue
<script setup>
import { ref, onMounted } from 'vue'
import { getUsers } from './api/user'

const count = ref(0)
const loading = ref(false)

// 组件挂载后自动请求（onMounted 类似 jQuery 的 $(function(){...}) 或 ready）
onMounted(async () => {
  loading.value = true
  try {
    const list = await getUsers()   // 拦截器已取出 data，这里就是数组
    count.value = list.length
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <el-card class="box">
    <h1>用户管理系统 · 骨架已就绪</h1>
    <p v-loading="loading">当前用户数：<strong>{{ count }}</strong></p>
    <p class="tip">看到数字（非 0/报错）就说明：Vue ✓ Element Plus ✓ axios ✓ json-server ✓ 全部联通！</p>
  </el-card>
</template>

<style>
body { font-family: system-ui, sans-serif; background: #f5f5f5; margin: 0; }
.box { max-width: 600px; margin: 60px auto; }
.tip { color: #888; font-size: 13px; }
</style>
```

---

## 八、目录结构规划

本章结束时的结构：

```
user-admin/
├── db.json              ← 假数据（json-server 用）
├── index.html
├── package.json
├── vite.config.js       ← 配了代理
└── src/
    ├── App.vue          ← 根组件
    ├── main.js          ← 注册 Element Plus
    └── api/
        ├── request.js   ← axios 封装
        └── user.js      ← 用户接口
```

后续章节会新增：

- `src/views/`（第 7~9 章）—— 页面：列表、编辑、详情
- `src/components/`（第 8 章）—— 弹窗表单组件
- `src/router/`（第 9 章）—— 路由配置
- `src/stores/`（第 10 章）—— Pinia 状态

---

## 九、两个终端跑起来

**终端 1**（起假后端）：

```bash
npm run server
```

> 需要在 `package.json` 的 `scripts` 里加：`"server": "json-server --watch db.json --port 3000"`。看到 `Resources: /users` 就成了。

**终端 2**（起前端）：

```bash
npm run dev
```

浏览器打开 `http://localhost:5173`。如果你是**从零跟着敲到本章**，会看到"用户数量"的联通测试页；如果直接用**配套的最终成品项目**，会看到顶栏 + 用户列表。无论哪种，只要能正常显示数据（而非报错），就说明前后端打通 🎉。

> 这就是"前后端分离"：**前端（Vue）和后端（json-server）是两个独立进程**，通过 HTTP 接口通信。jQuery 时代你可能还在一个项目里混着写 PHP/JSP + HTML，现代开发是把它们彻底分开。

---

## 🏋️ 小练习

1. 在 `db.json` 里多加几条用户，刷新页面看数量变化（体会"数据在后端，前端只管请求"）。
2. 在浏览器 F12 → Network 面板，找到那个 `/api/users` 请求，看看请求和响应长啥样。

---

## ✅ 本章你应掌握

- [ ] 会用脚手架建项目、安装 Element Plus / axios / json-server；
- [ ] 理解 Vite 代理如何解决跨域；
- [ ] 会封装 axios（实例 + 拦截器 + 接口分文件）；
- [ ] 跑通"前端 → json-server"的完整链路；
- [ ] 理解前后端分离（两个独立进程、HTTP 通信）。

骨架就绪，下一篇开始**填功能**：列表与查询。

下一篇 👉 [第 7 章 · 列表与查询：el-table + axios + 分页](07-列表与查询.md)
