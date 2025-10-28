import { createApp } from "vue";
import App from "./App.vue";
import router from "../router.js";
import IndexPage from "./components/IndexPage.vue";
import RegisterPage from "./components/RegisterPage.vue";
import LoginPage from "./components/LoginPage.vue";
import PerferenceSelected from "./components/PerferenceSelected.vue";
import NewsDetailPage from "./components/NewsDetailPage.vue";
import HomePage from "./components/HomePage.vue";

/*复用组件 */
import AppHeader from "./common-components/AppHeader.vue";

const app = createApp(App);
app.use(router);
app.mount("#app");
app.component("IndexPage", IndexPage);
app.component("AppHeader", AppHeader);
app.component("RegisterPage", RegisterPage);
app.component("LoginPage", LoginPage);
app.component("PerferenceSelected", PerferenceSelected);
app.component("NewsDetailPage", NewsDetailPage);
app.component("HomePage", HomePage);
