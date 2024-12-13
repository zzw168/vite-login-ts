import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import LoginPage from '../views/LoginPage.vue';
import HomePage from '../views/HomePage.vue';
import UserPage from '../views/UserPage.vue';
import { onMounted } from 'vue';
import BasicFrameWork from '@/views/BasicFrameWork.vue';

onMounted(() => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  if (!isAuthenticated) {
    router.push('/'); // 跳转到登录页面
  }
});


const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'Login',
    component: LoginPage, // 登录页
  },
  {
    path: '/',
    component: BasicFrameWork, // 主页
    meta: { requiresAuth: true }, // 需要登录
    children: [
      {
        path: '/home',
        name: 'Home',
        component: HomePage, // 主页
        meta: { requiresAuth: true, title: '首页'}, // 需要登录
      },
      {
        path: '/user',
        name: 'User',
        component: UserPage,
        meta: { requiresAuth: true, title: '用户设置' }, // 需要登录
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// 路由守卫：检查是否已登录
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

router.afterEach((to, from) => {
    console.log('Navigated to:', to.fullPath);
  });
  

export default router;
