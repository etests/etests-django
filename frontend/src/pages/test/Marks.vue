<template>
  <v-card :class="[$style.marksTable, 'title']">
    <v-card-title>
      {{ testName.toUpperCase() }}
      <v-spacer />
      <v-btn
        round
        outline
        color="primary"
        v-if="report.result"
        @click="$emit('review')"
      >
        Review
      </v-btn>
    </v-card-title>
    <v-data-table :headers="headers" :items="records" hide-actions>
      <template v-slot:items="props">
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.score }}</td>
        <td>{{ props.item.maxMarks }}</td>
        <td>{{ props.item.rank }}</td>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  props: {
    report: {
      required: true,
      type: Object
    },
    demo: {
      required: false,
      default: false
    }
  },
  data() {
    return {
      reviewing: false,
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
          sortable: false
        },
        {
          text: "Maximum Marks",
          value: "maxMarks",
          align: "center",
          sortable: false
        },
        {
          text: "Rank",
          value: "rank",
          align: "center",
          sortable: false
        }
      ]
    };
  },
  computed: {
    testName() {
      if (this.report) return this.report.test.name;
      else return "";
    },
    marks() {
      if (this.report) return this.report.marks;
      else return 0;
    },
    noOfSections() {
      if (this.report) return this.report.marks.maxMarks.length - 1;
      else return 0;
    },
    sections() {
      if (this.report) return this.report.test.sections;
      else return {};
    },
    sectionWiseMarks() {
      if (this.report) return this.report.marks.sectionWise;
      else return {};
    },
    records() {
      var a = [];
      if (this.report) {
        for (var i = 0; i < this.sections.length; i++) {
          var b = { name: "", maxMarks: 0, score: 0 };
          b["name"] = this.sections[i]["subject"];
          b["maxMarks"] = this.marks.maxMarks[i];
          b["score"] = this.sectionWiseMarks[i];
          b["rank"] = this.report.ranks
            ? this.report.ranks.sectionWise[i]
            : "-";
          a.push(b);
        }
        a.push({
          name: "Total Marks",
          maxMarks: this.marks.maxMarks[this.marks.length - 1],
          score: this.marks.total,
          rank: this.report.ranks ? this.report.ranks.overall : "Not Applicable"
        });
      }
      return a;
    }
  }
};
</script>

<style module lang="stylus">
@require '~@/stylus/components';
.marksTable{
  width: 100%;
  border-radius: 8px;
  border: 1px solid #eee;
  td{
    width: 25%;
  }
  margin-bottom: 12px;
}
</style>
