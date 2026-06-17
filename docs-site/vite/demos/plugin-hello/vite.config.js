import { defineConfig } from 'vite'
import hello from './plugins/vite-plugin-hello.js'

// 把自定义插件加进 plugins 数组
export default defineConfig({
  plugins: [hello()]
})
