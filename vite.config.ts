import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // 允许通过 IP 访问
    port: 8080, // 自定义端口（可选）
    strictPort: true, // 如果端口被占用则抛出错误
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
});
