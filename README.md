# Vue3 入门教程：写给 jQuery 程序员

> 从 jQuery 的世界，平滑迁移到现代 Vue3 开发。
> 全文以 **「jQuery 写法 → Vue 写法 → 为什么更好」** 三栏对照为主线，带你从零搭出一个 CRUD 用户管理系统。

很多 jQuery 老手第一次看 Vue 代码，心里都会冒出一个疑问：

> *"我用 jQuery 三行就搞定了，Vue 凭什么这么绕？"*

这份教程就是来正面回答这个问题的。每讲一个 Vue 概念，都会先给你看"这事儿 jQuery 怎么做"，再看"Vue 怎么做"，最后讲清"**Vue 这样做省掉了什么、换来了什么**"。等你把整本读完、把 CRUD 项目搭出来，你会自己得出答案。

---

## 🖥️ 用 MkDocs 本地预览（推荐阅读方式）

除了直接看 `docs/` 里的 Markdown，本仓库还配了一个 **MkDocs + Material** 文档站点，带顶部导航、全文搜索、代码高亮、暗色模式和可运行 demo 内嵌预览。

```bash
# 需要 Python 3.10+（装好 pip 即可）
pip install -r requirements-docs.txt   # 安装 mkdocs + mkdocs-material
mkdocs serve                            # 浏览器打开 http://127.0.0.1:8000
```

- 站点内容根在 `docs-site/`（`vue3/` + `vite/` + `npm` 三套教程，配置见 `mkdocs.yml`）；
- `mkdocs build` 可生成纯静态站点到 `site/`，便于部署；
- **单一真源**：教程正文以 `docs/`、`vite-tutorial/docs/` 等原件为准；`docs-site/` 是由脚本生成的站点副本。改了原件后跑一次同步即可：

  ```bash
  bash scripts/sync-docs-site.sh   # 从原件重新生成 docs-site，并跑 strict 构建校验
  ```

---

## 👤 这份教程写给谁

- 你写过 jQuery，熟悉 `$('#id')`、`$.ajax`、表单和表格的增删改查；
- 但你还没用过现代前端框架（Vue / React），对 `npm`、构建工具、组件化比较陌生；
- 你的 ES6 语法可能有点生疏——**没关系**，教程开头有一份极简速查。

## 🎯 学完你能做到什么

- 理解 Vue3 的三大核心心智：**响应式**、**声明式**、**组件化**；
- 用 **Vite + Vue3** 从零搭出一个带路由、Pinia 状态管理、接口请求的 CRUD 应用；
- 看得懂公司里现有的 Vue3 项目，包括老项目里的 **Options API** 写法。

## 🧰 技术栈一览

| 维度 | 选型 | 说明 |
|---|---|---|
| 框架 / 构建 | Vue 3 + Vite | 现代标准 |
| 代码风格 | `<script setup>`（Composition API） | 现代项目主流；Options API 仅作对比小节 |
| 语言 | 纯 JavaScript | 不上 TypeScript，结尾埋个钩子 |
| 路由 | Vue Router 4 | 多页面 |
| 状态管理 | Pinia | 全局状态（登录态等） |
| UI 组件库 | Element Plus | 只当工具用，不是 Vue 的一部分 |
| 请求 | axios | 对照 `$.ajax` |
| 假后端 | json-server | 一条命令起 REST API，不用写后端 |

> ⚠️ **关于 Element Plus**：它是第三方 UI 库，**不是 Vue 自带的**。换成 Ant Design Vue / Naive Vue 完全一样，这里用它纯粹是为了省掉 CSS，别误会成"Vue 自带表格表单"。

---

## 📂 目录结构

```
vue3-glm/
├── README.md                  ← 你在这里（总索引）
├── docs/                      ← 教程正文，每章一个 md
│   ├── 00-序言.md
│   ├── 00b-ES6极简速查.md
│   ├── 01-CDN热身-Todo.md
│   ├── 02-响应式.md
│   ├── 03-模板语法.md
│   ├── 04-从CDN到Vite.md
│   ├── 05-组件化.md
│   ├── 06-CRUD项目搭建.md
│   ├── 07-列表与查询.md
│   ├── 08-新增与编辑.md
│   ├── 09-路由.md
│   ├── 10-Pinia状态管理.md
│   ├── 11-收尾打包部署.md
│   ├── 12-TypeScript迁移实战.md
│   └── appendices/
│       ├── A-jQuery到Vue速查表.md
│       ├── B-常见报错与调试.md
│       └── C-下一步学什么.md
├── demos/                     ← 基础章（1-5）的独立小 demo，打开即跑
│   ├── ch01-todo-cdn/
│   ├── ch02-reactivity/
│   ├── ch03-template/
│   ├── ch04-vite-start/
│   └── ch05-components/
├── project/
│   ├── user-admin/            ← 实战章（6-11）累积而成的完整 CRUD 项目（JS 版）
│   │   ├── db.json            ← json-server 假数据
│   │   └── src/ ...
│   └── user-admin-ts/         ← 第 12 章扩展篇：把 JS 版迁移成 TypeScript 的版本
├── vite-tutorial/             ← 独立的 Vite 构建工具教程（平行教程，可单独学）
└── npm-tutorial/              ← 独立的 npm 速查教程（前置/工具速查，可单独学）
```

