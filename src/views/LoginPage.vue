<template>
  <div class="page-container">
    <div class="image-slider-container">
      <!-- 广告区域 -->
      <div class="login-ad">
        <!-- 左侧箭头按钮 -->
        <button class="arrow-button left" @click="previousImage">
            <img src="/images/5.png" alt="Left Arrow" />
        </button>
        <img :src="images[currentImageIndex]" alt="Advertisement" />
        <!-- 右侧箭头按钮 -->
        <button class="arrow-button right" @click="nextImage">
            <img src="/images/6.png" alt="Right Arrow" />
        </button>
      </div>
      <!-- 底部进度条 -->
      <div class="progress-indicator">
        <div
          v-for="(image, index) in images"
          :key="index"
          class="progress-bar"
          :class="{ active: index === currentImageIndex }"
        >
          <div
            class="progress"
            :style="{ width: index === currentImageIndex ? progressWidth + '%' : '0%' }"
          ></div>
        </div>
      </div>
    </div>
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
    // 进度条宽度
    const progressWidth = ref(0);

    // 自动轮播定时器
    let intervalId: number | null = null;
    let progressIntervalId: number | null = null;

    // 切换到下一个图片
    const nextImage = () => {
      currentImageIndex.value =
        (currentImageIndex.value + 1) % images.value.length;
      resetProgress();
    };

    // 切换到上一个图片
    const previousImage = () => {
      currentImageIndex.value =
        (currentImageIndex.value - 1 + images.value.length) %
        images.value.length;
      resetProgress();
    };

    // 自动轮播
    const startAutoSlide = () => {
      intervalId = setInterval(nextImage, 2000); // 每两秒切换到下一张图片
      startProgress(); // 开始进度条
    };

    // 停止自动轮播
    const stopAutoSlide = () => {
      if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
      }
      stopProgress(); // 停止进度条
    };

    // 进度条逻辑
    const startProgress = () => {
      progressWidth.value = 0;
      progressIntervalId = setInterval(() => {
        if (progressWidth.value < 100) {
          progressWidth.value += 5; // 每次增加 5%
        } else {
          progressWidth.value = 100;
        }
      }, 100); // 每 100 毫秒更新一次
    };

    const stopProgress = () => {
      if (progressIntervalId) {
        clearInterval(progressIntervalId);
        progressIntervalId = null;
      }
    };

    const resetProgress = () => {
      stopProgress();
      progressWidth.value = 0;
      startProgress();
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
      progressWidth,
      nextImage,
      previousImage,
      handleLogin,
    };
  },
});
</script>



<style scoped>
/* 页面整体容器 */
.page-container {
  display: flex; /* 使用 Flexbox 实现左右布局 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  min-height: 100vh; /* 占满视口高度 */
  background-color: #f9f9f9;
}

/* 整体容器样式 */
.image-slider-container {
  flex: 1;
  display:flex;
  flex-direction: column; /* 垂直排列：图片在上，进度条在下 */
  align-items: center;
  max-width: 400px; /* 控制登录表单宽度 */
  width: 100%;
  height: 500px; /* 高度填满父容器 */
  background: linear-gradient(to bottom, rgba(32, 63, 148, 0.5), rgba(31, 7, 77, 0.7)), url('/images/10.png');
  background-size: cover; /* 背景图片覆盖整个区域 */
  background-position: center;
  border: 1px solid #ccc;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.login-ad {
position: relative; /* 设置为相对定位，为子元素提供定位上下文 */
flex: 1; /* 使广告区域占满剩余空间 */
display: flex;
align-items: center; /* 图片垂直居中 */
justify-content: center; /* 图片水平居中 */
height: 100%; /* 高度填满父容器 */
}

.login-ad img {
max-width: 50%; /* 图片最大宽度为广告区域的 80% */
height: auto; /* 保持图片比例 */
border-radius: 8px;
}

/* 进度条容器 */
.progress-indicator {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 500px; /* 与广告图片宽度保持一致 */
  margin-top: 10px; /* 与图片之间添加间距 */
  gap: 5px; /* 每个小进度条之间的间距 */
}

/* 单个进度条 */
.progress-bar {
  width: 30px;
  height: 5px;
  background-color: #ddd;
  border-radius: 2px;
  overflow: hidden;
  position: relative;
}

.progress-bar.active {
  background-color: transparent;
}

.progress-bar .progress {
  height: 100%;
  background-color: #007bff;
  transition: width 0.1s linear;
  border-radius: 2px;
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
  flex: 1; /* 使登录表单区域占满剩余空间 */
  max-width: 400px; /* 控制登录表单宽度 */
  height: 500px; /* 高度填满父容器 */
  background: white;
  border: 1px solid #ccc;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
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

