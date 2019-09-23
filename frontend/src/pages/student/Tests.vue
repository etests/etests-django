<template>
  <StandardLayout>
    <v-flex xs12 class="px-3">
      <v-card :class="[$style.card, 'title elevation-3']">
        <v-card-title>
          Tests for your batch
        </v-card-title>
        <v-flex xs12>
          <v-text-field
            v-model="testSearch"
            append-icon="search"
            label="Search"
            single-line
          ></v-text-field>
        </v-flex>
        <v-flex xs12>
          <v-data-table
            v-if="tests"
            :headers="testHeaders"
            :items="tests"
            :search="testSearch"
          >
            <template v-slot:items="props">
              <tr @click="props.expanded = !props.expanded">
                <td class="text-xs-center">{{ props.item.name }}</td>
                <td class="text-xs-center">
                  {{ formatDate(props.item.activation_time) }}
                </td>
                <td class="text-xs-center">
                  <v-btn icon flat color="success">
                    <v-icon>mdi-chevron-down</v-icon>
                  </v-btn>
                </td>
              </tr>
            </template>
            <template v-slot:expand="props">
              <v-sheet>
                <v-layout align-center>
                  <v-flex xs4> </v-flex>
                  <v-flex xs4> </v-flex>
                  <v-flex xs4>
                    <v-btn
                      round
                      outline
                      color="success"
                      v-if="
                        !props.item.sessions.length && props.item.status == 1
                      "
                      @click="$router.push(`/test/${props.item.id}`)"
                    >
                      Start this test
                    </v-btn>
                    <v-btn
                      round
                      outline
                      disabled
                      v-else-if="
                        props.item.sessions.length && props.item.status == 1
                      "
                    >
                      Attempted
                    </v-btn>
                    <v-btn
                      round
                      outline
                      color="info"
                      v-else
                      @click="$router.push(`/test/${props.item.id}`)"
                    >
                      Practice Attempt
                    </v-btn>
                  </v-flex>
                </v-layout>
                <v-layout
                  align-center
                  v-for="(session, j) in props.item.sessions"
                  :key="j"
                >
                  <v-flex xs4>
                    <span class="info--text" v-if="session.practice">
                      Practice
                    </span>
                    <span v-else class="success--text">Ranked</span>
                  </v-flex>
                  <v-flex xs4>
                    {{ formatDate(session.checkin_time) }}
                  </v-flex>
                  <v-flex xs4>
                    <v-btn
                      icon
                      flat
                      color="info"
                      v-if="!session.completed"
                      @click="$router.push(`/test/${props.item.id}`)"
                    >
                      <v-icon>mdi-play-pause</v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      flat
                      color="success"
                      v-if="session.completed"
                      @click="$router.push(`/result/${session.id}`)"
                    >
                      <v-icon>mdi-file-chart</v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      flat
                      color="warning"
                      v-if="session.completed"
                      @click="$router.push(`/review/${session.id}`)"
                    >
                      <v-icon>mdi-file-find</v-icon>
                    </v-btn>
                    <v-btn v-if="session.practice" icon flat color="error">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-flex>
                </v-layout>
              </v-sheet>
            </template>
          </v-data-table>
        </v-flex>
      </v-card>
    </v-flex>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";
import utils from "@/js/utils";

export default {
  data() {
    return {
      testSearch: "",
      testHeaders: [
        { align: "center", sortable: true, text: "Name", value: "name" },
        {
          align: "center",
          sortable: true,
          text: "Date",
          value: "activation_time"
        },
        { align: "center", sortable: false, text: "Actions" }
      ]
    };
  },
  components: {
    StandardLayout
  },
  created() {
    this.$store.dispatch("tests/getAll");
  },
  computed: {
    tests() {
      return this.$store.state.tests.all.items;
    }
  },
  methods: {
    formatDate(dateString) {
      return utils.formatDate(dateString);
    }
  }
};
</script>

<style module lang="stylus">
.card{
  padding: 10px 20px;
  width: 100%;
  border-radius: 8px;
  td{
    width: 33%;
  }
  margin-bottom: 12px;
}
</style>
