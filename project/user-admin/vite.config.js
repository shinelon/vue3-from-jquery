import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 第 6 章：配置 Vite 代理，解决前后端跨域
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',          // json-server 地址
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')  // /api/users → /users
      }
    }
  }
})
