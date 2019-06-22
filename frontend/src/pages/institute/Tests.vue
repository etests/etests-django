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

      <SectionLayout heading="Unit Tests">
        <UnitTestCard
          v-for="(unitTest, i) in unitTests"
          :key="i"
          :test="unitTest"
        />
        <UnitTestCard new />
      </SectionLayout>
    </v-layout>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import SectionLayout from "@components/layouts/SectionLayout";
import TestSeriesCard from "@components/testLayouts/TestSeriesCard";
import TestCard from "@components/testLayouts/TestCard";
import UnitTestCard from "@components/testLayouts/UnitTestCard";
import ObjectCard from "@components/testLayouts/ObjectCard";

export default {
  data() {
    return {};
  },
  created() {
    this.fetchTestSeries();
    this.fetchUnitTests();
  },
  computed: {
    allTestSeries() {
      return this.$store.state.testSeries.all.items;
    },
    unitTests() {
      return this.$store.state.unitTests.all.items;
    }
  },
  methods: {
    fetchTestSeries() {
      this.$store.dispatch("testSeries/getAll");
    },
    fetchUnitTests() {
      this.$store.dispatch("unitTests/getAll");
    }
  },
  components: {
    StandardLayout,
    SectionLayout,
    TestSeriesCard,
    TestCard,
    UnitTestCard,
    ObjectCard
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
</style>
