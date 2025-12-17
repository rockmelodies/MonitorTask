<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="监控任务总数" :value="stats.total_tasks">
            <template #prefix>
              <el-icon color="#409eff"><Monitor /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="活跃任务" :value="stats.active_tasks">
            <template #prefix>
              <el-icon color="#67c23a"><CircleCheck /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="总变化数" :value="stats.total_changes">
            <template #prefix>
              <el-icon color="#e6a23c"><Bell /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="24小时变化" :value="stats.recent_changes">
            <template #prefix>
              <el-icon color="#f56c6c"><TrendCharts /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近变化</span>
              <el-button type="primary" link @click="router.push('/changes')">
                查看全部
              </el-button>
            </div>
          </template>
          
          <el-table :data="recentChanges" v-loading="loading">
            <el-table-column prop="detected_at" label="检测时间" width="180">
              <template #default="{ row }">
                {{ formatTime(row.detected_at) }}
              </template>
            </el-table-column>
            <el-table-column prop="task_id" label="任务ID" width="100" />
            <el-table-column prop="change_summary" label="变化摘要" show-overflow-tooltip />
            <el-table-column prop="matched_keywords" label="关键词" width="200">
              <template #default="{ row }">
                <el-tag
                  v-for="keyword in row.matched_keywords"
                  :key="keyword"
                  size="small"
                  type="danger"
                  style="margin-right: 5px;"
                >
                  {{ keyword }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="is_notified" label="通知状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.is_notified ? 'success' : 'info'" size="small">
                  {{ row.is_notified ? '已通知' : '未通知' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getStats, getAllChanges } from '@/api/task'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)

const stats = ref({
  total_tasks: 0,
  active_tasks: 0,
  total_changes: 0,
  recent_changes: 0,
  total_notifications: 0
})

const recentChanges = ref<any[]>([])

const fetchStats = async () => {
  try {
    const res = await getStats()
    stats.value = res.data
  } catch (error) {
    ElMessage.error('获取统计信息失败')
  }
}

const fetchRecentChanges = async () => {
  loading.value = true
  try {
    const res = await getAllChanges(1, 10)
    recentChanges.value = res.data.changes
  } catch (error) {
    ElMessage.error('获取变化记录失败')
  } finally {
    loading.value = false
  }
}

const formatTime = (time: string) => {
  return new Date(time).toLocaleString('zh-CN')
}

onMounted(() => {
  fetchStats()
  fetchRecentChanges()
})
</script>

<style scoped>
.dashboard {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
