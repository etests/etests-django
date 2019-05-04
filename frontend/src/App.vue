<template>
  <div id="app" class="text-xs-center">
    <v-app>
      <router-view />
    </v-app>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {}
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
</style>
