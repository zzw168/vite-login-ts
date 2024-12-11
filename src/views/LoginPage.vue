<template>
    <div class="login-page">
        <!-- 广告区域 -->
        <div class="login-ad">
        
        <!-- 左侧箭头按钮 -->
        <button class="arrow-button left" @click="previousImage">
            <img src="/images/8.png" alt="Left Arrow" />
        </button>
        <img :src="images[currentImageIndex]" alt="Advertisement" />
        <!-- 右侧箭头按钮 -->
        <button class="arrow-button right" @click="nextImage">
            <img src="/images/10.png" alt="Right Arrow" />
        </button>
        </div>
        <!-- <LoginBanner /> -->
      <!-- 右侧登录表单 -->
      <div class="login-container">
        <h1>Login</h1>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="username">Username:</label>
            <input
              id="username"
              type="text"
              v-model="username"
              placeholder="Enter your username"
              required
            />
          </div>
          <div class="form-group">
            <label for="password">Password:</label>
            <input
              id="password"
              type="password"
              v-model="password"
              placeholder="Enter your password"
              required
            />
          </div>
          <button type="submit">Login</button>
        </form>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </div>
    </div>
  </template>
  

  <script lang="ts">
  import { defineComponent, ref, onMounted, onUnmounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default defineComponent({
    name: 'LoginPage',
    setup() {
      const username = ref('');
      const password = ref('');
      const errorMessage = ref('');
      const router = useRouter();
  
      // 图片数组
      const images = ref([
        '/images/1.png',
        '/images/2.png',
        '/images/3.png',
      ]);
  
      // 当前显示的图片索引
      const currentImageIndex = ref(0);
  
      // 自动轮播定时器
      let intervalId: number | null = null;
  
      // 切换到下一个图片
      const nextImage = () => {
        currentImageIndex.value =
          (currentImageIndex.value + 1) % images.value.length;
      };
  
      // 切换到上一个图片
      const previousImage = () => {
        currentImageIndex.value =
          (currentImageIndex.value - 1 + images.value.length) %
          images.value.length;
      };
  
      // 自动轮播
      const startAutoSlide = () => {
        intervalId = setInterval(nextImage, 2000); // 每两秒切换到下一张图片
      };
  
      // 停止自动轮播
      const stopAutoSlide = () => {
        if (intervalId) {
          clearInterval(intervalId);
          intervalId = null;
        }
      };
  
      // 组件挂载时启动自动轮播
      onMounted(() => {
        startAutoSlide();
      });
  
      // 组件销毁时清除定时器
      onUnmounted(() => {
        stopAutoSlide();
      });
  
      // 登录逻辑
      const handleLogin = () => {
        if (username.value === 'admin' && password.value === '1234') {
          localStorage.setItem('isAuthenticated', 'true');
          router.push('/home');
        } else {
          errorMessage.value = 'Invalid username or password.';
        }
      };
  
      return {
        username,
        password,
        errorMessage,
        images,
        currentImageIndex,
        nextImage,
        previousImage,
        handleLogin,
      };
    },
  });
  </script>
  
  

<style scoped>
.login-page {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: stretch; /* 让子元素填满容器，等高对齐 */
  height: 100vh; /* 页面高度占满视口 */
  background-color: #f9f9f9;
}

.login-ad {
  flex: 0.3; /* 使广告区域占满剩余空间 */
  margin-top: 10%;
  background: linear-gradient(to bottom, rgba(32, 63, 148, 0.5), rgba(31, 7, 77, 0.7)), url('/path-to-your-image.jpg');
  background-size: cover; /* 背景图片覆盖整个区域 */
  background-position: center;
  display: flex;
  align-items: center; /* 图片垂直居中 */
  justify-content: center; /* 图片水平居中 */
  height: 60%; /* 高度填满父容器 */
}

.login-ad img {
  max-width: 20%; /* 图片最大宽度为广告区域的 80% */
  height: auto; /* 保持图片比例 */
  border-radius: 8px;
}

/* 箭头按钮样式 */
.arrow-button {
  position:static;
  top: 50%;
  width: 100px;
  transform: translateY(-45%);
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0; /* 不设置内边距 */
  z-index: 1; /* 确保按钮在图片之上 */
}

/* 禁用鼠标悬停时的按钮样式 */
.arrow-button:hover,
.arrow-button:focus,
.arrow-button:active {
  background: none; /* 鼠标悬停时仍然无背景 */
  border: none; /* 无边框 */
  outline: none; /* 移除聚焦时的轮廓 */
}

.arrow-button:hover img {
  transform: scale(1.3); /* 鼠标悬停时图标放大 10% */
  transition: transform 0.2s ease; /* 添加过渡效果 */
}

.arrow-button img {
  width: 100%; /* 设置箭头图标的大小 */
  height: 100%; /* 设置箭头图标的高度 */
}

.left {
  left: 10px; /* 左侧箭头 */
}

.right {
  right: 10px; /* 右侧箭头 */
}

.login-container {
  flex: 0.3; /* 使登录表单区域占满剩余空间 */
  margin-top: 10%;
  max-width: 400px; /* 控制登录表单宽度 */
  background: white;
  border: 1px solid #ccc;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  height: 60%; /* 高度填满父容器 */
}

h1 {
  margin-top: 80px;
  margin-bottom: 30px;
}

.form-group {
  margin-top: 20px;
  margin-bottom: 15px;
  text-align: center;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 50%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 55%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.error {
  margin-top: 10px;
  color: red;
}
</style>


