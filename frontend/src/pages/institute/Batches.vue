<template>
  <StandardLayout>
    <v-dialog v-if="batches" v-model="deleteDialog" max-width="400">
      <v-card :class="$style.addDialog">
        <v-card-title :class="$style.title">
          Remove student with roll number
          {{ rollNumber }}?
        </v-card-title>
        <v-card-text>
          The student will be removed from this batch. Are you sure you want to
          continue?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" flat @click="deleteDialog = false">
            Cancel
          </v-btn>
          <v-btn
            color="error"
            @click="
              remove(enrollmentId);
              deleteDialog = false;
            "
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-if="batches" v-model="addDialog" max-width="400">
      <v-card :class="$style.addDialog">
        <v-card-title :class="$style.title">
          Add students to {{ batches[batchIndex].name }}
        </v-card-title>
        <v-card-text>
          <template v-if="generated">
            Here is the list of generated keys <br />
            <table>
              <tr v-for="(enrollment, i) in generated" :key="i">
                <td>{{ enrollment.roll_number }}</td>
                <td>{{ enrollment.joining_key }}</td>
              </tr>
            </table>
          </template>
          <template v-else>
            Enter roll numbers of the students you want to add and we will
            generate a password for each.
            <textarea v-model="rollNumbers" :class="$style.listBox"></textarea>
          </template>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="info" flat @click="addDialog = false">
            Close
          </v-btn>
          <v-btn color="info" @click="generate">
            Generate
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-if="this.batches"
      v-model="dialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar dark color="primary">
          <v-btn icon dark @click="dialog = false">
            <v-icon>close</v-icon>
          </v-btn>
          <v-toolbar-title>{{ batches[batchIndex].name }}</v-toolbar-title>
          <v-spacer />
          <v-btn large flat @click="addDialog = true">
            <v-icon color="white" large class="ma-1">
              mdi-plus-circle
            </v-icon>
            Add students
          </v-btn>
        </v-toolbar>
        <v-layout row wrap align-center pa-5>
          <v-data-table
            :headers="enrollmentHeaders"
            :items="batches[batchIndex].enrollments"
            class="elevation-2"
          >
            <template v-slot:items="props">
              <td class="text-xs-center">{{ props.item.roll_number }}</td>
              <td class="text-xs-center">{{ props.item.joining_key }}</td>
              <td class="text-xs-center">
                <span class="success--text" v-if="props.item.student">
                  Joined
                </span>
                <span class="error--text" v-else>
                  Pending
                </span>
              </td>
              <td class="text-xs-center">
                <v-btn
                  flat
                  icon
                  color="error"
                  @click="
                    rollNumber = props.item.roll_number;
                    enrollmentId = props.item.pk;
                    deleteDialog = true;
                  "
                  ><v-icon>mdi-delete</v-icon></v-btn
                >
                <!-- <v-btn flat icon color="cyan"
                  ><v-icon>mdi-pencil</v-icon></v-btn
                >
                <v-btn flat icon color="green"><v-icon>mdi-redo</v-icon></v-btn> -->
              </td>
            </template>
          </v-data-table>
        </v-layout>
      </v-card>
    </v-dialog>
    <v-layout row wrap v-if="batches">
      <v-flex xs12 md4 v-for="(batch, i) in batches" :key="i">
        <v-card :class="$style.batchCard">
          <v-img
            class="white--text"
            height="200px"
            src="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
          >
            <v-card-title class="align-end fill-height">
              {{ batch.name }}
            </v-card-title>
          </v-img>

          <v-card-text>
            <span class="text--primary">
              {{ batch.enrollments.length }} student{{
                batch.enrollments.length > 1 ? "s" : ""
              }}
            </span>
          </v-card-text>

          <v-card-actions class="px-5 mx-auto">
            <v-btn flat color="error">
              Delete
            </v-btn>
            <v-btn
              flat
              color="error"
              @click="
                batchIndex = i;
                dialog = true;
              "
            >
              Open
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import SectionLayout from "@components/layouts/SectionLayout";

export default {
  data() {
    return {
      dialog: false,
      batchIndex: 0,
      rollNumber: 0,
      enrollmentId: 0,
      addDialog: false,
      deleteDialog: false,
      rollNumbers: "",
      enrollmentHeaders: [
        {
          align: "center",
          sortable: true,
          text: "Roll Number",
          value: "roll_number"
        },
        {
          align: "center",
          text: "Joining Key",
          value: "joining_key",
          sortable: false
        },
        {
          align: "center",
          text: "Status",
          value: "student",
          sortable: true
        },
        {
          align: "center",
          text: "Actions",
          sortable: false
        }
      ]
    };
  },
  components: {
    StandardLayout,
    SectionLayout
  },
  created() {
    this.$store.dispatch("batches/detailedList");
  },
  computed: {
    batches() {
      return this.$store.state.batches.all.items;
    },
    generated() {
      return this.$store.state.enrollments.generated;
    }
  },
  methods: {
    generate() {
      var data = {
        batch: this.batches[this.batchIndex].pk,
        rollNumbers: this.rollNumbers.trim().split(" ")
      };
      this.$store.dispatch("enrollments/batchEnroll", data);
    },
    remove(i) {
      this.$store.dispatch("enrollments/remove", i);
    }
  }
};
</script>

<style module lang="stylus">

.addDialog{
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


.studentCard, .batchCard{
    text-align: center;
    border: 1px solid #c9cbd0;
    border-radius: 8px;
    padding: 10px;
    font-family: "Product Sans Light";
    font-size: 12pt;
}
.batchCard{
    height: 320px;
    width: 300px;
}
.studentCard{
    height: 120px;
    width: 120px;
}
</style>
