import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import apiClient from "./plugins/axios";

const app = createApp(App);
app.config.globalProperties.$axios = apiClient;
app.use(router);
app.mount('#app');
