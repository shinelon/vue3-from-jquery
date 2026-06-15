# 第 12 章 · 扩展篇：给 user-admin 上 TypeScript

> 📂 可运行项目在 [`project/user-admin-ts/`](../project/user-admin-ts/)——第 6~11 章那个 JS 版 CRUD，整体迁移成了 TypeScript。功能、UI、目录结构跟 JS 版**一模一样**，区别只在 `.js → .ts` 和补上了类型。

---

恭喜你把 1~11 章的 user-admin 跑通了。附录 C 里埋过一个钩子：**真实公司里的 Vue 项目，大量用 TypeScript（TS）**。这一章就来兑现它——带你把亲手写的 JS 版 user-admin，整体改写成 TS 版。

这一章是**扩展篇**，排在「正文到此结束」之后：

- 正文（1~11 章）教的是 **Vue 本身**，全程纯 JS——这个顺序**不能反**，先学熟 JS 的 Vue，再上 TS；
- 这一章教的是 **TS 怎么叠加到 Vue 上**，是给「已经会 Vue」的人补的一层。

> 💡 还没把 1~11 章的 user-admin 跑起来？先回去跑通。这一章全程拿那个项目当对照。

---

## 一、先回答一个灵魂问题：什么时候值得上 TS？

jQuery 程序员的直觉是：「JS 跑得好好的，凭啥多一层 TS？多写一堆类型不累吗？」——这问得好。先给判断框架，别无脑上：

| 场景 | 要不要上 TS |
|---|---|
| 自己写个 demo、练手、一次性脚本 | **不用**。JS 更快，别给自己加戏 |
| 团队协作、多人改同一个项目 | **强烈建议**。类型就是「不用写在文档里的文档」，同事一看函数签名就知道怎么调 |
| 要长期维护、迭代半年的项目 | **建议**。TS 能在「重构」时救命（改个字段名，所有用到的地方立刻报错） |
| 接手公司存量 TS 项目 | **必须懂**。看不懂类型 = 看不懂代码 |

一句话：**TS 的价值在「项目变大、人变多、时间变长」时才兑现**。小项目上 TS 是给自己找麻烦——这也是为什么本教程正文用 JS、把 TS 放在最后。

> ⚠️ 本章不是 TS 语言教程，而是「**把你已经写熟的 Vue 项目，迁移到 TS**」。TS 语法只讲迁移用得上的那一点（下一节）。

---

## 二、迁移要用的 TS 极简速查

类比开头的「ES6 极简速查」——这一节只讲本章会用到的，够用就行，不展开成教科书。

**① 类型标注**：给变量/参数/返回值标类型

```ts
let count: number = 0
function add(a: number, b: number): number { return a + b }
```

**② `interface` / `type`**：描述一个数据的「形状」

```ts
interface User { id: number; name: string; role: 'admin' | 'editor' | 'viewer' }
```

**③ 字面量联合类型**：把一个值限定成几个固定选项（本章大杀器）

```ts
type Role = 'admin' | 'editor' | 'viewer'   // 只能是这三个字符串之一，写错就报错
type Status = 0 | 1                          // 只能是 0 或 1
```

**④ 泛型 `<T>`**：给函数/类型一个「占位类型」，调用时再确定

```ts
function get<T>(url: string): Promise<T> { /* ... */ }
const list = get<User[]>('/users')   // 这次 T = User[]
```

**⑤ 工具类型 `Omit` / `Partial`**：从已有类型派生新类型

```ts
type UserForm = Omit<User, 'id'>      // User 去掉 id 字段
type Patch = Partial<User>            // User 的所有字段都变成「可选」
```

**⑥ 断言 `as`**：手动告诉 TS「我知道它是什么类型，信我」

```ts
const el = route.params.id as string
```

就这六个。遇到不懂的，回来查这一节即可。

---

## 三、给项目装上 TS

我们**新建一个并列项目** `project/user-admin-ts/`（把 JS 版原样复制一份再改），不动原来的 `user-admin/`，方便两版并排对照。

### 3.1 装依赖

在 JS 版的依赖基础上，加三个开发依赖：

```bash
npm install -D typescript vue-tsc @types/node
```

| 包 | 干嘛的 |
|---|---|
| `typescript` | TS 语言本身 |
| `vue-tsc` | 给 `.vue` 文件做类型检查的工具（基于 Volar） |
| `@types/node` | 让 `vite.config.ts` 里用到的 Node API 有类型 |

### 3.2 加 `tsconfig.json`（TS 的总配置）

