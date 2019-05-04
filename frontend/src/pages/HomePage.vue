<template>
  <v-toolbar light color="white">
    <img src="~@assets/logos/etests.png" :class="$style.logo" />

    <v-toolbar-title class="secondary--text">eTests</v-toolbar-title>

    <v-spacer />

    <v-btn icon>
      <v-icon>search</v-icon>
    </v-btn>

    <v-menu bottom left>
      <template v-slot:activator="{ on }">
        <v-btn icon v-on="on">
          <v-icon>more_vert</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-tile v-for="(item, i) in items" :key="i" @click="">
          <v-list-tile-title>{{ item.title }}</v-list-tile-title>
        </v-list-tile>
      </v-list>
    </v-menu>
  </v-toolbar>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      title: "eTests",
      slogan: "an online testing platform",
      items: [{ title: "Login" }, { title: "Register" }]
    };
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

.logo{
  width: 50px;
}
</style>
