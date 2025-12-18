<template>
  <el-container class="layout-container">
    <el-aside :width="isCollapse ? '64px' : '220px'" class="sidebar">
      <div class="logo">
        <el-icon :size="28"><Monitor /></el-icon>
        <span v-show="!isCollapse">MonitorTask</span>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        router
        :unique-opened="true"
        :collapse="isCollapse"
        :collapse-transition="false"
      >
        <el-menu-item index="/dashboard">
          <el-icon><DataAnalysis /></el-icon>
          <template #title>仪表盘</template>
        </el-menu-item>
        
        <el-menu-item index="/tasks">
          <el-icon><Monitor /></el-icon>
          <template #title>监控任务</template>
        </el-menu-item>
        
        <el-menu-item index="/changes">
          <el-icon><Bell /></el-icon>
          <template #title>变化记录</template>
        </el-menu-item>
        
        <el-menu-item v-if="userStore.isAdmin" index="/users">
          <el-icon><User /></el-icon>
          <template #title>用户管理</template>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-icon class="collapse-icon" @click="toggleCollapse" :size="20">
            <Fold v-if="!isCollapse" />
            <Expand v-else />
          </el-icon>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item>{{ currentRouteName }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <div class="header-right">
          <!-- 主题切换 -->
          <el-tooltip :content="isDark ? '切换到亮色模式' : '切换到暗黑模式'" placement="bottom">
            <el-icon class="theme-icon" @click="toggleTheme" :size="20">
              <Sunny v-if="isDark" />
              <Moon v-else />
            </el-icon>
          </el-tooltip>
          
          <el-dropdown>
            <div class="user-info">
              <el-avatar :size="32" :icon="UserFilled" />
              <span>{{ userStore.userInfo?.username }}</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="router.push('/profile')">
                  <el-icon><User /></el-icon>
                  个人中心
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { UserFilled, Fold, Expand, Sunny, Moon } from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 菜单折叠
const isCollapse = ref(false)
const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
  localStorage.setItem('sidebar-collapse', String(isCollapse.value))
}

// 初始化折叠状态
onMounted(() => {
  const savedCollapse = localStorage.getItem('sidebar-collapse')
  if (savedCollapse) {
    isCollapse.value = savedCollapse === 'true'
  }
  
  // 初始化主题
  const savedTheme = localStorage.getItem('theme-mode')
  if (savedTheme === 'dark') {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
})

// 主题切换
const isDark = ref(false)
const toggleTheme = () => {
  isDark.value = !isDark.value
  
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme-mode', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme-mode', 'light')
  }
}

const activeMenu = computed(() => route.path)
const currentRouteName = computed(() => (route.meta.title as string) || '首页')

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    userStore.logout()
  }).catch(() => {})
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.sidebar {
  background-color: var(--sidebar-bg);
  transition: width 0.3s;
  overflow: hidden;
  box-shadow: 2px 0 8px 0 rgba(29, 35, 41, 0.05);
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 20px;
  font-weight: 600;
  color: var(--logo-color);
  border-bottom: 1px solid var(--sidebar-border);
  white-space: nowrap;
  overflow: hidden;
}

.el-menu {
  border-right: none;
  background-color: var(--sidebar-bg) !important;
}

/* 菜单项默认状态 */
:deep(.el-menu-item) {
  color: var(--menu-text-color) !important;
  background-color: transparent !important;
  transition: all 0.3s ease;
  font-weight: 500;
  border-radius: 0;
}

/* 菜单项悬停状态 */
:deep(.el-menu-item:hover),
:deep(.el-menu-item:focus) {
  color: var(--menu-hover-text) !important;
  background-color: var(--menu-hover-bg) !important;
  outline: none;
}

/* 菜单项激活状态 */
:deep(.el-menu-item.is-active) {
  color: var(--menu-active-text) !important;
  background-color: var(--menu-active-bg) !important;
  font-weight: 600;
  position: relative;
}

/* 激活状态左侧指示条 */
:deep(.el-menu-item.is-active::before) {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background-color: var(--menu-active-text);
}

/* 菜单图标颜色继承 */
:deep(.el-menu-item .el-icon) {
  color: inherit !important;
  transition: color 0.3s ease;
}

:deep(.el-menu-item:hover .el-icon),
:deep(.el-menu-item:focus .el-icon) {
  color: inherit !important;
}

:deep(.el-menu-item.is-active .el-icon) {
  color: inherit !important;
}

.header {
  background-color: var(--header-bg);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 1px 4px 0 rgba(0, 21, 41, 0.08);
}

.header-left {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 20px;
}

.collapse-icon {
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  transition: all 0.3s;
  color: var(--text-color);
}

.collapse-icon:hover {
  background-color: var(--hover-bg);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.theme-icon {
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  transition: all 0.3s;
  color: var(--text-color);
}

.theme-icon:hover {
  background-color: var(--hover-bg);
  transform: rotate(180deg);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
  color: var(--text-color);
}

.user-info:hover {
  background-color: var(--hover-bg);
}

.main-content {
  background-color: var(--main-bg);
  padding: 20px;
  overflow-y: auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ========== 默认亮色主题 ========== */
:root {
  /* 侧边栏 - 深蓝色 */
  --sidebar-bg: #001529;
  --sidebar-border: rgba(255, 255, 255, 0.1);
  --logo-color: #ffffff;
  
  /* 菜单 - 白色文字 */
  --menu-text-color: rgba(255, 255, 255, 0.65);
  --menu-hover-text: #ffffff;
  --menu-hover-bg: rgba(255, 255, 255, 0.08);
  --menu-active-text: #ffffff;
  --menu-active-bg: #1890ff;
  
  /* 顶栏 - 白色 */
  --header-bg: #ffffff;
  --border-color: #f0f0f0;
  
  /* 通用 */
  --text-color: rgba(0, 0, 0, 0.85);
  --hover-bg: rgba(0, 0, 0, 0.04);
  --main-bg: #f0f2f5;
}

/* ========== 暗黑主题 ========== */
html.dark {
  /* 侧边栏 - 深灰色 */
  --sidebar-bg: #1a1a1a;
  --sidebar-border: rgba(255, 255, 255, 0.12);
  --logo-color: #ffffff;
  
  /* 菜单 - 白色文字 */
  --menu-text-color: rgba(255, 255, 255, 0.65);
  --menu-hover-text: #ffffff;
  --menu-hover-bg: rgba(255, 255, 255, 0.08);
  --menu-active-text: #ffffff;
  --menu-active-bg: #1890ff;
  
  /* 顶栏 - 深灰色 */
  --header-bg: #1e1e1e;
  --border-color: #303030;
  
  /* 通用 */
  --text-color: rgba(255, 255, 255, 0.85);
  --hover-bg: rgba(255, 255, 255, 0.08);
  --main-bg: #141414;
}

html.dark .sidebar {
  box-shadow: 2px 0 12px 0 rgba(0, 0, 0, 0.3);
}
</style>
