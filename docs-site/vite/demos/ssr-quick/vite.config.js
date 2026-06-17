import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// SSR：让 Vite 以"中间件模式"运行，挂到我们自己的 express 服务器里
export default defineConfig({
  plugins: [vue()],
  server: { middlewareMode: true },
  appType: 'custom'
})
