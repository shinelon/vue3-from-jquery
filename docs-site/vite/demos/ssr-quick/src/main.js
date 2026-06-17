import { createSSRApp } from 'vue'
import App from './App.vue'

// 客户端入口：createSSRApp 会在挂载时"激活"服务端渲染好的 HTML（hydration）
createSSRApp(App).mount('#app')
