import request from '@/utils/request'

export interface LoginData {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  password: string
  email?: string
}

export interface User {
  id: number
  username: string
  email: string
  role: string
  is_active: boolean
  created_at: string
  last_login: string
}

// 登录
export const login = (data: LoginData) => {
  return request({
    url: '/auth/login',
    method: 'post',
    data
  })
}

// 注册
export const register = (data: RegisterData) => {
  return request({
    url: '/auth/register',
    method: 'post',
    data
  })
}

// 获取当前用户信息
export const getCurrentUser = () => {
  return request({
    url: '/auth/me',
    method: 'get'
  })
}

// 获取所有用户
export const getUsers = () => {
  return request({
    url: '/users',
    method: 'get'
  })
}

// 更新用户
export const updateUser = (id: number, data: any) => {
  return request({
    url: `/users/${id}`,
    method: 'put',
    data
  })
}

// 删除用户
export const deleteUser = (id: number) => {
  return request({
    url: `/users/${id}`,
    method: 'delete'
  })
}
