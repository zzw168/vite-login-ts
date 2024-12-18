// src/plugins/axios.ts
import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8086", // 后端服务地址
  timeout: 5000, // 请求超时时间
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;
