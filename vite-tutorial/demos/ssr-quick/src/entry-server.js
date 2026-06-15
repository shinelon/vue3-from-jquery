import { renderToString } from '@vue/server-renderer'
import { createSSRApp } from 'vue'
import App from './App.vue'

// 服务端入口：把组件渲染成 HTML 字符串
export function render() {
  const app = createSSRApp(App)
  return renderToString(app)
}
