<template>
    <div class="app-container">
        <aside class="sidebar">
            <ul>
                <li v-for="route in menuRoutes" :key="route.path">
                    <router-link :to="route.path">{{ route.meta.title || route.name }}</router-link>
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
        name: 'BasicFrameWork',
        setup() {
            const router = useRouter();

            // 筛选所有具有 meta 信息的子路由
            const menuRoutes = computed(() =>
            router.options.routes
                .find((route) => route.path === '/') // 找到框架的父路由
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
</style>
  