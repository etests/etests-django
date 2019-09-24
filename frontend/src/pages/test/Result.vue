<template>
  <Review :report="report" v-if="report && reviewing" />
  <StandardLayout v-else>
    <v-layout column align-center v-if="report">
      <SectionLayout heading="Subjectwise Marks">
        <v-flex xs12>
          <Marks :report="report" @review="reviewing = true" />
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
import StandardLayout from "@/components/layouts/StandardLayout";
import SectionLayout from "@/components/layouts/SectionLayout";
import Review from "./Review";
import Analysis from "./Analysis";
import Marks from "./Marks";

export default {
  props: {
    review: {
      required: false,
      default: false,
      type: Boolean
    }
  },
  data() {
    return {
      id: parseInt(this.$route.params.id),
      reviewing: this.review
    };
  },
  components: {
    StandardLayout,
    SectionLayout,
    Review,
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
@require '~@/stylus/components';
</style>
