# Vite 构建工具从入门到进阶：写给 jQuery 程序员

> 从「一个 index.html 写天下」的裸 HTML 时代，迁移到现代构建工具 Vite。
> 全文以 **「裸 HTML/CDN 写法 → Vite 写法 → 为什么更好」** 对照为主线，带你把一个笔记应用从零搭到能上线，再浅尝库模式、自定义插件、SSR。

这是 vue3-glm 教程家族里**独立的一本**——它不教 Vue（那是 [主教程](../README.md) 的活），它专门讲 **Vite 这个构建工具**：项目怎么组织、配置怎么写、开发服务器与 HMR 怎么工作、怎么打包部署，以及进阶的库模式、自定义插件、SSR。

---

## 👤 这份教程写给谁

- 你写过 jQuery / 裸 HTML，习惯一个 `index.html` + 一堆 `<script>` 标签搞定一切；
- 你听说过 `npm`、`vite`、`webpack`、`打包`，但没真正搞懂「构建工具到底在干嘛」；
- 你可能已经看过主教程的[第 4 章](../docs/04-从CDN到Vite.md)，知道怎么 `npm create` 建项目，但想**真正吃透 Vite 本身**。

## 🔗 和主教程是什么关系

| | 主教程（Vue3 入门） | 本教程（Vite 专项） |
|---|---|---|
| 教什么 | Vue（响应式、组件、路由、Pinia） | Vite（配置、HMR、构建、部署、库/插件/SSR） |
| 主线 | jQuery → Vue 写法对照 | 裸 HTML/CDN → Vite 工程化对照 |
| 重叠点 | 第 4 章「从 CDN 到 Vite」是工程化入门 | 第 0 章「为什么是 Vite」会更深入讲原理 |

> 💡 **重叠是刻意的**：主教程第 4 章是"够用就行"的工程化入门；本教程第 0 章会正面回答"Vite 凭什么这么快"。两本可独立读，也可互补。

## 🧰 环境准备

和主教程完全一样：

1. **Node.js LTS**：去 [nodejs.org](https://nodejs.org) 装 LTS，验证 `node -v`（≥ 18）。装包慢可换镜像：`npm config set registry https://registry.npmmirror.com`
2. **编辑器**：VS Code + **Vue - Official** 插件。

> 如果你已经按主教程装好环境，这里直接开始即可。
>
> 📦 对 `npm` 零基础？先过一遍 [npm 极简速查教程](../npm-tutorial/README.md)。

## 📦 关于版本

- 本教程跟随 `npm create vite@latest` 的**最新稳定版**（不钉死大版本号）。
- 主仓库里主教程的示例项目用的是 Vite 5。**两者在入门涉及的 API（别名、环境变量、代理、HMR、构建、库模式、插件、SSR）上完全一致**，不影响学习。
- Vite 近期的新特性（Environment API、Rolldown 等）只在[第 14 章](docs/14-生态与下一步.md)作为"展望"提及，正文不涉及。

## 🗺️ 章节导航

**上篇 · 入门：把一个笔记应用搭到能上线**
- [第 0 章 · 为什么是 Vite：裸 HTML 撞墙记](docs/00-为什么是Vite.md)
- [第 1 章 · 10 分钟建一个 Vite 项目](docs/01-十分钟建项目.md)
- [第 2 章 · 看懂 Vite 项目结构](docs/02-看懂项目结构.md)
- [第 3 章 · 路径别名：告别 ../../../](docs/03-路径别名.md)
- [第 4 章 · 环境变量：dev 和线上用不同配置](docs/04-环境变量.md)
- [第 5 章 · 开发服务器与代理：解决跨域](docs/05-开发服务器与代理.md)
- [第 6 章 · HMR 热更新原理：凭什么秒级](docs/06-HMR热更新原理.md)
- [第 7 章 · 静态资源与 CSS：图片/字体/样式怎么管](docs/07-静态资源与CSS.md)
- [第 8 章 · 插件机制初识：Vite 的扩展点](docs/08-插件机制初识.md)
- [第 9 章 · 构建与产物：vite build 到底做了什么](docs/09-构建与产物.md)
- [第 10 章 · 部署：把 dist 推上线](docs/10-部署.md)
- [小结 · 把 vite-notes 部署上线](docs/小结-部署上线.md)

**下篇 · 进阶：浅尝即止（各自独立 demo）**
- [第 11 章 · 库模式：打包一个组件库](docs/11-库模式.md)
- [第 12 章 · 自定义插件开发入门](docs/12-自定义插件.md)
- [第 13 章 · SSR 概览：服务端渲染跑通](docs/13-SSR概览.md)
- [第 14 章 · 生态与下一步：environments / Rolldown](docs/14-生态与下一步.md)

**附录**
- [A · vite.config 常用配置速查](docs/appendices/A-vite.config速查.md)
- [B · 常见报错与调试](docs/appendices/B-常见报错调试.md)
- [C · 下一步学什么](docs/appendices/C-下一步.md)

## 📂 配套项目：vite-notes

上篇（第 1~10 章 + 小结）围绕一个累积项目 **[`project/vite-notes/`](project/vite-notes/)**（一个 Vue 笔记应用）展开。每章对应一个 git 分支，标记该项目"长到这一步"的代码状态：

| 分支 | 对应章节 | 项目状态 |
|---|---|---|
| `vite/01-init` | 第 1~2 章 | 脚手架基座，最小笔记壳 |
| `vite/02-alias` | 第 3 章 | 加 `@` 路径别名 |
| `vite/03-env` | 第 4 章 | 加 `.env` 环境变量 |
| `vite/04-proxy` | 第 5~6 章 | 加开发代理（请求 mock 接口） |
| `vite/05-assets` | 第 7~8 章 | 加静态资源 / CSS modules |
| `vite/06-build` | 第 9 章 | 加构建配置（chunk 拆分） |
| `vite/07-deploy` | 第 10 章 | 加部署配置（base 路径 / 路由兜底） |
| `vite/08-final` | 小结 | 最终成品（所有配置收敛） |

> 🔑 **怎么用**：想看"第 5 章做完时代码长啥样"，`git checkout vite/04-proxy` 即可对照。
>
> ⚠️ **重要（关于正文与代码的关系）**：**章节正文（`docs/`）永远在 `main` 分支**，切到 `vite/NN` 只换 `project/vite-notes/` 的代码、不换正文。磁盘上 `project/vite-notes/` 默认是 `vite/08-final` 最终成品；要看某章的中间态，用 `git checkout` 切到对应分支。

下篇（第 11~13 章）是三个**互相独立**的小 demo，各在各的目录里、互不依赖：

| demo | 对应章节 | 主题 |
|---|---|---|
| [`demos/lib-mode/`](demos/lib-mode/) | 第 11 章 | 库模式：把组件打包成可发布的库 |
| [`demos/plugin-hello/`](demos/plugin-hello/) | 第 12 章 | 写一个 hello 级自定义 Vite 插件 |
| [`demos/ssr-quick/`](demos/ssr-quick/) | 第 13 章 | 用官方姿势跑通 SSR |

---

准备好了？从 [第 0 章 · 为什么是 Vite](docs/00-为什么是Vite.md) 开始吧。
