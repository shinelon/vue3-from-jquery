# 第 4 章 · 从 CDN 到 Vite：为什么要构建工具

前三章我们用一个 html 文件 + CDN 就跑起了 Vue——简单直接。但当项目变大，这种方式一定会**撞墙**。这一章我们升级到现代前端的标准姿势：**Vite 工程化**。

> 📂 配套项目在 [`demos/ch04-vite-start/`](../demos/ch04-vite-start/)，一个最小可跑的 Vite 项目。

---

## 一、CDN 方式为什么不够用

前面三章用一个 `index.html` 写所有代码，挺爽。但项目稍微大一点，你会发现：

1. **所有代码挤在一个 html 里**，几百上千行，改一处要翻半天；
2. **用不了 npm 生态**：Element Plus、axios、Pinia 这些库都靠 `import` 引入，CDN 方式很别扭；
3. **没法拆组件**：`.vue` 单文件组件是 Vue 的核心，CDN 方式用不顺；
4. **没法压缩打包**：上线时代码要压缩、合并、优化，手动做不现实；
5. **协作混乱**：版本管理、依赖统一都难。

jQuery 时代你也许用过 RequireJS / sea.js 管理模块——现代前端统一用 **npm + 构建工具** 来解决这些问题。这个构建工具，Vue 官方推荐 **Vite**。

---

## 二、npm 是什么（给 jQuery 老哥的解释）

`npm` = Node Package Manager，Node 的包管理器。

**类比一下你熟悉的方式：**

| | jQuery 时代 | npm 时代 |
|---|---|---|
| 怎么用库 | `<script src="cdn/jquery.js">` | `npm install axios` 然后 `import` |
| 库存哪 | 远程 CDN | 项目本地的 `node_modules/` |
| 仓库 | 各个 CDN 网站 | [npmjs.com](https://npmjs.com) 一个公共仓库 |

简单说：**npm 把库下载到你项目本地，你再 import 进来用**。好处是版本统一、离线可用、依赖清晰。

---

## 三、创建第一个 Vite 项目

打开终端（Windows 用 PowerShell 或 Git Bash），`cd` 到你想放项目的目录，执行：

```bash
npm create vue@latest
```

它会问你几个问题，**入门阶段这样选**：

```
Project name: … hello-vue        ← 项目名，随便起
TypeScript: … No                 ← 用纯 JS（本教程不用 TS）
JSX Support: … No
Vue Router: … Yes                ← 第 9 章要用，先装上
Pinia: … Yes                     ← 第 10 章要用，先装上
Vitest: … No
End-to-End Testing: … No
ESLint: … No                     ← 入门先不管代码规范
Prettier: … No
```

然后进入项目、装依赖、启动：

```bash
cd hello-vue
npm install      # 安装所有依赖（第一次稍慢，1~2 分钟）
npm run dev      # 启动开发服务器
```

终端会显示 `Local: http://localhost:5173/`，浏览器打开它，看到 Vue 欢迎页就成了。**改代码会自动刷新**（这叫热更新 HMR），非常舒服。

---

## 四、项目结构解读

```
hello-vue/
├── node_modules/      ← npm 装的依赖（别手动改，别提交 git）
├── public/            ← 静态资源（图标等，原样拷贝）
├── src/
│   ├── assets/        ← 图片等资源（会被构建处理）
│   ├── components/    ← 你的组件放这里
│   ├── App.vue        ← 根组件（主战场）
│   └── main.js        ← 入口文件
├── index.html         ← 页面入口（现在很干净）
├── package.json       ← 项目"身份证"：依赖清单 + 脚本
└── vite.config.js     ← Vite 配置
```

几个重点文件：

**`package.json`** —— 项目的身份证，记录了项目名、依赖了哪些包、有哪些命令：
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "vue": "^3.4.0"
  }
}
```

**`src/main.js`** —— 入口，创建 Vue 应用并挂载：
```js
import { createApp } from 'vue'   // ← 这就是 ES Module 的 import
import App from './App.vue'

createApp(App).mount('#app')      // ← 挂载到 index.html 的 #app
```

**`src/App.vue`** —— 根组件，你写代码的主战场。

**`index.html`** —— 现在干净得很，只有一个 `<div id="app">` 和一行 `<script src="/src/main.js">`，不再是 CDN 时代塞满代码的样子。

---

## 五、`.vue` 单文件组件（SFC）：三段式

一个 `.vue` 文件固定分三段：

```vue
<template>
  <!-- HTML 结构 -->
