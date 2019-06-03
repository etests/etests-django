<template>
  <v-container fluid>
    <Header :disableDrawerClose="true" />
    <v-content app>
      <v-card class="px-2 py-2 mb-2" width="420" style="margin:auto">
        <img src="~@assets/logos/etests.png" width="400" />
      </v-card>
      <Footer />
    </v-content>
  </v-container>
</template>

<script>
import Header from "@components/Header.vue";
import Footer from "@components/Footer.vue";

export default {
  data() {
    return {
      select: ["Vuetify", "Programming"],
      items: ["Programming", "Design", "Vue", "Vuetify"],
      subjects: ["Physics", "Chemistry", "Maths"],
      tabs: null
    };
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
