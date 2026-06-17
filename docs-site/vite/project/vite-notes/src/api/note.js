import request from './request'

// 获取所有笔记
export function getNotes() {
  return request.get('/notes')
}
