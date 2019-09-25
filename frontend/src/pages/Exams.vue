<template>
  <StandardLayout>
    <v-dialog
      v-if="selectedExam"
      v-model="examDialog"
      fullscreen
      hide-overlay
      transition="scale-transition"
    >
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon dark @click="examDialog = false">
            <v-icon>close</v-icon>
          </v-btn>
          <v-toolbar-title>
            {{ selectedExam.name }} Question Banks
          </v-toolbar-title>
        </v-toolbar>

        <v-layout row wrap align-center pa-3>
          <QuestionBankCard
            v-for="testSeries in selectedExam.test_series"
            :key="testSeries.id"
            :testSeries="testSeries"
            :outerParent="selectedExam.name"
          />
        </v-layout>
      </v-card>
    </v-dialog>
    <v-flex xs12 class="px-3">
      <v-text-field placeholder="Search Exams" v-model="searchExam" />
    </v-flex>

    <template v-if="status.loading">
      <LoadingCard v-for="i in 4" :key="i" />
    </template>
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
import QuestionBankCard from "./QuestionBankCard";
import LoadingCard from "@/components/layouts/LoadingCard";
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
    QuestionBankCard,
    LoadingCard
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
      status: state => state.exams.status,
      exams: state => state.exams.items
    })
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
  font-family: 'Montserrat Light', Roboto, Arial, sans-serif;
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
  margin: 20px;
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
