# 第 4 章 demo · Vite 起步项目

这是第 4 章的配套 Vite 项目，演示从 CDN 升级到工程化后的最小项目结构。

## 两种跑起来的方式

### 方式 A：用官方脚手架生成（推荐）

```bash
npm create vue@latest
# 项目名随意；TypeScript 选 No；Router/Pinia 选 Yes（后面章节要用）
cd 你的项目名
npm install
npm run dev
```

然后把本项目 `src/App.vue` 的内容复制过去对照即可。

### 方式 B：直接用本目录的最小项目

本目录已经是一个完整、最小、可独立运行的 Vite + Vue3 项目（不依赖脚手架向导）：

```bash
cd demos/ch04-vite-start
npm install
npm run dev
```

浏览器打开终端提示的地址（默认 `http://localhost:5173`）即可看到 Todo。

## 目录结构

```
ch04-vite-start/
├── index.html          页面入口
├── package.json        依赖清单 + 脚本
├── vite.config.js      Vite 配置
└── src/
    ├── main.js         入口：创建并挂载 Vue 应用
    └── App.vue         根组件：用 <script setup> 重写的 Todo
```

## 对照看

对比第 1 章 `demos/ch01-todo-cdn/index.html` 的 CDN 写法，体会 `<script setup>` 有多清爽——逻辑完全一样，只是不再需要 `createApp` / `setup()` / `return`。
