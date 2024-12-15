<template>
    <div class="table-container">
      <h1>记录管理表</h1>
  
      <!-- 查询栏 -->
      <div class="search-bar">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="输入关键字查询..."
          class="search-input"
        />
        <button @click="searchRecords" class="btn btn-search">查询</button>
        <button @click="resetSearch" class="btn btn-reset">重置</button>
      </div>
  
      <!-- 添加记录 -->
      <div class="add-record">
        <h2>添加新记录</h2>
        <form @submit.prevent="addRecord">
          <input v-model="newRecord.name" type="text" placeholder="姓名" />
          <input v-model="newRecord.age" type="number" placeholder="年龄" />
          <input v-model="newRecord.email" type="email" placeholder="邮箱" />
          <button type="submit" class="btn btn-add">添加</button>
        </form>
      </div>
  
      <!-- 表格 -->
      <table>
        <thead>
          <tr>
            <th>序号</th>
            <th>姓名</th>
            <th>年龄</th>
            <th>邮箱</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(record, index) in filteredRecords" :key="record.id">
            <td>{{ index + 1 }}</td>
            <td>{{ record.name }}</td>
            <td>{{ record.age }}</td>
            <td>{{ record.email }}</td>
            <td>
                <button @click="showDetails(record)" class="btn btn-details">详情</button>
              <button @click="editRecord(record)" class="btn btn-edit">编辑</button>
              <button @click="deleteRecord(record.id)" class="btn btn-delete">删除</button>
          
            </td>
          </tr>
          <tr v-if="filteredRecords.length === 0">
            <td colspan="5" class="no-records">暂无记录</td>
          </tr>
        </tbody>
      </table>
        <!-- 详情弹窗 -->
        <div v-if="showDetailsModal" class="modal">
        <div class="modal-content">
            <h2>记录详情</h2>
            <p><strong>姓名：</strong>{{ selectedRecord?.name }}</p>
            <p><strong>年龄：</strong>{{ selectedRecord?.age }}</p>
            <p><strong>邮箱：</strong>{{ selectedRecord?.email }}</p>
            <button @click="closeDetails" class="btn btn-close">关闭</button>
        </div>
        </div>

        <!-- 编辑弹窗 -->
        <div v-if="showEditModal" class="modal">
        <div class="modal-content">
            <h2>编辑记录</h2>
            <form @submit.prevent="saveEdit">
            <input v-model="editableRecord.name" type="text" placeholder="姓名" />
            <input v-model="editableRecord.age" type="number" placeholder="年龄" />
            <input v-model="editableRecord.email" type="email" placeholder="邮箱" />
            <button type="submit" class="btn btn-save">保存</button>
            <button @click="closeEdit" type="button" class="btn btn-cancel">取消</button>
            </form>
        </div>
        </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, computed } from 'vue';
  
  interface Record {
    id: number;
    name: string;
    age: number;
    email: string;
  }
  
  export default defineComponent({
    name: 'TablePage',
    setup() {
      // 记录数据
      const records = ref<Record[]>([
        { id: 1, name: '张三', age: 28, email: 'zhangsan@example.com' },
        { id: 2, name: '李四', age: 32, email: 'lisi@example.com' },
        { id: 3, name: '王五', age: 24, email: 'wangwu@example.com' },
      ]);
  
      // 查询关键字
      const searchQuery = ref('');
  
      // 新记录表单数据
      const newRecord = ref<Record>({
        id: 0,
        name: '',
        age: 0,
        email: '',
      });
  
      // 过滤后的记录
      const filteredRecords = computed(() => {
        if (!searchQuery.value) {
          return records.value;
        }
        return records.value.filter((record) =>
          record.name.includes(searchQuery.value)
        );
      });
      
        // 详情相关
        const showDetailsModal = ref(false);
        const selectedRecord = ref<Record | null>(null);

        const showDetails = (record: Record) => {
        selectedRecord.value = record;
        showDetailsModal.value = true;
        };

        const closeDetails = () => {
        selectedRecord.value = null;
        showDetailsModal.value = false;
        };

        // 编辑相关
        const showEditModal = ref(false);
        const editableRecord = ref<Record | null>(null);

        const editRecord = (record: Record) => {
        editableRecord.value = { ...record };
        showEditModal.value = true;
        };

        const saveEdit = () => {
        if (editableRecord.value) {
            const index = records.value.findIndex(
            (r) => r.id === editableRecord.value!.id
            );
            if (index !== -1) {
            records.value[index] = { ...editableRecord.value };
            }
            closeEdit();
        }
        };

        const closeEdit = () => {
        editableRecord.value = null;
        showEditModal.value = false;
        };

      // 添加记录
      const addRecord = () => {
        if (newRecord.value.name && newRecord.value.email && newRecord.value.age > 0) {
          const id = records.value.length
            ? Math.max(...records.value.map((r) => r.id)) + 1
            : 1;
          records.value.push({ ...newRecord.value, id });
          newRecord.value = { id: 0, name: '', age: 0, email: '' }; // 清空表单
        } else {
          alert('请完整填写表单！');
        }
      };
  
      // 删除记录
      const deleteRecord = (id: number) => {
        if (confirm('确定删除这条记录吗？')) {
          records.value = records.value.filter((record) => record.id !== id);
        }
      };
  
      // 查询记录
      const searchRecords = () => {
        // `filteredRecords` 自动响应，因此此处不需要额外处理
      };
  
      // 重置查询
      const resetSearch = () => {
        searchQuery.value = '';
      };
  
      return {
        records,
        searchQuery,
        newRecord,
        filteredRecords,
        showDetailsModal,
        selectedRecord,
        showDetails,
        closeDetails,
        showEditModal,
        editableRecord,
        editRecord,
        saveEdit,
        closeEdit,
        addRecord,
        deleteRecord,
        searchRecords,
        resetSearch,
      };
    },
  });
  </script>
  
  <style scoped>
  .table-container {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  h1 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .search-bar,
  .add-record {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
  }
  
  .search-bar input,
  .add-record input {
    padding: 8px;
    margin-right: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    flex: 1;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  table th,
  table td {
    padding: 10px;
    border: 1px solid #ddd;
    text-align: center;
  }
  
  .no-records {
    text-align: center;
    font-style: italic;
    color: #999;
  }
  
  .btn {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-search {
    background-color: #4caf50;
    color: white;
  }
  
  .btn-reset {
    background-color: #2196f3;
    color: white;
  }
  
  .btn-add {
    background-color: #007bff;
    color: white;
  }
  
  .btn-delete {
    background-color: #f44336;
    color: white;
  }

  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    }

    .modal-content {
    background: #fff;
    padding: 20px;
    border-radius: 8px;
    max-width: 400px;
    width: 100%;
    }

    .btn-close,
    .btn-save,
    .btn-cancel {
    margin-top: 10px;
    }
  </style>
  