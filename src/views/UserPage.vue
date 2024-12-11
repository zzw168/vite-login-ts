<template>
    <div>
      <h1>User Page</h1>
      <p>Welcome to the User Page!</p>
      <button @click="goBack">Back to Home</button>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default defineComponent({
    name: 'UserPage',
    setup() {
      const router = useRouter();
  
      const goBack = () => {
        router.push('/home'); // 返回主页
      };
  
      return { goBack };
    },
  });
  </script>
  
  <style scoped>
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
  </style>
  