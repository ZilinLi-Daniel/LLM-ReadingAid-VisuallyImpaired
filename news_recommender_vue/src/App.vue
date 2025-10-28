<template>
  <div id="app">
    <!-- 路由视图 -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif; /* 字体设置 */
  -webkit-font-smoothing: antialiased; /* 在WebKit浏览器中启用抗锯齿字体渲染 */
  -moz-osx-font-smoothing: grayscale; /* 在Firefox中为Mac OS X启用灰度抗锯齿字体渲染 */
  color: #2c3e50; /* 文字颜色 */
  /* width: 100%; 
  margin: 0px;
  padding: 0px; */
}
</style>
