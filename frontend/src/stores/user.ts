import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, getCurrentUser, type User, type LoginData } from '@/api/auth'
import { ElMessage } from 'element-plus'
import router from '@/router'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  const userInfo = ref<User | null>(null)

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.role === 'admin')
  const isUser = computed(() => userInfo.value?.role === 'user' || userInfo.value?.role === 'admin')

  // 登录
  const login = async (loginData: LoginData) => {
    try {
      const res = await loginApi(loginData)
      token.value = res.data.token
      userInfo.value = res.data.user
      
      localStorage.setItem('token', res.data.token)
      localStorage.setItem('user', JSON.stringify(res.data.user))
      
      ElMessage.success('登录成功')
      router.push('/')
    } catch (error) {
      console.error('登录失败:', error)
      throw error
    }
  }

  // 登出
  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
    ElMessage.success('已登出')
  }

  // 获取用户信息
  const fetchUserInfo = async () => {
    try {
      const res = await getCurrentUser()
      userInfo.value = res.data
      localStorage.setItem('user', JSON.stringify(res.data))
    } catch (error) {
      console.error('获取用户信息失败:', error)
      logout()
    }
  }

  // 初始化
  const init = () => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      try {
        userInfo.value = JSON.parse(storedUser)
      } catch (error) {
        console.error('解析用户信息失败:', error)
      }
    }
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    isAdmin,
    isUser,
    login,
    logout,
    fetchUserInfo,
    init
  }
})
