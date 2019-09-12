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
            <v-layout wrap>
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
                <v-text-field
                  v-model="newTest.duration"
                  type="time"
                  label="Duration"
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
      v-if="selectedTestSeries"
      v-model="testsDialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon dark @click="testsDialog = false">
            <v-icon>close</v-icon>
          </v-btn>
          <v-toolbar-title>
            {{ selectedTestSeries.name }} (Question Bank)
          </v-toolbar-title>
        </v-toolbar>
        <v-layout row wrap align-center py-5 px-4 ma-auto>
          <v-flex xs12>
            <v-card>
              <v-card-title>
                Tests
                <v-spacer />
                <div>
                  <v-btn
                    color="primary"
                    round
                    outline
                    @click="createTestDialog = true"
                  >
                    Add a test
                  </v-btn>
                </div>
              </v-card-title>
              <v-flex xs12>
                <v-data-table
                  :headers="testHeaders"
                  :items="selectedTestSeries.tests"
                >
                  <template v-slot:items="props">
                    <tr @click="props.expanded = !props.expanded">
                      <td class="text-xs-center">
                        <router-link :to="`/preview/${props.item.id}`">
                          {{ props.item.name }}
                        </router-link>
                      </td>

                      <td class="text-xs-center">
                        <v-btn
                          round
                          icon
                          small
                          color="info lighten-1"
                          @click="$router.push(`/test/${props.item.id}/edit`)"
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
                          :outline="props.item.status !== 0"
                          :disabled="props.item.status !== 0"
                        >
                          <v-icon small>mdi-delete</v-icon>
                        </v-btn>
                      </td>
                    </tr>
                  </template>
                </v-data-table>
              </v-flex>
            </v-card>
          </v-flex>
        </v-layout>
      </v-card>
    </v-dialog>
    <SectionLayout heading="My Question Banks">
      <template v-if="myTestSeries">
        <TestSeriesCard
          v-for="(testSeries, i) in myTestSeries"
          :key="i"
          :testSeries="testSeries"
          @viewTests="
            selectedTestSeries = testSeries;
            testsDialog = true;
          "
        />
      </template>
      <TestSeriesCard new />
    </SectionLayout>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import SectionLayout from "@components/layouts/SectionLayout";
import TestSeriesCard from "./TestSeriesCard";
import TestCard from "@components/institute/tests/TestCard";
import DateField from "@components/fields/DateField";
import TimeField from "@components/fields/TimeField";
import { testTemplate } from "@/js/test";

export default {
  data() {
    return {
      deleteDialog: false,
      test: {},
      createTestDialog: false,
      testsDialog: false,
      selectedTestSeries: {},
      testHeaders: [
        { align: "center", sortable: true, text: "Name", value: "name" },
        { align: "center", sortable: false, text: "Actions" }
      ],
      newTest: {
        name: "",
        activationDate: "",
        activationTime: "",
        duration: "03:00"
      }
    };
  },
  created() {
    this.$store.dispatch("testSeries/getMy");
  },
  computed: {
    user() {
      return this.$store.state.authentication.user;
    },
    status() {
      return this.$store.state.tests.status;
    },
    myTestSeries() {
      return this.$store.state.testSeries.my.items;
    }
  },
  methods: {
    createTest() {
      var data = {
        name: this.newTest.name,
        activation_time:
          this.newTest.activationDate + " " + this.newTest.activationTime,
        time_alotted: this.newTest.duration,
        questions: testTemplate.questions,
        answers: testTemplate.answers,
        sections: testTemplate.sections,
        practice: true,
        test_series: [this.selectedTestSeries.id]
      };
      this.$store.dispatch("tests/create", data);
    },
    deleteTest(id) {
      const { dispatch } = this.$store;
      dispatch("tests/remove", id).then((this.deleteDialog = false));
    }
  },
  components: {
    StandardLayout,
    SectionLayout,
    TestSeriesCard,
    TestCard,
    DateField,
    TimeField
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
</style>
