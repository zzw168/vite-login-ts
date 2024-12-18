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
  
      <!-- 添加记录按钮 -->
      <p>
        <button @click="showAddForm" class="btn add-btn">添加新记录</button>
        <button @click="deleteSelected" class="btn delete-btn">
            删除选中记录
        </button>
      </p>
      <!-- 添加记录表单（仅在 isAdding 为 true 时显示） -->
      <div v-if="isAdding" class="modal">
        <div class="modal-content">
          <h3>添加新记录</h3>
          <form @submit.prevent="handleAddRecord">
            <p><strong>头像：</strong>
              <div v-if="newRecord.avatar" class="avatar-preview">
                  <img :src="newRecord.avatar" alt="Avatar Preview" />
              </div>
              <input id="avatar" type="file" @change="handleAvatarUpload" accept="image/*" />
            </p>
            <p><strong>姓名：</strong>
              <input id="name" v-model="newRecord.name" type="text" required />
            </p>
            <p><strong>年龄：</strong>
              <input v-model="newRecord.age" type="text" required />
            </p> 
            <p><strong>邮箱：</strong>
              <input id="email" v-model="newRecord.email" type="email" required />
            </p> 
            <div style="text-align:right;">
              <button type="submit" class="btn btn-save">保存记录</button>
              <button type="button" @click="cancelAdd" class="btn btn-cancel">取消</button>
            </div>  
          </form>
        </div>
      </div>
  
      <!-- 表格 -->
      <table>
        <thead>
          <tr>
            <th><input type="checkbox" @change="toggleSelectAll" :checked="isAllSelected" /></th>
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
              <td>
                  <input
                  type="checkbox"
                  :value="record.id"
                  v-model="selectedRecordIds"
                  />
              </td>
              <td>{{ index + 1 }}</td>
              <td>
                  <img :src="record.avatar || placeholderAvatar" alt="头像" class="table-avatar" />
              </td>  
              <td>{{ record.name }}</td>
              <td>{{ record.age }}</td>
              <td>{{ record.email }}</td>
              <td>
                  <button @click="editRecord(record)" class="btn btn-edit">编辑</button>
                  <button @click="deleteRecord(record.id)"  class="btn btn-delete">删除</button>
                  <button @click="showDetails(record)" class="btn btn-details">详情</button>
              </td>
            </tr>
        </tbody>
      </table>
  
      <!-- 详情弹窗 -->
      <div v-if="showDetailsModal" class="modal">
        <div class="modal-content">
          <h2>记录详情</h2>
          <img :src="selectedRecord?.avatar || placeholderAvatar" alt="详情头像" class="details-avatar" />
          <p><strong>姓名：</strong>{{ selectedRecord?.name }}</p>
          <p><strong>年龄：</strong>{{ selectedRecord?.age }}</p>
          <p><strong>邮箱：</strong>{{ selectedRecord?.email }}</p>
          <div style="text-align:right;">
            <button @click="closeDetails" class="btn btn-close">关闭</button>
          </div>
        </div>
      </div>
  
      <!-- 编辑弹窗 -->
      <div v-if="showEditModal" class="modal">
        <div class="modal-content">
          <h2>编辑记录</h2>
          <form @submit.prevent="saveEdit">
            <div v-if="editableRecord.avatar" class="avatar-preview">
              <img :src="editableRecord.avatar" alt="编辑头像预览" />
            </div>
            <p><strong>姓名：</strong>
            <input v-model="editableRecord.name" type="text" placeholder="姓名" />
            </p>
            <p><strong>年龄：</strong>
            <input v-model="editableRecord.age" type="number" placeholder="年龄" />
            </p>
            <p><strong>邮箱：</strong>
            <input v-model="editableRecord.email" type="email" placeholder="邮箱" />
            </p>
            <p><strong>头像：</strong>
            <input type="file" @change="handleEditAvatarUpload" accept="image/*" />
            </p>
            <div style="text-align:right;">
              <button type="submit" class="btn btn-save">保存</button>
              <button @click="closeEdit" type="button" class="btn btn-cancel">取消</button>
            </div>
          </form>
          
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, computed, onMounted } from 'vue';
  import axios from 'axios';
  import apiClient from "@/plugins/axios";
  
  interface Record {
    id: number;
    name: string;
    age: number;
    email: string;
    avatar: string | null;
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

      const placeholderAvatar = '/images/5.png'; // 默认头像
      const selectedRecordIds = ref<number[]>([]);
        // 计算是否所有记录都被选中
        const isAllSelected = computed(() => {
        return records.value.length > 0 && selectedRecordIds.value.length === records.value.length;
        });

        // 切换全选/全取消
        const toggleSelectAll = (event: Event) => {
        const isChecked = (event.target as HTMLInputElement).checked;
        selectedRecordIds.value = isChecked ? records.value.map((record) => record.id) : [];
        };

        // 删除选中的记录
        // const deleteSelected = () => {
        //   if (confirm('确定删除选中的记录吗？')) {
        //     records.value = records.value.filter((record) => !selectedRecordIds.value.includes(record.id));
        //     selectedRecordIds.value = [];
        //   }
        // };
        const deleteSelected = async () => {
          if (confirm("确定删除选中的记录吗？")) {
            try {
              await apiClient.post("/records/batch-delete", {
                ids: selectedRecordIds.value,
              });

              // 从前端移除选中的记录
              records.value = records.value.filter((record) => !selectedRecordIds.value.includes(record.id));
              selectedRecordIds.value = [];
            } catch (error) {
              console.error("批量删除失败：", error);
              alert(`批量删除失败：${error || "未知错误"}`);
            }
          }
        };

        onMounted(async () => {
          try {
            const response = await apiClient.get("/records");
            records.value = response.data; // 初始化记录
            console.log(records.value)
          } catch (error) {
            console.error("获取记录失败：", error);
            alert("无法加载记录，请检查网络连接或后台服务是否正常");
          }
        });

      const isAdding = ref(false); // 是否显示添加表单

        // 显示添加表单
        const showAddForm = () => {
            isAdding.value = true;
            newRecord.value = { id: 0, name: '',age: 0, email: '', avatar: null }; // 重置表单
        };

        // 取消添加
        const cancelAdd = () => {
        isAdding.value = false;
        };

        // 保存新记录
        // const handleAddRecord = () => {
        // if (newRecord.value) {
        //     newRecord.value.id = Date.now(); // 使用时间戳作为唯一 ID
        //     records.value.push({ ...newRecord.value });
        //     isAdding.value = false; // 隐藏表单
        // }
        // };
        const handleAddRecord = async () => {
          if (newRecord.value) {
            try {
              const response = await apiClient.post("/records", newRecord.value);

              records.value.push(response.data); // 后端返回的数据直接更新前端表格
              isAdding.value = false; // 隐藏添加记录表单
            } catch (error) {
              console.error("新增记录失败：", error);
              alert(`新增记录失败：${error || "未知错误"}`);
            }
          }
        };

        // 查询记录
      const filteredRecords = computed(() => {
        if (!searchQuery.value) {
          return records.value;
        }
        return records.value.filter((record) =>
          record.name.includes(searchQuery.value)
        );
      });

      // 上传头像
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

      // 添加记录
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

      // 删除记录
      // const deleteRecord = (id: number) => {
      //   if (confirm('确定删除这条记录吗？')) {
      //     records.value = records.value.filter((record) => record.id !== id);
      //   }
      // };
      const deleteRecord = async (id: number) => {
        if (confirm("确定删除这条记录吗？")) {
          try {
            await apiClient.delete(`/records/${id}`);
            records.value = records.value.filter((record) => record.id !== id); // 前端移除该记录
          } catch (error) {
            console.error("删除记录失败：", error);
            alert(`删除记录失败：${error || "未知错误"}`);
          }
        }
      };

      
      // 搜寻记录
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
      // const editableRecord = ref<Record | null>(null);
      const editableRecord = ref<Record>({
        id: 0,
        name: '',
        age: 0,
        email: '',
        avatar: '',
      });
  
      // const editRecord = (record: Record) => {
      //   editableRecord.value = { ...record };
      //   showEditModal.value = true;
      // };

      const editRecord = async (record: Record) => {
        try {
          const response = await axios.get(`http://localhost:8086/records/${record.id}`);
          editableRecord.value = response.data; // 从后台获取的数据填充到表单
          showEditModal.value = true;
        } catch (error) {
          console.error('获取记录失败:', error);
          alert('无法加载记录数据，请稍后重试。');
        }
      };

  
      const handleEditAvatarUpload = (event: Event) => {
        const file = (event.target as HTMLInputElement).files?.[0];
        if (file && editableRecord.value) {
          const reader = new FileReader();
          reader.onload = (e) => {
            if (editableRecord.value) { // 再次检查非空
                editableRecord.value.avatar = e.target?.result as string;
            }
          };
          reader.readAsDataURL(file);
        }
      };
  
      // 保存编辑后的记录
      const saveEdit = async () => {
        if (editableRecord.value) {
          try {
            const response = await axios.put(
              `http://localhost:8086/records/${editableRecord.value.id}`,
              editableRecord.value
            );
            // 更新本地数据
            const index = records.value.findIndex((r) => r.id === editableRecord.value.id);
            if (index !== -1) {
              records.value[index] = response.data;
            }
            alert('记录已成功保存！');
            closeEdit();
          } catch (error) {
            console.error('编辑记录失败：', error);
            alert('保存失败，请稍后重试！');
          }
        }
      };

  
      const closeEdit = () => {
        // editableRecord.value = null;
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
        isAdding,
        placeholderAvatar,
        showAddForm,
        cancelAdd,
        handleAddRecord,
        toggleSelectAll,
        isAllSelected,
        selectedRecordIds,
        deleteSelected,
  
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
  
  .search-bar{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
  }
  .add-record {
    /* display: flex; */
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
  
  .btn-add, .add-btn {
    background-color: #007bff;
    color: white;
  }
  
  .btn-delete, .delete-btn {
    background-color: #f44336;
    color: white;
  }
  
  .btn-close {
    background-color: #f44336;
    color: white;
  }
  
  .btn-cancel {
    background-color: #f44336;
    color: white;
  }
  
  .btn-details {
    background-color: #2196f3;
    color: white;
  }
  
  .btn-edit {
    background-color: #4caf50;
    color: white;
  }
  
  .btn-save {
    background-color: #4caf50;
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
    width: 260px;
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
  