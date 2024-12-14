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
            <div class="header-left">
              <h1>网站标题</h1>
            </div>
            <div class="header-right">
              <div class="lang-switch-wrapper" @mouseleave="hideLanguageMenu">
                <button class="lang-switch" @mouseover="showLanguageMenu">
                    {{ currentLanguage === 'zh' ? '简体中文' : 'English' }}
                </button>
                <ul v-if="isLanguageMenuVisible" class="lang-menu">
                    <li @click="setLanguage('zh')">简体中文</li>
                    <li @click="setLanguage('en')">English</li>
                </ul>
              </div>
              <button class="fullscreen-btn" @click="toggleFullScreen">全屏</button>
              <div class="user-info-wrapper" @mouseleave="hideUserMenu">
                  <div class="user-info" @mouseover="showUserMenu">
                      <img src="/images/1.png" alt="User Avatar" class="avatar" />
                      <span class="user-name">用户名</span>
                  </div>
                  <ul v-if="isUserMenuVisible" class="user-menu">
                      <li @click="goToUserInfo">{{ userRouteTitle }}</li>
                      <li @click="logout">登出</li>
                  </ul>
              </div>
            </div>
          </header>
          <div class="inside-content">
              <section class="content">
                  <router-view />
              </section>
              <aside class="right_side">
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
  import { defineComponent, computed, ref } from 'vue';
  import { useRouter, useRoute } from 'vue-router';

  export default defineComponent({
  name: 'BasicFrameWork',
  setup() {
      const router = useRouter();
      const route = useRoute();

      // 获取具有 `meta.title` 的路由
      const menuRoutes = computed(() =>
      router.options.routes
          .find((route) => route.path === '/') // 获取主框架路由
          ?.children?.filter((child) => child.meta?.title) || []
      );
      // 页眉按钮***************************************************************
      const isLanguageMenuVisible = ref(false);
      const currentLanguage = ref('zh'); // 默认语言为中文

      const showLanguageMenu = () => {
          isLanguageMenuVisible.value = true;
      };

      const hideLanguageMenu = () => {
          isLanguageMenuVisible.value = false;
      };

      const setLanguage = (lang: string) => {
          currentLanguage.value = lang;
          hideLanguageMenu();
      };

      const toggleFullScreen = () => {
          if (!document.fullscreenElement) {
              document.documentElement.requestFullscreen();
          } else if (document.exitFullscreen) {
              document.exitFullscreen();
          }
      };
      // 页眉按钮***************************************************************
      // 用户信息***************************************************************
      const userRouteTitle = computed(() => {
            const userRoute = router.getRoutes().find((r) => r.path === '/user');
            return userRoute?.meta?.title || '用户信息';
        });
      const isUserMenuVisible = ref(false);
      const showUserMenu = () => {
          isUserMenuVisible.value = true;
      };

      const hideUserMenu = () => {
          isUserMenuVisible.value = false;
      };
      
      const goToUserInfo = () => {
            router.push('/user');
        };

      const logout = () => {
        if (confirm('Are you sure you want to logout?')) {
            localStorage.removeItem('isAuthenticated');
            router.push('/login');
        }
      };

      // 用户信息***************************************************************
      return { menuRoutes,
          isLanguageMenuVisible,
          currentLanguage,
          showLanguageMenu,
          hideLanguageMenu,
          setLanguage,
          toggleFullScreen,
          userRouteTitle,
          isUserMenuVisible,
          showUserMenu,
          hideUserMenu,
          goToUserInfo,
          logout,
       };
  },
  });
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
}

/*左侧菜单样式*************************************************** */ 
.sidebar {
  width: 150px;
  background-color: #f4f4f4;
  padding: 1rem;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

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
/************************************************** */
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #3f51b5;
  color: white;
  padding: 1rem;
}

.header-left h1 {
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}
/**用户信息************************************************************* */
.user-info-wrapper {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-size: 1rem;
}

.user-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  list-style: none;
  margin: 0;
  padding: 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.user-menu li {
  padding: 0.5rem 1rem;
  cursor: pointer;
  color: black;
  width: 60px;
  font-size: 14px;
  transition: background-color 0.3s;
}

.user-menu li:hover {
  background-color: #f4f4f4;
}
/**语言信息************************************************************* */
.lang-switch-wrapper {
  position: relative;
}

.lang-switch {
  background-color: #ffffff;
  border: none;
  border-radius: 5px;
  width: 90px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.fullscreen-btn {
  background-color: #ffffff;
  border: none;
  border-radius: 5px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.full {
  background-color: #ffffff;
  border: none;
  border-radius: 5px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.lang-switch:hover {
  background-color: #d3d3d3;
}

.lang-menu {
  position: absolute;
  top: 100%;
  left: 0;
  width: 90px;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  list-style: none;
  margin: 0;
  padding: 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.lang-menu li {
  padding: 0.5rem 1rem;
  cursor: pointer;
  color: black; /* 设置文字为黑色 */
  font-size: 14px; /* 设置文字大小为12px */
  transition: background-color 0.3s;
}

.lang-menu li:hover {
  background-color: #f4f4f4;
}



.content {
  flex: 1;
  padding: 1rem;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.right_side {
  width: 150px;
  padding: 1rem;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}


</style>
