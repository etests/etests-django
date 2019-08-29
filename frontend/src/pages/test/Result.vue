<template>
  <WideLayout>
    <v-layout column align-center v-if="marks">
      <v-flex xs12>
        <v-card :class="[$style.card, $style.message]">
          You got {{ marks.total }}/{{
            marks.max_marks[marks.max_marks.length - 1]
          }}
        </v-card>
      </v-flex>
      <v-flex xs12>
        <Analysis v-if="this.report && this.report.result" />
        <v-card v-else :class="[$style.card, $style.message]">
          Analysis of your test is not generated yet.
        </v-card>
      </v-flex>
    </v-layout>
  </WideLayout>
</template>

<script>
import WideLayout from "@components/layouts/WideLayout";
import Analysis from "./Analysis";

export default {
  data() {
    return {
      id: this.$route.params.id
    };
  },
  components: {
    WideLayout,
    Analysis
  },
  computed: {
    report() {
      return this.$store.state.results.result;
    },
    marks() {
      if (this.report) return this.report.marks;
      else return 0;
    }
  },
  created() {
    this.$store.dispatch("results/get", this.id);
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/components';
</style>
