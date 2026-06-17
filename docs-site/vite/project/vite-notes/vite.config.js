import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

// 第 9 章：加了 build 配置——编译目标 + chunk 拆分（vue/axios 单独成 chunk，提升缓存命中）。
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  build: {
    target: 'es2015',
    rollupOptions: {
      output: {
        // Vite 8（Rolldown）下 manualChunks 必须用函数形式（对象形式会报错）
        manualChunks(id) {
          if (id.includes('node_modules/vue') || id.includes('node_modules/@vue')) return 'vue'
          if (id.includes('node_modules/axios')) return 'axios'
        }
      }
    }
  }
})
