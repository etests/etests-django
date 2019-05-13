<template>
  <div id="app" class="text-xs-center">
    <v-app class="white">
      <router-view />
    </v-app>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {};
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
</style>
