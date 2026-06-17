# 第 1 章 · 10 分钟上手：用 CDN 写个 Todo

这一章我们**不装任何环境**，用浏览器直接打开一个 html 文件就能跑。目标是写一个最小版的 Todo（输入任务、添加、显示列表）——先用 jQuery 写一遍，再用 Vue 写一遍。你会亲眼看到两者最根本的差别。

> 📂 可运行 demo 在 [`demos/ch01-todo-cdn/`](../demos/ch01-todo-cdn/)，双击 `index.html` 就能跑。

---

## 一、先看 jQuery 版（你的老朋友）

新建 `index.html`，引入 jQuery：

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Todo - jQuery 版</title>
  <script src="https://cdn.jsdelivr.net/npm/jquery/dist/jquery.min.js"></script>
</head>
<body>
  <h1>Todo（jQuery 版）</h1>
  <input id="input" placeholder="输入任务" />
  <button id="add">添加</button>
  <ul id="list"></ul>

  <script>
    var todos = []
    $('#add').on('click', function () {
      var text = $('#input').val()
      if (!text) return
      todos.push(text)
      // ↓↓↓ 手动把列表重新渲染一遍 ↓↓↓
      $('#list').empty()
      todos.forEach(function (t) {
        $('#list').append('<li>' + t + '</li>')
      })
      $('#input').val('')
    })
  </script>
</body>
</html>
```

jQuery 版里，你要做这几个动作：

1. **读**输入框的值：`$('#input').val()`；
2. 数据 `push` 之后，**手动清空列表** `$('#list').empty()`；
3. **手动拼接** `<li>`、**手动追加** `append`；
4. **手动清空**输入框 `$('#input').val('')`。

最啰嗦的是第 2、3 步——**数据（`todos` 数组）和视图（`<ul>` 列表）之间的同步，全靠你手动维护**。数据一变，你就得记得去刷新视图。

---

## 二、再看 Vue 版（同样的功能，不一样的写法）

把页面换成 Vue：

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Todo - Vue 版</title>
  <!-- 通过 CDN 引入 Vue3 -->
  <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
</head>
<body>
  <div id="app">
    <h1>Todo（Vue 版）</h1>
    <input v-model="text" placeholder="输入任务" />
    <button @click="add">添加</button>
    <ul>
      <li v-for="todo in todos">{{ todo }}</li>
    </ul>
  </div>

  <script>
    const { createApp, ref } = Vue

    createApp({
      setup() {
        const text = ref('')           // 输入框的内容
        const todos = ref([])          // 任务列表
        function add() {
          if (!text.value.trim()) return
          todos.value.push(text.value.trim())  // ← 只改数据
          text.value = ''                       // ← 只改数据
        }
        return { text, todos, add }
      }
    }).mount('#app')
  </script>
</body>
</html>
```

---

## 三、对比：Vue 版到底少了什么？

| 做的事 | jQuery | Vue |
|---|---|---|
| 读输入框的值 | `$('#input').val()` | `v-model="text"` 自动双向绑定 |
| 添加后更新列表 | 手动 `empty` + `append` | `todos.push()` 后**页面自动更新** |
| 渲染列表 | `forEach` 拼 `<li>` | `<li v-for>` 自动遍历 |
| 清空输入框 | `$('#input').val('')` | `text.value = ''` 自动清空 |

**关键发现：Vue 版里，你完全没有碰 DOM。** 你只改了 `todos`（数据），列表自己就更新了；你只改了 `text`，输入框自己就清空了。

这就是序言里那句话的落地——**操作数据，而不是操作 DOM**。jQuery 时代最烦的"数据↔视图手动同步"，Vue 帮你自动做了。

---

## 四、逐行拆解（别慌，第一次见，慢慢看）

### 1. 引入 Vue

```html
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
```

CDN 引入后，全局会有一个 `Vue` 对象，所有 Vue 的功能都挂在它上面。

### 2. 挂载点 `#app`

