<template>
  <StandardLayout>
    <v-dialog v-if="test" v-model="deleteDialog" max-width="400">
      <v-card :class="$style.dialog">
        <v-card-title :class="$style.title">
          Are you sure you want to delete {{ test.name }}
        </v-card-title>
        <v-card-text>
          You will not be able to restore this test if you continue.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="info" flat @click="deleteDialog = false">
            Cancel
          </v-btn>
          <v-btn color="error" @click="deleteTest(test.id)">
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="declareDialog" max-width="400">
      <v-card :class="$style.dialog">
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
          <v-btn color="primary" flat @click="declareDialog = false">
            Close
          </v-btn>
          <v-btn
            v-if="!status.loading && !status.loaded"
            color="primary"
            @click="generateRanks(test.id)"
          >
            Confirm
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="createTestDialog" max-width="400">
      <v-card :class="$style.dialog">
        <v-card-title :class="$style.title">
          Create new test
        </v-card-title>
        <template v-if="status.creating">
          <v-card-text>
            Creating new test...
          </v-card-text>
        </template>
        <template v-else-if="status.created">
          <v-card-text>
            {{ status.test.name }} is successfully created. <br />
            <br />
            <ol>
              <li>
                You can start adding questions in
                <router-link :to="`/test/${status.test.id}/edit`">
                  Test Editor
                </router-link>
                or
              </li>
              <li>
                <a href="https://forms.gle/qvqtmpXo38xqWpq29" target="_blank">
                  Upload
                </a>
                a pdf or word file and we will add the questions with following
                details: <br />
                Institute Id: {{ user.id }} <br />
                Test Id: {{ status.test.id }}
              </li>
            </ol>
          </v-card-text>
        </template>
        <template v-else>
          <v-card-text>
            Enter the following details
          </v-card-text>
          <v-container grid-list-md>
            <v-layout column wrap>
              <v-flex xs12>
                <v-text-field v-model="newTest.name" label="Name" />
                <DateField
                  v-model="newTest.activationDate"
                  label="Activation Date"
                />
                <TimeField
                  v-model="newTest.activationTime"
                  label="Activation Time"
                />
                <DateField v-model="newTest.closingDate" label="End Date" />
                <TimeField v-model="newTest.closingTime" label="End Time" />
                <v-text-field
                  v-model="newTest.duration"
                  type="time"
                  label="Duration"
                />
              </v-flex>
              <v-flex xs12>
                Select bacthes eligible for this test:
                <v-checkbox
                  v-model="newTest.batches"
                  v-for="batch in batches"
                  :key="batch.id"
                  :label="batch.name"
                />
              </v-flex>
            </v-layout>
          </v-container>
        </template>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" flat @click="createTestDialog = false">
            Close
          </v-btn>
          <v-btn
            v-if="!status.creating && !status.created"
            color="primary"
            @click="createTest()"
          >
            Create
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
        <v-layout row wrap align-center py-5 px-4 ma-auto>
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
      <v-card :class="[$style.testCard, 'title elevation-3 text-xs-center']">
        <v-card-title>
          Tests for your batches
          <v-spacer />
          <div>
            <v-btn
              color="primary"
              round
              outline
              @click="createTestDialog = true"
            >
              Create a test
            </v-btn>
          </div>
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
                <td class="text-xs-center">
                  <router-link :to="`/preview/${props.item.id}`">
                    {{ props.item.name }}
                  </router-link>
                </td>
                <td class="text-xs-center">
                  {{ formatDate(props.item.activation_time) }}
                </td>
                <td class="text-xs-center">
                  {{ formatDate(props.item.closing_time) }}
                </td>
                <td class="text-xs-center">
                  <span v-if="props.item.status == 0">
                    Inactive
                  </span>
                  <span v-else-if="props.item.status == 1">
                    Active
                  </span>
                  <span v-else-if="props.item.status <= 3">
                    Ended
                  </span>
                  <span v-else-if="props.item.status == 4">
                    Ranks Declared
                  </span>
                </td>
                <td class="text-xs-center">
                  <v-btn
                    round
                    icon
                    small
                    color="info lighten-1"
                    @click="$router.push(`/test/${props.item.id}/edit`)"
                    v-if="[0, 1].includes(props.item.status)"
                  >
                    <v-icon small>mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn
                    round
                    icon
                    small
                    color="error lighten-1"
                    @click="
                      test = props.item;
                      deleteDialog = true;
                    "
                    v-if="props.item.status == 0"
                  >
                    <v-icon small>mdi-delete</v-icon>
                  </v-btn>
                  <v-btn
                    round
                    icon
                    small
                    disabled
                    outline
                    v-if="props.item.status == 1"
                  >
                    <v-icon small>mdi-delete</v-icon>
                  </v-btn>
                  <v-btn
                    round
                    small
                    outline
                    color="success lighten-1"
                    @click="
                      test = props.item;
                      declareDialog = true;
                    "
                    v-if="[2, 3].includes(props.item.status)"
                  >
                    Declare ranks
                  </v-btn>
                  <v-btn
                    round
                    outline
                    small
                    color="success lighten-1"
                    @click="
                      test = props.item;
                      getRankList(props.item.id);
                      rankDialog = true;
                    "
                    v-if="props.item.status == 4"
                  >
                    <v-icon>mdi-file-chart</v-icon>
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
import StandardLayout from "@/components/layouts/StandardLayout";
import RankList from "./RankList";
import DateField from "@/components/fields/DateField";
import TimeField from "@/components/fields/TimeField";
import { mapState } from "vuex";
import utils from "@/js/utils";
import { testTemplate } from "@/js/test";

export default {
  data() {
    return {
      test: {},
      declareDialog: false,
      createTestDialog: false,
      deleteDialog: false,
      rankDialog: false,
      testSearch: "",
      testHeaders: [
        { align: "center", sortable: true, text: "Name", value: "name" },
        {
          align: "center",
          sortable: true,
          text: "Activation Time",
          value: "activation_time"
        },
        {
          align: "center",
          sortable: true,
          text: "Closing Time",
          value: "closing_time"
        },
        {
          align: "center",
          sortable: true,
          text: "Status",
          value: "status"
        },
        { align: "center", sortable: false, text: "Actions" }
      ],
      dateMenu: false,
      timeMenu: false,
      newTest: {
        name: "",
        activationDate: "",
        activationTime: "",
        closingDate: "",
        closingTime: "",
        duration: "03:00",
        batches: []
      }
    };
  },
  components: {
    StandardLayout,
    RankList,
    DateField,
    TimeField
  },
  created() {
    this.$store.dispatch("tests/getAll");
    this.$store.dispatch("batches/list");
  },
  computed: {
    ...mapState({
      user: state => state.authentication.user,
      status: state => state.tests.status,
      tests: state => state.tests.all.items,
      rankLists: state => state.tests.rankLists,
      batches: state => state.batches.items
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
    },
    createTest() {
      var data = {
        name: this.newTest.name,
        activation_time:
          this.newTest.activationDate + " " + this.newTest.activationTime,
        closing_time: this.newTest.closingDate + " " + this.newTest.closingTime,
        time_alotted: this.newTest.duration,
        questions: testTemplate.questions,
        answers: testTemplate.answers,
        sections: testTemplate.sections,
        batches: this.newTest.batches
      };
      this.$store.dispatch("tests/create", data);
    },
    deleteTest(id) {
      const { dispatch } = this.$store;
      dispatch("tests/remove", id).then((this.deleteDialog = false));
    }
  }
};
</script>

<style module lang="stylus">
.dialog{
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
    width: 20%;
  }
  margin-bottom: 12px;
}
</style>
