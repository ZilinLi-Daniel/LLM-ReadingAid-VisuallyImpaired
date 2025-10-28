speak
<template>
  <AppHeader @update:version="onVersionChange"></AppHeader>
  <div class="home-page">
    <div class="left-part">
      <div class="news-list" id="news-list">
        <div
          v-for="newsItem in display_news_list"
          :key="newsItem.newsId"
          class="news-container"
        >
          <h3>
            <!-- news title -->
            <a
              href="#"
              @click="viewNewsDetail(newsItem.newsId)"
              class="news-header"
              @focus="
                speak(
                  newsItem.title,
                  headerVersion === 'en' ? 'News Title' : '当前新闻标题：'
                )
              "
              >{{ newsItem.title }}</a
            >
          </h3>
          <!-- news published time -->
          <small
            class="time"
            tabindex="0"
            @focus="
              speak(
                headerVersion === 'en' ? format(newsItem.time) : newsItem.time,
                headerVersion === 'en' ? 'Published Time' : '发布时间:'
              )
            "
          >
            {{ newsItem.time }}</small
          >
          <!-- new abstract -->
          <p
            class="news-content"
            tabindex="0"
            @focus="
              speak(
                newsItem.abstract,
                headerVersion === 'en' ? 'News Abstract' : '当前新闻摘要：'
              )
            "
            @mouseenter="hovering = true"
            @mouseleave="hovering = false"
          >
            {{ newsItem.abstract }}
          </p>
        </div>
      </div>
      <div class="changed-category">
        <!-- <p>根据您的浏览偏好，我们为您推荐了以下新闻类别：</p> -->
        <p>
          {{
            headerVersion === "en"
              ? "The data on the current page is presented for academic research only, and the news content of the page is no longer updated in real time."
              : ""
          }}
        </p>
        <div
          class="category-item"
          v-for="category in user_preference"
          :key="category.id"
        >
          <p>{{ category.name }}</p>
        </div>
      </div>
    </div>

    <!-- 推荐的新闻标题 -->
    <div class="right-part">
      <!-- 推荐新闻标题按钮 -->
      <button
        @click="getRecommendNewsList"
        @focus="
          speak(
            headerVersion === 'en'
              ? 'Get Recommended News List Button'
              : '获取推荐新闻按钮',
            headerVersion === 'en' ? 'Home Page:' : '首页:'
          )
        "
        class="recommend-news-list-button"
      >
        {{
          headerVersion === "en"
            ? "Get Recommended News List"
            : "获取推荐新闻列表"
        }}
      </button>

      <div v-if="loading" class="loading-animation">
        <!-- 这里放置 loading 动画的 HTML 代码 -->
        <img src="../assets/loading.gif" alt="Loading..." />
      </div>

      <div class="recommended-news-list">
        <div
          class="recommended-news-item"
          v-for="(newsItem, index) in recommend_news_list"
          :key="index"
        >
          <div class="recommend-news-title">
            <a
              href="#"
              @click="viewNewsDetail(newsItem.newsId)"
              class="recommend-news-header"
              @focus="
                speak(
                  newsItem.title,
                  headerVersion === 'en'
                    ? 'Recommended News Title'
                    : '当前推荐新闻标题：'
                )
              "
              >{{ index + 1 }}.{{ newsItem.title }}</a
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from "../common-components/AppHeader.vue";
import { store } from "../store/store.js";
import axios from "axios";
import { format, parseISO } from "date-fns";
export default {
  name: "HomePage",
  components: {
    AppHeader,
  },
  mounted() {
    window.addEventListener("keyup", this.handleKeyPress);
  },
  beforeUnmount() {
    window.removeEventListener("keyup", this.handleKeyPress);
  },
  data() {
    return {
      headerVersion: store.version,
      // 从sessionStorage中获取用户的浏览偏好
      userId: JSON.parse(sessionStorage.getItem("userId") || "{}"),
      display_news_list: [],
      recommend_news_list: [],
      hovering: false, // Initialize hovering state
      loading: false,
    };
  },
  created() {
    // 从sessionStorage中获取用户的浏览偏好
    // 根据用户的浏览偏好，获取推荐的新闻列表
    this.getCategoryNewsList();
  },
  methods: {

    async getCategoryNewsList() {
      try {
        // 根据用户的浏览偏好，获取新闻种类信息
        const apiUrl = process.env.VUE_APP_API_URL
        const response = await axios.get(`${apiUrl}/api/category_news_list`, {
          params: {
            lang: this.headerVersion,
            user_id: this.userId,
          },
        });
        this.display_news_list = response.data.display_news_list;
      } catch (error) {
        console.log(error);
      }
      console.log(this.display_news_list);
    },

    //format the date
    format(dateString) {
      const date = parseISO(dateString);
      return format(date, "iiii, MMMM d, yyyy"); // 'Sunday, March 31, 2024'
    },
    async getRecommendNewsList() {
      this.loading = true;
      try {
        // 获取推荐的新闻列表
        const apiUrl = process.env.VUE_APP_API_URL
        const response = await axios.get(`${apiUrl}/api/recommend_news_list`, {
          params: {
            lang: this.headerVersion,
            user_id: this.userId,
          },
        });
        this.recommend_news_list = response.data.news_recommend_list;
      } catch (error) {
        console.log(error);
      } finally {
        this.loading = false;
      }
      console.log(this.recommend_news_list);
    },
    async viewNewsDetail(news_id) {
      sessionStorage.setItem("viewNewsId", JSON.stringify(news_id));
      try {
        this.$router.push({
          name: "NewsDetailPage",
        });
      } catch (error) {
        console.error("Error fetching news detail:", error);
      }
    },
    onVersionChange(newVersion) {
      this.headerVersion = newVersion;
      this.getCategoryNewsList();
      this.recommend_news_list = [];
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
    // Handle key press events:when press ctrl + q, stop reading
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
    stopReading() {
      // Stop the speech synthesis
      window.speechSynthesis.cancel();
    },
  },
};
</script>

<style scoped>
body {
  font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
  color: #333;
  line-height: 1.6;
  background-color: #f5f5f5;
}

h1,
h2,
h4,
h5,
h6 {
  font-family: "SimHei", "黑体", sans-serif;
  font-weight: normal;
  color: red;
}

.news-content,
.category-item p {
  font-family: "SimSun", "宋体", serif;
  font-size: 16px;
  color: red;
  line-height: 1.8;
}

/* Modern and clean font for UI elements */
.ui-element {
  font-family: "PingFang SC", "苹方-简", sans-serif;
  font-size: 12px;
  color: #666;
}

/* Alternative font for non-Chinese text and fallback */
.non-chinese-text {
  font-family: "Source Han Sans", "思源黑体", Arial, sans-serif;
}

/* 页面的基本设置 */
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

html,
body {
  background-color: rgba(233, 233, 233, 0.545);
  display: flex;
  justify-content: center;
  height: 100vh;
  align-items: center;
  font-family: "Arial", sans-serif;
  background-size: cover;
}
/* 总页面 */
.home-page {
  display: flex;
  width: 99%;
  height: 100%;
  display: flex;
  position: absolute;
  top: 50px;
}

/* 左右栏目通用的样式 */
.left-part,
.right-part {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 100px;
  padding-left: 30px;
  display: flex;
  position: relative;
}

.left-part {
  width: 70%;
}

.right-part {
  width: 30%;
}

.news-list,
.recommended-news-list {
  width: 100%;
  overflow-y: auto;
}

.news-container {
  background-color: rgba(184, 236, 245, 0.335);
  padding: 10px 15px;
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.news-header {
  margin: 5px;
}

.news-header a {
  font-weight: bold;
  font-size: 1.5em;
  color: red;
  transition: color 0.3s ease;
  margin: 10px;
}
.news-header h3 {
  font-weight: bold;
  font-size: 1.5em;
  color: red;
  transition: color 0.3s ease;
  margin: 10px;
}

.news-header a:hover {
  text-decoration: underline;
}

.time {
  font-size: 0.85em;
  color: rgb(52, 51, 47);
  margin: 5px;
  font-weight: bold;
}

.news-content,
.category-item p {
  font-size: 1em;
  line-height: 1.6;
  color: #444;
}

.recommend-news-title {
  width: 100%;
  height: 100%;
}

.recommend-news-title a {
  font-size: 1em;
  font-weight: bold;
  color: #333;
  transition: color 0.3s ease;
  margin: 10px;
  white-space: nowrap; /* 确保内容在一行显示 */
  overflow: hidden; /* 超出容器的内容会被隐藏 */
  text-overflow: ellipsis; /* 用省略号表示被截断的文本 */
  display: block;
}
.recommend-news-list-button {
  width: 80%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 15px;
}
</style>
