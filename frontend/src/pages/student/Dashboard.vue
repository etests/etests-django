<template>
  <DashboardLayout :profile="student" :controls="controls" />
</template>

<script>
import DashboardLayout from "@components/layouts/DashboardLayout.vue";

export default {
  data() {
    return {
      editing: false,
      student: {
        basic: {
          title: "Basic",
          items: [
            { title: "Name", detail: "abc", icon: "domain" },
            { title: "Email", detail: "xyz@gmail", icon: "email" },
            { title: "City", detail: "jnk", icon: "home" },
            { title: "Mobile", detail: "55479", icon: "phone" }
          ]
        }
      },
      controls: [
        {
          name: "Tests",
          image: require("@assets/images/student/dashboard/test.png")
        },
        {
          name: "Test Series",
          image: require("@assets/images/student/dashboard/testseries.png")
        },
        {
          name: "Question Bank",
          image: require("@assets/images/student/dashboard/questionbank.png")
        },
        {
          name: "Results",
          image: require("@assets/images/student/dashboard/results.png")
        },
        {
          name: "Notifications",
          image: require("@assets/images/student/dashboard/notifications.png")
        },
        {
          name: "Discuss",
          image: require("@assets/images/student/dashboard/discuss.png")
        },
        {
          name: "Analysis",
          image: require("@assets/images/student/dashboard/analytics.png")
        },
        {
          name: "Schedule",
          image: require("@assets/images/student/dashboard/schedule.png")
        },
        {
          name: "Batches",
          image: require("@assets/images/student/dashboard/groups.png")
        }
      ]
    };
  },
  components: {
    DashboardLayout
  }
};
</script>