```jsonc
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,            // ← 关键：开严格模式，类型问题一个不漏
    "jsx": "preserve",
    "noEmit": true,            // 只做类型检查，不输出 JS（交给 Vite 打包）
    "verbatimModuleSyntax": true,
    "types": ["node"]
    // ... 其余省略，见项目里完整文件
  },
  "include": ["src/**/*.ts", "src/**/*.vue", "vite.config.ts"]
}
```

`strict: true` 是重点——它一开，TS 会把「可能为 null」「类型对不上」这些隐患全揪出来。脚手架 `npm create vue` 默认就开它，我们跟默认保持一致。

### 3.3 加 `env.d.ts`（让 TS 认得 `.vue` 文件）

```ts
/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent
  export default component
}
```

没有它，TS 看不懂 `import App from './App.vue'`。

### 3.4 改三个入口后缀 + 一行 `lang`

| 改动 | JS 版 | TS 版 |
|---|---|---|
| 入口 | `main.js` | `main.ts` |
| 构建配置 | `vite.config.js` | `vite.config.ts` |
| `index.html` 里引用 | `/src/main.js` | `/src/main.ts` |
| 每个组件 | `<script setup>` | `<script setup lang="ts">` |

`main.ts` 内容跟 `main.js` 一字不差——TS 是 JS 的超集，原来能跑的 JS 代码，原样放进 `.ts` 照样能跑。`lang="ts"` 就像告诉 Vue「这个 `<script>` 块按 TS 来编译」。

### 3.5 改 `package.json` 的 `build` 脚本

```jsonc
{
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc --noEmit && vite build",   // ← 先类型检查，再打包
    "type-check": "vue-tsc --noEmit"             // ← 只类型检查，不打包
  }
}
```

**这就是 TS 和 JS 最大的工程差别**：JS 版的 `build` 直接打包；TS 版的 `build` 会**先跑 `vue-tsc` 类型检查**，有类型错误就**编译失败**——bug 在「打包那一刻」就被挡住，根本到不了线上。

骨架装好了。接下来按「数据 → 接口 → 状态 → 组件 → 页面」的顺序，逐层迁移。

---

## 四、第一步：定义领域类型 `types/user.ts`

迁移 TS 项目，**第一步永远是定义数据类型**——它是一切的基础。

新建 `src/types/user.ts`，把 db.json 里「一条用户长什么样」翻译成类型：

```ts
// 角色是固定的三种之一 —— 字面量联合类型，写错一个字母都报错
export type Role = 'admin' | 'editor' | 'viewer'

// 一条用户（对应 db.json 里的一个对象）
export interface User {
  id: number
  name: string
  email: string
  phone: string
  role: Role
  status: 0 | 1          // 0=禁用 1=启用，也用字面量联合锁死
}

// 新增/编辑表单：新增时还没 id，编辑时才有
export type UserForm = Omit<User, 'id'> & { id?: number }
```

| JS 版 | TS 版 | 换来了什么 |
|---|---|---|
| 没有任何类型定义，`user` 是个「黑盒对象」，写 `user.nam` 不报错 | `User` 接口白纸黑字写清字段 | 任何地方写错字段名，**立刻红线** |

> 💡 重点体会 `role: Role` 和 `status: 0 | 1`。JS 里 `role` 是个随便的字符串，拼成 `'adimn'`（笔误）运行时才发现；TS 里它只能是那三个值之一，**笔误当场报错**。这是 TS 最直观的收益。

---

## 五、api 层迁移：泛型封装 + 工具类型

### 5.1 `request.ts`——本章最经典的一个坑

JS 版的 `request.js` 有个响应拦截器，把 `response.data` 拆出来：

```js
// JS 版 request.js
request.interceptors.response.use(
  (response) => response.data,   // ← 运行时：直接返回 data，拆掉外壳
  (error) => { /* ... */ }
)
```

这个拦截器改了**运行时返回值**（从 `AxiosResponse` 变成 `data` 本身），**但 axios 自带的类型不知道这件事**。结果就是：类型说 `.get()` 返回 `AxiosResponse`，运行时却返回 `data`——**类型和现实对不上**。

TS 版用一层泛型封装把类型「对齐到现实」：

```ts
// TS 版 request.ts
const instance = axios.create({ baseURL: '/api', timeout: 10000 })

instance.interceptors.response.use(
  (response) => response.data,   // 运行时照旧拆外壳
  (error) => { /* ... */ }
)

// 包一层：<T> 是泛型，调用时告诉它「这次返回什么类型」
async function get<T>(url: string): Promise<T> {
  // 运行时已经是 data，但类型还以为是 AxiosResponse，用 as 对齐
  return instance.get(url) as unknown as Promise<T>
}
// post / put / delete 同理……

export default { get, post, put, delete: del }
```

