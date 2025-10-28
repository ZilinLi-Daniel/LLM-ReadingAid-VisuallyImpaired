import { createRouter, createWebHistory } from "vue-router";
import IndexPage from "./src/components/IndexPage.vue";
import RegisterPage from "./src/components/RegisterPage.vue";
import LognPage from "./src/components/LoginPage.vue";
import PerferenceSelected from "./src/components/PerferenceSelected.vue";
import NewsDetailPage from "./src/components/NewsDetailPage.vue";
import HomePage from "./src/components/HomePage.vue";

const routes = [
  {
    path: "/",
    name: "Index",
    component: IndexPage,
  },
  {
    path: "/register",
    name: "Register",
    component: RegisterPage,
  },
  {
    path: "/login",
    name: "Login",
    component: LognPage,
  },
  {
    path: "/perference",
    name: "PerferenceSelected",
    component: PerferenceSelected,
  },
  {
    path: "/newsdetail",
    name: "NewsDetailPage",
    component: NewsDetailPage,
  },
  {
    path: "/HomePage",
    name: "HomePage",
    component: HomePage,
  },
  // ...其他路由配置
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

//添加路由守卫,检查用户是否已登录
router.beforeEach((to, from, next) => {
  // 检查用户是否已登录
  const isLoggedIn = sessionStorage.getItem("userId"); // 假设登录状态保存在 localStorage
  if (to.path === "/HomePage" && !isLoggedIn) {
    // 如果用户未登录且尝试访问非登录页面，重定向到登录页面
    next({ path: "/login" });
  } else {
    // 其他情况，正常进行路由跳转
    next();
  }
});

export default router;
