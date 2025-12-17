<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
        </div>
      </template>
      
      <el-table :data="users" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="roleType(row.role)" size="small">
              {{ roleLabel(row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
              {{ row.is_active ? '激活' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="last_login" label="最后登录" width="180">
          <template #default="{ row }">
            {{ row.last_login ? formatTime(row.last_login) : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="showUserDialog(row)">
              编辑
            </el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)" :disabled="row.username === 'admin'">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 用户编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="编辑用户"
      width="500px"
    >
      <el-form
        ref="userFormRef"
        :model="userForm"
        label-width="100px"
      >
        <el-form-item label="用户名">
          <el-input v-model="userForm.username" disabled />
        </el-form-item>
        
        <el-form-item label="邮箱">
          <el-input v-model="userForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        
        <el-form-item label="角色">
          <el-select v-model="userForm.role" placeholder="请选择角色">
            <el-option label="管理员" value="admin" />
            <el-option label="普通用户" value="user" />
            <el-option label="访客" value="viewer" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-switch v-model="userForm.is_active" />
        </el-form-item>
        
        <el-form-item label="重置密码">
          <el-input v-model="userForm.password" type="password" placeholder="留空则不修改密码" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getUsers, updateUser, deleteUser, type User } from '@/api/auth'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'

const loading = ref(false)
const users = ref<User[]>([])
const dialogVisible = ref(false)
const userFormRef = ref<FormInstance>()
const editingUser = ref<User | null>(null)

const userForm = reactive({
  id: 0,
  username: '',
  email: '',
  role: 'user',
  is_active: true,
  password: ''
})

const roleType = (role: string) => {
  const map: Record<string, any> = { admin: 'danger', user: 'primary', viewer: 'info' }
  return map[role] || 'info'
}

const roleLabel = (role: string) => {
  const map: Record<string, string> = { admin: '管理员', user: '用户', viewer: '访客' }
  return map[role] || role
}

const formatTime = (time: string) => {
  return new Date(time).toLocaleString('zh-CN')
}

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await getUsers()
    users.value = res.data
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const showUserDialog = (user: User) => {
  editingUser.value = user
  Object.assign(userForm, {
    id: user.id,
    username: user.username,
    email: user.email,
    role: user.role,
    is_active: user.is_active,
    password: ''
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    const updateData: any = {
      email: userForm.email,
      role: userForm.role,
      is_active: userForm.is_active
    }
    
    if (userForm.password) {
      updateData.password = userForm.password
    }
    
    await updateUser(userForm.id, updateData)
    ElMessage.success('更新成功')
    dialogVisible.value = false
    fetchUsers()
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const handleDelete = (user: User) => {
  ElMessageBox.confirm(`确定要删除用户 "${user.username}" 吗?`, '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteUser(user.id)
      ElMessage.success('删除成功')
      fetchUsers()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
