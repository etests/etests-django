<template>
  <ObjectCard>
    <div slot="content" :class="$style.content">
      <v-progress-circular
        :size="70"
        :width="7"
        color="grey darken-1"
        indeterminate
        v-if="loading"
        class="mt-5"
      ></v-progress-circular>
      <template v-else>
        <template v-if="meta.new">
          <v-icon
            color="grey"
            class="display-4 mt-4"
            @click="editing = true"
            v-if="!editing"
          >
            mdi-plus-circle
          </v-icon>
          <template v-else>
            <v-text-field
              autofocus
              placeholder="Name"
              v-model="batch.name"
              :class="$style.editTitle"
              v-if="editing"
            />
            <v-text-field
              v-model="batch.description"
              :class="$style.editDescription"
              v-if="editing"
            />
          </template>
        </template>
        <template v-else>
          <v-card-title :class="$style.title">
            {{ batch.name }}
          </v-card-title>
          <v-card-text :class="$style.description">
            {{ batch.text }}
          </v-card-text>
        </template>
      </template>
    </div>
    <div slot="actions">
      <template v-if="this.showActions">
        <v-btn icon flat color="success lighten-1" @click="viewDialog = true">
          <v-icon class="px-1">mdi-eye</v-icon>
        </v-btn>
        <v-btn icon flat color="info lighten-1">
          <v-icon class="px-1">mdi-square-edit-outline</v-icon>
        </v-btn>

        <v-btn icon flat color="error lighten-1" @click="deleteDialog = true">
          <v-icon class="px-1">mdi-delete</v-icon>
        </v-btn>

        <v-dialog
          v-model="viewDialog"
          fullscreen
          hide-overlay
          transition="dialog-bottom-transition"
        >
          <v-card>
            <v-toolbar dark color="primary">
              <v-btn icon dark @click="viewDialog = false">
                <v-icon>close</v-icon>
              </v-btn>
              <v-toolbar-title>{{ batch.name }}</v-toolbar-title>
              <v-spacer />
              <v-btn large flat @click="addDialog = true">
                <v-icon color="white" large class="ma-1">
                  mdi-plus-circle
                </v-icon>
                Add students
              </v-btn>
            </v-toolbar>
            <v-layout row wrap align-center pa-5>
              <v-card :class="[$style.studentsTable, 'title']">
                <v-card-title>
                  Students
                </v-card-title>
                <v-data-table
                  :headers="enrollmentHeaders"
                  :items="batch.enrollments"
                >
                  <template v-slot:items="props">
                    <td class="text-xs-center">
                      {{ props.item.roll_number }}
                    </td>
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
                          deleteStudentDialog = true;
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
              </v-card>
            </v-layout>
          </v-card>
        </v-dialog>

        <v-dialog v-model="deleteDialog" max-width="290">
          <v-card :class="$style.dialog">
            <v-card-title :class="$style.title">
              Are you sure you want to delete {{ batch.name }}
            </v-card-title>
            <v-card-text>
              You will not be able to restore this batch and all the students
              will be unenrolled.
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="info" flat @click="deleteDialog = false">
                Cancel
              </v-btn>
              <v-btn color="error" @click="remove">
                Delete
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-dialog v-model="deleteStudentDialog" max-width="400">
          <v-card :class="$style.dialog">
            <v-card-title :class="$style.title">
              Remove student with roll number
              {{ rollNumber }}?
            </v-card-title>
            <v-card-text>
              The student will be removed from this batch. Are you sure you want
              to continue?
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="error" flat @click="deleteStudentDialog = false">
                Cancel
              </v-btn>
              <v-btn
                color="error"
                @click="
                  removeStudent(enrollmentId);
                  deleteStudentDialog = false;
                "
              >
                Delete
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-dialog v-model="addDialog" max-width="400">
          <v-card :class="$style.dialog">
            <v-card-title :class="$style.title">
              Add students to {{ batch.name }}
            </v-card-title>
            <v-card-text>
              <template v-if="enrollmentStatus.loading">
                Please wait...
              </template>
              <template v-else-if="enrollmentStatus.loaded">
                Here is the list of generated keys <br />
                <v-layout
                  align-center
                  text-xs-center
                  row
                  v-for="(enrollment, i) in generated"
                  :key="i"
                  my-2
                >
                  <v-flex xs2> {{ i + 1 }}, </v-flex>
                  <v-flex xs5>
                    {{ enrollment.roll_number }}
                  </v-flex>
                  <v-flex xs5>
                    {{ enrollment.joining_key }}
                  </v-flex>
                </v-layout>
              </template>
              <template v-else>
                Enter roll numbers of the students or upload an excel file with
                a list of roll numbers and we will generate a password for each.
                <input type="file" @change="onFileChange" />
                <xlsx-read :file="file">
                  <template v-slot:default="{ loading }">
                    <span v-if="loading">Loading...</span>
                  </template>
                </xlsx-read>
                <textarea
                  v-model="rollNumbers"
                  :class="$style.listBox"
                ></textarea>
              </template>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="info"
                flat
                @click="
                  $store.commit('enrollments/clearGenerated');
                  addDialog = false;
                "
              >
                Close
              </v-btn>
              <v-btn
                color="info"
                v-if="!enrollmentStatus.loading && !enrollmentStatus.loaded"
                @click="generate"
              >
                Generate
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>
      <template v-else>
        <template v-if="meta.new">
          <v-btn flat disabled v-if="!editing"> new {{ meta.type }} </v-btn>
          <template v-else>
            <v-btn icon dark color="error lighten-1" @click="editing = false">
              <v-icon class="px-1">mdi-close</v-icon>
            </v-btn>
            <v-btn icon dark color="blue lighten-1" @click="save">
              <v-icon class="px-1">mdi-content-save</v-icon>
            </v-btn>
          </template>
        </template>
      </template>
    </div>
  </ObjectCard>
