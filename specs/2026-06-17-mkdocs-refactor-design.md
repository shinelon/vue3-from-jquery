# 设计：将教程重构为 MkDocs（Material）站点

> **⚠️ 现状勘误（落地后演进，以仓库现状为准）**
>
> 本文档记录的是 MkDocs 重构最初的设计决策。落地后有三处发生了演进，**实际配置以 `mkdocs.yml`、根 `README.md` 为准**：
>
> 1. **教程范围**：已从「Vue3 + Vite 两套」扩展为**三套**，新增 `npm` 速查教程（`docs-site/npm/`）。下文凡写「两套」处均应理解为已含 npm。
> 2. **搜索分词语言**：`plugins.search.lang` 已从 `[en, ja]` 调整为 **`[en]`**（ja 在 lunr 下并不能真正提升中文召回，且有构建报错风险），见 `mkdocs.yml` 注释。
> 3. **`docs-site/` 定位**：已从「教程唯一源」调整为**「由 `scripts/sync-docs-site.sh` 生成的站点副本」**；正文单一真源仍是原件（`docs/`、`vite-tutorial/docs/` 等），原件保留不删。
>
> 其余决策（Material 主题、`use_directory_urls: false`、`font: false` 等）与现状一致。

- 日期：2026-06-17
- 目标：把仓库内两套教程（主 Vue3 教程 + Vite 工具教程）重构为一个 Python MkDocs 站点。
- 决策（已与用户确认）：
  1. 范围 = Vue3 + Vite 合建一个站点。
  2. 主题 = Material（mkdocs-material）。
  3. 源码布局 = 新建 `docs-site/` 迁入内容，原 `docs/`、`demos/`、`project/`、`vite-tutorial/` 保留不动。

## 1. 现状

- 主教程：`docs/`（14 篇正文 `00`~`12` + `appendices/` A/B/C），全中文。
- Vite 教程：`vite-tutorial/docs/`（`00`~`14` + `小结-部署上线.md` + `appendices/` A/B/C）。
- 可运行代码：`demos/`（17 文件）、`project/`（35 文件）、`vite-tutorial/demos/`（23 文件）；`node_modules` 未被 git 跟踪。
- 无图片资源（纯文本 + 代码块）。
- git remote：https://github.com/shinelon/vue3-from-jquery（`repo_url` 已配置在 `mkdocs.yml`）。
- 环境：Python 3.14.2 + pip 25.3 可用；无任何现成 MkDocs 配置。
- Markdown 内链形式：`../demos/chXX-…/`、`../project/…/`、同目录 `XX-章.md`。

## 2. 目标目录结构

按「每套教程的 docs/demos/project 作为同级三件套」整体迁入 `docs-site/`，使原始相对链接**零改写**继续生效：

```
vue3-glm/
├── mkdocs.yml
├── requirements-docs.txt
├── docs-site/
│   ├── index.md                      # 站点首页（总入口）
│   ├── vue3/
│   │   ├── docs/                     # 00-序言 … 12-TypeScript + appendices/
│   │   ├── demos/                    # ch01-05
│   │   └── project/                  # user-admin, user-admin-ts
│   └── vite/
│       ├── docs/                     # 00-为什么是Vite … 14 + 小结 + appendices/
│       ├── demos/                    # lib-mode, plugin-hello, ssr-quick
│       └── project/                  # vite-notes
├── site/                             # mkdocs build 产物（.gitignore）
└── 原有 docs/ demos/ project/ vite-tutorial/   # 保留不动
```

链接解析验证（无需改写）：
- `docs-site/vue3/docs/02-响应式.md` 中 `../demos/ch02-reactivity/` → `docs-site/vue3/demos/ch02-reactivity/` ✓
- `docs-site/vue3/docs/06-CRUD项目搭建.md` 中 `../project/user-admin/` → `docs-site/vue3/project/user-admin/` ✓
- 同目录 `03-模板语法.md` → `docs-site/vue3/docs/03-模板语法.md` ✓
- Vite 同理（`docs-site/vite/...`）✓

## 3. mkdocs.yml 配置

- `docs_dir: docs-site`
- `site_name`、`site_description`、`site_url`（留空）
- `theme.name: material`，`language: zh`
  - `features`：`navigation.tabs`、`navigation.sections`、`navigation.top`、`search.suggest`、`search.highlight`、`content.code.copy`、`content.code.annotate`、`toc.follow`
  - `palette`：明/暗双主题，跟随系统 + 手动切换
- `markdown_extensions`：
  - `admonition`、`pymdownx.details`、`pymdownx.superfences`
  - `pymdownx.highlight`（`anchor_linenums: true`）、`pymdownx.inlinehilite`
  - `pymdownx.tabbed`（`alternate_style: true`）
  - `pymdownx.tasklist`（`custom_checkbox: true`）
  - `pymdownx.emoji`
  - `toc`（`permalink: true`）
  - `attr_list`、`md_in_html`、`tables`、`def_list`
- `plugins`：
  - `search`，`lang: [en, ja]`（借日语分词近似支持中文搜索，社区常用，无额外依赖；如构建报错则回退 `[en]`）
- `nav`：首页 → Vue3 教程（序言、ES6、1~12 章、附录 A/B/C）→ Vite 工具教程（0~14 章、小结、附录 A/B/C）。
- 顶部 tabs 对应三大区。

## 4. 依赖（requirements-docs.txt）

```
mkdocs>=1.6
mkdocs-material>=9.5
```

仅两个核心包，最小化依赖。

## 5. 首页 index.md

从根 README 提炼，做成站点落地页：教程定位、写给谁、技术栈表、章节导航两大区入口、本地预览说明。不照搬 README（README 仍是仓库说明）。

## 6. 构建与验证

- 安装：`pip install -r requirements-docs.txt`
- 预览：`mkdocs serve` → http://127.0.0.1:8000
- 构建：`mkdocs build` → `site/`
- `.gitignore` 增加 `site/`、`__pycache__/`。
- 验证项：构建零严重错误；内链不报 broken；中文搜索可用；代码高亮、勾选框、提示块正常渲染。

## 7. 后续维护

- `docs-site/` 成为教程**唯一源**；原 `docs/` 等保留为历史副本，待用户确认后可删。
- 根 README 增补「用 MkDocs 本地预览」小节。

## 8. 不做（YAGNI）

- 不做 GitHub Pages 自动部署（无 remote，且未要求）。
- 不引入版本化（mike）。
- 不做 i18n 多语言切换。
- 不写自定义插件。
