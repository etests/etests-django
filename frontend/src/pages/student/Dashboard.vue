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
          image: require("@/assets/images/student/dashboard/test.png"),
          link: { path: "tests" }
        },
        // {
        //   name: "Test Series",
        //   image: require("@/assets/images/student/dashboard/testseries.png"),
        //   link: { name: "testseries" }
        // },
        {
          name: "My Question Banks",
          image: require("@/assets/images/student/dashboard/testseries.png"),
          link: { path: "question-banks" }
        },
        {
          name: "Notifications",
          image: require("@/assets/images/student/dashboard/notifications.png"),
          link: { path: "notifications" }
        },
        // {
        //   name: "Discuss",
        //   image: require("@/assets/images/student/dashboard/discuss.png"),
        //   link: { name: "discuss" }
        // },
        // {
        //   name: "Progress Report",
        //   image: require("@/assets/images/student/dashboard/analytics.png"),
        //   link: { path: "report" }
        // },
        // {
        //   name: "Schedule",
        //   image: require("@/assets/images/student/dashboard/schedule.png"),
        //   link: { path: "schedule" }
        // },
        {
          name: "Batches",
          image: require("@/assets/images/student/dashboard/groups.png"),
          link: { path: "batches" }
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
