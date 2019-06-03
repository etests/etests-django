import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "root",
      component: () => import("@/pages/HomePage")
    },
    {
      path: "/home",
      name: "home",
      component: () => import("@/pages/HomePage")
    },
    {
      path: "/student/dashboard",
      name: "student-dashboard",
      component: () => import("@/pages/student/Dashboard")
    },
    {
      path: "/student/profile",
      name: "profile",
      component: () => import("@/pages/student/Profile")
    },
    {
      path: "/student/report",
      name: "report",
      component: () => import("@/pages/student/Report")
    },
    {
      path: "/student/schedule",
      name: "exams",
      component: () => import("@/pages/student/Schedule")
    },
    {
      path: "/institutes",
      name: "institutes",
      component: () => import("@/pages/Institutes")
    },
    {
      path: "/discuss",
      name: "discuss",
      component: () => import("@/pages/Discuss")
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
