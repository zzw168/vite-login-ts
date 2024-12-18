<template>
  <div class="user-profile">
    <h2 class="title">{{ userTitle }}</h2>
    <div class="tabs">
      <button
        :class="{ active: activeTab === 'view' }"
        @click="activeTab = 'view'"
      >
        查看资料
      </button>
      <button
        :class="{ active: activeTab === 'edit' }"
        @click="activeTab = 'edit'"
      >
        编辑资料
      </button>
    </div>
    <div v-if="activeTab === 'view'" class="user-details">
      <img :src="user.avatar" alt="User Avatar" class="user-avatar" />
      <div class="user-info">
        <p><strong>用户名：</strong>{{ user.name }}</p>
        <p><strong>邮箱：</strong>{{ user.email }}</p>
        <p><strong>手机号：</strong>{{ user.phone }}</p>
      </div>
    </div>
    <div v-if="activeTab === 'edit'" class="edit-section">
      <h3>编辑资料</h3>
      <form @submit.prevent="saveChanges">
        <div class="form-group">
          <div v-if="editableUser.avatarPreview" class="avatar-preview">
            <img :src="editableUser.avatarPreview" alt="Avatar Preview" class="user-avatar" />
          </div>
          <input
            id="avatar"
            type="file"
            @change="handleAvatarUpload"
            accept="image/*"
          />
        </div>
        <div class="form-group">
          <label for="name">用户名</label>
          <input id="name" v-model="editableUser.name" type="text" />
        </div>
        <div class="form-group">
          <label for="email">邮箱</label>
          <input id="email" v-model="editableUser.email" type="email" />
        </div>
        <div class="form-group">
          <label for="phone">手机号</label>
          <input id="phone" v-model="editableUser.phone" type="text" />
        </div>
        <button type="submit" class="save-btn">保存修改</button>
      </form>
    </div>
    <div class="actions">
      <button class="back-btn" @click="goBack">返回上一页</button>
      <button class="logout-btn" @click="logout">退出登录</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

interface User {
  name: string;
  email: string;
  phone: string;
  avatar: string;
}

interface EditableUser extends Omit<User, 'avatar'> {
  avatarPreview: string | null;
}

export default defineComponent({
  name: 'UserProfile',
  setup() {
    const router = useRouter();
    const route = useRoute();

    const user = ref<User>({
      avatar: '/images/1.png', // 替换为实际的头像路径
      name: '示例用户',
      email: 'user@example.com',
      phone: '123-456-7890',
    });

    // const editableUser = ref({ ...user.value });
    // 可编辑的用户数据
    const editableUser = ref<EditableUser>({
      name: user.value.name,
      email: user.value.email,
      phone: user.value.phone,
      avatarPreview: user.value.avatar,
    });

    const userTitle = computed(() => {
      return route.meta?.title || '个人中心';
    });

    const activeTab = ref<'view' | 'edit'>('view');

    // 处理头像上传
    const handleAvatarUpload = (event: Event): void => {
      const input = event.target as HTMLInputElement;
      const file = input.files?.[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          editableUser.value.avatarPreview = e.target?.result as string;
        };
        reader.readAsDataURL(file);
      }
    };

    const saveChanges = (): void => {
      user.value = {
        ...user.value,
        name: editableUser.value.name,
        email: editableUser.value.email,
        phone: editableUser.value.phone,
        avatar: editableUser.value.avatarPreview || user.value.avatar,
      };
      activeTab.value = 'view'; // 切换回查看页面
      alert('资料已更新！');
    };

    const logout = () => {
      if (confirm('Are you sure you want to logout?')) {
            localStorage.removeItem('isAuthenticated');
            router.push('/login');
        }
    };

    const goBack = () => {
      router.back();
    };

    return {
      user,
      editableUser,
      userTitle,
      activeTab,
      handleAvatarUpload,
      saveChanges,
      logout,
      goBack,
    };
  },
});
</script>

<style scoped>
.user-profile {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.title {
  margin-bottom: 1.5rem;
  text-align: center;
  font-size: 1.5rem;
  color: #333;
}

.tabs {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.tabs button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #f1f1f1;
  color: #333;
  transition: background-color 0.3s;
}

.tabs button.active {
  background-color: #4caf50;
  color: white;
}

.tabs button:hover {
  background-color: #ddd;
}

.user-details {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

.user-info p {
  margin: 0.5rem 0;
  font-size: 1rem;
  color: #555;
}

.edit-section {
  flex: 1;
}

.edit-section h3 {
  margin-bottom: 1rem;
  font-size: 1.25rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.save-btn {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #4caf50;
  color: white;
  transition: background-color 0.3s;
}

.save-btn:hover {
  background-color: #45a049;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.back-btn, .logout-btn {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-btn {
  background-color: #2196f3;
  color: white;
}

.back-btn:hover {
  background-color: #1976d2;
}

.logout-btn {
  background-color: #f44336;
  color: white;
}

.logout-btn:hover {
  background-color: #e53935;
}
</style>
