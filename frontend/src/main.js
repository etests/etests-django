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
import vueMq from "vue-mq";
import "./registerServiceWorker";
import Notifications from "vue-notification";
import VueGoogleCharts from "vue-google-charts";
import CKEditor from "@ckeditor/ckeditor5-vue";

Vue.use(CKEditor);

Vue.use(VueGoogleCharts);

Vue.use(Notifications, {
  componentName: "Notification"
});

Vue.use(vueMq, {
  breakpoints: {
    xs: 600,
    sm: 960,
    md: 1264,
    lg: 1904,
    xl: Infinity
  }
});

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
