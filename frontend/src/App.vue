<template>
  <div id="app" class="text-xs-center">
    <v-app class="white">
      <router-view />
    </v-app>
  </div>
</template>

<script>
export default {
  name: "app"
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
</style>
