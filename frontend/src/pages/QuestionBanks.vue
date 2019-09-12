<template>
  <StandardLayout>
    <v-dialog
      v-if="selectedTestSeries"
      v-model="viewDialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon dark @click="viewDialog = false">
            <v-icon>close</v-icon>
          </v-btn>
          <v-toolbar-title>{{ selectedTestSeries.name }}</v-toolbar-title>
        </v-toolbar>
        <v-layout row wrap align-center pa-3>
          <ObjectCard v-for="test in selectedTestSeries.tests" :key="test.id">
            <div slot="content" :class="$style.content">
              <v-card-title :class="$style.title">
                {{ test.name }}
              </v-card-title>
              <v-divider class="mb-3 mx-3" />
              <v-icon color="blue" class="ml-3" small>mdi-calendar</v-icon>
              {{ formatDate(test.activation_time) }}
            </div>
            <div slot="actions">
              <v-card-actions>
                <v-layout row fill-height py-2>
                  <v-flex xs4>
                    <v-btn large color="primary" flat round>
                      {{ test.time_alotted }}
                    </v-btn>
                  </v-flex>
                </v-layout>
              </v-card-actions>
            </div>
          </ObjectCard>
        </v-layout>
      </v-card>
    </v-dialog>

    <v-flex xs12>
      <v-card class="elevation-0">
        <v-card-title class="title">
          Question Banks
          <v-spacer />
          <div v-if="loggedIn">
            <v-btn
              color="primary"
              round
              outline
              @click="$router.push(`/${user.type}/question-banks`)"
            >
              See purchased question banks
            </v-btn>
          </div>
        </v-card-title>
        <v-flex xs12 class="px-3">
          <v-text-field
            placeholder="Search Question Banks"
            v-model="searchTestSeries"
          />
        </v-flex>
        <v-flex xs12 class="px-3">
          <ObjectCard
            v-for="testSeries in filteredTestSeries"
            :key="testSeries.id"
          >
            <div slot="content" :class="$style.content">
              <div :class="$style.title">
                {{ testSeries.name }} <br />
                <span class="body-1 mx-1">{{ testSeries.institute.name }}</span>
              </div>
              <v-divider class="my-3" />
              <v-icon color="blue" small>mdi-file-outline</v-icon>
              {{ testSeries.tests.length }} tests ({{ testSeries.exam }})
            </div>
            <div slot="actions">
              <v-card-actions>
                <v-layout row fill-height py-2>
                  <v-flex xs4>
                    <v-btn large color="blue" flat>
                      &#8377; {{ testSeries.price }}
                    </v-btn>
                  </v-flex>

                  <v-flex xs4>
                    <v-btn round outline color="primary" v-if="loggedIn">
                      Buy
                    </v-btn>
                  </v-flex>
                  <v-flex xs4>
                    <v-btn
                      round
                      outline
                      color="primary"
                      @click="
                        selectedTestSeries = testSeries;
                        viewDialog = true;
                      "
                    >
                      View
                    </v-btn>
                  </v-flex>
                </v-layout>
              </v-card-actions>
            </div>
          </ObjectCard>
        </v-flex>
      </v-card>
    </v-flex>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import ObjectCard from "@components/layouts/ObjectCard";
import { mapState } from "vuex";
import utils from "@js/utils";

export default {
  data() {
    return {
      viewDialog: false,
      searchTestSeries: "",
      filteredTestSeries: [],
      followDialog: false,
      selectedTestSeries: {}
    };
  },
  components: {
    StandardLayout,
    ObjectCard
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
      status: state => state.testSeriesList.status,
      loggedIn: state => state.authentication.status.loggedIn,
      user: state => state.users.user
    }),
    testSeriesList() {
      return this.$store.state.testSeries.all.items;
    }
  },
  methods: {
    formatDate(dateString) {
      return utils.formatDate(dateString);
    }
  },
  mounted() {}
};
</script>

<style module lang="stylus">
.card{
    text-align: center;
    border-radius: 8px;
    height: 220px;
    width: 270px;
    margin: 10px;
    cursor: pointer;
}

.dialog{
  border: 1px solid #dadce0;
  border-radius: 5px;
  font-family: 'Product Sans Light',Roboto,Arial,sans-serif;
  text-align: left;
  .title{
    font-size: 1.375rem;
    line-height: 1.75rem;
    color: #5e5766;
  }
}

.content{
  padding: 20px;
  min-height: 160px;
  background-color: #fafafa;
  border-radius: 8px 8px 0 0;
  text-align: left;
  &:hover{
      background-color: #f5f5f5;
  }
}
.title{
  text-align: left;
  font-size: 1.375rem;
  line-height: 1.75rem;
  color: #7e777e;
}
</style>
