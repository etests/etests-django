<template>
  <WideLayout>
    <v-layout column v-if="tests">
      <v-flex xs12 v-for="test in tests" :key="test.id">
        <v-card :class="$style.testCard">{{ test.name }}</v-card>
      </v-flex>
    </v-layout>
  </WideLayout>
</template>

<script>
import WideLayout from "@components/layouts/WideLayout";

export default {
  data() {
    return {};
  },
  components: {
    WideLayout
  },
  created() {
    this.$store.dispatch("tests/getAll");
  },
  computed: {
    tests() {
      return this.$store.state.tests.all.items;
    }
  }
};
</script>

<style module lang="stylus">
.testCard{
    text-align: left;
    border: 1px solid #c9cbd0;
    border-radius: 8px;
    height: 50px;
    padding: 10px;
    font-family: "Product Sans Light";
    font-size: 14pt;
}
</style>
