<template>
  <StandardLayout>
    <v-card class="mb-2 px-5" width="300" height="300" style="margin:auto">
      <v-card-text class="body1 primary--text">
        <span v-if="user" class="text-xs-center">Hello {{ user.name }}!</span>
        <span v-else class="text-xs-center">Welcome!</span>
      </v-card-text>
      <img src="~@assets/logos/etests.png" width="200" />
    </v-card>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";

export default {
  data() {
    return {};
  },
  components: {
    StandardLayout
  },
  computed: {
    auth() {
      return this.$store.state.authentication.auth;
    },
    user() {
      if (this.auth) return this.auth.user;
      else return null;
    }
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
