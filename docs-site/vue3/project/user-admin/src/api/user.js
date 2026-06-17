import request from './request'

// 用户相关接口集中管理（CRUD + 单查）
// 对照 jQuery：相当于把 $.ajax({url, type, data}) 收拢成函数

// 查列表（GET /api/users）
export function getUsers(params) {
  return request.get('/users', { params })
}

// 查单个（GET /api/users/:id）—— 第 9 章详情页用
export function getUserById(id) {
  return request.get(`/users/${id}`)
}

// 增（POST /api/users）
export function addUser(data) {
  return request.post('/users', data)
}

// 改（PUT /api/users/:id）
export function updateUser(id, data) {
  return request.put(`/users/${id}`, data)
}

// 删（DELETE /api/users/:id）
export function deleteUser(id) {
  return request.delete(`/users/${id}`)
}
