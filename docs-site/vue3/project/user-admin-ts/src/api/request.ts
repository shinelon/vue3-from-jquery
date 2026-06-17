import axios from 'axios'
import type { AxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例，统一配置（baseURL 走 Vite 代理）
const instance = axios.create({
  baseURL: '/api', // → http://localhost:3000（由 vite.config.ts 的 proxy 转发）
  timeout: 10000
})

// 响应拦截器：成功时直接返回 response.data（拆掉外壳）
// ⚠️ 重点：这个拦截器改了「运行时返回值」，但 axios 自带的类型并不知道这件事！
//    所以下面我们另包一层，把类型对齐到「运行时真实返回的数据」。
instance.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const msg = error.response?.data?.message || error.message || '请求失败'
    ElMessage.error(msg)
    return Promise.reject(error)
  }
)

// 轻封装：让调用方拿到的就是「拆掉外壳后的数据」本身，而不是 AxiosResponse
// <T> 是泛型：调用时告诉它「这次返回的数据是什么类型」
async function get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
  // 运行时 instance.get 已经返回 data（被拦截器拆过），
  // 但它的类型仍以为是 AxiosResponse，所以用 as 对齐一下
  return instance.get(url, config) as unknown as Promise<T>
}
async function post<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
  return instance.post(url, data, config) as unknown as Promise<T>
}
async function put<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
  return instance.put(url, data, config) as unknown as Promise<T>
}
async function del<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
  return instance.delete(url, config) as unknown as Promise<T>
}

export default { get, post, put, delete: del }
