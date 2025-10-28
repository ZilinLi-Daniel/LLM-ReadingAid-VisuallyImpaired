<template>
  <div>
    <AppHeader @update:version="onVersionChange"></AppHeader>
    <!-- 背景图片 -->
    <div class="background"></div>
    <!-- 背景图之上的内容图片 -->
    <div class="container">
      <h1>
        {{
          headerVersion === "en"
            ? "Please select the type of news you areinterested in!"
            : "请选择你感兴趣的新闻种类"
        }}
      </h1>
      <div class="topics">
        <div
          v-for="topic in topics"
          :key="topic.id"
          class="topic"
          @click="toggleSelection(topic.id)"
        >
          <div
            tabindex="0"
            @focus="
              speak(
                topic.name,
                this.headerVersion === 'en'
                  ? 'Preferences page, current options'
                  : '偏好选择页，当前选项'
              )
            "
          >
            <div>
              <img :src="topic.logo" alt="topic.name" class="topic-logo" />
            </div>
            <div
              :class="[
                'selected-indicator',
                isSelected(topic.id) ? 'selected' : '',
              ]"
              tabindex="0"
            >
              <img
                src="/assets/unSelected.png"
                style="width: 20px; height: 20px; top: 5px"
              />
            </div>
          </div>
          <p class="topic-name">{{ topic.name }}</p>
        </div>
      </div>
      <div
        class="nextButton"
        tabindex="0"
        @focus="
          speak(
            '{{topic.name}}',
            this.headerVersion === 'en'
              ? 'Preferences page, current options'
              : '当前页面偏好选择页，当前选项'
          )
        "
      >
        <button @click="confirmSelection">
          {{ headerVersion === "en" ? "Finish Register" : "完成注册" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from "../common-components/AppHeader.vue";
import axios from "axios";
import { store } from "../store/store.js";
export default {
  name: "PerferenceSelected",
  components: {
    AppHeader,
  },
  data() {
    return {
      headerVersion: store.version,
      username: JSON.parse(sessionStorage.getItem("username") || "{}"),
      email: JSON.parse(sessionStorage.getItem("email") || "{}"),
      password: JSON.parse(sessionStorage.getItem("password") || "{}"),
      selectedTopics: [],
    };
  },
  computed: {
    topics() {
      return [
        {
          id: 1,
          name: this.headerVersion === "en" ? "Economy" : "经济",
          logo: "/assets/finance.png",
        },
        {
          id: 2,
          name: this.headerVersion === "en" ? "Real estate" : "房地产",
          logo: "/assets/culture.png",
        },
        {
          id: 3,
          name: this.headerVersion === "en" ? "Military" : "军事",
          logo: "/assets/military.png",
        },
        {
          id: 4,
          name: this.headerVersion === "en" ? "Social" : "社会",
          logo: "/assets/food.png",
        },
        {
          id: 5,
          name: this.headerVersion === "en" ? "Science and Technology" : "科技",
          logo: "/assets/tech.png",
        },
        {
          id: 6,
          name: this.headerVersion === "en" ? "Entertainment" : "娱乐",
          logo: "/assets/entertainment.png",
        },
        {
          id: 7,
          name: this.headerVersion === "en" ? "Internet" : "互联网",
          logo: "/assets/sports.png",
        },
        {
          id: 8,
          name: this.headerVersion === "en" ? "Education" : "教育",
          logo: "/assets/travel.png",
        },
        // Add more topics as needed
      ];
    },
    selectedTopicNames() {
      return this.topics
        .filter((topic) => this.selectedTopics.includes(topic.id))
        .map((topic) => topic.name);
    },
  },
  mounted() {
    // 页面加载时，清空sessionStorage
    window.addEventListener("keyup", this.handleKeyPress);
  },
  beforeMount() {
    // 页面卸载时，清空sessionStorage
    window.removeEventListener("keyup", this.handleKeyPress);
  },
  methods: {
    toggleSelection(id) {
      const index = this.selectedTopics.indexOf(id);
      if (index > -1) {
        this.selectedTopics.splice(index, 1);
      } else {
        this.selectedTopics.push(id);
      }
    },
    isSelected(id) {
      return this.selectedTopics.includes(id);
    },
    onVersionChange(newVersion) {
      this.headerVersion = newVersion;
    },
    async confirmSelection() {
      console.log(this.email);
      console.log(this.password);
      const apiUrl = process.env.VUE_APP_API_URL;
      const response = await axios.post(`${apiUrl}/api/user_regist`, {
        username: this.username, // 发送用户名
        email: this.email, // 发送电子邮箱
        password: this.password, // 发送密码
        preferences: this.selectedTopicNames,
        lang: this.headerVersion,
      });
      // 处理注册成功，可能是显示一个成功消息
      if (response.data.message === "True") {
        this.$router.push("/login");
      } else {
        alert(response.data.message);
      }
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
      } else if (event.key === "Escape") {
        this.$router.go(-1);
      }
    },
  },
};
</script>

<style scoped>
/* 全局样式调整 */
body {
  font-family: "Roboto", sans-serif; /* 举例，可以选择其他字体 */
  background-color: #f8f9fa;
  color: #333;
}
.background {
  position: fixed; /* 或absolute，取决于你的布局需求 */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("../assets/preference_back.png");
  background-size: cover;
  background-position: center;
  filter: blur(1px);
  z-index: -2; /* 确保背景位于内容下方 */
}
.container {
  position: relative;
  z-index: 1;
}

h1 {
  color: white; /* 白色字体 */
  text-align: center;
  position: relative; /* 确保它位于背景之上 */
  margin-top: 140px;
  z-index: 1;
}

p {
  color: #6c757d;
}

/*主题卡片整体布局 */
.topics {
  display: grid;
  grid-template-columns: repeat(4, 10fr); /* 创建四列 */
  grid-gap: 20px; /* 卡片之间的间距 */
  padding: 20px;
  position: relative; /* 确保它位于背景之上 */
  z-index: 1;
}

/* 主题卡片样式 */
.topic {
  position: relative;
  cursor: pointer;
  padding: 10px;
  width: 300px;
  height: 180px;
  border: 1px solid #dee2e6;
  border-radius: 10px; /* 添加圆角 */
  margin: 10px;
  display: inline-block;
  background-color: rgb(253, 222, 187);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  transition: all 0.3s ease; /* 过渡效果 */
  display: flex;
  flex-direction: column;
  align-items: center;
}

.topic-logo {
  width: 300px; /* 或根据需要调整宽度，保证图像适应卡片 */
  height: 150px; /* 自动调整高度以保持图像比例 */
  object-fit: contain; /* 保证图像完整显示在分配的空间内 */
  margin: 5 auto; /* 居中图像 */
}

.topic img {
  z-index: -1;
  margin: -20px, 50px;
}

.topic:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); /* 鼠标悬停时增加阴影 */
}

.selected-indicator {
  position: absolute; /* 绝对定位 */
  bottom: 2px; /* 距离卡片底部10px */
  left: 50%; /* 居中定位 */
  transform: translateX(-50%); /* 精确居中调整 */
  width: 20px;
  height: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.nextButton {
  display: flex;
  margin: 0, center;
  justify-content: center;
  align-items: center;
}

/* 按钮样式 */
button {
  background-color: #007bff;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin: 20px, auto;
  position: relative; /* 确保它位于背景之上 */
  z-index: 1;
}

button:hover {
  background-color: #0056b3;
}
.selected img {
  content: url("../assets/selected.png"); /* 使用你的选中图片路径 */
}
.topic-name {
  text-align: center;
  font-size: 15px;
  color: black;
  font-weight: bold;
}
</style>
