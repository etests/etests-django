<template>
  <div id="app" class="text-xs-center">
    <v-app class="white">
      <router-view />
    </v-app>
  </div>
</template>

<script>
export default {
  name: "app",
  computed: {
    alert() {
      return this.$store.state.alert;
    }
  },
  watch: {
    $route(to, from) {
      // clear alert on location change
      this.$store.dispatch("alert/clear");
    }
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
</style>
