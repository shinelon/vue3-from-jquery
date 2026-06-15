import request from './request'
import type { User } from '../types/user'

// 用户相关接口集中管理（CRUD + 单查）
// 现在每个函数都「自带说明书」：参数是什么、返回什么，一看类型签名就知道

// 查列表 → 返回 User[]
export function getUsers(): Promise<User[]> {
  return request.get<User[]>('/users')
}

// 查单个 → 返回 User
export function getUserById(id: number | string): Promise<User> {
  return request.get<User>(`/users/${id}`)
}

// 增 → 新增数据不含 id（id 由服务器生成），用 Omit<User, 'id'> 表达「User 去掉 id」
export function addUser(data: Omit<User, 'id'>): Promise<User> {
  return request.post<User>('/users', data)
}

// 改 → 只改部分字段，用 Partial<User> 表达「User 的所有字段都变可选」
export function updateUser(id: number | string, data: Partial<User>): Promise<User> {
  return request.put<User>(`/users/${id}`, data)
}

// 删 → 没有返回体，用 void
export function deleteUser(id: number | string): Promise<void> {
  return request.delete<void>(`/users/${id}`)
}
