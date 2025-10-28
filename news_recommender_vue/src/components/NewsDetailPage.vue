<template>
  <AppHeader @update:version="onVersionChange" :is-news-page="true"></AppHeader>
  <div class="news-detail-page">
    <div class="left-panel">
      <!-- 新闻详情 -->
      <div class="part_1" id="part_1">
        <P
          ref="newsTitle"
          tabindex="1"
          id="news-title"
          class="news-title"
          @focus="
            speak(
              title,
              headerVersion === 'en'
                ? 'News Detail Page Title:'
                : '新闻详情页标题:'
            )
          "
        >
          {{ title }}
        </P>
        <p
          id="news-time"
          class="news-time"
          tabindex="2"
          @focus="
            speak(
              headerVersion === 'en' ? format(time) : time,
              headerVersion === 'en'
                ? 'News Detail Page Publish Time:'
                : '新闻详情页时间:'
            )
          "
        >
          {{ time }}
        </p>
        <p
          id="news-content"
          class="news-content"
          tabindex="4"
          @focus="
            speak(
              content,
              headerVersion === 'en'
                ? 'News Detail Page Content:'
                : '新闻详情页内容:'
            )
          "
        >
          {{ content }}
        </p>
      </div>
      <p>
        {{
          headerVersion === "en"
            ? "The data on the current page is presented for academic research only, and the news content of the page is no longer updated in real time."
            : ""
        }}
      </p>
    </div>
    <div class="divider"></div>

    <div class="right-panel">
      <button
        @click="getNewsSummary"
        @focus="
          speak(
            this.headerVersion === 'en'
              ? 'Get News Summary Button'
              : '获取新闻摘要按钮',
            this.headerVersion === 'en' ? 'News Detail Page:' : '详情页:'
          )
        "
        class="recommend-news-list-button"
      >
        {{ headerVersion === "en" ? "Get News Summary" : "获取新闻摘要" }}
      </button>

      <div v-if="summary_loading" class="loading-animation">
        <img src="../assets/loading.gif" alt="Loading..." />
      </div>

      <div class="news-summary">
        <p>{{ newsSummary }}</p>
      </div>

      <button
        @click="getRecommendNewsList"
        @focus="
          speak(
            this.headerVersion === 'en'
              ? 'Get Recommended News List Button'
              : '获取推荐新闻按钮',
            this.headerVersion === 'en' ? 'News Detail Page:' : '详情页:'
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
      <div v-if="recommend_loading" class="loading-animation">
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
                    ? 'News Detail Page Recommended News Title:'
                    : '当前详情页推荐新闻标题：'
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
  name: "NewsDetailPage",
  components: {
    AppHeader,
  },
  data() {
    return {
      userId: JSON.parse(sessionStorage.getItem("userId") || "{}"),
      newId: JSON.parse(sessionStorage.getItem("viewNewsId") || "{}"),
      title: "",
      time: "",
      content: "",
      summary_loading: false,
      recommend_loading: false,
      categories: [], // 推荐的主题类别
      recommend_news_list: [], // 推荐新闻列表
      hovering: false, // Initialize hovering state
      headerVersion: store.version,
      newsSummary: "",
    };
  },
  created() {
    this.getNewsDetailById();
  },
  mounted() {
    this.$nextTick(() => {
      this.$refs.newsTitle.focus();
    });

    window.addEventListener("keyup", this.handleKeyPress);
  },
  beforeUnmount() {
    window.removeEventListener("keyup", this.handleKeyPress);
  },
  methods: {
    // 方法来获取新闻详情和推荐新闻
    async getNewsDetailById() {
      try {
        const apiUrl = process.env.VUE_APP_API_URL;
        const response = await axios.get(`${apiUrl}/api/news_detail`, {
          params: {
            new_id: JSON.parse(sessionStorage.getItem("viewNewsId") || "{}"),
            user_id: JSON.parse(sessionStorage.getItem("userId") || "{}"),
          },
        });
        this.newId = response.data.news_detail.newsId;
        this.title = response.data.news_detail.title;
        this.time = response.data.news_detail.time;
        this.content = response.data.news_detail.content;
      } catch (error) {
        console.log("error information:" + error);
      }
    },
    //更改语言版本
    onVersionChange(newVersion) {
      this.headerVersion = newVersion;
    },
    async getRecommendNewsList() {
      this.recommend_loading = true;
      try {
        // 获取推荐的新闻列表
        const apiUrl = process.env.VUE_APP_API_URL;
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
        this.recommend_loading = false;
      }
      console.log(this.recommend_news_list);
    },
    //format the date
    format(dateString) {
      const date = parseISO(dateString);
      return format(date, "iiii, MMMM d, yyyy"); // 'Sunday, March 31, 2024'
    },

    async getNewsSummary() {
      this.summary_loading = true;
      try {
        const apiUrl = process.env.VUE_APP_API_URL
        const response = await axios.get(`${apiUrl}/api/news_summary`, {
          params: {
            lang: this.headerVersion,
            user_id: this.userId,
            news_id: this.newId,
          },
        });
        this.newsSummary = response.data.news_summary;
        this.speak(
          this.newsSummary,
          this.headerVersion === "en" ? "News Summary:" : "新闻摘要："
        );
      } catch (error) {
        console.log(error);
      } finally {
        this.summary_loading = false;
      }
    },
    async viewNewsDetail(news_id) {
      sessionStorage.setItem("viewNewsId", JSON.stringify(news_id));
      try {
        this.$router.push({
          name: "NewsDetailPage",
        });
        this.getNewsDetailById();
        this.recommend_news_list = [];
        this.newsSummary = "";
        this.loading = false;
      } catch (error) {
        console.error("Error fetching news detail:", error);
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
* {
  padding: 0;
  margin: 0;
  text-decoration: none;
}

html body {
  background-color: rgba(233, 233, 233, 0.545);
  display: flex;
  height: 100vh;
  background-size: cover;
}
.news-detail-page {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  padding: 20px; /* 页面主体的内边距 */
  font-family: "Roboto", sans-serif;
}

.left-panel {
  width: 60%;
  height: 815px; /* 你可以根据需要调整这个值 */
  overflow-y: auto;
  position: absolute;
  right: 80% !important;
  left: 3% !important;
  top: 13% !important;
  color: #272d3590;
}

.part_1 {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #afb8d98e; /* 为新闻项目添加底部边框 */
  font-size: smaller;
  background-color: #dae7fb47 !important;
  border-radius: 13px;
}
.news-title {
  text-align: center;
  line-height: 30px;
  padding: 20px 10px;
  font-size: 20px;
  font-weight: bold;
}

.news-time {
  /* margin-left: auto; */
  font-size: 12px;
  color: grey;
  padding: 10px;
  text-align: center;
}

.left-panel p {
  line-height: 30px;
  text-indent: 2em;
  font-size: 15px;
}

.part_5 {
  /* display: none; */
  margin-top: 2%;
  margin-bottom: 2%;
  background-color: #dae7fb47 !important;
  border-radius: 13px;
  border-bottom: 1px solid #bbbabaa4;
  padding: 20px;
}

.part_5 h3 {
  margin-top: 2%;
  margin-bottom: 2%;
  color: #526366;
}

.news-detail,
.recommendation-section {
  margin: 20px;
  padding: 20px;
}

.recommendation-section {
  background-color: #f0f0f0;
  border-radius: 10px;
  padding: 10px;
}

.category-button {
  background-color: transparent;
  border: 2px solid #007bff;
  border-radius: 20px;
  padding: 5px 15px;
  margin: 5px;
  cursor: pointer;
}

.category-button:hover {
  background-color: #007bff;
  color: white;
}

.divider {
  width: 2px;
  height: 815px;
  position: absolute;
  background-color: rgba(12, 34, 49, 1);
  right: 35% !important;
  top: 13% !important;
}

.right-panel {
  position: absolute;
  width: 30%;
  height: 815px;
  top: 13% !important;
  right: 3% !important;
  background-color: #dae7fb2b;
  border: 1px solid #afb8d98e;
  border-radius: 10px;
}
.news-summary {
  padding: 10px;
  margin: 3px;
  text-align: left;
}

.loading-animation {
  text-align: center;
}
.recommended-news-list {
  width: 100%;
  overflow-y: auto;
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
  width: 95%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 15px;
  margin: 10px auto; /* 水平居中 */
  display: block;
}
</style>
