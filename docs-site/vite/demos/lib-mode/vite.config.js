import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 库模式：把组件打包成一个可被别人 import 的库
export default defineConfig({
  plugins: [vue()],
  build: {
    lib: {
      entry: 'src/index.js',        // 库的入口
      name: 'LibModeDemo',          // UMD 模式下的全局变量名
      formats: ['es', 'umd'],       // 输出 ES 和 UMD 两种格式
      fileName: 'lib-mode'          // 输出文件名
    },
    rollupOptions: {
      external: ['vue'],            // vue 不打进库（用库的人自己有 vue）
      output: {
        exports: 'named',           // 库以具名导出为主（消除 MIXED_EXPORTS 警告）
        globals: { vue: 'Vue' }     // UMD 模式下 vue 的全局变量名
      }
    }
  }
})
