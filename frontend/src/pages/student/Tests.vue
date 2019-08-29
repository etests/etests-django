<template>
  <StandardLayout>
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
        class="elevation-3"
      >
        <template v-slot:items="props">
          <td class="text-xs-center">{{ props.item.name }}</td>
          <td class="text-xs-center">{{ props.item.activation_time }}</td>
          <td class="text-xs-center">
            <v-btn
              icon
              flat
              :color="action.color"
              v-for="(action, i) in actions"
              :key="`${props.item.id}-${i}`"
              @click="$router.push(`/${action.path}/${props.item.id}`)"
            >
              <v-icon>{{ action.icon }}</v-icon>
            </v-btn>
          </td>
        </template>
      </v-data-table>
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
      ],
      actions: [
        { icon: "mdi-play", color: "success", path: "test" },
        { icon: "mdi-file-chart", color: "info", path: "result" },
        { icon: "mdi-file-find", color: "warning", path: "review" }
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
  }
};
</script>

<style module lang="stylus">
.testCard{
    text-align: left;
    border: 1px solid #c9cbd0;
    border-radius: 8px;
    height: 50px;
    margin: 10px auto;
    padding: 10px;
    font-family: "Product Sans Light";
    font-size: 14pt;
}
</style>
