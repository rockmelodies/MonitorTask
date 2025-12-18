<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>变化记录</span>
          <div>
            <el-button 
              type="danger" 
              :disabled="selectedIds.length === 0"
              @click="handleBatchDelete"
            >
              <el-icon><Delete /></el-icon>
              批量删除 ({{ selectedIds.length }})
            </el-button>
            <el-button @click="fetchChanges">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>
      </template>
      
      <el-table 
        :data="changes" 
        v-loading="loading" 
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
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
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button type="danger" link size="small" @click="handleDelete(row)">
              删除
            </el-button>
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
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'

const loading = ref(false)
const changes = ref<any[]>([])
const selectedIds = ref<number[]>([])

const pagination = reactive({
  page: 1,
  perPage: 20,
  total: 0
})

const formatTime = (time: string) => {
  return new Date(time).toLocaleString('zh-CN')
}

const handleSelectionChange = (selection: any[]) => {
  selectedIds.value = selection.map(item => item.id)
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

const handleDelete = (row: any) => {
  ElMessageBox.confirm(`确定要删除这条变化记录吗?`, '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await request.delete(`/api/changes/${row.id}`)
      ElMessage.success('删除成功')
      fetchChanges()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

const handleBatchDelete = () => {
  ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 条记录吗?`, '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await request.delete('/api/changes/batch', {
        data: { ids: selectedIds.value }
      })
      ElMessage.success('批量删除成功')
      selectedIds.value = []
      fetchChanges()
    } catch (error) {
      ElMessage.error('批量删除失败')
    }
  }).catch(() => {})
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
