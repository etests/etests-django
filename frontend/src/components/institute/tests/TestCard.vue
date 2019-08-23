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
              v-model="test.name"
              :class="$style.editTitle"
              v-if="editing"
            />
            <v-text-field
              v-model="test.description"
              :class="$style.editDescription"
              v-if="editing"
            />
          </template>
        </template>
        <template v-else>
          <v-card-title :class="$style.title">
            {{ test.name }}
          </v-card-title>
          <v-card-text :class="$style.description">
            {{ test.text }}
          </v-card-text>
        </template>
      </template>
    </div>
    <div slot="actions">
      <template v-if="this.showActions">
        <v-btn
          icon
          flat
          color="success lighten-1"
          @click="$router.push({ path: `/test/${test.id}` })"
        >
          <v-icon class="px-1">mdi-eye</v-icon>
        </v-btn>
        <v-btn
          icon
          flat
          color="info lighten-1"
          @click="$router.push({ path: `/edit-test/${test.id}` })"
        >
          <v-icon class="px-1">mdi-square-edit-outline</v-icon>
        </v-btn>

        <v-btn icon flat color="error lighten-1" @click="deleteDialog = true">
          <v-icon class="px-1">mdi-delete</v-icon>
        </v-btn>
        <v-dialog v-model="deleteDialog" max-width="290">
          <v-card :class="$style.deleteDialog">
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
              <v-btn color="error" @click="remove">
                Delete
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
import ObjectCard from "./ObjectCard";
import { mapState } from "vuex";
import { testTemplate } from "@/js/test";

export default {
  props: {
    test: {
      required: false,
      default: () => {
        return { name: "", description: "", new: true };
      },
      type: Object
    },
    testSeries: {
      required: false,
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
      editing: false,
      deleteDialog: false,
      loading: false,
      showActions: !this.new,
      meta: {
        type: "test",
        action: this.new ? "tests/create" : "tests/edit",
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
      status: state => state.tests.status
    })
  },
  components: {
    ObjectCard
  },
  methods: {
    updateStatus(newValue, oldValue) {
      this.loading =
        (newValue.removing && newValue.id === this.test.id) ||
        (newValue.creating && this.new);

      if (newValue.removed && newValue.id === this.test.id) {
        this.$destroy();
        this.$el.parentNode.removeChild(this.$el);
      }
    },
    save(e) {
      const { dispatch } = this.$store;
      var data = this.meta.data;
      data.name = this.test.name;
      data.test_series = this.testSeries.id;
      data.questions = testTemplate.questions;
      data.answers = testTemplate.answers;
      data.sections = testTemplate.sections;
      var unwatch = this.$watch("status", this.updateStatus);
      dispatch(this.meta.action, data).then((this.editing = false), unwatch);
    },
    remove() {
      const { dispatch } = this.$store;
      var unwatch = this.$watch("status", this.updateStatus);
      dispatch("tests/remove", this.test.id).then(
        (this.deleteDialog = false),
        unwatch
      );
    }
  },
  mounted() {}
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

.deleteDialog{
  border: 1px solid #dadce0;
  border-radius: 5px;
  font-family: 'Product Sans Light',Roboto,Arial,sans-serif;
  text-align: left;
  .title{
    font-size: 1.375rem;
    line-height: 1.75rem;
    color: #5e5766;
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
