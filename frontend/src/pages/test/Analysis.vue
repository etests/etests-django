<template>
  <div>
    {{ detailedReport }}
    <GChart
      style="width: 800px; height: 500px;"
      type="ColumnChart"
      :data="chartData"
      :options="chartOptions"
      :resizeDebounce="500"
    />
    <GChart
      style="width: 800px; height: 500px;"
      type="PieChart"
      :data="chartData"
      :options="chartOptions"
      :resizeDebounce="500"
    />
  </div>
</template>
<script src="vue-google-charts/dist/vue-google-charts.browser.js"></script>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import SectionLayout from "@components/layouts/SectionLayout";
import { GChart } from "vue-google-charts";

export default {
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
          title: "Company Performance",
          subtitle: "Sales, Expenses, and Profit: 2014-2017"
        }
      }
    };
  },
  created() {
    this.$store.dispatch("reviews/get", this.id);
  },
  computed: {
    detailedReport() {
      return this.$store.state.reviews.review;
    }
  },
  methods: {
    onChartReady(chart, google) {
      const query = new google.visualization.Query(
        "https://url-to-spreadsheet..."
      );
      query.send(response => {
        const options = {
          // some custom options
        };
        const data = response.getDataTable();
        chart.draw(data, options);
      });
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
</style>
