<template>
  <StandardLayout>
    <v-flex xs12>
      <v-card class="elevation-0">
        <v-layout row wrap>
          <v-flex xs12 md8 lg10 class="pl-3">
            <v-text-field
              placeholder="Search Question Banks"
              v-model="searchTestSeries"
            />
            <v-spacer />
          </v-flex>
          <v-flex sm12 md4 lg2 v-if="loggedIn">
            <v-btn
              color="primary"
              round
              outline
              @click="$router.push(`/${user.type}/question-banks`)"
            >
              my question banks
            </v-btn>
          </v-flex>
        </v-layout>
        <v-layout row wrap align-center px-1>
          <template v-if="status.loading">
            <LoadingCard v-for="i in 4" :key="i" />
          </template>
          <QuestionBankCard
            v-for="testSeries in filteredTestSeries"
            :key="testSeries.id"
            :testSeries="testSeries"
          />
        </v-layout>
      </v-card>
    </v-flex>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";
import LoadingCard from "@/components/layouts/LoadingCard";
import QuestionBankCard from "./QuestionBankCard";
import { mapState } from "vuex";
import utils from "@/js/utils";

export default {
  data() {
    return {
      searchTestSeries: "",
      filteredTestSeries: [],
      selectedTestSeries: {}
    };
  },
  components: {
    StandardLayout,
    QuestionBankCard,
    LoadingCard
  },
  created() {
    this.$store.dispatch("testSeries/getAll");
  },
  watch: {
    searchTestSeries: function(newValue, oldValue) {
      this.filteredTestSeries = this.testSeriesList.filter(testSeries =>
        testSeries.name.toLowerCase().includes(newValue)
      );
    },
    testSeriesList: function(newList, oldList) {
      if (!this.filteredTestSeries || this.filteredTestSeries.length === 0)
        this.filteredTestSeries = this.testSeriesList;
    }
  },
  computed: {
    ...mapState({
      status: state => state.testSeries.status,
      loggedIn: state => state.authentication.status.loggedIn,
      user: state => state.authentication.user
    }),
    testSeriesList() {
      return this.$store.state.testSeries.all.items;
    }
  },
  mounted() {}
};
</script>

<style module lang="stylus">
.card {
  text-align: center;
  border-radius: 8px;
  height: 220px;
  width: 270px;
  margin: 10px;
  cursor: pointer;
}

.dialog {
  border: 1px solid #dadce0;
  border-radius: 5px;
  font-family: 'Product Sans Light', Roboto, Arial, sans-serif;
  text-align: left;

  .title {
    font-size: 1.375rem;
    line-height: 1.75rem;
    color: #5e5766;
  }
}

.content {
  padding: 20px;
  min-height: 160px;
  background-color: #fafafa;
  border-radius: 8px 8px 0 0;
  text-align: left;

  &:hover {
    background-color: #f5f5f5;
  }
}

.title {
  text-align: left;
  font-size: 1.375rem;
  line-height: 1.75rem;
  color: #7e777e;
}
</style>
