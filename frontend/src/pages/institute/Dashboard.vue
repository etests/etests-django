<template>
  <DashboardLayout :profile="institute" :controls="controls" />
</template>

<script>
import DashboardLayout from "@components/layouts/DashboardLayout.vue";

export default {
  data() {
    return {
      editing: false,
      institute: {
        basic: {
          title: "Basic",
          items: [
            { title: "Name", detail: "abc", icon: "domain" },
            { title: "Email", detail: "xyz@gmail", icon: "email" },
            { title: "City", detail: "jnk", icon: "home" },
            { title: "Mobile", detail: "55479", icon: "phone" }
          ]
        },
        account: {
          title: "Account",
          items: [
            {
              title: "Tests",
              detail: 5,
              icon: "mdi-clipboard-text-outline"
            },
            {
              title: "TestSeries",
              detail: 5,
              icon: "mdi-clipboard-text-play-outline"
            },
            {
              title: "Question Banks",
              detail: 5,
              icon: "mdi-book-open-page-variant"
            },
            { title: "Batches", detail: 5, icon: "mdi-group" },
            { title: "Students", detail: 5, icon: "mdi-account-group-outline" }
          ]
        }
      },
      controls: [
        {
          name: "Test",
          image: require("@assets/images/institute/dashboard/test.png")
        },
        {
          name: "Test Series",
          image: require("@assets/images/institute/dashboard/testseries.png")
        },
        {
          name: "Question Bank",
          image: require("@assets/images/institute/dashboard/questionbank.png")
        },
        {
          name: "Results",
          image: require("@assets/images/institute/dashboard/results.png")
        },
        {
          name: "Transactions",
          image: require("@assets/images/institute/dashboard/transactions.png")
        },
        {
          name: "Notifications",
          image: require("@assets/images/institute/dashboard/notifications.png")
        },
        {
          name: "Discuss",
          image: require("@assets/images/institute/dashboard/discuss.png")
        },
        {
          name: "Analytics",
          image: require("@assets/images/institute/dashboard/analytics.png")
        },
        {
          name: "Groups",
          image: require("@assets/images/institute/dashboard/groups.png")
        }
      ]
    };
  },
  components: {
    DashboardLayout
  }
};
</script>
