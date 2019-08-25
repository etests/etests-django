import Vue from "vue";
import Router from "vue-router";
import store from "@/store";

Vue.use(Router);

const router = new Router({
  routes: [
    {
      path: "/",
      name: "root",
      component: () => import("@/pages/HomePage"),
      meta: {
        title: "Home"
      }
    },
    {
      path: "/home",
      name: "home",
      component: () => import("@/pages/HomePage"),
      meta: {
        title: "Home"
      }
    },
    {
      path: "/student",
      name: "student",
      component: () => import("@/components/layouts/EmptyLayout"),
      meta: {
        title: "Student",
        requiresAuth: true,
        requiresStudent: true
      },
      children: [
        {
          path: "dashboard",
          name: "dashboard",
          component: () => import("@/pages/student/Dashboard"),
          meta: {
            title: "Dashboard"
          }
        },
        {
          path: "tests",
          component: () => import("@/pages/student/Tests"),
          meta: {
            title: "Tests"
          }
        },
        {
          path: "profile",
          name: "profile",
          component: () => import("@/components/auth/RegisterStudent"),
          meta: {
            title: "Profile"
          }
        },
        {
          path: "report",
          name: "report",
          component: () => import("@/pages/student/Report"),
          meta: {
            title: "Progress Report"
          }
        },
        {
          path: "schedule",
          name: "schedule",
          component: () => import("@/pages/student/Schedule"),
          meta: {
            title: "Test Schedule"
          }
        },
        {
          path: "batches",
          component: () => import("@/pages/student/Batches"),
          meta: {
            title: "Batches"
          }
        }
      ]
    },
    {
      path: "/institute",
      name: "institute",
      component: () => import("@/components/layouts/EmptyLayout"),
      meta: {
        title: "Institute",
        requiresAuth: true,
        requiresInstitute: true
      },
      children: [
        {
          path: "dashboard",
          name: "institute-dashboard",
          component: () => import("@/pages/institute/Dashboard"),
          meta: {
            title: "Dashboard"
          }
        },
        {
          path: "profile",
          name: "institute-profile",
          component: () => import("@/components/auth/RegisterInstitute"),
          meta: {
            title: "Profile"
          }
        },
        {
          path: "batches",
          name: "batches",
          component: () => import("@/pages/institute/Batches"),
          meta: {
            title: "Batches"
          }
        },
        {
          path: "notifications",
          name: "institute-notifications",
          component: () => import("@/pages/institute/Notifications"),
          meta: {
            title: "Notifications"
          }
        },
        {
          path: "plans",
          name: "plans",
          component: () => import("@/pages/institute/Plans"),
          meta: {
            title: "Plans"
          }
        },
        {
          path: "tests",
          name: "institute-tests",
          component: () => import("@/pages/institute/Tests"),
          meta: {
            title: "Tests"
          }
        },
        {
          path: "tests-series",
          name: "institute-test-series",
          component: () => import("@/pages/institute/TestSeries"),
          meta: {
            title: "Tests Series"
          }
        },
        {
          path: "test/:id/edit",
          name: "edit-test",
          component: () => import("@/pages/institute/EditTest"),
          meta: {
            title: "Edit Test"
          }
        },
        {
          path: "test/preview",
          component: () => import("@/pages/institute/TestPreview"),
          meta: {
            title: "Test Preview"
          }
        }
      ]
    },
    {
      path: "/institutes",
      name: "institutes",
      component: () => import("@/pages/Institutes"),
      meta: {
        title: "Institutes"
      }
    },
    {
      path: "/discuss",
      name: "discuss",
      component: () => import("@/pages/Discuss"),
      meta: {
        title: "Discuss"
      }
    },
    {
      path: "/auth/:authType",
      name: "auth",
      component: () => import("@/pages/Auth"),
      props: true,
      meta: {
        title: "Login/Register"
      }
    },
    {
      path: "/test/:id",
      name: "test",
      component: () => import("@/pages/test/Test"),
      meta: {
        title: "Test"
      }
    },
    {
      path: "/result/:id",
      name: "result",
      component: () => import("@/pages/test/Result"),
      meta: {
        title: "Result"
      }
    },
    {
      path: "/review/:id",
      name: "review",
      component: () => import("@/pages/test/Review"),
      meta: {
        title: "Review"
      }
    }
  ]
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = store.state.authentication.status.loggedIn;

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (isLoggedIn) {
      const isStudent = store.state.authentication.user.is_student;
      const isInstitute = store.state.authentication.user.is_institute;

      if (to.matched.some(record => record.meta.requiresStudent)) {
        if (isStudent) return next();
        else return next("/home");
      }
      if (to.matched.some(record => record.meta.requiresInstitute)) {
        if (isInstitute) return next();
        else return next("/home");
      }
    } else
      return next({
        name: "auth",
        params: { authType: 2 },
        query: {
          redirect: to.fullPath
        }
      });
  }

  if (isLoggedIn && to === "auth/2")
    return next({
      name: "dashboard"
    });

  if (to.meta && to.meta.title) document.title = to.meta.title;
  next();
});

export default router;
