<template>
  <div id="app" class="text-xs-center">
    <v-app class="white">
      <Notification position="top center" />
      <vue-progress-bar></vue-progress-bar>
      <router-view />
    </v-app>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "app",
  computed: {
    alert() {
      return this.$store.state.alert;
    },
    ...mapState({
      alertType: state => state.alert.type
    })
  },
  watch: {
    alertType: function(newType, oldType) {
      if (newType === "success") {
        this.$notify({
          type: newType,
          title: "Done!",
          text: this.alert.message
        });
        this.$store.dispatch("alert/clear");
      } else if (newType === "error") {
        this.$notify({
          type: newType,
          title: "There's an error!",
          text: this.alert.message
        });
        this.$store.dispatch("alert/clear");
      }
    },
    $route(to, from) {
      this.$store.dispatch("alert/clear");
    }
  },
  created() {
    this.$Progress.start();
    this.$router.beforeEach((to, from, next) => {
      if (to.meta.progress !== undefined) {
        let meta = to.meta.progress;
        this.$Progress.parseMeta(meta);
      }
      this.$Progress.start();
      next();
    });
    this.$router.afterEach((to, from) => {
      this.$Progress.finish();
    });
  },
  mounted() {
    this.$Progress.finish();
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
</style>
