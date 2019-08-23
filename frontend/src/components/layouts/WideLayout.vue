<template>
  <v-container fluid>
    <Header :temporaryDrawer="true" />
    <v-content app>
      <v-container fluid grid-list-lg>
        <v-layout row wrap class="mb-4">
          <slot></slot>
        </v-layout>
      </v-container>
      <Footer />
    </v-content>
  </v-container>
</template>

<script>
import Header from "@components/Header.vue";
import Footer from "@components/Footer.vue";

export default {
  data() {
    return {};
  },
  components: {
    Header,
    Footer
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

.logo{
  width: 40px;
  float: left;
  margin: 0 5px;
}
</style>
