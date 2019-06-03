<template>
  <v-container fluid>
    <Header :disableDrawerClose="true" />
    <v-content app>
      <div style="max-width: 80%; margin: auto;">
        <v-container fluid grid-list-lg>
          <v-layout row wrap>
            <v-flex xs4>
              <v-card>
                <v-layout>
                  <v-flex xs5>
                    <v-icon x-large>
                      mdi-account
                    </v-icon>
                  </v-flex>
                  <v-flex xs7>
                    <v-card-title primary-title>
                      <div>
                        <div class="title">Your Profile</div>
                      </div>
                    </v-card-title>
                  </v-flex>
                </v-layout>
                <v-divider light></v-divider>
                <v-card-actions class="pa-3">
                  <v-spacer></v-spacer>
                  <v-btn color="info" to="profile">Go</v-btn>
                </v-card-actions>
              </v-card>
            </v-flex>

            <v-flex xs4>
              <v-card>
                <v-layout>
                  <v-flex xs5>
                    <v-icon x-large>
                      mdi-monitor-screenshot
                    </v-icon>
                  </v-flex>
                  <v-flex xs7>
                    <v-card-title primary-title>
                      <div>
                        <div class="title">Upcoming Tests</div>
                      </div>
                    </v-card-title>
                  </v-flex>
                </v-layout>
                <v-divider light></v-divider>
                <v-card-actions class="pa-3">
                  <v-spacer></v-spacer>
                  <v-btn color="info" to="schedule">Go</v-btn>
                </v-card-actions>
              </v-card>
            </v-flex>

            <v-flex xs4>
              <v-card>
                <v-layout>
                  <v-flex xs5>
                    <v-icon x-large>
                      mdi-chart-line
                    </v-icon>
                  </v-flex>
                  <v-flex xs7>
                    <v-card-title primary-title>
                      <div>
                        <div class="title">Progress Report</div>
                      </div>
                    </v-card-title>
                  </v-flex>
                </v-layout>
                <v-divider light></v-divider>
                <v-card-actions class="pa-3">
                  <v-spacer></v-spacer>
                  <v-btn color="info" to="report">Go</v-btn>
                </v-card-actions>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </div>
      <Footer />
    </v-content>
  </v-container>
</template>

<script>
import Header from "@components/Header.vue";
import Footer from "@components/Footer.vue";

export default {
  data() {
    return {};
  },
  components: {
    Header,
    Footer
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

.logo{
  width: 40px;
  float: left;
  margin: 0 5px;
}
</style>
