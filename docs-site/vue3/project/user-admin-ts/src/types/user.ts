// 领域类型：整个项目对「用户」的数据契约
// 对照 JS 版：db.json 里一条用户长什么样，这里就定义成什么形状

// 角色是固定的三种之一 —— 用「字面量联合类型」锁死，写错一个字母（如 'adimn'）都报错
export type Role = 'admin' | 'editor' | 'viewer'

// 一条用户（对应 db.json 里的一个对象 / 数据库的一行）
export interface User {
  id: number
  name: string
  email: string
  phone: string
  role: Role
  status: 0 | 1 // 0=禁用 1=启用，也用字面量联合锁死
}

// 新增/编辑表单：新增时还没有 id，编辑时才有
// Omit<User, 'id'> = User 去掉 id，再补一个「可选的 id」
export type UserForm = Omit<User, 'id'> & { id?: number }
