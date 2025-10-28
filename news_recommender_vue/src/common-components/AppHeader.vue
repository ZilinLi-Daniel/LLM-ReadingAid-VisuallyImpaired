<template>
  <header>
    <!-- 网站标志 -->
    <div class="logo">
      <img src="/assets/news_recommend_logo.png" />
      <div>
        <span class="site-name">{{
          version === "en" ? "EarSphere" : "耳界"
        }}</span>
      </div>
    </div>

    <!-- 导航栏 -->
    <div class="nav">
      <router-link
        to="/"
        tabindex="4"
        @focus="
          speak(
            this.headerVersion === 'en' ? 'HomePage Button' : '主页',
            this.headerVersion === 'en' ? 'Navigation bar' : '导航栏'
          )
        "
        >{{ version === "en" ? "Home" : "主页" }}
      </router-link>
      <router-link
        to="/HomePage"
        tabindex="5"
        @focus="
          speak(
            this.headerVersion === 'en' ? 'News' : '新闻',
            this.headerVersion === 'en' ? 'Navigation bar' : '导航栏'
          )
        "
        >{{ version === "en" ? "News" : "新闻页" }}
      </router-link>
      <img v-if="userLoggedIn" :src="userImage" class="user-image" alt="User" />
      <!-- 控制版本按钮 -->
      <button
        tabindex="5"
        @click="toggleVersion"
        @focus="
          speak(
            headerVersion === 'en' ? 'Control Version' : '版本控制',
            headerVersion === 'en' ? 'Navigation bar' : '导航栏'
          )
        "
      >
        {{ version === "en" ? "中文版" : "English" }}
      </button>
    </div>
  </header>
</template>

<script>
import { store } from "../store/store.js";
export default {
  name: "AppHeader",
  props: {
    userLoggedIn: {
      type: Boolean,
      default: false,
    },
    userImage: {
      type: String,
      default: "",
    },
    isNewsPage: {
      // 添加新 prop 来检查是否在 news_detail 页面中
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      headerVersion: store.version, // 用于语音播报
      version: store.version, // 默认为国内版
    };
  },
  methods: {
    toggleVersion() {
      store.version = this.version === "en" ? "zh" : "en"; // 切换版本
      this.version = store.version;
      this.$emit("update:version", this.version);
      if (this.isNewsPage) {
        this.$router.push("HomePage");
      }
    },
    speak(text, prefix) {
      // clear the previous speech
      window.speechSynthesis.cancel();
      // Combine the additional text with the news item's time if a prefix is provided
      const fullText = prefix ? prefix + " " + text : text;
      // Speak the new text
      const speech = new SpeechSynthesisUtterance(fullText);
      speech.rate = 1.5;
      window.speechSynthesis.speak(speech);
    },
  },
};
</script>

<style scoped>
header {
  position: absolute;
  width: 100%;
  height: 80px;
  top: 0;
  left: 0;
  background-color: rgba(12, 34, 49, 1); /* 半透明背景 */
  justify-content: space-between;
  display: flex;
  align-items: center;
  overflow: hidden;
}

/* 网站标志logo */
.logo {
  width: 150px;
  height: 50px;
  padding-left: 50px;
  padding-top: 15px;
  left: 20px;
  display: flex;
  align-items: center;
}

.logo img {
  width: 65px;
  height: auto;
}

.site-name {
  font-size: 25px;
  font-weight: bold;
  margin-left: 5px;
  margin-top: 5px;
  color: white;
}

/* 导航栏的相关样式 */
.nav {
  display: flex; /* 使用弹性布局 */
  gap: 35px; /* 项目间距 */
  top: 30px;
  right: 8%;
  position: absolute;
}

.nav a {
  font-size: 20px;
  color: white;
  padding: 2px;
  padding-top: 5px;
  text-decoration: none; /* 无下划线 */
  font-weight: bold;
}

/* 你的CSS样式 */
.user-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

button {
  color: white;
  background-color: transparent;
  border: none;
  cursor: pointer;
  font-size: 19px;
  margin-top: 2px;
  margin-right: 10px;
}
</style>
