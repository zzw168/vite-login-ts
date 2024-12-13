<template>
    <div class="app-container">
      <header class="header">
        <h1>网站标题</h1>
      </header>
      <div class="main-content">
        <aside class="sidebar">
          <ul>
            <li><a href="#">菜单项 1</a></li>
            <li><a href="#">菜单项 2</a></li>
            <li><a href="#">菜单项 3</a></li>
          </ul>
        </aside>
        <section class="content">
          <router-view />
        </section>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  export default {
    name: 'BasicFrameWork',
  };
  </script>
  
  <style scoped>
  .app-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }
  
  .header {
    background-color: #3f51b5;
    color: white;
    padding: 1rem;
    text-align: center;
  }
  
  .main-content {
    display: flex;
    flex: 1;
  }
  
  .sidebar {
    width: 250px;
    background-color: #f4f4f4;
    padding: 1rem;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  }
  
  .content {
    flex: 1;
    padding: 1rem;
  }
  </style>
  