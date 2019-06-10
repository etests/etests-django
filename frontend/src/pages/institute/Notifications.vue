<template>
  <StandardLayout>
    <TextCard :card="newNotification">
      <v-divider />
      <v-btn icon color="info lighten-1">
        <v-icon large color="white">mdi-plus</v-icon>
      </v-btn>
    </TextCard>
    <TextCard
      v-for="(notification, i) in notifications"
      :key="i"
      :card="notification"
    />
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import TextCard from "@components/layouts/TextCard";

export default {
  data() {
    return {
      newNotification: {
        title: "New notification"
      },
      notifications: [
        {
          title: "Major Test 2 Launched",
          text:
            "Next test in the Test Series 1 is launched. It will start on June 20."
        },
        {
          title: "Major Test 1 Launched",
          text:
            "Next test in the Test Series 1 is launched. It will start on June 15."
        }
      ]
    };
  },
  components: {
    StandardLayout,
    TextCard
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
</style>