### 两种代码，两种用法

- **`demos/`（第 1~5 章）**：每章一个**独立小 demo**，互不依赖。基础概念用它练，打开就能跑，聚焦当章知识点。
- **`project/user-admin/`（第 6~11 章）**：一个**逐渐长大的完整项目**。磁盘上的代码是**最终成品（≈ 第 11 章状态）**，仓库里**并未为每章单独建 git 分支**。各章的演进阶段见 [`project/user-admin/README.md`](project/user-admin/README.md) 的「章节进度对照」表：

  | 阶段 | 章节 | 内容 |
  |---|---|---|
  | `ch06-init` | 第6章 | 脚手架 + Element Plus + json-server |
  | `ch07-list` | 第7章 | 列表与查询 |
  | `ch08-form` | 第8章 | 新增与编辑 |
  | `ch09-router` | 第9章 | 路由 |
  | `ch10-pinia` | 第10章 | Pinia 状态管理 |
  | `ch11-deploy` | 第11章 | 收尾、打包、最终成品（= 当前磁盘状态） |

  想看“第 7 章做完时代码长啥样”，可按上表自行 `git init` 后分阶段提交，再 `git checkout ch07-list` 对照。

---

## 🔧 环境准备

先把项目代码克隆到本地，再装好这两样：

```bash
git clone https://github.com/shinelon/vue3-from-jquery.git
cd vue3-from-jquery
```

### 1. Node.js（自带 npm）

Vue3 的开发离不开 Node。去 [nodejs.org](https://nodejs.org) 下载 **LTS 版本**，一路下一步安装即可。

装完打开终端（Windows 用 PowerShell 或 Git Bash）验证：

```bash
node -v   # 应输出 v18 或更高
npm -v    # 应输出 9.x 或更高
```

> 装包慢的话，可以换成国内镜像：`npm config set registry https://registry.npmmirror.com`
>
> 📦 对 `npm` 完全零基础？先花 15 分钟过一遍 [npm 极简速查教程](npm-tutorial/README.md)，再回来会顺畅很多。

### 2. 编辑器：VS Code + Vue 官方插件

- 安装 [VS Code](https://code.visualstudio.com/)；
- 在插件市场搜索安装 **Vue - Official**（原名 Volar），这是 Vue 官方推荐的高亮/提示插件。

---

## 📖 怎么用这份教程

1. **顺序读 `docs/`**：章节是层层递进的，别跳着看，前面讲过的后面默认你会了。
2. **边读边跑代码**：每章都有对应的 `demos/` 或 `project/`，打开它、跑起来、**改一改**——jQuery 程序员最擅长"改了看效果"，这套反馈循环在 Vue 里照样适用。
3. **做完每章的小练习**：每章末尾有 1~3 个动手题和一份"本章你应掌握"清单，别跳过，那是把知识变成手感的关键。

---

## 🗺️ 章节导航

**热身（CDN，不用装环境）**
- [序言：为什么 jQuery 程序员要学 Vue](docs/00-序言.md)
- [前置：必须懂的 ES6 极简速查](docs/00b-ES6极简速查.md)
- [第 1 章 · 10 分钟上手：用 CDN 写个 Todo](docs/01-CDN热身-Todo.md)
- [第 2 章 · 响应式：告别手动改 DOM](docs/02-响应式.md)

**基础**
- [第 3 章 · 模板语法：v-if / v-for / v-model / v-on](docs/03-模板语法.md)
- [第 4 章 · 从 CDN 到 Vite：为什么要构建工具](docs/04-从CDN到Vite.md)
- [第 5 章 · 组件化：拆分与复用](docs/05-组件化.md)

**实战（CRUD 用户管理系统）**
- [第 6 章 · 项目搭建：脚手架 + Element Plus + json-server](docs/06-CRUD项目搭建.md)
- [第 7 章 · 列表与查询：el-table + axios + 分页](docs/07-列表与查询.md)
- [第 8 章 · 新增与编辑：el-form + 校验 + 弹窗](docs/08-新增与编辑.md)

**进阶**
- [第 9 章 · 路由 Vue Router：多页面](docs/09-路由.md)
- [第 10 章 · 状态管理 Pinia：登录态（先痛后甜）](docs/10-Pinia状态管理.md)
- [第 11 章 · 收尾：loading / 错误 / 打包部署](docs/11-收尾打包部署.md)

**扩展篇（正文之外）**
- [第 12 章 · 给 user-admin 上 TypeScript：迁移实战](docs/12-TypeScript迁移实战.md)

**🛠️ 工具专项（独立教程）**
- [Vite 构建工具从入门到进阶](vite-tutorial/README.md) —— 平行教程，专讲 Vite 本身，可单独学
- [npm 极简速查](npm-tutorial/README.md) —— 前置/工具速查，15 分钟搞懂 npm

**附录**
- [A · jQuery → Vue 速查对照表](docs/appendices/A-jQuery到Vue速查表.md)
- [B · 常见报错与调试](docs/appendices/B-常见报错与调试.md)
- [C · 下一步学什么](docs/appendices/C-下一步学什么.md)

---

准备好了？从 [序言](docs/00-序言.md) 开始吧。
