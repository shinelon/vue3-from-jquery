# 附录 A · jQuery → Vue 速查对照表

写代码卡壳时翻这个表。全书所有"jQuery 写法 → Vue 写法"的对照，汇总在一份。

---

## 一、文本 / DOM 操作

| 场景 | jQuery | Vue |
|---|---|---|
| 显示文本 | `$('#x').text(v)` | `{{ v }}`（响应式自动更新） |
| 显示 HTML | `$('#x').html(h)` | `v-html="h"`（⚠️ 慎用，XSS） |
| 读输入框值 | `$('#i').val()` | `v-model="x"`（自动双向） |
| 设置属性 | `$('img').attr('src', url)` | `:src="url"` |

---

## 二、事件

| 场景 | jQuery | Vue |
|---|---|---|
| 点击 | `$('...').on('click', fn)` | `@click="fn"` |
| 阻止冒泡 | `e.stopPropagation()` | `@click.stop="fn"` |
| 阻止默认 | `e.preventDefault()` | `@submit.prevent="fn"` |
| 回车触发 | `if (e.key === 'Enter')` | `@keyup.enter="fn"` |
| 仅按一次 | `$('...').one(...)` | 自己用变量控制 |

---

## 三、条件 / 循环

| 场景 | jQuery | Vue |
|---|---|---|
| 显示/隐藏 | `.show() / .hide()` | `v-show`（切 display） |
| 按条件渲染 | `if` 后 `.append()/.remove()` | `v-if`（真删/建 DOM） |
| 条件分支 | `if / else if / else` | `v-if / v-else-if / v-else` |
| 遍历列表 | `$.each(list, fn)` + 拼 HTML | `v-for="(item, i) in list" :key="item.id"` |

---

## 四、表单

| 场景 | jQuery | Vue |
|---|---|---|
| 文本框 | `.val()` 读写 + 监听 change | `v-model="x"` |
| 复选框（单个） | `.prop('checked')` | `v-model="checked"`（布尔） |
| 复选框（多个） | 遍历取值 | `v-model="tags"`（数组） |
| 单选 | `:checked` 判断 | `v-model="picked"` |
| 下拉 | `.val()` | `v-model="city"` |
| 失焦才同步 | — | `v-model.lazy` |
| 自动转数字 | `parseInt()` | `v-model.number` |
| 去空格 | `.trim()` | `v-model.trim` |

---

## 五、样式

| 场景 | jQuery | Vue |
|---|---|---|
| 加/删类 | `.addClass() / .removeClass()` | `:class="{ active: isActive }"` |
| 多类 | — | `:class="['a', cond && 'b']"` |
| 改样式 | `.css('color', 'red')` | `:style="{ color: textColor }"` |

---

## 六、组件 / 复用

| 场景 | jQuery | Vue |
|---|---|---|
| 复用一块 UI | 复制粘贴 / jQuery 插件 | `.vue` 组件 |
| 父传子数据 | 函数参数 | `props` |
| 子通知父 | 回调函数 | `emit('事件', 数据)` |
| 给组件塞内容 | — | `<slot />` |
| 数据归谁管 | 全局乱改 | 单向数据流（父管数据，子只 emit） |

---

## 七、数据 / 响应式

| 场景 | jQuery | Vue |
|---|---|---|
| 存数据 | `var x = ...` | `const x = ref(...)`（响应式） |
| 存对象 | `var obj = {...}` | `reactive({...})` 或 `ref({...})` |
| 派生值 | 手动函数 + 手动更新 | `computed(() => ...)`（自动） |
| 监听变化 | — | `watch(x, fn)` |
| 挂载后执行 | `$(function(){})` | `onMounted(fn)` |

> ⚠️ `ref` 在 JS 里要 `.value`（模板里不用）；`reactive` 解构会丢响应式。

---

## 八、AJAX / 请求

| 场景 | jQuery | Vue（axios） |
|---|---|---|
| GET | `$.get(url, cb)` | `axios.get(url)` / `request.get` |
| POST | `$.ajax({type:'POST'})` | `axios.post(url, data)` |
| 异步风格 | 回调 / `$.Deferred` | `async/await`（推荐） |
| 错误处理 | `error` 回调 | 拦截器统一 + `try/catch` |

---

## 九、状态 / 全局

| 场景 | jQuery | Vue |
|---|---|---|
| 全局共享数据 | `window.xxx`（不响应式） | Pinia `store`（响应式 + 可控） |
| 跨组件传值 | 全局变量 | `useXxxStore()`（任意组件直接用） |

---

## 十、路由 / 多页面

| 场景 | jQuery | Vue |
|---|---|---|
| 跳转 | `location.href = 'x.html'` | `router.push('/x')` |
| 跳转（标签） | `<a href="x.html">` | `<router-link to="/x">` |
| 多页面 | 多个 `.html` 文件 | 单 html + 组件切换（SPA） |
| 取 URL 参数 | 解析 `location.search` | `route.params.id` |

---

## 十一、构建 / 工程

| 场景 | jQuery | Vue |
|---|---|---|
| 引入库 | `<script src="cdn">` | `npm install` + `import` |
| 开发 | 直接开 html | `npm run dev`（热更新） |
| 上线 | 直接传 html | `npm run build` → `dist/` |
| 模块化 | `<script>` 顺序加载 | ES Module `import/export` |

---

> 💡 **一句话总纲**：jQuery 是"**你操作 DOM**"，Vue 是"**你操作数据，Vue 替你操作 DOM**"。卡住时默念这句，多半就通了。
