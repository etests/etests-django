<template>
  <v-layout>
    <v-content app class="my-0 py-0">
      <Header
        :temporaryDrawer="true"
        :disableDrawerClose="true"
        :showSearchBar="false"
      >
      </Header>
      <v-layout row wrap class="mb-4 mx-0 px-0">
        <slot></slot>
      </v-layout>
    </v-content>
  </v-layout>
</template>

<script>
import Header from "@/components/Header.vue";

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
@require '~@/stylus/theme/colors';

body{
  margin: 0;
  padding: 0;
}

.logo{
  width: 40px;
  float: left;
  margin: 0 5px;
}
</style>
