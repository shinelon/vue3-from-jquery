# Vue3 入门教程 · 写给 jQuery 程序员

> 从 jQuery 的世界，平滑迁移到现代 Vue3 + Vite 开发。

很多 jQuery 老手第一次看 Vue 代码，心里都会冒出一个疑问：

> *"我用 jQuery 三行就搞定了，Vue 凭什么这么绕？"*

这份教程正面回答它。每讲一个 Vue 概念，都会先给你看 **「jQuery 怎么做 → Vue 怎么做 → 为什么更好」** 的对照，等你把整本读完、把 CRUD 项目搭出来，你会自己得出答案。

---

## 👤 写给谁

- 写过 jQuery，熟悉 `$('#id')`、`$.ajax`、表单和表格的增删改查；
- 但还没用过现代前端框架（Vue / React），对 `npm`、构建工具、组件化比较陌生；
- ES6 语法有点生疏——**没关系**，开头有一份极简速查。

## 🎯 学完能做到

- 理解 Vue3 三大核心心智：**响应式、声明式、组件化**；
- 用 **Vite + Vue3** 从零搭出带路由、Pinia、接口请求的 CRUD 应用；
- 看得懂公司里的 Vue3 项目，包括老项目的 **Options API** 写法。

## 🧰 技术栈

| 维度 | 选型 | 说明 |
|---|---|---|
| 框架 / 构建 | Vue 3 + Vite | 现代标准 |
| 代码风格 | `<script setup>`（Composition API） | 主流写法 |
| 语言 | 纯 JavaScript（结尾埋 TS 钩子） | 第 12 章迁移 |
| 路由 | Vue Router 4 | 多页面 |
| 状态管理 | Pinia | 全局状态 |
| UI 组件库 | Element Plus | 只当工具用 |
| 请求 | axios | 对照 `$.ajax` |
| 假后端 | json-server | 一条命令起 REST API |

> ⚠️ Element Plus 是第三方 UI 库，**不是 Vue 自带**。换成 Ant Design Vue / Naive Vue 完全一样。

---

## 📚 两套教程

本站收录两套层层递进的教程，从顶部标签页切换：

### 一、Vue3 入门教程

[:octicons-arrow-right-24: 序言：为什么 jQuery 程序员要学 Vue](vue3/docs/00-序言.md)
[:octicons-arrow-right-24: 前置：ES6 极简速查](vue3/docs/00b-ES6极简速查.md)
[:octicons-arrow-right-24: 第 1 章 · CDN 热身 Todo](vue3/docs/01-CDN热身-Todo.md)
[:octicons-arrow-right-24: 第 2 章 · 响应式](vue3/docs/02-响应式.md)
[:octicons-arrow-right-24: 第 3 章 · 模板语法](vue3/docs/03-模板语法.md)
[:octicons-arrow-right-24: 第 4 章 · 从 CDN 到 Vite](vue3/docs/04-从CDN到Vite.md)
[:octicons-arrow-right-24: 第 5 章 · 组件化](vue3/docs/05-组件化.md)
[:octicons-arrow-right-24: 第 6 章 · 项目搭建（CRUD）](vue3/docs/06-CRUD项目搭建.md)
[:octicons-arrow-right-24: 第 7 章 · 列表与查询](vue3/docs/07-列表与查询.md)
[:octicons-arrow-right-24: 第 8 章 · 新增与编辑](vue3/docs/08-新增与编辑.md)
[:octicons-arrow-right-24: 第 9 章 · 路由 Vue Router](vue3/docs/09-路由.md)
[:octicons-arrow-right-24: 第 10 章 · 状态管理 Pinia](vue3/docs/10-Pinia状态管理.md)
[:octicons-arrow-right-24: 第 11 章 · 收尾打包部署](vue3/docs/11-收尾打包部署.md)
[:octicons-arrow-right-24: 第 12 章 · TypeScript 迁移实战](vue3/docs/12-TypeScript迁移实战.md)

附录：[A · jQuery→Vue 速查表](vue3/docs/appendices/A-jQuery到Vue速查表.md) ·
[B · 常见报错与调试](vue3/docs/appendices/B-常见报错与调试.md) ·
[C · 下一步学什么](vue3/docs/appendices/C-下一步学什么.md)

### 二、Vite 构建工具教程（平行，可单独学）

[:octicons-arrow-right-24: 第 0 章 · 为什么是 Vite](vite/docs/00-为什么是Vite.md)
[:octicons-arrow-right-24: 第 1 章 · 十分钟建项目](vite/docs/01-十分钟建项目.md)
[:octicons-arrow-right-24: 第 2 章 · 看懂项目结构](vite/docs/02-看懂项目结构.md)
[:octicons-arrow-right-24: 第 3 章 · 路径别名](vite/docs/03-路径别名.md)
[:octicons-arrow-right-24: 第 4 章 · 环境变量](vite/docs/04-环境变量.md)
[:octicons-arrow-right-24: 第 5 章 · 开发服务器与代理](vite/docs/05-开发服务器与代理.md)
[:octicons-arrow-right-24: 第 6 章 · HMR 热更新原理](vite/docs/06-HMR热更新原理.md)
[:octicons-arrow-right-24: 第 7 章 · 静态资源与 CSS](vite/docs/07-静态资源与CSS.md)
[:octicons-arrow-right-24: 第 8 章 · 插件机制初识](vite/docs/08-插件机制初识.md)
[:octicons-arrow-right-24: 第 9 章 · 构建与产物](vite/docs/09-构建与产物.md)
[:octicons-arrow-right-24: 第 10 章 · 部署](vite/docs/10-部署.md)
[:octicons-arrow-right-24: 第 11 章 · 库模式](vite/docs/11-库模式.md)
[:octicons-arrow-right-24: 第 12 章 · 自定义插件](vite/docs/12-自定义插件.md)
[:octicons-arrow-right-24: 第 13 章 · SSR 概览](vite/docs/13-SSR概览.md)
[:octicons-arrow-right-24: 第 14 章 · 生态与下一步](vite/docs/14-生态与下一步.md)

附录：[A · vite.config 速查](vite/docs/appendices/A-vite.config速查.md) ·
[B · 常见报错调试](vite/docs/appendices/B-常见报错调试.md) ·
[C · 下一步](vite/docs/appendices/C-下一步.md)

---

## 🚀 本地预览

本站由 [MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) 驱动。在仓库根目录：

```bash
pip install -r requirements-docs.txt   # 安装 mkdocs + mkdocs-material
mkdocs serve                            # 打开 http://127.0.0.1:8000
```

修改 `docs-site/` 下任意 markdown，浏览器会自动刷新。

---

准备好了？从 [:octicons-arrow-right-24: 序言](vue3/docs/00-序言.md) 开始吧。
