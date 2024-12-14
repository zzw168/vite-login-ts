<template>
    <div class="home-container">
      <h1>Home Page</h1>
      <p>Welcome to the Home Page!</p>
      <button @click="goToUserPage">Go to User Page</button>
      <button @click="logout" class="logout-button">Logout</button>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default defineComponent({
    name: 'HomePage',
    setup() {
      const router = useRouter();
  
      const goToUserPage = () => {
        router.push('/user'); // 跳转到用户页面
      };
  
      const logout = () => {
        if (confirm('Are you sure you want to logout?')) {
            localStorage.removeItem('isAuthenticated');
            router.push('/login');
        }
      };

    return { goToUserPage, logout };
    },
  });
  </script>
  
  <style scoped>
  .home-container {
    max-width: 600px;
    margin: 100px auto;
    text-align: center;
  }
  button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  button:hover {
    background-color: #0056b3;
  }
  /* 登出按钮的特殊样式 */
.logout-button {
  background-color: #ff4d4f;
}
.logout-button:hover {
  background-color: #d9363e;
}
  </style>
  