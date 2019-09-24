<template>
  <div id="app">
    <v-app class="white text-xs-center">
      <Notification class="my-1" position="top center" />
      <vue-progress-bar />
      <router-view />
    </v-app>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "app",
  computed: {
    ...mapState({
      loggedIn: state => state.authentication.status.loggedIn,
      alertType: state => state.alert.type,
      alert: state => state.alert
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
    var vm = this;
    // if(this.loggedIn){
    //   setInterval(_ =>{
    //     vm.$store.dispatch("authentication/refresh");
    //   }, 9*30*1000);
    // }
  }
};
</script>
