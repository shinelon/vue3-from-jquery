# npm 极简速查：写给 jQuery 程序员

你习惯了 `<script src="cdn/xxx.js">` 引库；现代前端几乎全靠 **npm**。这篇把 npm 讲到「够用且讲透」——**为什么需要它、怎么装好、最常用的几条命令、以及中国网络下的镜像与排错**。读完就能无障碍跟完 [主教程（Vue3）](../../docs/00-序言.md) 和 [Vite 教程](../../vite-tutorial/README.md)。

> 📂 配套 demo 在 [`demos/npm-demo/`](../demos/npm-demo/package.json)，一个最小可跑的 npm 项目。

---

## 一、为什么需要 npm（先对照 jQuery）

jQuery 时代用库的方式：去 CDN 网站或官网**手动下载** js 文件，塞进 `<script src>`。项目一大，痛点全来了：

- **版本靠脑子记**：用的 jQuery 是 1.x 还是 3.x？下错版本就出 bug；
- **依赖链要手动**：库 A 依赖库 B，你得自己再下个 B；
- **团队各下各的**：张三的 jQuery 3.5、李四的 3.7，环境不统一；
- **删库/改名就 404**：CDN 挂了，全站崩。

npm 时代一条命令搞定：`npm install axios` 把库拉到项目本地的 `node_modules/`，版本记进 `package.json`。团队共享同一份清单，谁 `npm install` 一下就能复刻全部依赖。

| | jQuery 时代 | npm 时代 |
|---|---|---|
| 怎么用库 | `<script src="cdn/xxx.js">` | `npm install xxx` 然后 `import` |
| 库存哪 | 远程 CDN | 项目本地 `node_modules/` |
| 版本管理 | 靠手 / 靠脑子 | 写进 `package.json`，可复刻 |

> 💡 一句话：**npm 把"用第三方库"这件事，从手动下载变成了可记录、可复刻的命令。**

---

## 二、装好 Node 就有了 npm

npm 跟着 Node 一起装，不用单独装。

