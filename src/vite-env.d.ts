/// <reference types="vite/client" />


// env.d.ts
import 'vue-router';

declare module 'vue-router' {
  interface RouteMeta {
    title?: string; // 菜单标题
    requiresAuth?: boolean; // 是否需要登录
    icon?: string; // 图标（可选）
  }
}
