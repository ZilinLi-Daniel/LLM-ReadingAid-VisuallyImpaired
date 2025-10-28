<template>
  <!-- appheader 的复用组件 -->
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
            headerVersion === 'en' ? 'Register Page:' : '注册页'
          )
        "
      />
    </div>

    <form class="auth-form" id="registerForm" @submit.prevent="handleSubmit">
      <div class="form-group">
        <label
          for="username"
          tabindex="0"
          @focus="
            speak(
              headerVersion === 'en' ? 'Username:' : '用户名',
              headerVersion === 'en' ? 'Register Page:' : '注册页'
            )
          "
          >{{ headerVersion === "en" ? "Username" : "用户名" }}</label
        >
        <input
          type="text"
          id="username"
          name="username"
          :placeholder="
            headerVersion === 'en'
              ? 'Please input the username'
              : '请输入用户名'
          "
          v-model="username"
          required
          tabindex="0"
          @focus="
            speak(
              headerVersion === 'en'
                ? 'User name input box, please enter a user name:'
                : '用户名输入框，请输入用户名',
              headerVersion === 'en' ? 'Register Page:' : '注册页'
            )
          "
        />
      </div>
      <div class="form-group">
        <label
          for="email"
          tabindex="0"
          @focus="
            speak(
              headerVersion === 'en' ? 'Mailbox:' : '邮箱',
              headerVersion === 'en' ? 'Register Page:' : '注册页'
            )
          "
          >{{ headerVersion === "en" ? "Email" : "邮箱" }}</label
        >
        <input
          type="email"
          id="email"
          name="email"
          :placeholder="
            headerVersion === 'en' ? 'Please input the Email' : '请输入邮箱'
          "
          v-model="email"
          required
          tabindex="0"
          @focus="
            speak(
              headerVersion === 'en'
                ? 'Mailbox input box, please input mail:'
                : '邮箱输入框，请输入邮箱',
              headerVersion === 'en' ? 'Register Page:' : '注册页'
            )
          "
        />
      </div>
      <div class="form-group">
        <label
          for="password"
          tabindex="0"
          @focus="
            speak(
              headerVersion === 'en' ? 'password:' : '密码',
              headerVersion === 'en' ? 'Register Page:' : '注册页'
            )
          "
          >{{ headerVersion === "en" ? "Password" : "密码" }}</label
        >
        <input
          type="password"
          id="password"
          name="password"
          :placeholder="
            headerVersion === 'en' ? 'Please input the Password' : '请输入密码'
          "
          v-model="password"
          required
          tabindex="0"
          @focus="
            speak(
              headerVersion === 'en'
                ? 'Password input box, please enter your password'
                : '密码输入框，请输入密码',
              headerVersion === 'en' ? 'Register Page:' : '注册页'
            )
          "
        />
      </div>

      <button
        type="submit"
        class="submitbutton"
        tabindex="0"
        @focus="
          speak(
            headerVersion === 'en'
              ? 'Register button, click to jump to preference selection'
              : '注册按钮，点击跳转至偏好选择',
            headerVersion === 'en' ? 'Register Page:' : '注册页'
          )
        "
      >
        {{ headerVersion === "en" ? "Register" : "注册" }}
      </button>
      <p>
        {{
          headerVersion === "en"
            ? "Already have one accout?"
            : "已经有账户了？"
        }}<a
          href="/login"
          @focus="
            speak(
              headerVersion === 'en'
                ? 'Already have an account, click login'
                : '已有账户，点击登录',
              headerVersion === 'en' ? 'Register Page:' : '注册页'
            )
          "
        >
          {{ headerVersion === "en" ? "Login" : "登录" }}</a
        >
      </p>
    </form>
  </div>
</template>

<script>
import AppHeader from "../common-components/AppHeader.vue";
import { store } from "../store/store.js";

// import axios from 'axios'
export default {
  name: "RegisterPage",
  components: {
    AppHeader,
  },
  data() {
    return {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
      headerVersion: store.version,
    };
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
    handleSubmit() {
      try {
        sessionStorage.setItem("username", JSON.stringify(this.username));
        sessionStorage.setItem("email", JSON.stringify(this.email));
        sessionStorage.setItem("password", JSON.stringify(this.password));

        this.$router.push("/perference");
      } catch (error) {
        // 处理注册错误，可能是显示一个错误消息
        console.log("error information:" + error);
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
.auth-container {
  max-width: 400px;
  margin: 180px auto;
  padding: 10px;
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

.auth-form {
  padding: 0, 5px;
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
  /* border: 1px solid #ccc; */
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

.auth-form p {
  text-align: left;
}

/*注册的提交按钮 */
.submitbutton {
  width: auto;
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
</style>
