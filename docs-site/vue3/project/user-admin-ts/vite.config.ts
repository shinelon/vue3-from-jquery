import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 配置 Vite 代理，解决前后端跨域（和 JS 版完全一致，只是后缀改成 .ts）
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
