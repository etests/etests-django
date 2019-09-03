<template>
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
        <td>{{ props.item.maxMarks }}</td>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  props: ["report", "questionWise"],
  data() {
    return {
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
        }
      ]
    };
  },
  computed: {
    testName() {
      if (this.report) return this.report.test.name;
    },
    marks() {
      if (this.report) return this.report.marks;
      else return 0;
    },
    noOfSections() {
      if (this.report) return this.report.marks.maxMarks.length - 1;
    },
    sections() {
      if (this.report) return this.report.test.sections;
    },
    sectionWiseMarks() {
      if (this.report) return this.report.marks.sectionWise;
    },
    records() {
      var a = [];
      if (this.report) {
        for (var i = 0; i < this.sections.length; i++) {
          var b = { name: "", maxMarks: 0, score: 0 };
          b["name"] = this.sections[i]["subject"];
          b["maxMarks"] = this.marks.maxMarks[i];
          b["score"] = this.sectionWiseMarks[i];
          a.push(b);
        }
        a.push({
          name: "Total Marks",
          maxMarks: this.marks.maxMarks[this.marks.length - 1],
          score: this.marks.total
        });
      }
      return a;
    }
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/components';
.marksTable{
  width: 100%;
  border-radius: 8px;
  border: 1px solid #eee;
  td{
    width: 33%;
  }
  margin-bottom: 12px;
}
</style>
