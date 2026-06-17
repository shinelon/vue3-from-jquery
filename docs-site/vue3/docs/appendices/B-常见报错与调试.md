# 附录 B · 常见报错与调试

新手阶段一定会踩坑。这里收集了最常见的报错和现象，给出原因和解法。卡住时先来这里找。

---

## 🐛 常见错误

### 1. 改了数据，页面没变

**原因**：八成是 `ref` 忘了 `.value`。

```js
const count = ref(0)
function inc() {
  count++          // ❌ 错：count 是 ref 对象，不是数字
  count.value++    // ✅ 对
}
```

**记住**：JS 里读写 `ref` 要 `.value`，模板里不用。

---

### 2. `Cannot read properties of undefined (reading 'xxx')`

**原因**：访问了不存在的深层属性。常见于请求回来的数据还没到（`null`）。

```vue
<p>{{ user.name }}</p>     <!-- ❌ user 还是 null 时就崩 -->
```

**解决**：用可选链 `?.`，或先判断。

```vue
<p>{{ user?.name }}</p>           <!-- ✅ -->
<p v-if="user">{{ user.name }}</p> <!-- ✅ -->
```

---

### 3. `v-for` 列表渲染错乱 / 报 key 警告

**原因**：`v-for` 没加 `:key`，或用了 `index` 当 key。

```vue
<li v-for="(item, i) in list" :key="i">   <!-- ❌ 用 index 会错乱 -->
<li v-for="item in list" :key="item.id">  <!-- ✅ 用稳定 id -->
```

---

### 4. 改了对象/数组，视图没更新

**原因**（如果用 `reactive`）：直接替换整个对象会丢响应式。

```js
const state = reactive({ user: {} })
state.user = { name: 'x' }    // ⚠️ 这样可能丢响应式（看场景）
// 建议逐个赋值，或改用 ref
```

**或**：解构 `reactive` 对象会丢响应式——别解构，或用 `ref` / `storeToRefs`。

---

### 5. 组件用了不显示 / 报"未注册"

**原因**：忘了 `import`，或 `import` 的名字和用法不一致。

```vue
<script setup>
import UserCard from './UserCard.vue'   <!-- ✅ 必须先 import -->
</script>
<template>
  <UserCard />                           <!-- 才能用 -->
</template>
```

---

### 6. Element Plus 组件没样式 / 不生效

**原因**：`main.js` 里忘了引入样式。

```js
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'   <!-- ✅ 这行不能少 -->
app.use(ElementPlus)
```

---

### 7. 接口请求 404 / 跨域报错（CORS）

**原因**：开发时前端 `:5173`、后端 `:3000`，端口不同会跨域。

**解决**：用 Vite 代理（见第 6 章 `vite.config.js` 的 `proxy` 配置），请求 `/api/xxx`。

---

### 8. `v-model` 没生效

**原因**：可能用在了非受控元素上，或绑错了。`v-model` 只能用在表单元素（input/textarea/select）或支持它的组件上。检查拼写和绑定对象是不是 `ref`。

---

### 9. 打包部署后刷新子路由 404

**原因**：用了 `createWebHistory`，服务器没配 fallback。

**解决**：服务器配 `try_files $uri $uri/ /index.html`（Nginx），或改用 `createWebHashHistory`（见第 11 章）。

---

### 10. `[Vue warn]: Component template should contain exactly one root element`（旧版）

Vue3 已支持多根节点，但如果你混用了某些库报这个，把模板用一个外层 `<div>` 包起来即可。

---

## 🛠️ 调试利器：Vue DevTools

**必装**：浏览器装 [Vue DevTools](https://devtools.vuejs.org/) 扩展（Chrome / Firefox / Edge 都有）。

它能让你：

- 📦 **查看组件树**：当前页面有哪些组件、嵌套关系；
- 🔍 **查看/修改组件数据**：实时看每个组件的 `ref`/`props` 值，还能临时改；
- 🗺️ **看路由、Pinia store**：当前路由信息、store 里的状态一目了然。

装上后 F12 打开开发者工具，会有一个 **Vue** 标签页。调试响应式问题、组件传值问题时，它比 `console.log` 强一百倍。

---

## 💡 调试小技巧

1. **怀疑数据不对？** 用 Vue DevTools 看组件状态，或 `console.log(x.value)`（ref 记得 `.value`）。
2. **怀疑请求不对？** F12 → Network 面板，看请求 URL、参数、响应。
3. **怀疑样式不对？** F12 → Elements 面板，检查元素和 CSS。
4. **改了代码没生效？** 确认保存了、`npm run dev` 没报错、浏览器没缓存（Ctrl+Shift+R 强刷）。
