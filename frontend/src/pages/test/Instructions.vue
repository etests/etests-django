<template>
  <StandardLayout>
    <v-card class="elevation-2">
      <v-card-title>
        Instructions
      </v-card-title>
      <v-card-text>
        <v-btn @click="$router.push(`/test/${id}`)">Proceed</v-btn>
      </v-card-text>
    </v-card>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout.vue";

export default {
  data() {
    return {
      id: this.$route.params.id
    };
  },
  created() {
    if (!this.$store.state.sessions.status.exists) {
      this.$watch("status", function(newStatus, oldStatus) {
        this.loading = newStatus.loading;
        this.error = newStatus.error;
      });
      this.$store.dispatch(`sessions/get`, this.id);
    }
  },
  components: {
    StandardLayout
  }
};
</script>

<style module lang="stylus"></style>
