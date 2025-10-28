<template>
  <AppHeader @update:version="onVersionChange"></AppHeader>
  <!-- 注册页面的内容 -->
  <div class="auth-container">
    <div class="logo-circle">
      <img
        src="/assets/news_recommend_logo.png"
        tabindex="0"
        @focus="
          speak(
            headerVersion === 'en' ? 'Icon:' : '图标',
            headerVersion === 'en' ? 'Login page:' : '登录页'
          )
        "
      />
    </div>

    <form class="auth-form" id="registerForm" @submit.prevent="submitLogin">
      <div class="form-group">
        <label
          for="email"
          tabindex="0"
          @focus="
            speak(
              headerVersion === 'en' ? 'Email:' : '邮箱',
              headerVersion === 'en' ? 'Login page:' : '登录页'
            )
          "
          >{{ headerVersion === "en" ? "Email" : "邮箱" }}:</label
        >

        <input
          type="email"
          id="email"
          name="email"
          v-model="email"
          :placeholder="
            headerVersion === 'en' ? 'Please input the email' : '请输入邮箱'
          "
          tabindex="0"
          @focus="
            speak(
              headerVersion === 'en'
                ? 'Email input box, please input your email:'
                : '邮箱输入框，请输入邮箱',
              headerVersion === 'en' ? 'Login page:' : '登录页'
            )
          "
          required
        />
      </div>

      <div class="form-group">
        <label
          for="password"
          tabindex="0"
          @focus="
            speak(
              headerVersion === 'en' ? 'password' : '密码',
              headerVersion === 'en' ? 'Login page' : '登录页'
            )
          "
          >{{ headerVersion === "en" ? "Password" : "密码" }}:</label
        >
        <input
          type="password"
          id="password"
          name="password"
          v-model="password"
          :placeholder="
            headerVersion === 'en' ? 'Please input the password' : '请输入密码'
          "
          tabindex="0"
          @focus="
            speak(
              headerVersion === 'en'
                ? 'Password input box, please input your password'
                : '密码输入框，请输入密码',
              headerVersion === 'en' ? 'Login page:' : '登录页'
            )
          "
          required
        />
      </div>

      <button
        type="submit"
        class="submitbutton"
        tabindex="0"
        @focus="
          speak(
            headerVersion === 'en' ? 'Submit button' : '提交按钮',
            headerVersion === 'en' ? 'Login page:' : '登录页'
          )
        "
      >
        {{ headerVersion === "en" ? "Submit" : "提交" }}
      </button>
    </form>
  </div>
</template>

<script>
import AppHeader from "../common-components/AppHeader.vue";
import { store } from "../store/store.js";
import axios from "axios";
export default {
  name: "LoginPage",
  components: {
    AppHeader,
  },
  data() {
    return {
      email: "",
      password: "",
      headerVersion: store.version,
      // 其他数据
    };
  },
  mounted() {
    // 页面加载时，添加sessionStorage
    window.addEventListener("keyup", this.handleKeyPress);
  },
  beforeMount() {
    // 页面卸载时，清空sessionStorage
    window.removeEventListener("keyup", this.handleKeyPress);
  },
  methods: {
    async submitLogin() {
      // 登录表单提交时调用的方法
      const apiUrl = process.env.VUE_APP_API_URL
      const response = await axios.post(`${apiUrl}/api/login_check`, {
        email: this.email, // 发送电子邮箱
        password: this.password, // 发送密码
      });
      if (response.data.message == "True") {
        //存储用户的浏览偏好至sessionStorage
        sessionStorage.setItem("userId", JSON.stringify(response.data.userId));
        this.$router.push("/HomePage");
      } else {
        // 如果登录失败，则弹出提示
        alert(response.data.message);
      }
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
      if (event.key === "Escape") {
        this.$router.go(-1);
      }
    },
  },
};
</script>
<style scoped>
.auth-container {
  max-width: 400px;
  margin: 180px auto;
  padding: 10px;
}

.auth-form {
  padding: 0, 5px;
}

.logo-circle {
  width: 100%;
  height: 50px;
  display: flex;
  margin: 0, auto;
  justify-content: center;
  align-items: center;
}
.logo-circle img {
  width: 60px;
  height: 60px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 94%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.auth-form button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.auth-form button:hover {
  background-color: #0056b3;
}
.submitbutton {
  margin-top: 30px;
}
</style>
