# 用户管理系统 · CRUD 实战项目

这是第 6~11 章的实战项目，从零搭建的 Vue3 用户管理后台。

技术栈：**Vue3 + Vite + Element Plus + axios + json-server**（第 9 章加 Vue Router，第 10 章加 Pinia）。

## 运行（需要两个终端）

**终端 1 — 起假后端：**

```bash
cd project/user-admin
npm install
npm run server      # json-server 跑在 :3000
```

**终端 2 — 起前端：**

```bash
npm run dev         # Vite 跑在 :5173
```

浏览器打开 http://localhost:5173 。

## 目录结构

```
user-admin/
├── db.json              假数据（json-server 的"数据库"）
├── vite.config.js       含 /api → :3000 代理配置
└── src/
    ├── App.vue          根组件
    ├── main.js          入口（注册 Element Plus / Router / Pinia）
    └── api/
        ├── request.js   axios 封装（实例 + 拦截器）
        └── user.js      用户接口
```

> 随章节推进，会陆续新增 `views/`（页面）、`components/`（弹窗表单）、`router/`（路由）、`stores/`（Pinia）。

## 章节进度对照

> 下表"阶段"对应各章代码的演进状态。**本项目磁盘是最终成品（≈ 第 11 章状态）**，并未真正初始化 git 分支；若想对照某章的中间态，请自行 `git init` 后按章节顺序分阶段提交。

| 阶段 | 章节 | 内容 |
|---|---|---|
| `ch06-init` | 第 6 章 | 骨架 + Element Plus + json-server 联通 |
| `ch07-list` | 第 7 章 | 列表与查询 |
| `ch08-form` | 第 8 章 | 新增与编辑 |
| `ch09-router` | 第 9 章 | 路由 |
| `ch10-pinia` | 第 10 章 | Pinia 状态管理 |
| `ch11-deploy` | 第 11 章 | 收尾打包部署（= 当前磁盘状态） |