</template>

<script setup>
// JS 逻辑
</script>

<style scoped>
/* CSS（scoped = 只作用于当前组件，不会污染别的组件） */
</style>
```

> 这种"一个文件里把结构/逻辑/样式写一起"的方式，叫**单文件组件（SFC）**。它是 Vue 的核心组织方式——每个 `.vue` 就是一个自包含的组件。

---

## 六、`<script setup>`：比第 1 章清爽得多

回忆第 1 章 CDN 的写法：

```js
createApp({
  setup() {
    const count = ref(0)
    return { count }          // ← 要手动 return
  }
}).mount('#app')
```

现在用 `<script setup>`：

```vue
<script setup>
import { ref } from 'vue'
const count = ref(0)          // ← 直接写，不用包在 setup() 里，不用 return
</script>

<template>
  <button @click="count++">{{ count }}</button>
</template>
```

清爽多了！**逻辑和上一章完全一样**，区别只是：

1. 不用写 `createApp` / `setup()` / `return`；
2. 顶层声明的变量、函数**自动**就能在模板里用；
3. `import` 正常用（如 `import { ref } from 'vue'`）。

> 📌 这就是序言里承诺的"第 4 章后写法更清爽、但逻辑一样"。**从现在起，所有代码都用 `<script setup>`**。

---

## 七、对照：把第 1 章的 Todo 搬进 Vite

看 [`demos/ch04-vite-start/src/App.vue`](../demos/ch04-vite-start/src/App.vue)，同样的 Todo，现在用 `<script setup>` 写：

```vue
<script setup>
import { ref } from 'vue'

const text = ref('')
const todos = ref([])

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
  <h1>Todo · Vite + script setup 版</h1>
  <input v-model="text" placeholder="输入任务" @keyup.enter="add" />
  <button @click="add">添加</button>
  <ul>
    <li v-for="t in todos" :key="t.id">
      {{ t.text }}
      <button @click="remove(t.id)">删除</button>
    </li>
  </ul>
</template>

<style scoped>
/* 这里的样式只作用于本组件 */
ul { list-style: none; padding: 0; }
li { padding: 8px 0; border-bottom: 1px solid #eee; }
</style>
```

跑起来看看（`npm run dev`），效果和第 1 章一样，但代码组织正规多了。

---

## 八、常用 npm 命令速查

| 命令 | 作用 |
|---|---|
| `npm install`（或 `npm i`） | 安装 `package.json` 里列的所有依赖 |
| `npm install axios` | 安装某个包（会写进 dependencies） |
| `npm run dev` | 启动开发服务器（热更新，改代码自动刷新） |
| `npm run build` | 打包生产版本（输出到 `dist/`，准备上线） |
| `npm run preview` | 本地预览打包后的结果 |

> 🔑 **记住三连**：建项目（`npm create`）→ 装依赖（`npm install`）→ 跑起来（`npm run dev`）。

---

## 九、为什么是 Vite，不是 webpack

你可能听过 webpack。简单说：

- **webpack**：老牌、功能全、但配置复杂、启动慢；
- **Vite**：新一代、启动**秒级**、配置极少、Vue 官方推荐。

入门直接用 Vite，没必要碰 webpack。等以后公司老项目用到，再补也不迟。

---

## 🏋️ 小练习

1. 把欢迎页改成你自己的内容（改 `App.vue` 的 `<template>`）；
2. 把**第 2 章的商品计算器**搬进这个 Vite 项目（新建一个 `Calculator.vue` 组件，在 `App.vue` 里用 `<Calculator />` 引入——这其实就是在练第 5 章的组件化）。

---

## ✅ 本章你应掌握

- [ ] 知道 CDN 方式为什么不够用；
- [ ] 会用 `npm create vue@latest` 建项目、`npm install` 装依赖、`npm run dev` 跑起来；
- [ ] 看懂 Vite 项目的基本结构（`src`、`App.vue`、`main.js`、`package.json`）；
- [ ] 理解 `.vue` 的三段式（`template`/`script setup`/`style scoped`）；
- [ ] 会用 `<script setup>` 写组件，理解它和第 1 章 CDN 写法的对应关系。

> 🎉 到这里，你已经具备了 Vue 的全部基础。接下来第 5 章讲组件化（把页面拆成零件），然后第 6 章起，我们正式开干 **CRUD 用户管理系统**。

下一篇 👉 [第 5 章 · 组件化：拆分与复用](05-组件化.md)
