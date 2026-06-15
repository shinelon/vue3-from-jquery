# 附录 C · 下一步学什么

恭喜你读完整本教程！你已经具备用 Vue3 独立做项目的实战能力。这一页给你指几条"下一步"的路，按需挑选。

---

## 🪜 优先级最高的几步

### 1. 把这个 CRUD 项目玩熟

别急着学新东西。把这个用户管理系统**反复改、加功能**：

- 加用户头像上传、加批量删除、加导出 Excel；
- 拆分更多组件、抽离通用的"搜索栏"组件；
- 把前端分页改成后端分页。

**改的过程才是真正消化知识的过程。**一个自己折腾透的项目，胜过读十本书。

### 2. 学 TypeScript（本教程埋的钩子）

本教程全程用纯 JS。但真实 Vue3 项目**大量用 TypeScript**。你现在已经懂 Vue 了，补 TS 是顺势而为：

- 给 `ref`/`props`/`emit` 加类型；
- 给接口返回的数据定义 `interface`；
- 学 `defineProps<T>()`、`ref<T>()`。

资源：[Vue 官方 TS 指南](https://cn.vuejs.org/guide/typescript/overview.html)。先把 JS 的 Vue 写熟，再上 TS，顺序别反。

> 👉 本教程已补一篇动手实战：[第 12 章 · 给 user-admin 上 TypeScript](../12-TypeScript迁移实战.md)——带你把前面写的 user-admin 整体迁移成 TS，边迁边学。

### 3. 装一个代码规范工具

真实团队协作必备：

- **ESLint**：自动检查代码错误/风格；
- **Prettier**：自动格式化代码；
- **Vue 官方推荐配置**：`@vue/eslint-config-typescript` 等。

脚手架建项目时勾上 ESLint + Prettier 即可。

---

## 🚀 进阶方向（按兴趣挑）

### 组合式函数（Composables）

把可复用的逻辑（如"带分页的列表请求""防抖 ref"）抽成函数，跨组件复用。这是 Composition API 的精髓，相当于"自定义 hook"。VueUse（[vueuse.org](https://vueuse.org/)）是几百个现成组合式函数的库，强烈推荐。

### 组件设计

- **进阶 slot**：具名插槽、作用域插槽、动态组件 `<component :is>`；
- **依赖注入** `provide/inject`：跨多层组件传值（比 props 钻孔优雅，比 Pinia 轻）；
- **`<Teleport>`**：把弹窗渲染到 body；
- **`<Suspense>`**：异步组件加载状态。

### 按需引入 / 性能优化

- Element Plus 按需引入（`unplugin-vue-components`），减小打包体积；
- 路由懒加载（`() => import('./X.vue')`）；
- `<keep-alive>` 缓存组件状态；
- 虚拟滚动长列表。

### 测试

- **Vitest**：单元测试（组件、函数、store）；
- **Vue Test Utils**：专门测 Vue 组件。

### 服务端渲染（SSR）/ 全栈框架

- **Nuxt**：Vue 的全栈框架（SSR、文件路由、SEO）。当你需要 SEO 或首屏速度时上它。

---

## 📚 官方权威资源（收藏）

- **Vue 官方文档**：[cn.vuejs.org](https://cn.vuejs.org/) —— 最权威，遇到 API 问题第一站；
- **Vue Router 文档**：[router.vuejs.org](https://router.vuejs.org/zh/)；
- **Pinia 文档**：[pinia.vuejs.org](https://pinia.vuejs.org/zh/)；
- **Element Plus 文档**：[element-plus.org](https://element-plus.org/zh-CN/) —— 查组件用法；
- **Vite 文档**：[cn.vitejs.dev](https://cn.vitejs.dev/)。

---

## 🧭 思维上的下一步

你已经完成了最关键的转变：**从"操作 DOM"到"操作数据"**。带着这个思维：

- 学 **React**：思想几乎一样（声明式、组件、状态），只是 API 不同；
- 学 **React Native / 各种跨端**：同一套思维做移动端；
- 关注**前端工程化**：CI/CD、Docker、监控——从"写页面"到"交付产品"。

---

## 最后

你已经从 jQuery 程序员，成长为能独立做现代 Vue 项目的开发者。这不是终点，而是真正高效的起点。

去折腾、去造东西、去踩坑再爬出来——**这就是工程师成长的方式。** 🚀
