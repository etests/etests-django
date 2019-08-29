<template>
  <StandardLayout>
    <v-layout column align-center v-if="marks">
      <v-flex xs12>
        <v-card :class="[$style.marksTable, 'title']">
          <v-card-title>
            {{ testName.toUpperCase() }}
            <v-spacer />
            {{ report.test.time_alotted }}
          </v-card-title>
          <v-data-table :headers="headers" :items="records" hide-actions>
            <template v-slot:items="props">
              <td>{{ props.item.name }}</td>
              <td>{{ props.item.score }}</td>
              <td>{{ props.item.max_marks }}</td>
            </template>
          </v-data-table>
        </v-card>
        <Analysis v-if="this.report && this.report.result" />
        <v-card v-else :class="[$style.card, $style.message]">
          Analysis of your test is not generated yet.
        </v-card>
      </v-flex>
    </v-layout>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import Analysis from "./Analysis";

export default {
  data() {
    return {
      id: this.$route.params.id,
      headers: [
        {
          text: "Subjects",
          align: "center",
          sortable: false,
          value: "name"
        },
        {
          text: "Marks Scored",
          value: "score",
          align: "center",
          sortable: true
        },
        {
          text: "Maximum Marks",
          value: "total_marks",
          align: "center",
          sortable: false
        }
      ]
    };
  },
  components: {
    StandardLayout,
    Analysis
  },
  computed: {
    report() {
      return this.$store.state.results.result;
    },
    marks() {
      if (this.report) return this.report.marks;
      else return 0;
    },
    noOfSections() {
      if (this.report) return this.report.marks.max_marks.length - 1;
    },
    testName() {
      if (this.report) return this.report.test.name;
    },
    sections() {
      if (this.report) return this.report.test.sections;
    },
    sectionWiseMarks() {
      if (this.report) return this.report.marks.sectionwise;
    },
    records() {
      var a = [];
      var b = { name: "", total_marks: 0, score: 0 };
      if (this.report) {
        for (var i = 0; i < this.noOfSections; i++) {
          b["name"] = this.sections[i]["subject"];
          b["max_marks"] = this.marks.max_marks[i];
          b["score"] = this.sectionWiseMarks[i];
          a.push(b);
        }
        a.push({
          name: "Total Marks",
          max_marks: this.marks.max_marks[this.marks.max_marks.length - 1],
          score: this.marks.total
        });
      }
      return a;
    }
  },
  created() {
    this.$store.dispatch("results/get", this.id);
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/components';
.marksTable{
  border-radius: 8px;
  border: 1px solid #eee;
  td{
    width: 33%;
  }
  margin-bottom: 12px;
}
</style>