> ⚠️ 这里出现 `as unknown as Promise<T>` 这种「看起来很 hack」的写法。它的意思是「**TS 啊，运行时的真实形状和你以为的不一样，听我的**」。这是 TS 给你的「逃生舱」——能绕过类型检查，但**用一次就要为它的正确性负责**。本章只在这一处用，因为它确实必要（拦截器改了返回值）。

### 5.2 `user.ts`——函数签名变成「自带说明书」

有了泛型 `request`，接口函数的类型签名就非常清晰：

```ts
// TS 版 user.ts
import request from './request'
import type { User } from '../types/user'

export function getUsers(): Promise<User[]> {
  return request.get<User[]>('/users')        // 返回 User 数组
}
export function addUser(data: Omit<User, 'id'>): Promise<User> {
  return request.post<User>('/users', data)   // 新增不带 id（服务器生成）
}
export function updateUser(id: number | string, data: Partial<User>): Promise<User> {
  return request.put<User>(`/users/${id}`, data)   // 改：只改部分字段
}
```

| JS 版 | TS 版 |
|---|---|
| `function addUser(data) { ... }`——`data` 是啥、返回啥，全靠注释或猜 | `addUser(data: Omit<User, 'id'>): Promise<User>`——一眼看穿 |

`Omit<User, 'id'>` 表达「新增数据没有 id」，`Partial<User>` 表达「更新只改部分字段」。这俩工具类型让函数签名**精确到「业务语义」级别**，而 JS 只能靠注释含糊表达。

---

## 六、Pinia store 迁移：组合式 store 几乎全自动推断

```ts
// TS 版 stores/user.ts
interface SessionUser { name: string }   // 登录者只需一个名字（演示用）

export const useUserStore = defineStore('user', () => {
  const currentUser = ref<SessionUser | null>(null)   // ← 明确：要么登录者，要么 null
  const isLoggedIn = computed(() => !!currentUser.value) // 推断出 ComputedRef<boolean>
  const displayName = computed(() => currentUser.value?.name || '未登录')

  function login(user: SessionUser) { currentUser.value = user }
  function logout() { currentUser.value = null }

  return { currentUser, isLoggedIn, displayName, login, logout }
})
```

好消息：**组合式 store（setup 写法）的类型基本全自动推断**，你只要给 `ref` 标上泛型、给函数参数标上类型，剩下的 TS 全包了。这也是为什么本教程第 10 章坚持用 setup 写法——它跟 TS 配合最自然。

> 💡 `currentUser.value?.name` 里的 `?.`（可选链）是 TS 时代的常用写法：`currentUser` 可能是 `null`，`?.` 保证它为 null 时不报错、直接返回 undefined。JS 里只能 `currentUser.value && currentUser.value.name`。

---

## 七、组件迁移：`defineProps<T>` + Element Plus 类型

弹窗组件 `UserDialog.vue` 是类型最密集的地方，也是 TS 收益最大的地方。

### 7.1 props / emit：从「运行时声明」到「类型声明」

```ts
// JS 版：运行时声明，类型很粗（editing 只知道是 Object）
const props = defineProps({ modelValue: Boolean, editing: Object })
const emit = defineEmits(['update:modelValue', 'success'])
```

```ts
// TS 版：直接写类型，精确到每个字段
const props = defineProps<{
  modelValue: boolean
  editing: User | null
}>()
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  success: []
}>()
```

差别：JS 版 `editing: Object` 是个「啥都能塞」的黑盒；TS 版 `editing: User | null` 精确到「要么一个用户、要么空」。父组件传错类型，立刻报错。

### 7.2 `ref<T>`：让 ref 有明确类型

```ts
const formRef = ref<FormInstance>()   // FormInstance 来自 element-plus，能点出 validate()
const form = ref<UserForm>({ name: '', email: '', phone: '', role: 'viewer', status: 1 })
```

`FormInstance` 是 Element Plus 给「表单实例」定义的类型——标了它，`formRef.value.validate()` / `.clearValidate()` 才有类型提示。不标的话，`formRef.value` 是个 `any`，调用啥都没提示。

### 7.3 校验规则：标成 `FormRules`

```ts
import type { FormInstance, FormRules } from 'element-plus'

const rules: FormRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  // ...
}
```

### 7.4 两个 TS 时代的小细节

```ts
// 编辑时一定有 id，用 !（非空断言）告诉 TS「这里 id 不是 undefined」
await updateUser(form.value.id!, form.value)

// catch 里的 e 是 unknown（TS 不让你随便 .message），先断言成 Error
} catch (e) {
  ElMessage.error('保存失败：' + (e as Error).message)
}
```

