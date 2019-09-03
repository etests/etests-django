<template>
  <StandardLayout>
    {{ report }}
    <v-layout column align-center v-if="report">
      <SectionLayout heading="Subjectwise Marks">
        <v-flex xs12>
          <Marks :report="report" />
          <Analysis v-if="report && report.result" :report="report" />
          <v-card v-else :class="[$style.card, $style.message]">
            Analysis of your test is not generated yet.
          </v-card>
        </v-flex>
      </SectionLayout>
    </v-layout>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import SectionLayout from "@components/layouts/SectionLayout";
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
    SectionLayout,
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
<style module lang="stylus">
@require '~@stylus/components';
</style>
