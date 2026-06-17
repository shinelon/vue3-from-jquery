# Vue3 入门教程 · 写给 jQuery 程序员

> 从 jQuery 的世界，平滑迁移到现代 Vue3 + Vite 开发。

很多 jQuery 老手第一次看 Vue 代码，心里都会冒出一个疑问：

> *"我用 jQuery 三行就搞定了，Vue 凭什么这么绕？"*

这份教程正面回答它。每讲一个 Vue 概念，都会先给你看 **「jQuery 怎么做 → Vue 怎么做 → 为什么更好」** 的对照，等你把整本读完、把 CRUD 项目搭出来，你会自己得出答案。

---

## 👤 写给谁

- 写过 jQuery，熟悉 `$('#id')`、`$.ajax`、表单和表格的增删改查；
- 还没用过现代前端框架（Vue / React），对 `npm`、构建工具、组件化比较陌生；
- ES6 有点生疏——**没关系**，开头有极简速查。

## 🎯 学完能做到

- 理解 Vue3 三大核心心智：**响应式、声明式、组件化**；
- 用 **Vite + Vue3** 从零搭出带路由、Pinia、接口请求的 CRUD 应用；
- 看得懂公司里的 Vue3 项目，包括老项目的 **Options API** 写法。

## 🧰 技术栈

| 维度 | 选型 |
|---|---|
| 框架 / 构建 | Vue 3 + Vite |
| 代码风格 | `<script setup>`（Composition API） |
| 语言 | 纯 JS（第 12 章迁移 TS） |
| 路由 / 状态 | Vue Router 4 / Pinia |
| UI / 请求 / 假后端 | Element Plus / axios / json-server |

> ⚠️ Element Plus 是第三方 UI 库，**不是 Vue 自带**。换成 Ant Design Vue / Naive Vue 完全一样。

---

## 📚 从这里开始

本站收录两套教程，从顶部标签页切换，左侧目录即为完整章节导航。

**一、Vue3 入门教程** —— 从 jQuery 平滑迁移到 Vue3 + Vite，搭出一个 CRUD 用户管理系统。

:material-arrow-right: [序言：为什么 jQuery 程序员要学 Vue](vue3/docs/00-序言.md) ·
[ES6 极简速查](vue3/docs/00b-ES6极简速查.md) ·
[第 1 章 · CDN 热身 Todo](vue3/docs/01-CDN热身-Todo.md)

**二、Vite 构建工具教程**（平行，可单独学）—— 正面讲清 Vite 凭什么这么快。

:material-arrow-right: [第 0 章 · 为什么是 Vite](vite/docs/00-为什么是Vite.md) ·
[第 1 章 · 十分钟建项目](vite/docs/01-十分钟建项目.md)

**附录速查**：
[Vue3 · jQuery→Vue 速查表](vue3/docs/appendices/A-jQuery到Vue速查表.md) ·
[Vue3 · 常见报错与调试](vue3/docs/appendices/B-常见报错与调试.md) ·
[Vite · vite.config 速查](vite/docs/appendices/A-vite.config速查.md)

---

## 🚀 本地预览

本站由 [MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) 驱动：

```bash
pip install -r requirements-docs.txt   # 安装 mkdocs + mkdocs-material
mkdocs serve                            # 打开 http://127.0.0.1:8000
```

修改 `docs-site/` 下任意 markdown，浏览器自动刷新。

---

准备好了？从 [:material-arrow-right: 序言](vue3/docs/00-序言.md) 开始吧。
