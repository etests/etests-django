<template>
  <router-view></router-view>
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
</style>
