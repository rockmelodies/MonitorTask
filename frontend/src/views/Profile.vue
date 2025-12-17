<template>
  <div>
    <el-card>
      <template #header>
        <span>个人中心</span>
      </template>
      
      <el-descriptions :column="2" border>
        <el-descriptions-item label="用户名">{{ userStore.userInfo?.username }}</el-descriptions-item>
        <el-descriptions-item label="角色">
          <el-tag :type="roleType">{{ roleLabel }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ userStore.userInfo?.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="账户状态">
          <el-tag :type="userStore.userInfo?.is_active ? 'success' : 'danger'">
            {{ userStore.userInfo?.is_active ? '激活' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatTime(userStore.userInfo?.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="最后登录">{{ formatTime(userStore.userInfo?.last_login) }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const roleType = computed(() => {
  const map: Record<string, any> = { admin: 'danger', user: 'primary', viewer: 'info' }
  return map[userStore.userInfo?.role || 'user']
})

const roleLabel = computed(() => {
  const map: Record<string, string> = { admin: '管理员', user: '用户', viewer: '访客' }
  return map[userStore.userInfo?.role || 'user']
})

const formatTime = (time?: string) => {
  return time ? new Date(time).toLocaleString('zh-CN') : '-'
}
</script>
