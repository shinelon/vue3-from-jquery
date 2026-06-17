import axios from 'axios'

// 创建 axios 实例，统一配置
const request = axios.create({
  baseURL: '/api',        // 走 Vite 代理 → http://localhost:3000
  timeout: 10000
})

export default request
