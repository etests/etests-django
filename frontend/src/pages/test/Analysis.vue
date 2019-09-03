<template>
  <div>
    <SectionLayout heading="Detailed Performance">
      <v-flex
        v-for="(performanceData, i) in topicwisePerformance"
        :key="i"
        xs12
        md6
        lg4
      >
        <GChart
          :class="$style.chart"
          type="ColumnChart"
          :data="performanceData"
          :options="chartOptions.chart"
          :resizeDebounce="500"
        />
      </v-flex>
    </SectionLayout>
    <SectionLayout heading="Topicwise score">
      <v-flex
        v-for="(sectionData, i) in this.topicWiseScore"
        :key="i"
        xs12
        md6
        lg4
      >
        <GChart
          v-if="sectionData.length > 1"
          :class="$style.chart"
          type="PieChart"
          :data="sectionData"
          :options="getOptions(i)"
          :resizeDebounce="500"
        />
      </v-flex>
    </SectionLayout>
    <SectionLayout heading="Topicwise weightage">
      <v-flex
        v-for="(sectionData, i) in this.topicWiseWeightage"
        :key="i"
        xs12
        md6
        lg4
      >
        <GChart
          v-if="sectionData.length > 1"
          :class="$style.chart"
          type="PieChart"
          :data="sectionData"
          :options="getOptions(i)"
          :resizeDebounce="500"
        />
      </v-flex>
    </SectionLayout>
  </div>
</template>
<script src="vue-google-charts/dist/vue-google-charts.browser.js"></script>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import SectionLayout from "@components/layouts/SectionLayout";
import { GChart } from "vue-google-charts";
import { subjectTopics } from "@js/subjects";

export default {
  props: ["report"],
  data() {
    return {
      id: this.$route.params.id,
      chartData: [
        ["Year", "Sales", "Expenses", "Profit"],
        ["2014", 1000, 400, 200],
        ["2015", 1170, 460, 250],
        ["2016", 660, 1120, 300],
        ["2017", 1030, 540, 350]
      ],
      chartOptions: {
        chart: {
          subtitle: "",
          legend: "none"
        }
      },
      sectionWiseNegativeMarks: []
    };
  },
  computed: {
    topics() {
      return subjectTopics.topics;
    },
    sections() {
      return this.report.test.sections;
    },
    topicWiseScoreBarData() {
      var data = new Array(this.report.test.sections.length);
      this.report.result.topicWiseMarks.forEach((section, i) => {
        data[i] = [];
        data[i].push(["Topic", "Marks"]);
        this.sectionWiseNegativeMarks.push([]);
        for (var prop in section) {
          data[i].push([
            this.topics[this.sections[i].subjectIndex][prop],
            section[prop]
          ]);
        }
      });
      return data;
    },
    topicWiseScore() {
      var data = new Array(this.report.test.sections.length);
      var questions = this.report.test.questions;
      var questionWiseMarks = this.report.result.questionWiseMarks;
      this.report.test.sections.forEach((section, i) => {
        data[i] = [];
        data[i].push(["Topic", "Maximum Marks"]);
        var scored = {};
        for (var j = section.start; j <= section.end; j++) {
          var topicIndex = questions[j].topicIndex;
          var score;
          if (Array.isArray(questionWiseMarks[j].marks))
            score = questionWiseMarks[j].marks.reduce((a, b) => a + b, 0);
          else score = questionWiseMarks[j].marks;
          if (scored.hasOwnProperty(topicIndex)) scored[topicIndex] += score;
          else scored[topicIndex] = score;
        }
        for (var prop in scored) {
          data[i].push([
            this.topics[this.sections[i].subjectIndex][prop],
            Math.max(scored[prop], 0)
          ]);
        }
      });

      return data;
    },
    topicWiseWeightage() {
      var data = new Array(this.report.test.sections.length);
      var questions = this.report.test.questions;
      this.report.test.sections.forEach((section, i) => {
        data[i] = [];
        data[i].push(["Topic", "Maximum Marks"]);
        var weightage = {};
        for (var j = section.start; j <= section.end; j++) {
          var topicIndex = questions[j].topicIndex;
          if (weightage.hasOwnProperty(topicIndex))
            weightage[topicIndex] += questions[j].correctMarks;
          else weightage[topicIndex] = questions[j].correctMarks;
        }
        for (var prop in weightage) {
          data[i].push([
            this.topics[this.sections[i].subjectIndex][prop],
            weightage[prop]
          ]);
        }
      });
      return data;
    },
    topicwisePerformance() {
      var data = new Array(this.report.test.sections.length);
      for (var i = 0; i < data.length; i++) {
        data[i] = [];
        data[i].push(["Topic", "Marks scored", "Maximum marks"]);
        for (var j = 1; j < this.topicWiseScore[i].length; j++) {
          data[i].push([
            this.topicWiseScore[i][j][0],
            this.topicWiseScore[i][j][1],
            this.topicWiseWeightage[i][j][1]
          ]);
        }
      }
      return data;
    }
  },
  methods: {
    getOptions(i) {
      return {
        title: this.report.test.sections[i].subject,
        legend: "none"
      };
    }
  },
  components: {
    StandardLayout,
    SectionLayout,
    GChart
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
.chart{
  width: 100%;
  height: 100%;
  min-height: 500px;
}
</style>
