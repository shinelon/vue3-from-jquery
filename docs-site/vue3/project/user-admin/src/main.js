import { createApp } from 'vue'
import { createPinia } from 'pinia'      // 第 10 章：引入 Pinia
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.use(createPinia())                    // 注册 Pinia
app.mount('#app')
