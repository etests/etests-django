<template>
  <StandardLayout>
    <v-dialog v-model="declareDialog" max-width="400">
      <v-card :class="$style.declareDialog">
        <v-card-title :class="$style.title">
          Declare ranks for {{ test.name }}
        </v-card-title>
        <template v-if="status.loading">
          <v-card-text>
            Please wait...
          </v-card-text>
        </template>
        <template v-else-if="status.loaded">
          <v-card-text>
            {{ status.message }}
          </v-card-text>
        </template>
        <template v-else>
          <v-card-text>
            Are you sure you want to declare the final ranks for this test?
          </v-card-text>
        </template>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="info" flat @click="declareDialog = false">
            Close
          </v-btn>
          <v-btn
            v-if="!status.loading && !status.loaded"
            color="info"
            @click="generateRanks(test.id)"
          >
            Confirm
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-if="test"
      v-model="rankDialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon dark @click="rankDialog = false">
            <v-icon>close</v-icon>
          </v-btn>
          <v-toolbar-title>{{ test.name }}</v-toolbar-title>
        </v-toolbar>
        <v-layout row wrap align-center pa-5>
          <v-card :class="[$style.studentsTable, 'title']">
            <v-card-title>
              Ranks
            </v-card-title>
            <RankList :rankList="rankList(test.id)" />
          </v-card>
        </v-layout>
      </v-card>
    </v-dialog>
    <v-flex xs12>
      <v-card :class="[$style.testCard, 'title elevation-3']">
        <v-card-title>
          Tests
          <v-spacer />
          <router-link to="tests-series"> Manage Tests </router-link>
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
                  <span v-if="props.item.status == 0">
                    Inactive
                  </span>
                  <span v-else-if="props.item.status == 1">
                    Active
                  </span>
                  <v-btn
                    v-else-if="[2, 3].includes(props.item.status)"
                    round
                    color="success lighten-1"
                    @click="
                      test = props.item;
                      declareDialog = true;
                    "
                  >
                    <v-icon>mdi-play</v-icon>
                    Declare ranks
                  </v-btn>
                  <v-btn
                    v-else-if="props.item.status == 4"
                    round
                    color="success lighten-1"
                    @click="
                      test = props.item;
                      getRankList(props.item.id);
                      rankDialog = true;
                    "
                  >
                    <v-icon>mdi-play</v-icon>
                    View ranks
                  </v-btn>
                </td>
              </tr>
            </template>
          </v-data-table>
        </v-flex>
      </v-card>
    </v-flex>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import RankList from "./RankList";
import { mapState } from "vuex";
import utils from "@js/utils";

export default {
  data() {
    return {
      test: {},
      declareDialog: false,
      rankDialog: false,
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
    StandardLayout,
    RankList
  },
  created() {
    this.$store.dispatch("tests/getAll");
  },
  computed: {
    ...mapState({
      status: state => state.tests.status,
      tests: state => state.tests.all.items,
      rankLists: state => state.tests.rankLists
    })
  },
  methods: {
    formatDate(dateString) {
      return utils.formatDate(dateString);
    },
    generateRanks(id) {
      this.$store.dispatch("tests/generateRanks", id);
    },
    getRankList(id) {
      var index = this.rankLists.findIndex(rankList => rankList.id === id);
      if (index === -1) this.$store.dispatch("tests/getRankList", id);
    },
    rankList(id) {
      return this.rankLists.find(rankList => rankList.id === id);
    }
  }
};
</script>

<style module lang="stylus">
.declareDialog{
  border: 1px solid #dadce0;
  border-radius: 5px;
  font-family: 'Product Sans Light',Roboto,Arial,sans-serif;
  text-align: left;
  .title{
    font-size: 1.375rem;
    line-height: 1.75rem;
    color: #5e5766;
  }
  .listBox{
    margin: 10px auto 5px;
    padding: 10px;
    width: 100%;
    height: 300px;
    border: 1px solid #999;
    border-radius: 5px;
  }
}

.testCard{
  padding: 10px 20px;
  width: 100%;
  border-radius: 8px;
  td{
    width: 33%;
  }
  margin-bottom: 12px;
}
</style>
