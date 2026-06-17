import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Vite 配置：这里只做最小配置——注册 Vue 插件
export default defineConfig({
  plugins: [vue()]
})
