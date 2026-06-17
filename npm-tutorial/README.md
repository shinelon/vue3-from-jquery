# npm 极简速查：写给 jQuery 程序员

> 从「手动下载 js 文件 / 用 CDN」的 jQuery 时代，迁移到现代前端的包管理器 npm。
> 一篇讲透：为什么需要 npm、怎么装好、最常用的几条命令、中国网络下的镜像与排错。

这是 vue3-glm 教程家族里**独立的一本**——它不教 Vue、也不教 Vite，它专门讲 **npm 这个包管理器**：怎么装依赖、`package.json` 是什么、`npm run` / `npx` 怎么用、国内怎么换镜像加速。

主教程和 Vite 教程里只要碰到 `npm install`、`npm run`，都默认你会了。这一本就是给你补这块前置知识的。

---

## 👤 这份教程写给谁

- 你写过 jQuery / 裸 HTML，习惯 `<script src="cdn/xxx.js">` 引库；
- 你听说过 `npm`、`node_modules`、`package.json`，但没真正搞懂「包管理器到底在干嘛」；
- 你想跟完 [主教程](../README.md) 或 [Vite 教程](../vite-tutorial/README.md)，但一上来就被各种 npm 命令劝退。

## 🔗 和另外两套教程是什么关系

| | 主教程（Vue3 入门） | Vite 教程（工具专项） | 本教程（npm 速查） |
|---|---|---|---|
| 教什么 | Vue（响应式、组件、路由、Pinia） | Vite（配置、HMR、构建、部署） | npm（装依赖、命令、镜像、排错） |
| 定位 | 主体 | 工具专项 | **前置 / 工具速查** |
| 篇幅 | 14 章 + 附录 | 15 章 + 附录 | 1 篇速查 + 命令附录 |

> 💡 **先读哪本**：如果你 npm 完全零基础，建议**先花 15 分钟过一遍本教程**，再进主教程或 Vite 教程，会顺畅很多。已有基础的可以直接当字典查。

## 🧰 环境准备

和主教程完全一样：去 [nodejs.org](https://nodejs.org) 装 **Node.js LTS**（装好 Node 就自动有了 npm），验证：

```bash
node -v   # ≥ 18
npm -v    # ≥ 9
```

## 🗺️ 章节导航

- [npm 极简速查（正文）](docs/00-npm速查.md) —— 8 节讲透，约 15 分钟读完
- [附录 A · npm 命令速查表](docs/appendices/A-命令速查表.md) —— 卡壳时当字典查

## 📂 配套 demo

正文第四、五节围绕一个极简 demo [`demos/npm-demo/`](demos/npm-demo/package.json) 展开：装一个依赖（lodash）、定义一个脚本、用 `npm run` 跑起来。

```bash
cd demos/npm-demo
npm install      # 装 lodash
npm run pick     # 跑脚本：随机抽一件「今天先做」的事
```

---

准备好了？从 [npm 极简速查](docs/00-npm速查.md) 开始吧。
