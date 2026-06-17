import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例，统一配置（baseURL 走 Vite 代理）
const request = axios.create({
  baseURL: '/api',       // → http://localhost:3000（由 vite.config.js 的 proxy 转发）
  timeout: 10000
})

// 响应拦截器
request.interceptors.response.use(
  // 成功：统一取出 response.data
  (response) => response.data,
  // 失败：全局错误提示（第 11 章完善）
  (error) => {
    const msg = error.response?.data?.message || error.message || '请求失败'
    ElMessage.error(msg)
    return Promise.reject(error)
  }
)

export default request
