# 第 7 章 · 静态资源与 CSS：图片/字体/样式怎么管

裸 HTML 时代，图片往项目里一丢、`<img src="logo.png">` 一引用就行。工程化后，资源分两类、各有处理方式，CSS 也有多种写法。这一章理清 Vite 里资源与样式的管理。

> 📂 配套项目 `project/vite-notes/`，本章对应分支 `vite/05-assets`。

---

## 一、两种资源，两种放法：`public/` vs `src/assets/`

这是最容易混淆的一点。Vite 里静态资源有两个家：

| | `public/` | `src/assets/`（或 src 下任意处） |
|---|---|---|
| 怎么引用 | 绝对路径 `/xxx.png` | `import` 引入 |
| 构建处理 | **原样拷贝**到 dist 根 | 被 Vite **处理**（可压缩、加 hash 指纹） |
| 适合 | favicon、robots.txt、不需要改的第三方文件 | 你项目里用的图片、字体 |

### `public/`：原样拷贝

放 `public/` 里的文件，构建时**原样**拷到 `dist/` 根目录，引用时用绝对路径：

```html
<!-- public/robots.txt → 部署后 /robots.txt -->
<!-- public/favicon.svg → <link rel="icon" href="/favicon.svg"> -->
```

> 💡 `public/` 适合"不经过处理、直接放上线"的东西，比如 `robots.txt`、第三方统计脚本。

### `src/assets/`：被构建处理

放 `src/` 下的资源，要 `import` 引入，Vite 会处理它（小图转 base64 内联、大图加 hash 指纹防缓存）：

```vue
<script setup>
import logo from '@/assets/logo.svg'   // ← import 进来，logo 是处理后的 URL
</script>

<template>
  <img :src="logo" />   <!-- 用 import 来的地址 -->
</template>
```

> 🔑 为什么要 import 而不是直接写路径？因为 Vite 要**参与构建**——它会给文件加 hash（`logo-a3f9.svg`）防浏览器缓存、小文件转 base64 省请求。直接写 `src="@/assets/logo.svg"` 字符串，Vite 不认识、处理不了。

---

## 二、CSS 的几种写法

Vite 对 CSS 支持开箱即用，无需配置。常见几种：

### 1. 组件内 `<style scoped>`（最常用）

```vue
<style scoped>
h1 { color: #42b883; }   /* scoped：只作用于当前组件，不污染别的 */
</style>
```

`scoped` 给元素加 data 属性、CSS 加属性选择器，实现"样式只管这个组件"。

### 2. CSS Modules：类名自动加 hash

文件名 `xxx.module.css`，import 进来当对象用：

```css
/* NoteItem.module.css */
.item { padding: 8px 0; }
.done { text-decoration: line-through; }
```

```vue
<script setup>
import styles from './NoteItem.module.css'
</script>

<template>
  <li :class="styles.item">
    <span :class="{ [styles.done]: note.done }">{{ note.title }}</span>
  </li>
</template>
```

`styles.item` 实际编译成 `NoteItem_item_a3f9` 这样的唯一类名，**天然隔离**，不怕重名。

> 💡 `scoped` 和 CSS Modules 都解决"样式隔离"。`scoped` 是 Vue 特性、写法简单；CSS Modules 是通用标准、更灵活。日常用 `scoped` 居多。

### 3. 预处理器：Sass / Less

想用变量、嵌套、mixin？装个预处理器，Vite 自动识别：

```bash
npm install -D sass    # 或 less
```

```vue
<style lang="scss" scoped>
$primary: #42b883;
h1 { color: $primary; }
</style>
```

> 📌 Vite 对 Sass/Less/Stylus 都是"装了就能用"，不用配 loader（这点比 webpack 爽多了）。

### 4. 全局 CSS

在 `main.js` 引入一个全局样式：
```js
import './assets/global.css'
```

---

## 三、在 vite-notes 里实操

看 `vite/05-assets` 分支：

- 加了 `src/assets/logo.svg`，在 `App.vue` 里 `import logo from '@/assets/logo.svg'` 显示；
- 加了 `public/robots.txt`（演示 public 原样拷贝）；
- `NoteItem.vue` 改用 CSS Modules（`NoteItem.module.css`），演示类名隔离。

---

## 对照：资源与样式管理

| | 裸 HTML 时代 | Vite 工程化 |
|---|---|---|
| 图片 | 丢文件夹，`<img src="...">` | `src/assets/` + `import`（带 hash 防缓存） |
| 静态文件 | — | `public/` 原样拷贝 |
| 样式隔离 | 靠命名约定（易冲突） | `scoped` / CSS Modules 自动隔离 |
| 预处理器 | 单独编译 | 装了就能用 |

---

## 🏋️ 小练习

1. 把 `logo.svg` 换成你自己的图标，`npm run build` 后看 `dist/assets/` 里文件名是否带 hash；
2. 装 `sass`，把某组件的 `<style>` 改成 `lang="scss"`，用个变量。

---

## ✅ 本章你应掌握

- [ ] 区分 `public/`（原样拷贝、绝对路径）和 `src/assets/`（import、被处理）；
- [ ] 会 `import` 图片资源在模板里用；
- [ ] 知道 `scoped` 和 CSS Modules 两种样式隔离方式；
- [ ] 知道装 sass/less 后 `lang="scss"` 即可用预处理器。

> 🎉 资源和样式理清了。下一篇揭开 Vite 的"扩展点"——插件机制，搞懂 `@vitejs/plugin-vue` 干了啥，以及生态里那些"自动导入"插件。

下一篇 👉 [第 8 章 · 插件机制初识：Vite 的扩展点](08-插件机制初识.md)