- `!`（非空断言）：`form.value.id` 类型是 `number | undefined`，但「编辑」分支里它一定有值，用 `!` 告诉 TS「别管 undefined」。
- `catch (e)` 里 `e` 是 `unknown`（TS 的安全设计，不让你假设它是 Error），用 `as Error` 断言后再 `.message`。

> ⚠️ `!` 和 `as` 都是「我比你（TS）更懂，听我的」。它们是逃生舱，**用一次就要自己担保正确**。新手容易滥用 `as any` 把 TS 关掉——那就白上 TS 了。原则：能靠类型自然解决的，绝不用断言。

---

## 八、列表页与详情页迁移

### 8.1 列表页：`ref<User[]>` + 表格插槽

```ts
const users = ref<User[]>([])                                    // 一开始就是 User[]
const roleMap: Record<Role, string> = { admin: '管理员', editor: '编辑', viewer: '访客' }
async function handleDelete(row: User) { /* row.id、row.name 全有提示 */ }
```

`roleMap` 的类型 `Record<Role, string>` 把 key 锁成 `Role`——你写 `roleMap['adimn']`（笔误）会报错。

表格插槽里有个小坑：Element Plus 的 `el-table` 默认不强类型化插槽的 `row`，所以模板里要收窄一下：

```vue
<template #default="{ row }">
  <el-tag>{{ roleMap[row.role as Role] || row.role }}</el-tag>
</template>
```

> 💡 这里 `row` 在 TS 眼里是松散的，用 `row.role as Role` 收窄。Element Plus 表格的强类型化是进阶话题（要用泛型 `<el-table>`），本章不展开，留作「下一步」。

### 8.2 详情页：路由参数的收窄

```ts
const user = ref<User | null>(null)

onMounted(async () => {
  const id = route.params.id as string   // ← 收窄
  user.value = await getUserById(id)
})
```

`route.params.id` 默认类型是 `string | string[]`（Vue Router 不自动判断 `:id` 是单个值）。这里 `:id` 一定是单个字符串，用 `as string` 收窄。进阶做法是「路由类型扩展声明」，同样留作下一步。

> 💡 详情页模板里 `v-if="user"` 之后，TS 能自动把 `user` 从 `User | null` 收窄成 `User`，所以 `{{ user.name }}` 不会报「可能为 null」。这是现代 Volar（vue-tsc 底层）的模板类型收窄能力。

---

## 九、亲眼见证：TS 帮你挡错

讲这么多，不如看一个**真实的「JS 静默出错、TS 当场拦截」**的例子。回到列表页，假设你手滑把 `role` 写成了 `'adimn'`：

**JS 版**——一切照常运行，没人拦你：

```js
// 假设某个新增逻辑里笔误
const u = { name: '张三', role: 'adimn' }   // 笔误！adimn ≠ admin
addUser(u)
// → 静默地往数据库塞了一条 role='adimn' 的脏数据
// → 列表里 roleMap['adimn'] 是 undefined，那一行的角色列显示空白
// → 你得等用户反馈「怎么有个用户没角色」才发现，可能是上线后
```

**TS 版**——红线当场亮起：

```ts
const u: Omit<User, 'id'> = { name: '张三', role: 'adimn' }
//                                            ~~~~~~~
// 报错：不能将类型 '"adimn"' 分配给类型 'Role'('"admin" | "editor" | "viewer"')
```

再来一个，字段名笔误 `nmae`：

```ts
addUser({ nmae: '张三', email: '...', phone: '...', role: 'admin', status: 1 })
//       ~~~~
// 报错：对象文字可以只指定已知属性，但不存在 'nmae'（你是指 'name' 吗？）
```

| | JS 版 | TS 版 |
|---|---|---|
| 笔误 `role: 'adimn'` | 静默塞脏数据，UI 显示异常，**上线后**才发现 | **写下的瞬间**就红线报错 |
| 笔误字段名 `nmae` | 静默发送，服务器存了个没 name 的用户 | 红线 + 友好提示「你是指 name 吗？」 |

**这就是 TS 换来的核心东西：把「运行时才暴露的 bug」提前到「写代码时」暴露。** 对 jQuery 程序员来说，这一点冲击最大——你习惯了「改完刷新看效果、报错了再调」，TS 让你在**敲键盘的那一刻**就知道错了。

---

## 十、跑一次完整的类型检查 + 打包

迁移完，验证它真的能过类型检查：

```bash
cd project/user-admin-ts
npm install          # 装依赖（含 typescript / vue-tsc）
npm run type-check   # 只类型检查
npm run build        # 类型检查 + 打包
```

