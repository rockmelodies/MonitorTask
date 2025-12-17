<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>监控任务列表</span>
          <el-button type="primary" @click="showTaskDialog()">
            <el-icon><Plus /></el-icon>
            添加任务
          </el-button>
        </div>
      </template>
      
      <el-table :data="tasks" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="name" label="任务名称" min-width="150" />
        <el-table-column prop="url" label="监控URL" min-width="200" show-overflow-tooltip />
        <el-table-column prop="check_interval" label="检查间隔" width="100">
          <template #default="{ row }">
            {{ row.check_interval }}秒
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="优先级" width="90">
          <template #default="{ row }">
            <el-tag :type="priorityType(row.priority)" size="small">
              {{ priorityLabel(row.priority) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="{ row }">
            <el-switch
              v-model="row.is_active"
              @change="handleStatusChange(row)"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="showTaskDialog(row)">
              编辑
            </el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 任务对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
    >
      <el-form
        ref="taskFormRef"
        :model="taskForm"
        :rules="taskRules"
        label-width="120px"
      >
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="taskForm.name" placeholder="请输入任务名称" />
        </el-form-item>
        
        <el-form-item label="监控URL" prop="url">
          <el-input v-model="taskForm.url" placeholder="https://example.com" />
        </el-form-item>
        
        <el-form-item label="检查间隔" prop="check_interval">
          <el-input-number v-model="taskForm.check_interval" :min="60" :step="60" />
          <span style="margin-left: 10px; color: #909399;">秒</span>
        </el-form-item>
        
        <el-form-item label="CSS选择器">
          <el-input v-model="taskForm.selector" placeholder="可选，如: .content" />
        </el-form-item>
        
        <el-form-item label="关键词">
          <el-select
            v-model="taskForm.keywords"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="输入后按回车添加"
            style="width: 100%;"
          >
          </el-select>
        </el-form-item>
        
        <el-form-item label="钉钉Webhook">
          <el-input v-model="taskForm.dingtalk_webhook" placeholder="https://oapi.dingtalk.com/robot/..." />
        </el-form-item>
        
        <el-form-item label="优先级" prop="priority">
          <el-radio-group v-model="taskForm.priority">
            <el-radio label="low">低</el-radio>
            <el-radio label="medium">中</el-radio>
            <el-radio label="high">高</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="标签">
          <el-select
            v-model="taskForm.tags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="输入后按回车添加"
            style="width: 100%;"
          >
          </el-select>
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
import { ref, reactive, onMounted, computed } from 'vue'
import { getTasks, createTask, updateTask, deleteTask, type MonitorTask } from '@/api/task'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'

const loading = ref(false)
const tasks = ref<MonitorTask[]>([])
const dialogVisible = ref(false)
const taskFormRef = ref<FormInstance>()
const editingTask = ref<MonitorTask | null>(null)

const dialogTitle = computed(() => editingTask.value ? '编辑任务' : '添加任务')

const taskForm = reactive<MonitorTask>({
  name: '',
  url: '',
  check_interval: 300,
  selector: '',
  keywords: [],
  dingtalk_webhook: '',
  priority: 'medium',
  tags: [],
  is_active: true
})

const taskRules: FormRules = {
  name: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
  url: [
    { required: true, message: '请输入URL', trigger: 'blur' },
    { type: 'url', message: '请输入有效的URL', trigger: 'blur' }
  ],
  check_interval: [{ required: true, message: '请输入检查间隔', trigger: 'blur' }],
  priority: [{ required: true, message: '请选择优先级', trigger: 'change' }]
}

const priorityType = (priority: string) => {
  const map: Record<string, any> = { high: 'danger', medium: 'warning', low: 'info' }
  return map[priority] || 'info'
}

const priorityLabel = (priority: string) => {
  const map: Record<string, string> = { high: '高', medium: '中', low: '低' }
  return map[priority] || priority
}

const fetchTasks = async () => {
  loading.value = true
  try {
    const res = await getTasks()
    tasks.value = res.data
  } catch (error) {
    ElMessage.error('获取任务列表失败')
  } finally {
    loading.value = false
  }
}

const showTaskDialog = (task?: MonitorTask) => {
  if (task) {
    editingTask.value = task
    Object.assign(taskForm, task)
  } else {
    editingTask.value = null
    resetForm()
  }
  dialogVisible.value = true
}

const resetForm = () => {
  Object.assign(taskForm, {
    name: '',
    url: '',
    check_interval: 300,
    selector: '',
    keywords: [],
    dingtalk_webhook: '',
    priority: 'medium',
    tags: [],
    is_active: true
  })
  taskFormRef.value?.clearValidate()
}

const handleSubmit = async () => {
  if (!taskFormRef.value) return
  
  await taskFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (editingTask.value) {
          await updateTask(editingTask.value.id!, taskForm)
          ElMessage.success('更新成功')
        } else {
          await createTask(taskForm)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchTasks()
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }
  })
}

const handleStatusChange = async (task: MonitorTask) => {
  try {
    await updateTask(task.id!, { is_active: task.is_active })
    ElMessage.success('状态更新成功')
  } catch (error) {
    ElMessage.error('状态更新失败')
    task.is_active = !task.is_active
  }
}

const handleDelete = (task: MonitorTask) => {
  ElMessageBox.confirm(`确定要删除任务 "${task.name}" 吗?`, '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteTask(task.id!)
      ElMessage.success('删除成功')
      fetchTasks()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchTasks()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
