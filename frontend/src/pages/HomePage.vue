<template>
  <v-card color="white" flat>
    <Header />

    <v-card class="fill-height">
      <v-sheet height="700"></v-sheet>
    </v-card>
    <!-- <Footer :fixed="true" />   -->
  </v-card>
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
