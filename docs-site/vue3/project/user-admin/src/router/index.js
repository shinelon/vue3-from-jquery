import { createRouter, createWebHistory } from 'vue-router'
import UserList from '../views/UserList.vue'
import UserDetail from '../views/UserDetail.vue'

// 路由表：网址路径 → 显示哪个组件
const routes = [
  { path: '/',          name: 'list',   component: UserList },
  { path: '/users/:id', name: 'detail', component: UserDetail }   // :id 动态参数
]

const router = createRouter({
  history: createWebHistory(),   // HTML5 history 模式（URL 干净）
  routes
})

export default router
