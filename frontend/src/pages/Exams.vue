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
              <div :class="$style.title">
                {{ test.name }}
                <br />
              </div>
              <v-divider class="my-3" />
              <v-icon color="blue" small>mdi-calendar</v-icon>
              {{ formatDate(test.activation_time) }}
            </div>
            <div slot="actions">
              <v-card-actions>
                <v-layout row fill-height py-2>
                  <v-flex xs4>
                    <v-btn large color="primary" flat round>{{ test.time_alotted }}</v-btn>
                  </v-flex>
                </v-layout>
              </v-card-actions>
            </div>
          </ObjectCard>
        </v-layout>
      </v-card>
    </v-dialog>
    <v-dialog
      v-if="selectedExam"
      v-model="examDialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon dark @click="examDialog = false">
            <v-icon>close</v-icon>
          </v-btn>
          <v-toolbar-title>{{ selectedExam.name }} Question Banks</v-toolbar-title>
        </v-toolbar>

        <v-layout row wrap align-center pa-3>
          <ObjectCard v-for="testSeries in selectedExam.test_series" :key="testSeries.id">
            <div slot="content" :class="$style.content">
              <div :class="$style.title">
                {{ testSeries.name }}
                <br />
                <span class="body-1 mx-1">{{ testSeries.institute.name }}</span>
              </div>
              <v-divider class="my-3" />
              <v-icon color="blue" small>mdi-file-outline</v-icon>
              {{ testSeries.tests.length }} tests
            </div>
            <div slot="actions">
              <v-card-actions>
                <v-layout row fill-height py-2>
                  <v-flex xs4>
                    <v-btn large color="blue" flat>&#8377; {{ testSeries.price }}</v-btn>
                  </v-flex>

                  <v-flex xs4>
                    <v-btn round outline color="primary">Buy</v-btn>
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
                    >View</v-btn>
                  </v-flex>
                </v-layout>
              </v-card-actions>
            </div>
          </ObjectCard>
        </v-layout>
      </v-card>
    </v-dialog>
    <v-flex xs12>
      <v-text-field placeholder="Search Exams" v-model="searchExam" />
    </v-flex>

    <v-card
      v-for="exam in filteredExams"
      :key="exam.id"
      @click="
        selectedExam = exam;
        examDialog = true;
      "
      :class="$style.card"
    >
      <v-img
        class="white--text"
        height="170px"
        :src="require(`@/assets/images/exams/${exam.image}`)"
      />
      <v-card-title class="subheading">{{ exam.name }}</v-card-title>
    </v-card>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";
import ObjectCard from "@/components/layouts/ObjectCard";
import { mapState } from "vuex";
import utils from "@/js/utils";

export default {
  data() {
    return {
      examDialog: false,
      viewDialog: false,
      searchExam: "",
      filteredExams: [],
      followDialog: false,
      selectedTestSeries: {},
      selectedExam: {}
    };
  },
  components: {
    StandardLayout,
    ObjectCard
  },
  created() {
    this.$store.dispatch("exams/getAll");
  },
  watch: {
    searchExam: function(newValue, oldValue) {
      this.filteredExams = this.exams.filter(exam =>
        exam.name.toLowerCase().includes(newValue)
      );
    },
    exams: function(newList, oldList) {
      if (this.filteredExams.length === 0) this.filteredExams = this.exams;
    }
  },
  computed: {
    ...mapState({
      status: state => state.exams.status
    }),
    exams() {
      return this.$store.state.exams.items;
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
@require '~@/stylus/theme/colors';

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

.card {
  text-align: center;
  border-radius: 8px;
  height: 220px;
  width: 270px;
  margin: 10px;
  cursor: pointer;
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
