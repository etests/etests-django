<template>
  <v-layout>
    <v-content app class="my-0 py-0">
      <Header
        :temporaryDrawer="true"
        :disableDrawerClose="true"
        :showSearchBar="false"
      >
      </Header>
      <v-layout class="grey lighten-4">
        <v-container grid-list-xs fluid>
          <v-layout row justify-center wrap mx-auto>
            <v-flex xs12 md4>
              <v-card :class="[$style.dashboardCard, 'px-4 py-4']">
                <v-btn
                  style="width:100%; margin: 15px auto"
                  round
                  color="primary"
                  large
                  depressed
                >
                  <v-icon left large>laptop</v-icon>
                  Dashboard
                </v-btn>
                <v-img
                  src="https://picsum.photos/id/11/500/300"
                  lazy-src="https://picsum.photos/id/11/10/6"
                  aspect-ratio="1"
                  class="grey lighten-2"
                  style="max-height:200px;"
                ></v-img>
                <v-divider class="my-3"></v-divider>
                <v-flex xs12 md12 class="pb-4">
                  <v-sheet>
                    <v-list>
                      <v-list-tile
                        v-for="item in student.basic.items"
                        :key="item.title"
                      >
                        <v-layout row align-center wrap>
                          <v-flex xs2>
                            <v-list-tile-action>
                              <v-icon>{{ item.icon }}</v-icon>
                            </v-list-tile-action>
                          </v-flex>

                          <v-flex xs4>
                            <v-list-tile-content>
                              <v-list-tile-title>
                                {{ item.title }}
                              </v-list-tile-title>
                            </v-list-tile-content>
                          </v-flex>

                          <v-flex xs6>
                            <v-list-tile-content>
                              <span style="padding-left:9px;" v-if="!editing">{{
                                item.detail
                              }}</span>
                              <span v-else>
                                <input
                                  :class="$style.textbox"
                                  type="text"
                                  v-model="item.detail"
                                />
                              </span>
                            </v-list-tile-content>
                          </v-flex>
                        </v-layout>
                      </v-list-tile>
                    </v-list>
                    <v-layout mt-4>
                      <v-fab-transition>
                        <v-btn
                          @click="editing = !editing"
                          color="pink"
                          dark
                          absolute
                          bottom
                          right
                          fab
                        >
                          <v-icon v-if="!editing">mdi-lead-pencil</v-icon>
                          <v-icon v-else>mdi-content-save</v-icon>
                        </v-btn>
                      </v-fab-transition>
                    </v-layout>
                  </v-sheet>
                </v-flex>
              </v-card>
            </v-flex>
            <v-flex xs12 md8>
              <v-card :class="[$style.dashboardCard, 'px-2 py-2']">
                <v-container grid-list-sm fluid>
                  <v-layout row wrap>
                    <v-flex
                      v-for="control in controls"
                      :key="control.name"
                      xs12
                      sm6
                      lg4
                      xl3
                    >
                      <v-card flat tile class="d-flex">
                        <v-layout column align-center justify-center>
                          <v-flex xs12>
                            <v-hover>
                              <v-img
                                slot-scope="{ hover }"
                                :class="[
                                  `elevation-${hover ? 6 : 0}`,
                                  $style.control
                                ]"
                                :src="control.image"
                                aspect-ratio="1"
                                width="212"
                                class="ma-4"
                              />
                            </v-hover>
                          </v-flex>
                          <v-flex xs12>
                            <v-spacer></v-spacer>
                            <div class="subheading">{{ control.name }}</div>
                          </v-flex>
                        </v-layout>
                      </v-card>
                    </v-flex>
                  </v-layout>
                </v-container>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-layout>
    </v-content>
  </v-layout>
</template>

<script>
import Header from "@components/Header.vue";

export default {
  data() {
    return {
      editing: false,
      student: {
        basic: {
          title: "Basic",
          items: [
            { title: "Name", detail: "abc", icon: "domain" },
            { title: "Email", detail: "xyz@gmail", icon: "email" },
            { title: "City", detail: "jnk", icon: "home" },
            { title: "Mobile", detail: "55479", icon: "phone" }
          ]
        }
      },
      controls: [
        {
          name: "Unit Tests",
          image: require("@assets/images/student/dashboard/test.png")
        },
        {
          name: "Test Series",
          image: require("@assets/images/student/dashboard/testseries.png")
        },
        {
          name: "Question Bank",
          image: require("@assets/images/student/dashboard/questionbank.png")
        },
        {
          name: "Results",
          image: require("@assets/images/student/dashboard/results.png")
        },
        {
          name: "Notifications",
          image: require("@assets/images/student/dashboard/notifications.png")
        },
        {
          name: "Discuss",
          image: require("@assets/images/student/dashboard/discuss.png")
        },
        {
          name: "Analytics",
          image: require("@assets/images/student/dashboard/analytics.png")
        },
        {
          name: "Batches",
          image: require("@assets/images/student/dashboard/groups.png")
        }
      ]
    };
  },
  components: {
    Header
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

.dashboardCard{
    text-align: left;
    border: 1px solid #c9cbd0;
    border-radius: 8px;
    margin: 70px 15px;
    font-family: "Product Sans";
}

.control{
  border-radius: 100%;
  cursor: pointer
}
.textbox{
  width:100%;
  height:100%;
  padding: 12px 8px;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
</style>
