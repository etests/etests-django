<template>
  <div id="app" class="text-xs-center">
    <v-app class="white">
      <Notification position="top center" />
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
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
</style>
