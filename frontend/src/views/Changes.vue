<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>变化记录</span>
          <el-button @click="fetchChanges">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
      </template>
      
      <el-table :data="changes" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="detected_at" label="检测时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.detected_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="task_id" label="任务ID" width="100" />
        <el-table-column prop="change_summary" label="变化摘要" min-width="300" show-overflow-tooltip />
        <el-table-column prop="matched_keywords" label="匹配关键词" width="200">
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
            <span v-if="!row.matched_keywords || row.matched_keywords.length === 0">-</span>
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
      
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.perPage"
        :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="fetchChanges"
        @current-change="fetchChanges"
        style="margin-top: 20px; justify-content: center;"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getAllChanges } from '@/api/task'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const changes = ref<any[]>([])

const pagination = reactive({
  page: 1,
  perPage: 20,
  total: 0
})

const formatTime = (time: string) => {
  return new Date(time).toLocaleString('zh-CN')
}

const fetchChanges = async () => {
  loading.value = true
  try {
    const res = await getAllChanges(pagination.page, pagination.perPage)
    changes.value = res.data.changes
    pagination.total = res.data.total
  } catch (error) {
    ElMessage.error('获取变化记录失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchChanges()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
