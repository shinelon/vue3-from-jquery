# 第 5 章 demo · 组件化

演示 `props`（父传子）、`emit`（子传父）、单向数据流。

## 运行

```bash
cd demos/ch05-components
npm install
npm run dev
```

## 结构

```
ch05-components/
└── src/
    ├── App.vue              父组件：拥有用户数据，监听 @delete
    ├── main.js              入口
    └── components/
        └── UserCard.vue     子组件：props 接收 user，emit('delete', id)
```

点删除按钮，观察"子组件 emit → 父组件改数据 → 列表自动更新"的完整链路：删除逻辑只存在于父组件一处。