```html
<div id="app"> ... </div>
```

```js
}).mount('#app')
```

`#app` 是 **Vue 接管的区域**。`.mount('#app')` 告诉 Vue："这个 div 里面归你管"。注意：**Vue 只管这个 div 内部**，外面它不管——这和 jQuery 能管整个 `document` 不同。

### 3. `createApp` + `setup`

```js
createApp({
  setup() {
    // 数据和逻辑放这里
    return { text, todos, add }   // 暴露给模板用
  }
})
```

- `createApp({...})`：创建一个 Vue 应用；
- `setup()`：放数据和函数的地方（这是 **Composition API** 的入口，第 4 章用 Vite 后会简化成更清爽的 `<script setup>`）；
- `return { ... }`：把想让模板用的数据和函数"交出去"。

### 4. `ref`：让数据变成"响应式"

```js
const todos = ref([])
```

`ref()` 把一个普通值包成**响应式**的——**它一变，页面自动更新**。

⚠️ **一个新手必踩的坑**：在 JS 里读写 `ref`，要加 `.value`：

```js
todos.value.push(...)   // 读/写都要 .value
text.value = ''
```

但在**模板里不用加**（`{{ todo }}`、`v-for="todo in todos"`），Vue 会自动帮你拆开。

> 为什么 JS 里要 `.value`？因为 `ref` 返回的是一个"盒子"对象 `{ value: 数据 }`，Vue 靠这个盒子追踪变化。第 2 章会深入讲，现在先记住"JS 里加 `.value`，模板里不加"。

### 5. 模板里的几个"指令"

| 写法 | 作用 | 对应 jQuery |
|---|---|---|
| `v-model="text"` | 输入框和 `text` 双向绑定（打字→text 变；text 变→框也变） | `$('#input').val()` 读写 |
| `@click="add"` | 点击触发 `add` 函数 | `on('click', ...)` |
| `v-for="todo in todos"` | 遍历 `todos`，每项生成一个 `<li>` | `forEach` + 拼 `<li>` |
| `{{ todo }}` | 把 `todo` 的值显示出来 | `.text(todo)` |

---

## 五、动手跑起来

1. 打开 [`demos/ch01-todo-cdn/index.html`](../demos/ch01-todo-cdn/index.html)，双击用浏览器打开，试试添加几条任务；
2. 在 `add` 函数里加一行 `console.log(todos.value)`，按 F12 打开控制台，看看数据长啥样；
3. 对比旁边的 [`jquery-version.html`](../demos/ch01-todo-cdn/jquery-version.html)，感受"手动同步"vs"自动同步"。

---

## 🏋️ 小练习

1. **加删除按钮**：在每个 `<li>` 后面加个"删除"按钮，点击删掉对应任务。
   - 提示：`v-for="(todo, i) in todos"` 能拿到索引 `i`；删除用 `todos.value.splice(i, 1)`。
2. **显示总数**：在列表下方显示"共 X 条任务"。
   - 提示：`{{ todos.length }}`（模板里不用 `.value`）。

> 这两个练习的答案，其实就藏在 demo 里——做完可以对照。

---

## ✅ 本章你应掌握

- [ ] 知道用 CDN 引入 Vue，不装环境就能跑；
- [ ] 体会到"**操作数据，Vue 自动更新 DOM**"这个核心思想；
- [ ] 大致看懂 `ref`、`v-model`、`@click`、`v-for`、`{{ }}` 各自干什么；
- [ ] 明白 jQuery 版"手动同步数据↔视图"的繁琐，Vue 版省掉了这步。

> 💡 **关于这种 CDN 写法**：本章 `createApp + setup` 是"完整版"写法。第 4 章引入 Vite 后，我们会换成更简洁的 `<script setup>`——到时你会发现**逻辑一模一样，只是写法更清爽**。现在先用 CDN 建立直觉，别纠结语法细节。

下一篇 👉 [第 2 章 · 响应式：告别手动改 DOM](02-响应式.md)
