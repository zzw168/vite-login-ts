<template>
    <div class="app-container">
        <aside class="sidebar">
            <ul>
                <li v-for="route in menuRoutes" :key="route.path"
                :class="{ active: route.path === $route.path }">
                    <router-link :to="route.path" class="menu-item">
                        {{ route.meta.title || route.name }}
                    </router-link>
                </li>
            </ul>
        </aside>
        <div class="main-content">
            
            <header class="header">
                <h1>网站标题</h1>
            </header>
            <div class="inside-content">
                <section class="content">
                    <router-view />
                </section>
                <aside class="left_side">
                    <ul>
                    <li><a href="#">菜单项 1</a></li>
                    <li><a href="#">菜单项 2</a></li>
                    <li><a href="#">菜单项 3</a></li>
                    </ul>
                </aside>
            </div>
        </div>
    </div>
</template>
  
<script lang="ts">
    import { defineComponent, computed } from 'vue';
    import { useRouter } from 'vue-router';

    export default defineComponent({
    name: 'MainLayout',
    setup() {
        const router = useRouter();

        // 获取具有 `meta.title` 的路由
        const menuRoutes = computed(() =>
        router.options.routes
            .find((route) => route.path === '/') // 获取主框架路由
            ?.children?.filter((child) => child.meta?.title) || []
        );

        return { menuRoutes };
    },
    });
</script>
  
<style scoped>
  .app-container {
    display: flex;
    height: 100vh;
  }
    
  .sidebar {
    width: 150px;
    background-color: #f4f4f4;
    padding: 1rem;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  }
 
  .main-content {
    display: flex;
    flex-direction: column;
    flex: 1;
  }
   
  .inside-content {
    display: flex;
    flex: 1;
  }

  .header {
    background-color: #3f51b5;
    color: white;
    padding: 1rem;
    text-align: center;
  } 

  .content {
    flex: 1;
    padding: 1rem;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  }

  .left_side {
    width: 150px;
    padding: 1rem;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  }

  /* 左侧菜单样式 */
.sidebar {
  width: 250px;
  background-color: #f4f4f4;
  padding: 1rem;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar ul {
  list-style: none; /* 去掉列表前的点 */
  padding: 0; /* 去掉默认内边距 */
  margin: 0; /* 去掉默认外边距 */
}

.sidebar li {
  margin: 0.5rem 0;
}

.sidebar li.active .menu-item {
  background-color: #3f51b5;
  color: white;
  border-radius: 8px;
}

  /* 按钮样式 */
.menu-item {
  display: block;
  padding: 0.8rem 1rem;
  color: #333;
  text-decoration: none;
  border-radius: 5px;
  transition: all 0.3s ease;
}

/* 悬停效果 */
.menu-item:hover {
  background-color: #3f51b5;
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}

/* 点击效果 */
.menu-item:active {
  transform: scale(0.98);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* 动画效果 */
.menu-item {
  position: relative;
  overflow: hidden;
}

.menu-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.3);
  transform: skewX(-30deg);
  transition: 0.5s;
}

.menu-item:hover::before {
  left: 100%;
}
</style>
  