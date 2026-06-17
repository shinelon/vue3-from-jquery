# 附录 A · npm 命令速查表

写代码卡壳时翻这个表。本教程涉及的 npm 命令，按用途汇总。

---

## 安装 / 卸载

| 命令 | 作用 |
|---|---|
| `npm install`（或 `npm i`） | 按 `package.json` 装齐所有依赖 |
| `npm install <包>` | 装某个包，写进 `dependencies` |
| `npm install -D <包>` | 装开发依赖，写进 `devDependencies` |
| `npm install -g <包>` | 全局安装（命令行工具，如 `json-server`） |
| `npm uninstall <包>` | 卸载并从 `package.json` 移除 |

---

## 运行脚本

| 命令 | 作用 |
|---|---|
| `npm run <脚本名>` | 跑 `package.json` 的 `scripts` 里定义的命令 |
| `npm start` | 特权命令，等于 `npm run start` |
| `npm test` | 特权命令，等于 `npm run test` |
| `npx <包>` | 临时下载并运行某个包的命令（不长期安装） |

---

## 建项目

| 命令 | 作用 |
|---|---|
| `npm init -y` | 用默认值快速生成 `package.json` |
| `npm create vite@latest` | 用 Vite 脚手架建项目（背后是 `npx create-vite`） |
| `npm create vue@latest` | 用 Vue 官方脚手架建项目 |

---

## 查看 / 管理

| 命令 | 作用 |
|---|---|
| `npm list` | 查看已装的依赖树 |
| `npm outdated` | 查看哪些依赖有新版本 |
| `npm update` | 升级能升的依赖（受 semver 约束） |
| `npm -v` / `node -v` | 查看 npm / node 版本 |

---

## 镜像 / 缓存

| 命令 | 作用 |
|---|---|
| `npm config set registry https://registry.npmmirror.com` | 换阿里云镜像（国内加速） |
| `npm config get registry` | 查看当前镜像源 |
| `npm cache clean --force` | 清空 npm 缓存（装包出问题时试试） |

---

## 急救（报错时）

| 命令 | 作用 |
|---|---|
| 删 `node_modules` + `package-lock.json` 后 `npm install` | 万能急救，解决一大半莫名报错 |
| `npm install --legacy-peer-deps` | 应急绕过 `ERESOLVE` 依赖冲突 |

---

> 💡 完整命令查 [npm 官方文档](https://docs.npmjs.com/cli/)。
