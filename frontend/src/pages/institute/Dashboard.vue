<template>
  <StandardLayout>
    <DisplayCard xs12 md6 v-for="(card, i) in cards" :key="i" :card="card" />
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import DisplayCard from "@components/layouts/DisplayCard";

export default {
  data() {
    return {
      cards: [
        {
          title: "Notifications",
          text:
            "Create and manage notifications for students. Notify about upcoming tests, updates about solutions to past tests etc.",
          action: {
            text: "Manage notifications",
            icon: "mdi-bell",
            link: { path: "/institute/notifications" },
            color: "amber"
          }
        },
        {
          title: "Tests",
          text:
            "Create test series and add tests to them, or edit existing tests and unit tests.",
          action: {
            text: "Create and view tests",
            icon: "mdi-note-multiple",
            link: { path: "/institute/tests" },
            color: "info"
          }
        },
        {
          title: "Batches",
          text:
            "Create separate batches for your students using a list of roll numbers.",
          action: {
            text: "Manage your batches",
            icon: "mdi-account-multiple",
            link: { path: "/institute/batches" },
            color: "success"
          }
        },
        {
          title: "Profile",
          text:
            "Edit your profile to make it stand out. This is essential because it show others what your institute is.",
          action: {
            text: "Edit your profile",
            icon: "mdi-account",
            link: { path: "/institute/profile" },
            color: "error"
          }
        }
      ]
    };
  },
  components: {
    StandardLayout,
    DisplayCard
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
</style>
