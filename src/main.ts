import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import '@arco-design/web-vue/dist/arco.css'; // 引入 Arco 样式

const app = createApp(App);
app.use(router);
app.mount('#app');