如果 `npm run build` 一路绿灯、打出 `dist/`，说明**整个项目类型正确、可以上线**。任何一处类型不对，这一步都会红字拒绝——bug 出不了门。

跑起来看效果（两个终端，跟 JS 版一样）：

```bash
npm run server   # 终端 1：json-server 假后端
npm run dev      # 终端 2：Vite 前端
```

打开 http://localhost:5173 ——你会发现 **UI、交互、数据和 JS 版完全一样**。TS 没改变任何运行时行为，它只在「写代码」和「打包」这两个时刻帮你把关。

---

## 十一、JS 版 vs TS 版：全景对照

把 9 个文件的改动浓缩成一张表：

| 文件 | JS 版 → TS 版 的关键改动 |
|---|---|
| `types/user.ts` | **新增**：`User` / `Role` / `UserForm`（字面量联合 + `Omit`） |
| `main.ts` | 改后缀，内容不变 |
| `api/request.ts` | 泛型封装 `get<T>(): Promise<T>`，对齐拦截器拆外壳 |
| `api/user.ts` | 函数签名带 `Omit`/`Partial`，返回 `Promise<User[]>` 等 |
| `stores/user.ts` | `ref<SessionUser \| null>`，参数标类型 |
| `router/index.ts` | `routes: RouteRecordRaw[]` |
| `UserDialog.vue` | `defineProps<T>` / `defineEmits<T>` / `FormInstance` / `FormRules` / `!` / `catch as Error` |
| `UserList.vue` | `ref<User[]>` / `Record<Role,string>` / 插槽 `as Role` |
| `UserDetail.vue` | `ref<User \| null>` / `route.params.id as string` |

**并排打开 `project/user-admin/`（JS）和 `project/user-admin-ts/`（TS），逐文件对照**——这是消化这一章最快的方式。

---

## 🏋️ 小练习

1. **加一个类型严格化的收益**：把 `stores/user.ts` 的 `SessionUser` 扩展成包含 `id` 和 `role`，然后让 `App.vue` 登录时也带上这两个字段（类型不匹配会报错，逼你改对）。
2. **体验挡错**：故意在 `UserList.vue` 的 `handleDelete` 里把 `row.id` 写成 `row.iid`，跑 `npm run type-check`，看 TS 怎么报错；再想想这在 JS 版会怎样。
3. **加一个工具类型**：给「搜索关键字」相关的逻辑加一个类型，体会 `Partial` 或 `Pick` 的用法。

---

## ✅ 本章你应掌握

- [ ] 知道**什么时候该上 TS**（团队/长期/接手存量 → 上；小 demo → 不必）；
- [ ] 会用 `interface` / `type` / 字面量联合 / `Omit` / `Partial` / 泛型 / `as` 这六个迁移必备语法；
- [ ] 会给一个 Vite + Vue 项目**装上 TS**（`tsconfig` + `env.d.ts` + `vue-tsc` + `lang="ts"`）；
- [ ] 会写带类型的 `ref<T>` / `defineProps<T>` / `defineEmits<T>`，会用 Element Plus 的 `FormInstance` / `FormRules`；
- [ ] 理解 axios 拦截器「拆外壳」带来的**类型与现实脱节**，会用泛型封装对齐；
- [ ] 亲眼看懂 **TS 如何在「写代码时」挡住 JS 要到「运行时」才暴露的 bug**；
- [ ] 会让 `npm run build` 跑 `vue-tsc` 类型检查，把类型错误挡在打包之前。

---

## 下一步（留给你的进阶钩子）

本章只覆盖了「实用够用」的类型。真实 TS Vue 项目还有这些进阶，按需深挖：

- **路由类型扩展声明**：用 `declare module 'vue-router'` 让 `router.push({ name: 'detail', params: { id } })` 的参数也类型安全（不再需要 `as string`）；
- **Element Plus 表格强类型化**：用泛型 `<el-table>` 让插槽 `row` 自动是 `User` 类型；
- **`composable` 的类型**：自定义组合式函数（第 11 章附录提到的「自定义 hook」）怎么写泛型；
- **`vue-tsc` 进阶**：`strict` 之外的更严选项（`noUncheckedIndexedAccess` 等）。

> 这条路没有终点——TS 的类型系统是个能陪你走很久的工具。但记住附录 C 那句话：**先把 JS 的 Vue 写熟，再上 TS，顺序别反**。你现在两样都有了。

🎉 **扩展篇到此结束。** 回到 [附录 C · 下一步学什么](appendices/C-下一步学什么.md) 看更多方向，或者把 user-admin（JS 版 / TS 版）继续拿去折腾——**改的过程才是真正消化知识的过程。**
