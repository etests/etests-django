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
      path: "/career",
      name: "career",
      component: () => import("@/pages/career.vue"),
      meta: {
        title: "Career"
      }
    },
    {
      path: "/terms",
      name: "career",
      component: () => import("@/pages/terms.vue"),
      meta: {
        title: "Terms And Conditions"
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
      path: "/payment",
      name: "payment",
      component: () => import("@/pages/Payment.vue"),
      meta: {
        title: "Payment"
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
          path: "question-banks",
          component: () => import("@/pages/student/TestSeries"),
          meta: {
            title: "My Question Banks"
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
          component: () => import("@/pages/student/Profile"),
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
          path: "transactions",
          name: "institute-transactions",
          component: () => import("@/pages/institute/Transactions"),
          meta: {
            title: "Dashboard"
          }
        },
        {
          path: "profile",
          name: "institute-profile",
          component: () => import("@/pages/institute/Profile"),
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
          path: "question-banks",
          name: "my-question-banks",
          component: () => import("@/pages/institute/TestSeries"),
          meta: {
            title: "My Question Banks"
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
      path: "/exams",
      name: "exams",
      component: () => import("@/pages/Exams"),
      meta: {
        title: "Exams"
      }
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
      path: "/question-banks",
      component: () => import("@/pages/QuestionBanks"),
      meta: {
        title: "Question Banks"
      }
    },
    {
      path: "/faq",
      name: "faq",
      component: () => import("@/pages/FAQ"),
      meta: {
        title: "FAQ"
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
      path: "/test/:id/edit",
      name: "edit-test",
      component: () => import("@/pages/test/EditTest"),
      meta: {
        title: "Edit Test",
        requiresAuth: true,
        requiresInstitute: true
      }
    },
    {
      path: "/test/:id",
      name: "test",
      props: { demo: false },
      component: () => import("@/pages/test/StartTest"),
      meta: {
        title: "Start Test"
      }
    },
    {
      path: "/test/demo/:id",
      name: "test",
      props: { demo: true },
      component: () => import("@/pages/test/StartTest"),
      meta: {
        title: "Start Test"
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
    },
    {
      path: "/demo/test",
      component: () => import("@/pages/test/DemoTest"),
      meta: {
        title: "Demo Test"
      }
    },
    {
      path: "/demo/edit-test",
      component: () => import("@/pages/test/DemoEditTest"),
      meta: {
        title: "Demo Edit Test"
      }
    }
  ]
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = store.state.authentication.status.loggedIn;

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (isLoggedIn) {
      const isStudent = store.state.authentication.user.type === "student";
      const isInstitute = store.state.authentication.user.type === "institute";

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
