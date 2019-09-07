<template>
  <StandardLayout>
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
                <td class="text-xs-center">{{ props.item.activation_time }}</td>
                <td class="text-xs-center">
                  <v-btn round color="success lighten-1">
                    <v-icon>mdi-play</v-icon>
                    Generate Results
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
        { align: "center", sortable: true, text: "Actions" }
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
      var date = new Date(Date.parse(dateString));
      return (
        date.getDate() +
        "/" +
        (date.getMonth() + 1) +
        "/" +
        date.getFullYear() +
        " " +
        date.getHours() +
        ":" +
        date.getMinutes() +
        ":" +
        date.getSeconds()
      );
    }
  }
};
</script>

<style module lang="stylus">
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
