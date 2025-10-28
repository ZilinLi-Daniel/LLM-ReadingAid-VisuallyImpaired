const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    open: true,
    host: "localhost",
    port: 8080,
    https: false,
    proxy: {
      "/api": {
        target: process.env.VUE_APP_API_URL,
        changeOrigin: true,
      },
    },
  },
});