</template>

<script>
import ObjectCard from "@components/layouts/ObjectCard";
import { XlsxRead, XLsxJson } from "vue-xlsx";
import { mapState } from "vuex";

export default {
  props: {
    batch: {
      required: false,
      default: () => {
        return { name: "", description: "", new: true };
      },
      type: Object
    },
    new: {
      required: false,
      default: false,
      type: Boolean
    }
  },
  data() {
    return {
      file: null,
      editing: false,
      viewDialog: false,
      deleteDialog: false,
      deleteStudentDialog: false,
      addDialog: false,
      loading: false,
      rollNumbers: "",
      batchIndex: 0,
      rollNumber: 0,
      enrollmentId: 0,
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
      ],
      showActions: !this.new,
      meta: {
        type: "batch",
        action: this.new ? "batches/create" : "batches/edit",
        new: this.new,
        data: {
          name: "",
          price: 0,
          sections: [],
          questions: [],
          answers: []
        }
      }
    };
  },
  computed: {
    ...mapState({
      status: state => state.batches.status,
      enrollmentStatus: state => state.enrollments.status,
      generated: state => state.enrollments.generated
    })
  },
  components: {
    ObjectCard,
    XlsxRead,
    XLsxJson
  },
  methods: {
    onFileChange(event) {
      this.file = event.target.files ? event.target.files[0] : null;
    },
    sheetUpload(file) {},

    generate() {
      var data = {
        batch: this.batch.pk,
        rollNumbers: this.rollNumbers
          .trim()
          .split(" ")
          .replace(/(\r\n|\n|\r)/gm, " ")
          .replace(/\s+/g, " ")
      };
      this.$store.dispatch("enrollments/batchEnroll", data);
    },
    removeStudent(i) {
      this.$store.dispatch("enrollments/remove", i);
    },
    updateStatus(newValue, oldValue) {
      this.loading =
        (newValue.removing && newValue.id === this.batch.id) ||
        (newValue.creating && this.new);

      if (newValue.removed && newValue.id === this.batch.id) {
        this.$destroy();
        this.$el.parentNode.removeChild(this.$el);
      }
    },
    save(e) {
      const { dispatch } = this.$store;
      var data = this.meta.data;
      data.name = this.batch.name;
      var unwatch = this.$watch("status", this.updateStatus);
      dispatch(this.meta.action, data).then((this.editing = false), unwatch);
    },
    remove() {
      const { dispatch } = this.$store;
      var unwatch = this.$watch("status", this.updateStatus);
      dispatch("batches/remove", this.batch.pk).then(
        (this.deleteDialog = false),
        unwatch
      );
    }
  },
  mounted() {}
};
</script>

<style module lang="stylus">
.studentsTable{
  border-radius: 8px;
  border: 1px solid #eee;
  td{
    width: 25%;
  }
  margin-bottom: 12px;
}

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

.content{
  min-height: 160px;
  background-color: #fcfcfc;
  border-radius: 8px 8px 0 0;
  text-align: center;
  &:hover{
      background-color: #f5f5f5;
  }
}

.title, .editTitle{
  text-align: left;
  font-size: 1.375rem;
  line-height: 1.75rem;
  color: #7e777e;
}

.editTitle, .editDescription{
  padding: 12px 15px 0;
  margin: 0;
  input{
    color: #7e777e !important;
    letter-spacing: 0.06rem;
    border-color: #eee !important;
  }
}

.description, .editDescription{
  letter-spacing: .014em;
  text-align: left;
  font-size: 0.9rem;
  line-height: 1.25rem;
  color: #5f6368;
}
</style>
