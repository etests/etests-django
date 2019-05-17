<template>
  <v-container fluid>
    <Header :disableDrawerClose="true" />
    <v-content app>
      <span v-if="user">Hello {{ user.name }}!</span>
      <v-card class="px-2 py-2 mb-2" width="420" style="margin:auto">
        <img src="~@assets/logos/etests.png" width="400" />
      </v-card>
      <Footer />
    </v-content>
    <Header />
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
  },
  computed: {
    auth() {
      return this.$store.state.authentication.auth;
    },
    user() {
      if (this.auth) return this.auth.user;
      else return null;
    }
  },
  created() {}
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
