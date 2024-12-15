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
          <input type="file" @change="handleAvatarUpload" accept="image/*" />
          <button type="submit" class="btn btn-add">添加</button>
        </form>
        <!-- 头像预览 -->
        <div v-if="newRecord.avatar" class="avatar-preview">
          <img :src="newRecord.avatar" alt="头像预览" />
        </div>
      </div>
  
      <!-- 表格 -->
      <table>
        <thead>
          <tr>
            <th>序号</th>
            <th>头像</th>
            <th>姓名</th>
            <th>年龄</th>
            <th>邮箱</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(record, index) in filteredRecords" :key="record.id">
            <td>{{ index + 1 }}</td>
            <td>
              <img :src="record.avatar" alt="头像" class="table-avatar" />
            </td>
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
            <td colspan="6" class="no-records">暂无记录</td>
          </tr>
        </tbody>
      </table>
  
      <!-- 详情弹窗 -->
      <div v-if="showDetailsModal" class="modal">
        <div class="modal-content">
          <h2>记录详情</h2>
          <img :src="selectedRecord?.avatar" alt="详情头像" class="details-avatar" />
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
            <input type="file" @change="handleEditAvatarUpload" accept="image/*" />
            <button type="submit" class="btn btn-save">保存</button>
            <button @click="closeEdit" type="button" class="btn btn-cancel">取消</button>
          </form>
          <div v-if="editableRecord.avatar" class="avatar-preview">
            <img :src="editableRecord.avatar" alt="编辑头像预览" />
          </div>
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
    avatar: string;
  }
  
  export default defineComponent({
    name: 'TablePage',
    setup() {
      const records = ref<Record[]>([
        {
          id: 1,
          name: '张三',
          age: 28,
          email: 'zhangsan@example.com',
          avatar: '/images/1.png',
        },
        {
          id: 2,
          name: '李四',
          age: 32,
          email: 'lisi@example.com',
          avatar: '/images/9.png',
        },
      ]);
  
      const searchQuery = ref('');
      const newRecord = ref<Record>({
        id: 0,
        name: '',
        age: 0,
        email: '',
        avatar: '',
      });
  
      const filteredRecords = computed(() => {
        if (!searchQuery.value) {
          return records.value;
        }
        return records.value.filter((record) =>
          record.name.includes(searchQuery.value)
        );
      });
  
      const handleAvatarUpload = (event: Event) => {
        const file = (event.target as HTMLInputElement).files?.[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (e) => {
            newRecord.value.avatar = e.target?.result as string;
          };
          reader.readAsDataURL(file);
        }
      };
  
      const addRecord = () => {
        if (newRecord.value.name && newRecord.value.age > 0 && newRecord.value.email) {
          const id = records.value.length
            ? Math.max(...records.value.map((r) => r.id)) + 1
            : 1;
          records.value.push({ ...newRecord.value, id });
          newRecord.value = { id: 0, name: '', age: 0, email: '', avatar: '' };
        } else {
          alert('请完整填写表单！');
        }
      };
  
      const deleteRecord = (id: number) => {
        if (confirm('确定删除这条记录吗？')) {
          records.value = records.value.filter((record) => record.id !== id);
        }
      };
  
      const searchRecords = () => {};
      const resetSearch = () => {
        searchQuery.value = '';
      };
  
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
  
      const showEditModal = ref(false);
      const editableRecord = ref<Record | null>(null);
  
      const editRecord = (record: Record) => {
        editableRecord.value = { ...record };
        showEditModal.value = true;
      };
  
      const handleEditAvatarUpload = (event: Event) => {
        const file = (event.target as HTMLInputElement).files?.[0];
        if (file && editableRecord.value) {
          const reader = new FileReader();
          reader.onload = (e) => {
            editableRecord.value!.avatar = e.target?.result as string;
          };
          reader.readAsDataURL(file);
        }
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
  
      return {
        records,
        searchQuery,
        newRecord,
        filteredRecords,
        handleAvatarUpload,
        addRecord,
        deleteRecord,
        searchRecords,
        resetSearch,
        showDetailsModal,
        selectedRecord,
        showDetails,
        closeDetails,
        showEditModal,
        editableRecord,
        editRecord,
        handleEditAvatarUpload,
        saveEdit,
        closeEdit,
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
    /* 头像样式 */
    .table-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    }

    .details-avatar,
    .avatar-preview img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    }
  </style>
  