import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/pages/HomePage")
    },
    {
      path: "/auth/:authType",
      name: "auth",
      component: () => import("@/pages/Auth"),
      props: true
    },
    {
      path: "/test",
      name: "test",
      component: () => import("@/pages/Test")
    }
  ]
});
