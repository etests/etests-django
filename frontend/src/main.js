import Vue from "vue";
import App from "./App";
import router from "./router";
import Vuetify from "vuetify";
import "material-design-icons-iconfont/dist/material-design-icons.css";
import "@mdi/font/css/materialdesignicons.css";
import "./stylus/main.styl";
import "chartist/dist/chartist.min.css";
import store from "./store";
import VueFullPage from "vue-fullpage.js";

Vue.use(VueFullPage);

Vue.use(require("vue-chartist"));

Vue.config.productionTip = false;

Vue.use(Vuetify, {
  iconfont: "mdi" || "md",
  theme: {
    primary: "#28CC9E",
    secondary: "#196B69"
  }
});

/* eslint-disable no-new */
new Vue({
  el: "#app",
  store,
  router,
  components: {
    App
  },
  template: "<App/>"
});
