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
            :test="test"
          />
          <CreateNewCard objectType="Test" />
        </TestSeriesCard>
        <CreateNewCard objectType="Test Series" />
      </SectionLayout>

      <SectionLayout heading="Unit Tests">
        <TestCard
          v-for="(unitTest, i) in unitTests"
          :key="i"
          :test="unitTest"
        />
        <CreateNewCard objectType="Unit Test" />
      </SectionLayout>
    </v-layout>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import SectionLayout from "@components/layouts/SectionLayout";
import TestSeriesCard from "@components/testLayouts/TestSeriesCard";
import TestCard from "@components/testLayouts/TestCard";
import CreateNewCard from "@components/testLayouts/CreateNewCard";

export default {
  data() {
    return {};
  },
  created() {
    this.$store.dispatch("testSeries/getAll");
    this.$store.dispatch("tests/getAll");
    this.$store.dispatch("unitTests/getAll");
  },
  computed: {
    allTestSeries() {
      return this.$store.state.testSeries.all.items;
    },
    tests() {
      return this.$store.state.tests.all.items;
    },
    unitTests() {
      return this.$store.state.unitTests.all.items;
    }
  },
  components: {
    StandardLayout,
    SectionLayout,
    TestSeriesCard,
    TestCard,
    CreateNewCard
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
</style>
