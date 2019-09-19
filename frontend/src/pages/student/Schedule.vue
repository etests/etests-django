<template>
  <v-container fluid>
    <Header :disableDrawerClose="true" />
    <v-content app>
      <v-layout>
        <v-flex>
          <v-card height="450" class="mx-4 pb-2">
            <v-calendar
              interval-height="20"
              :now="today"
              :value="today"
              color="info"
            >
              <template v-slot:day="{ date }">
                <template v-for="event in eventsMap[date]">
                  <v-menu
                    :key="event.title"
                    v-model="event.open"
                    full-width
                    offset-x
                  >
                    <template v-slot:activator="{ on }">
                      <div
                        v-if="!event.time"
                        v-ripple
                        class="my-event"
                        v-on="on"
                        v-html="event.title"
                      ></div>
                    </template>
                    <v-card color="grey lighten-4" min-width="350px" flat>
                      <v-toolbar color="primary" dark>
                        <v-btn icon>
                          <v-icon>edit</v-icon>
                        </v-btn>
                        <v-toolbar-title v-html="event.title"></v-toolbar-title>
                        <v-spacer></v-spacer>
                        <v-btn icon>
                          <v-icon>favorite</v-icon>
                        </v-btn>
                        <v-btn icon>
                          <v-icon>more_vert</v-icon>
                        </v-btn>
                      </v-toolbar>
                      <v-card-title primary-title>
                        <span v-html="event.details"></span>
                      </v-card-title>
                      <v-card-actions>
                        <v-btn flat color="secondary">
                          Cancel
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-menu>
                </template>
              </template>
            </v-calendar>
          </v-card>
        </v-flex>
      </v-layout>
      <Footer />
    </v-content>
  </v-container>
</template>

<script>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";

export default {
  data: () => ({
    today: "2019-06-08",
    events: [
      {
        title: "Unit Test 1",
        details: "New test venue will be declared soon.",
        date: "2018-12-30",
        open: false
      },
      {
        title: "Unit Test 1",
        details: "New test venue will be declared soon.",
        date: "2018-12-31",
        open: false
      },
      {
        title: "Unit Test 1",
        details: "New test venue will be declared soon.",
        date: "2019-06-07",
        open: false
      },
      {
        title: "Unit Test 1",
        details: "New test venue will be declared soon.",
        date: "2019-06-03",
        open: false
      },
      {
        title: "Unit Test 1",
        details: "New test venue will be declared soon.",
        date: "2019-06-01",
        open: false
      },
      {
        title: "Unit Test 1",
        details: "New test venue will be declared soon.",
        date: "2019-06-21",
        open: false
      },
      {
        title: "Unit Test 1",
        details: "New test venue will be declared soon.",
        date: "2019-02-01",
        open: false
      }
    ]
  }),
  components: {
    Header,
    Footer
  },
  computed: {
    eventsMap() {
      const map = {};
      this.events.forEach(e => (map[e.date] = map[e.date] || []).push(e));
      return map;
    }
  },
  methods: {
    open(event) {
      alert(event.title);
    }
  }
};
</script>

<style module lang="stylus">
@require '~@/stylus/theme/colors';

.logo{
  width: 40px;
  float: left;
  margin: 0 5px;
}
</style>
