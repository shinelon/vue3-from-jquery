# 用户管理系统 · CRUD 实战项目（TypeScript 版）

这是第 12 章「扩展篇」的产物——把第 6~11 章的 JS 版 `user-admin` 整体迁移成 TypeScript。
功能、目录结构、UI 与 JS 版**完全一致**，区别仅在于：`.js` → `.ts`、`<script setup>` → `<script setup lang="ts">`、并补上了类型。

## 运行（需要两个终端）

**终端 1 — 起假后端：**

```bash
cd project/user-admin-ts
npm install
npm run server      # json-server 跑在 :3000
```

**终端 2 — 起前端：**

```bash
npm run dev         # Vite 跑在 :5173
```

浏览器打开 http://localhost:5173 。

## 多出来的两个命令（JS 版没有）

```bash
npm run type-check   # 只做类型检查（vue-tsc --noEmit），不打包
npm run build        # 先 vue-tsc 类型检查，通过后再 vite build
```

JS 版的 `npm run build` 只打包；TS 版的 `build` 会**先类型检查**，类型有错就编译失败——这正是 TS 的价值所在。

## 与 JS 版对照

| 文件 | JS 版 | TS 版 |
|---|---|---|
| 领域类型 | 无 | `src/types/user.ts`（`User` / `Role` / `UserForm`） |
| 入口 | `main.js` | `main.ts` |
| axios 封装 | `api/request.js` | `api/request.ts`（泛型封装，对齐拦截器拆外壳） |
| 接口 | `api/user.js` | `api/user.ts`（函数签名带 `Omit`/`Partial`） |
| Pinia | `stores/user.js` | `stores/user.ts`（`ref<SessionUser \| null>`） |
| 路由 | `router/index.js` | `router/index.ts`（`RouteRecordRaw[]`） |
| 弹窗 | `components/UserDialog.vue` | 同名，`<script setup lang="ts">`（`defineProps<T>` / `FormInstance`） |
| 列表 / 详情 | `views/*.vue` | 同名，`<script setup lang="ts">` |

> JS 版（`project/user-admin`）保持原样不动，方便两版并排对照「JS 写法 → TS 写法 → 换来了什么」。
