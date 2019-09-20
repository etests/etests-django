<template>
  <StandardLayout>
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
                        {{ props.item.activation_time }}
                      </td>
                      <td class="text-xs-center"></td>
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
      <template v-if="myTestSeries && myTestSeries.length">
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
      <template v-else>
        <div class="ml-2 subheading text-xs-left">
          You have not purchased any question banks.
          <v-btn
            small
            color="primary"
            round
            outline
            @click="$router.push('/question-banks')"
          >
            Explore question banks
          </v-btn>
          <br />
          To know more see
          <router-link to="/faq">FAQ</router-link>
        </div>
      </template>
    </SectionLayout>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";
import SectionLayout from "@/components/layouts/SectionLayout";
import TestSeriesCard from "./TestSeriesCard";

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
        {
          align: "center",
          sortable: true,
          text: "Date",
          value: "activation_time"
        },
        { align: "center", sortable: false, text: "Actions" }
      ],
      newTest: {
        name: "",
        activationDate: "",
        activationTime: "",
        duration: null
      }
    };
  },
  created() {
    this.$store.dispatch("testSeries/getMy");
  },
  computed: {
    status() {
      return this.$store.state.tests.status;
    },
    myTestSeries() {
      return this.$store.state.testSeries.my.items;
    }
  },
  methods: {},
  components: {
    StandardLayout,
    SectionLayout,
    TestSeriesCard
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
