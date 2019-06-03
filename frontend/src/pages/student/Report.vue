<template>
  <v-container fill-height fluid grid-list-xl>
    <Header :disableDrawerClose="true" />
    <v-content app>
      <v-layout wrap>
        <v-flex md12 sm12 lg4>
          <v-card color="white px-2 py-2">
            <h4 class="title font-weight-light">Percentile</h4>
            <chartist
              :data="percentileChart.data"
              :options="percentileChart.options"
              type="Line"
            />
            <p class="category d-inline-flex font-weight-light">
              <v-icon color="green" small>
                mdi-arrow-up
              </v-icon>
              <span class="green--text">19.5%</span>&nbsp; increase in your
              percentile
            </p>

            <template slot="actions">
              <v-icon class="mr-2" small>
                mdi-clock-outline
              </v-icon>
              <span class="caption grey--text font-weight-light"
                >updated 4 minutes ago</span
              >
            </template>
          </v-card>
        </v-flex>
        <v-flex md12 sm12 lg4>
          <v-card color="white px-2 py-2">
            <h4 class="title font-weight-light">Percentage Marks</h4>
            <chartist
              :data="marksChart.data"
              :options="marksChart.options"
              :responsive-options="marksChart.responsiveOptions"
              type="Bar"
            />
            <p class="category d-inline-flex font-weight-light">
              Last year performance
            </p>

            <template slot="actions">
              <v-icon class="mr-2" small>
                mdi-clock-outline
              </v-icon>
              <span class="caption grey--text font-weight-light"
                >updated 10 minutes ago</span
              >
            </template>
          </v-card>
        </v-flex>
        <v-flex md12 sm12 lg4>
          <v-card color="white px-2 py-2">
            <h3 class="title font-we ight-light">
              Time elapsed per question
            </h3>
            <chartist
              :data="dataCompletedTasksChart.data"
              :options="dataCompletedTasksChart.options"
              type="Line"
            />
            <p class="category d-inline-flex font-weight-light">
              Last test performance
            </p>
          </v-card>
        </v-flex>
        <v-flex xs12>
          <v-card class="card-tabs" color="success">
            <v-flex>
              <v-tabs v-model="tabs" color="transparent" dark hide-slider>
                <v-tab class="mr-3">
                  <v-icon class="mr-2">mdi-atom</v-icon>
                  Physics
                </v-tab>
                <v-tab class="mr-3">
                  <v-icon class="mr-2">mdi-test-tube</v-icon>
                  Chemistry
                </v-tab>
                <v-tab>
                  <v-icon class="mr-2">mdi-math-compass</v-icon>
                  Maths
                </v-tab>
              </v-tabs>
            </v-flex>

            <v-tabs-items v-model="tabs">
              <v-tab-item v-for="n in 3" :key="n">
                <v-list three-line>
                  <v-list-tile @click="complete(0)">
                    <v-list-tile-title>
                      Less than average in thermodynamics.
                    </v-list-tile-title>
                    <div class="d-flex">
                      <v-tooltip top content-class="top">
                        <v-btn slot="activator" class="v-btn--simple" icon>
                          <v-icon color="error">mdi-close</v-icon>
                        </v-btn>
                        <span>Close</span>
                      </v-tooltip>
                    </div>
                  </v-list-tile>
                </v-list>
              </v-tab-item>
            </v-tabs-items>
          </v-card>
        </v-flex>
      </v-layout>
    </v-content>
  </v-container>
</template>

<script>
import Header from "@components/Header.vue";
import Footer from "@components/Footer.vue";

export default {
  data() {
    return {
      percentileChart: {
        data: {
          labels: ["M", "T", "W", "T", "F", "S", "S"],
          series: [[82, 87, 97, 99, 95, 91, 98]]
        },
        options: {
          lineSmooth: this.$chartist.Interpolation.cardinal({
            tension: 0
          }),
          low: 80,
          high: 100,
          chartPadding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0
          }
        }
      },
      dataCompletedTasksChart: {
        data: {
          labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
          series: [[2, 7, 4, 3, 2, 6, 3, 1, 2, 2]]
        },
        options: {
          lineSmooth: this.$chartist.Interpolation.cardinal({
            tension: 0
          }),
          low: 0,
          high: 10,
          chartPadding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0
          }
        }
      },
      marksChart: {
        data: {
          labels: [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec"
          ],
          series: [[54, 44, 32, 78, 55, 45, 32, 43, 56, 61, 75, 89]]
        },
        options: {
          axisX: {
            showGrid: false
          },
          low: 0,
          high: 100,
          chartPadding: {
            top: 0,
            right: 5,
            bottom: 0,
            left: 0
          }
        },
        responsiveOptions: [
          [
            "screen and (max-width: 640px)",
            {
              seriesBarDistance: 5,
              axisX: {
                labelInterpolationFnc: function(value) {
                  return value[0];
                }
              }
            }
          ]
        ]
      },
      tabs: 0,
      list: {
        0: false,
        1: false,
        2: false
      }
    };
  },
  components: {
    Header,
    Footer
  },
  methods: {
    complete(index) {
      this.list[index] = !this.list[index];
    }
  }
};
</script>
