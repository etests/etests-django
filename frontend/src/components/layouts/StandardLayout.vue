<template>
  <v-container fluid class="mt-4">
    <Header
      :temporaryDrawer="true"
      :disableDrawerClose="true"
      :showSearchBar="false"
    >
    </Header>
    <v-content app class="my-0 py-4">
      <v-layout column wrap :class="[$style.layout, 'mb-4 mt-4 pb-4']">
        <slot></slot>
      </v-layout>
    </v-content>
  </v-container>
</template>

<script>
import Header from "@components/Header.vue";

export default {
  data() {
    return {};
  },
  components: {
    Header
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

body{
  margin: 0;
  padding: 0;
}

.layout{
  font-family: "Product Sans Light";
}

.logo{
  width: 40px;
  float: left;
  margin: 0 5px;
}
</style>
