import request from '@/utils/request'

export interface MonitorTask {
  id?: number
  name: string
  url: string
  check_interval: number
  selector?: string
  keywords: string[]
  dingtalk_webhook?: string
  priority: string
  tags: string[]
  is_active: boolean
  last_check_time?: string
  created_at?: string
  updated_at?: string
}

// 获取所有任务
export const getTasks = () => {
  return request({
    url: '/tasks',
    method: 'get'
  })
}

// 获取单个任务
export const getTask = (id: number) => {
  return request({
    url: `/tasks/${id}`,
    method: 'get'
  })
}

// 创建任务
export const createTask = (data: MonitorTask) => {
  return request({
    url: '/tasks',
    method: 'post',
    data
  })
}

// 更新任务
export const updateTask = (id: number, data: Partial<MonitorTask>) => {
  return request({
    url: `/tasks/${id}`,
    method: 'put',
    data
  })
}

// 删除任务
export const deleteTask = (id: number) => {
  return request({
    url: `/tasks/${id}`,
    method: 'delete'
  })
}

// 获取任务变化记录
export const getTaskChanges = (taskId: number, page = 1, perPage = 20) => {
  return request({
    url: `/tasks/${taskId}/changes`,
    method: 'get',
    params: { page, per_page: perPage }
  })
}

// 获取所有变化记录
export const getAllChanges = (page = 1, perPage = 20) => {
  return request({
    url: '/changes',
    method: 'get',
    params: { page, per_page: perPage }
  })
}

// 获取统计信息
export const getStats = () => {
  return request({
    url: '/stats',
    method: 'get'
  })
}