1. 去 [nodejs.org](https://nodejs.org) 下载 **LTS 版本**，一路下一步；
2. 打开终端（Windows 用 PowerShell 或 Git Bash）验证：

```bash
node -v   # 应输出 v18 或更高
npm -v    # 应输出 9.x 或更高
```

> 有 `node` 就一定有 `npm`。两个命令都输出版本号，就说明装好了。

---

## 三、package.json：项目清单

每个 npm 项目根目录都有一个 `package.json`——项目的"身份证"，记录项目名、版本、依赖了哪些包、有哪些命令。

生成它（在项目目录里）：

```bash
npm init -y     # -y：用默认值快速生成
```

生成的 `package.json` 长这样（关键字段）：

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "scripts": {                 // 自定义命令，见第五节
    "dev": "vite"
  },
  "dependencies": {            // 生产依赖（运行时要用的）
    "vue": "^3.4.0"
  },
  "devDependencies": {         // 开发依赖（只在开发时用的）
    "vite": "^5.0.0"
  }
}
```

> 你**几乎不用手写** `package.json`——`npm install xxx` 会自动把依赖写进去。

---

## 四、npm install 与「依赖三件套」

最常用的两条：

```bash
npm install            # 不带参数：按 package.json 装齐所有依赖
npm install lodash     # 带包名：装某个包，并写进 package.json
```

装完会多出几个东西，搞清它们的**关系**是核心心智（新手最爱混）：

| 文件 / 目录 | 是什么 | 提交 git 吗 |
|---|---|---|
| `package.json` | **清单**：声明依赖了哪些包（你/团队维护） | ✅ 提交 |
| `node_modules/` | **实体**：实际下载的依赖代码（巨大、自动生成） | ❌ 不提交 |
| `package-lock.json` | **锁**：锁定每个依赖的确切版本，保证大家装的一致 | ✅ 提交 |

> 🔑 记住：**清单 + 锁 要提交，实体（node_modules）绝不提交**。别人拿到你的代码，跑一次 `npm install` 就能凭清单 + 锁，在本机复刻出一模一样的 `node_modules`。

**生产依赖 vs 开发依赖**（`-D`）：

```bash
npm install axios          # 默认进 dependencies（运行时要用，如 vue/axios）
npm install -D vitest      # -D 进 devDependencies（只开发时用，如测试/构建工具）
```

> 判断标准：**这个包上线后还要不要用它？** 要 → dependencies；只在本机开发/打包时用 → devDependencies。

**版本号前的 `^` 和 `~`**（semver）：

- `"vue": "^3.4.0"`：允许 `3.x.x`（小版本自动升）——**默认就是这个**，多数情况别动；
- `"vue": "~3.4.0"`：只允许 `3.4.x`（更保守）；
- `"vue": "3.4.0"`：写死，绝不升级（最稳但享受不到补丁）。

---

## 五、npm scripts：自定义命令

`package.json` 的 `scripts` 字段里定义命令，用 `npm run xxx` 跑：

```json
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "pick": "node pick.js"
}
```

```bash
npm run dev     # 等于执行 vite
npm run pick    # 等于执行 node pick.js
```

**为什么不直接敲 `vite`，非要 `npm run`？** 因为 `vite` 装在 `node_modules/.bin/` 里，不在系统 PATH 里，直接敲会"command not found"。`npm run` 会自动把 `node_modules/.bin` 加进 PATH，省得你写一长串路径。

> ⚠️ 几个"特权"命令可以省略 `run`：`npm start`、`npm test`（分别等于 `npm run start` / `npm run test`）。**其它命令都必须带 `run`**。新手常犯的错就是敲 `npm dev`（漏了 run）然后报错。

---

## 六、npx：一次性跑命令

`npx xxx` = 临时下载并运行某个包的命令，**跑完不留**，适合一次性的工具（比如脚手架）。

你其实已经见过它了——建项目用的：

```bash
npm create vite@latest     # 它背后就是 npx create-vite@latest
```

`npx` vs `npm run` 的区别：

| | `npm run xxx` | `npx xxx` |
|---|---|---|
| 跑什么 | `package.json` scripts 里**已定义**的命令 | 任意包里的命令 |
| 要先 install 吗 | 要（命令得先在 scripts 里定义好） | **不用**（临时下载来跑） |
| 典型场景 | `npm run dev` / `npm run build` | 建项目、跑一次性脚手架 |

---

## 七、换国内镜像（重要！）

npm 默认仓库 `registry.npmjs.org` 在国外，国内装包经常**慢到怀疑人生**甚至超时。换成阿里云镜像，速度立竿见影：

```bash
npm config set registry https://registry.npmmirror.com
```

验证是否换成功：

```bash
npm config get registry     # 应输出 https://registry.npmmirror.com/
```

> ⚠️ **旧的 `registry.npm.taobao.org` 已于 2022 年停用**，一定要用上面的 `npmmirror.com`，否则会装包失败。

---

## 八、常见排错

新手 90% 的"npm 怎么报错了"都在这几条里：

- **权限报错 `EACCES`**（macOS/Linux 常见）：别用 `sudo` 装包，改用 [nvm](https://github.com/nvm-sh/nvm) 管理 Node，或配置 npm 的全局前缀目录。Windows 一般没这问题。
- **依赖冲突 `ERESOLVE`**：装的几个包版本互相不兼容。先应急 `npm install --legacy-peer-deps`；根治得理清是谁和谁冲突。
- **装包慢 / 卡住**：先确认换了镜像（第七节）；还慢就清缓存 `npm cache clean --force` 再试。
- **`^` 误装了不兼容的新版**：把 `package.json` 里对应包的 `^` 改成 `~` 或写死版本，删掉 `node_modules` 和 `package-lock.json`，重新 `npm install`。

> 🚑 **万能急救**：遇到莫名其妙的错，**删掉 `node_modules` 和 `package-lock.json`，重新 `npm install`**，能解决一大半。这不是笑话，是真实经验。

---

## 小结

npm 三连，记住这个节奏就能跟完所有教程：

```
建项目  →  装依赖  →  跑命令
npm create    npm install    npm run xxx
```

外加两个关键认知：**依赖三件套**（清单 / 实体 / 锁）、**换好镜像**。

> 💡 想要完整命令字典随时查？看 [附录 A · npm 命令速查表](appendices/A-命令速查表.md)。
>
> 📦 npm 之外还有 **pnpm / yarn / cnpm**，命令大同小异（`pnpm install` / `yarn add`）。入门用 npm 就够了，等以后觉得慢再换 pnpm 不迟。

---

## ✅ 本篇你应掌握

- [ ] 说得出 npm 解决了 jQuery 时代手动下库的哪些痛点；
- [ ] 会验证 `node -v` / `npm -v`、用 `npm init -y` 生成 `package.json`；
- [ ] 理解**依赖三件套**：`package.json`（清单）/ `node_modules`（实体）/ `package-lock.json`（锁），知道哪些该提交 git；
- [ ] 会用 `npm install`（含 `-D` 区分生产/开发依赖）、`npm run xxx`、`npx`；
- [ ] 换好国内镜像（`npmmirror.com`），遇到报错知道先「删 node_modules 重装」。

> 🎉 搞定 npm，你就能顺畅地跟 [Vue3 主教程第 4 章](../../docs/04-从CDN到Vite.md) 和 [Vite 教程](../../vite-tutorial/README.md) 了。
