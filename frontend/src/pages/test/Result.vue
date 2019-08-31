<template>
  <StandardLayout>
    <v-layout column align-center v-if="marks">
      <v-flex xs12>
        <Marks :report="report" />
        <Analysis v-if="report && report.result" />
        <v-card v-else :class="[$style.card, $style.message]">
          Analysis of your test is not generated yet.{{ report }}
        </v-card>
      </v-flex>
    </v-layout>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import Analysis from "./Analysis";
import Marks from "./Marks";

export default {
  data() {
    return {
      id: this.$route.params.id
    };
  },
  components: {
    StandardLayout,
    Analysis,
    Marks
  },
  computed: {
    report() {
      return this.$store.state.results.result;
    }
  },
  created() {
    this.$store.dispatch("results/get", this.id);
  }
};
</script>
