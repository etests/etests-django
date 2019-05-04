// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import App from "./App";
import router from "./router";
import Vuetify from "vuetify";
import "material-design-icons-iconfont/dist/material-design-icons.css";
import "./stylus/main.styl";

Vue.config.productionTip = false;

Vue.use(Vuetify, {
  theme: {
    primary: "#28CC9E",
    secondary: "#196B69"
  }
});

/* eslint-disable no-new */
new Vue({
  el: "#app",
  router,
  components: {
    App
  },
  template: "<App/>"
});
