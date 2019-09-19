const path = require("path");

module.exports = {
  chainWebpack: config => {
    config.resolve.alias.set("vue$", "vue/dist/vue.esm.js");
  },
  productionSourceMap: false,
  devServer: {
    host: "0.0.0.0"
  }
};
