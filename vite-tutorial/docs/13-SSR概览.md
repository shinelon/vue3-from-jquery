# 第 13 章 · SSR 概览：服务端渲染跑通

前面所有应用都是 **CSR（客户端渲染）**——浏览器下载空 HTML + JS，JS 在浏览器里把页面渲染出来。这一章看另一种方式 **SSR（服务端渲染）**——HTML 在服务器上就渲染好再发给浏览器。我们用官方姿势跑通一个最小 SSR。**本章浅尝即止，重点是建立概念。**

> 📂 配套 demo 在 [`demos/ssr-quick/`](../demos/ssr-quick/)，一个最小 SSR 应用。

---

## 一、CSR vs SSR：为什么要 SSR

**CSR（客户端渲染）**：你前面写的所有应用都是。
- 浏览器拿到一个几乎空的 `index.html`（只有 `<div id="app">`）；
- JS 下载后，在浏览器里执行，把页面"画"出来；
- **缺点**：首屏白屏（要等 JS 下载执行）、SEO 差（爬虫看到的是空 HTML）。

**SSR（服务端渲染）**：
- 服务器把 Vue 组件渲染成 HTML 字符串，**直接放进响应的 HTML**；
- 浏览器拿到的是**已经有内容的 HTML**，首屏立即可见、爬虫能抓到；
- 然后浏览器再"激活（hydration）"这个 HTML，接上交互。

| | CSR | SSR |
|---|---|---|
| 首屏速度 | 慢（等 JS） | 快（HTML 直接有内容） |
| SEO | 差 | 好 |
| 服务器负担 | 轻（只发静态文件） | 重（要渲染） |
| 复杂度 | 简单 | 复杂（要写服务端代码） |

> 📌 大多数后台管理系统用 CSR 就够（不要 SEO、内网用）；要做内容站、官网、电商首屏，才考虑 SSR。

---

## 二、SSR 的核心：同一套 Vue 代码，两个入口

SSR 的关键是：**同一个 Vue 应用，既能在服务器渲染成 HTML，又能在浏览器接管交互**。所以有两个入口：

- `entry-server.js`：服务端入口，用 `@vue/server-renderer` 把组件渲染成 HTML 字符串；
- `main.js`（客户端入口）：用 `createSSRApp` 在浏览器"激活"HTML。

加一个 `server.js`（用 express + Vite 的 middleware 模式）把两者串起来。

---

## 三、最小 SSR 的结构

看 [`demos/ssr-quick/`](../demos/ssr-quick/)：

```
ssr-quick/
├── server.js            ← express 服务器，中间件模式跑 Vite
├── vite.config.js       ← server.middlewareMode: true
├── index.html           ← 含 <!--ssr-outlet--> 占位
└── src/
    ├── App.vue          ← 同一个组件
    ├── main.js          ← 客户端入口（createSSRApp + hydration）
    └── entry-server.js  ← 服务端入口（renderToString）
```

`vite.config.js` 关键：开启 middleware 模式，让 Vite 在服务端跑：
```js
export default defineConfig({
  plugins: [vue()],
  server: { middlewareMode: true }   // 让 Vite 当中间件，而非独立 dev 服务器
})
```

`server.js` 用 express 接管：每个请求来了，用 `vite.ssrLoadModule` 加载 `entry-server.js` 渲染出 HTML，塞进模板返回。

---

## 四、跑起来

```bash
cd demos/ssr-quick
npm install
npm run dev      # 实际跑 node server
```

打开 `http://localhost:3000`，**查看网页源代码**（Ctrl+U）——你会看到 `<div id="app">` 里**已经有组件的 HTML 内容**（而不是空的）。这就是 SSR：服务器把内容渲染好了。

> 🔑 对比 CSR：CSR 的源代码里 `<div id="app">` 是空的，内容靠 JS 现填；SSR 的源代码里已经有内容。

---

## 五、hydration（激活）

服务器返回的 HTML 是"静态"的（没有交互）。浏览器加载 `main.js` 后，用 `createSSRApp` 把这个静态 HTML"激活"——挂上事件监听、接管响应式。这个过程叫 **hydration（水合/激活）**。

如果 hydration 出问题（服务端和客户端渲染结果不一致），Vue 会警告。这是 SSR 调试的常见坑。

---

## 六、生产部署 SSR（了解）

dev 用 `node server`。生产要：
1. `vite build`（构建客户端）+ `vite build --ssr`（构建服务端 bundle）；
2. 跑 `node server`（用打包后的 bundle，不再实时编译）。

> ⚠️ 完整的 SSR 生产部署较复杂（进程管理、缓存、流式渲染等）。**实际项目别手搭**，用现成框架：
> - **Nuxt**（Vue 的 SSR 框架，开箱即用，最推荐）；
> - 或 Vite 官方的 [SSR 指南](https://vite.dev/guide/ssr)。
> 本章只是让你理解原理、跑通最小例子。

---

## 对照：渲染方式

| | CSR（前面所有章节） | SSR（本章） |
|---|---|---|
| HTML 来源 | 浏览器 JS 现渲染 | 服务器渲染好 |
| 首屏 | 白屏等 JS | 直接有内容 |
| SEO | 差 | 好 |
| 适合 | 后台管理、内网应用 | 内容站、官网、电商首屏 |

---

## 🏋️ 小练习

1. 跑起 ssr-quick，查看页面源代码，确认 `<div id="app">` 里有内容（SSR 生效）；
2. 把 App.vue 改成显示当前时间（`new Date()`），观察服务端和客户端渲染的时间是否一致（hydration 的典型坑）。

---

## ✅ 本章你应掌握

- [ ] 区分 CSR 和 SSR，知道各自的优缺点和适用场景；
- [ ] 理解 SSR 的核心：同一套代码，两个入口（server + client）；
- [ ] 会用 middleware 模式 + express 跑通最小 SSR；
- [ ] 知道 hydration 是什么；
- [ ] 知道生产用 Nuxt 等框架，别手搭。

> 🎉 三个进阶主题（库/插件/SSR）都浅尝过了。下一篇收尾，讲讲 Vite 的生态走向（environments / Rolldown）和你接下来该学什么。

下一篇 👉 [第 14 章 · 生态与下一步：environments / Rolldown](14-生态与下一步.md)
