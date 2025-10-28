part_1
<template>
  <!-- 网页头部 -->
  <AppHeader @update:version="onVersionChange"></AppHeader>
  <!-- 给予按键控制的说明  -->
  <div v-if="showPopup" class="popup-mask">
    <div class="popup-box">
      <!-- Popup content -->
      <div class="popup-content">
        <p>
          {{
            headerVersion == "en"
              ? "Welcome to the Earsphere Blind News Recommender"
              : "欢迎来到耳界盲人新闻推荐系统"
          }}
        </p>
        <p>
          {{
            headerVersion == "en"
              ? "Use the Tab key to toggle elements for positioning"
              : "使用Tab键切换元素进行定位"
          }}
        </p>
        <p>
          {{
            headerVersion == "en"
              ? "Use the Enter key to jump to the next page"
              : "使用Enter键跳转到下一页"
          }}
        </p>
        <p>
          {{
            headerVersion == "en"
              ? "Use the ESC key to jump to the previous page"
              : "使用ESC键跳转到上一页"
          }}
        </p>
        <p>
          {{
            headerVersion == "en"
              ? "Use the Q key to pause and play news reading"
              : "使用Q键进行暂停和播放新闻阅读"
          }}
        </p>
      </div>
    </div>
  </div>

  <!-- 背景图表示 -->
  <div class="background-style">
    <img src="/assets/news_recommend_back.png" />
    <div class="background-space"></div>
  </div>

  <!-- 注册和登录按钮 -->
  <div class="auth-buttons">
    <div class="auth-buttons">
      <router-link
        to="/login"
        class="login-button"
        tabindex="0"
        @focus="
          speak(
            headerVersion == 'en' ? 'Login button:' : '登录按钮',
            headerVersion == 'en' ? 'Home page:' : '首页'
          )
        "
        >{{ headerVersion === "en" ? "Login" : "登录" }}</router-link
      >
      <router-link
        to="/register"
        class="register-button"
        tabindex="0"
        @focus="
          speak(
            headerVersion == 'en' ? 'Register button:' : '注册按钮',
            headerVersion == 'en' ? 'Home page:' : '首页'
          )
        "
        >{{ headerVersion === "en" ? "Register" : "注册" }}</router-link
      >
    </div>
  </div>
</template>

<script>
import { store } from "../store/store.js";
import AppHeader from "../common-components/AppHeader.vue";

export default {
  name: "IndexPage",
  components: {
    AppHeader,
  },

  mounted() {
    //清除localstorage中的所有内容
    localStorage.clear();
    this.speak(
      this.headerVersion == "en"
        ? "Welcome to EarSphere's news recommendation system for the blind. Use the Tab key to toggle elements for positioning, the Enter key to jump to the next page, the ESC key to jump to the previous page, and the Q key to pause and play the news reader."
        : "欢迎来到EarSphere盲人新闻推荐系统，使用Tab键切换元素进行定位，使用Enter键跳转到下一页，使用ESC键跳转到上一页，使用Q键进行暂停和播放新闻阅读",
      ""
    );
    setTimeout(() => {
      this.showPopup = false;
    }, 5000);
  },
  data() {
    return {
      headerVersion: store.version,
      showPopup: true,
    };
  },
  methods: {
    mounted() {
      // 页面加载时，添加sessionStorage
      window.addEventListener("keyup", this.handleKeyPress);
    },
    beforeMount() {
      // 页面卸载时，清空sessionStorage
      window.removeEventListener("keyup", this.handleKeyPress);
    },
    onVersionChange(newVersion) {
      this.headerVersion = newVersion;
    },
    speak(text, prefix) {
      // Clear the previous speech
      window.speechSynthesis.cancel();
      // Combine the additional text with the news item's time if a prefix is provided
      const fullText = prefix ? prefix + " " + text : text;
      // Speak the new text
      const speech = new SpeechSynthesisUtterance(fullText);
      speech.rate = 1.5;
      window.speechSynthesis.speak(speech);
    },
    handleKeyPress(event) {
      // Check if Ctrl + Q is pressed
      if (event.key === "q") {
        //  change the value about the hovering,Invert the hovering
        if (!this.hovering) {
          window.speechSynthesis.pause();
        } else {
          window.speechSynthesis.resume();
        }
        this.hovering = !this.hovering;
      }
    },
  },
};
</script>
<style scoped>
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

.background-style {
  position: relative;
  width: 100%;
  height: auto;
  top: 70px;
  left: 180px;
  display: flex;
  z-index: -1;
  display: block;
  margin: 0, auto;
}

.background-style img {
  width: 70%; /* 使图片宽度等于容器宽度 */
  height: auto; /* 保持图片的原始宽高比 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.background-space {
  background-color: linear-gradient(
    to right,
    red,
    blue
  ); /* 使用渐变颜色填充空白 */
  width: 100%; /* 调整空白宽度为图片宽度的百分之三十 */
  height: 100%; /* 充满整个父容器的高度 */
  z-index: -1;
}

/* 登录和注册按钮的容器样式 */
.auth-buttons {
  position: absolute;
  width: 100%;
  display: flex;
  justify-content: center;
  gap: 20px; /* 按钮间距 */
  top: calc(100% - 25px); /* 根据需要调整此值以放在背景图之上 */
  z-index: 1;
}

/* 登录按钮样式 */
.login-button {
  padding: 10px 30px;
  font-size: 20px;
  font-weight: bold;
  color: white; /* 字体颜色 */
  background-color: #007bff; /* 按钮背景颜色 */
  border: none; /* 无边框 */
  cursor: pointer; /* 鼠标悬停时的光标形状 */
  border-radius: 5px; /* 按钮边缘圆角 */
  text-decoration: none; /* 无下划线 */
}

/* 注册按钮样式 */
.register-button {
  padding: 10px 30px;
  font-size: 20px;
  font-weight: bold;
  color: #007bff; /* 字体颜色 */
  background-color: white; /* 按钮背景颜色 */
  border: 2px solid #007bff; /* 边框颜色 */
  cursor: pointer; /* 鼠标悬停时的光标形状 */
  border-radius: 5px; /* 按钮边缘圆角 */
  text-decoration: none; /* 无下划线 */
}

/* 调整按钮的交互效果 */
.login-button:hover,
.register-button:hover {
  opacity: 0.9; /* 悬停时的透明度变化 */
}

/* 弹出的窗口样式 */
.popup-mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Transparent black */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999; /* Set a high z-index value */
}

.popup-box {
  background-color: rgb(91, 167, 214);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000; /* Make sure the popup box appears above the mask */
}
</style>
