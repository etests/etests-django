<template>
  <DashboardLayout :profile="profile" :controls="controls" />
</template>

<script>
import DashboardLayout from "@/components/layouts/DashboardLayout.vue";

export default {
  data() {
    return {
      editing: false,
      controls: [
        {
          name: "Tests",
          image: require("@/assets/images/dashboard/test.png"),
          link: { path: "tests" }
        },
        {
          name: "My Question Banks",
          image: require("@/assets/images/dashboard/questionbank.png"),
          link: { path: "question-banks" }
        },
        // {
        //   name: "Results",
        //   image: require("@/assets/images/dashboard/results.png"),
        //   link: { path: "results" }
        // },
        // {
        //   name: "Transactions",
        //   image: require("@/assets/images/dashboard/transactions.png"),
        //   link: { path: "transactions" }
        // },
        // {
        //   name: "Notifications",
        //   image: require("@/assets/images/dashboard/notifications.png"),
        //   link: { path: "notifications" }
        // },
        // {
        //   name: "Discuss",
        //   image: require("@/assets/images/dashboard/discuss.png"),
        //   link: { path: "discuss" }
        // },
        // {
        //   name: "Analytics",
        //   image: require("@/assets/images/dashboard/analytics.png"),
        //   link: { path: "analytis" }
        // },
        {
          name: "Batches",
          image: require("@/assets/images/dashboard/groups.png"),
          link: { path: "batches" }
        },
          {
          name: "Buyers",
          image: require("@/assets/images/dashboard/groups.png"),
          link: { path: "buyers" }
        }
      ]
    };
  },
  components: {
    DashboardLayout
  },
  computed: {
    user() {
      return this.$store.state.authentication.user;
    },
    profile() {
      return {
        name: {
          title: "Name",
          value: this.user.name,
          icon: "mdi-account-outline"
        },
        email: {
          title: "Email",
          value: this.user.email,
          icon: "mdi-email-outline"
        },
        city: {
          title: "City",
          value: this.user.city,
          icon: "mdi-home-outline"
        },
        phone: {
          title: "Mobile",
          value: this.user.phone,
          icon: "mdi-phone-outline"
        }
      };
    }
  }
};
</script>
