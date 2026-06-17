# 附录 A · vite.config 常用配置速查

写代码卡壳时翻这个表。本教程涉及的 vite.config 配置项，按用途汇总。

---

## 基础结构

```js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  // 各项配置...
})
```

---

## plugins：插件

```js
plugins: [vue()]
```

---

## resolve.alias：路径别名

```js
import { fileURLToPath, URL } from 'node:url'
resolve: { alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) } }
```

---

## server：开发服务器

```js
server: {
  port: 5173,                       // 端口
  open: true,                       // 启动自动开浏览器
  proxy: {                          // 开发代理（解决跨域）
    '/api': {
      target: 'http://localhost:3000',
      changeOrigin: true,
      rewrite: (p) => p.replace(/^\/api/, '')
    }
  }
}
```

---

## build：构建

```js
build: {
  outDir: 'dist',                   // 输出目录
  target: 'es2015',                 // 编译目标
  sourcemap: false,                 // 是否生成 sourcemap
  rollupOptions: {
    output: {
      manualChunks(id) {            // chunk 拆分（Vite 8 用函数形式）
        if (id.includes('node_modules/vue')) return 'vue'
      }
    }
  }
}
```

---

## base：部署基础路径

```js
base: '/',          // 默认，根域部署
base: '/notes/',    // 子路径部署：https://example.com/notes/
base: './'          // 相对路径（适合不确定部署位置）
```

---

## 库模式

```js
build: {
  lib: { entry: 'src/index.js', name: 'MyLib', formats: ['es', 'umd'], fileName: 'my-lib' },
  rollupOptions: { external: ['vue'] }
}
```

---

## 环境变量（无需配置）

`.env` 文件自动加载，代码用 `import.meta.env.VITE_XXX` 读。见第 4 章。

---

> 💡 完整配置项查 [官方文档](https://vite.dev/config/)。
