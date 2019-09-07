<template>
  <StandardLayout>
    <v-layout row wrap>
      <SectionLayout heading="Test Series">
        <TestSeriesCard
          v-for="(testSeries, i) in allTestSeries"
          :key="i"
          :testSeries="testSeries"
        >
          <TestCard
            v-for="(test, j) in testSeries.tests"
            :key="j"
            :testSeries="testSeries"
            :test="test"
          />
          <TestCard :testSeries="testSeries" new />
        </TestSeriesCard>
        <TestSeriesCard new />
      </SectionLayout>

      <SectionLayout heading="Tests">
        <TestCard v-for="test in tests" :key="test.name" :test="test" />
        <TestCard new />
      </SectionLayout>
    </v-layout>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import SectionLayout from "@components/layouts/SectionLayout";
import TestSeriesCard from "@components/institute/tests/TestSeriesCard";
import TestCard from "@components/institute/tests/TestCard";

import ObjectCard from "@components/layouts/ObjectCard";

export default {
  data() {
    return {};
  },
  created() {
    this.fetchTestSeries();
    this.fetchTests();
  },
  computed: {
    allTestSeries() {
      return this.$store.state.testSeries.all.items;
    },
    tests() {
      return this.$store.state.tests.all.items;
    }
  },
  methods: {
    fetchTestSeries() {
      this.$store.dispatch("testSeries/getAll");
    },
    fetchTests() {
      this.$store.dispatch("tests/getAll");
    }
  },
  components: {
    StandardLayout,
    SectionLayout,
    TestSeriesCard,
    TestCard,
    ObjectCard
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
</style>
