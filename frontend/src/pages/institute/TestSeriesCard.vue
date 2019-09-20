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
            <div class="px-3 py-1 text-xs-left">
              <input
                type="text"
                autofocus
                placeholder="Question Bank Name"
                v-model="testSeries.name"
                :class="$style.textBox"
                v-if="editing"
              />
              <input
                type="text"
                v-model="testSeries.price"
                placeholder="Price"
                :class="$style.textBox"
                v-if="editing"
              />
            </div>
          </template>
        </template>
        <template v-else>
          <v-card-title class="title grey--text">
            {{ testSeries.name }}
          </v-card-title>
          <v-card-text>
            {{ testSeries.text }}
          </v-card-text>
        </template>
      </template>
    </div>
    <div slot="actions">
      <v-card-actions>
        <v-layout row>
          <template v-if="this.showActions">
            <v-flex xs4>
              <v-btn large color="blue" flat>
                &#8377; {{ testSeries.price }}
              </v-btn>
            </v-flex>

            <v-flex xs4>
              <v-btn round outline color="primary" @click="$emit('viewTests')">
                View
              </v-btn>
            </v-flex>
            <v-flex xs4>
              <v-btn
                round
                outline
                color="error lighten-1"
                @click="deleteDialog = true"
              >
                Delete
              </v-btn>
            </v-flex>

            <v-dialog v-model="deleteDialog" max-width="400">
              <v-card :class="$style.deleteDialog">
                <v-card-title class="$style.title">
                  Are you sure you want to delete {{ testSeries.name }}
                </v-card-title>
                <v-card-text>
                  You will not be able to restore this question bank if you
                  continue.
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
              <v-btn flat disabled v-if="!editing">
                <v-flex xs12> new {{ meta.type }} </v-flex>
              </v-btn>
              <template v-else>
                <v-flex xs6>
                  <v-btn
                    round
                    outline
                    color="error lighten-1"
                    @click="editing = false"
                  >
                    Cancel
                  </v-btn>
                </v-flex>
                <v-flex xs6>
                  <v-btn round outline color="blue lighten-1" @click="save">
                    Save
                  </v-btn>
                </v-flex>
              </template>
            </template>
          </template>
        </v-layout>
      </v-card-actions>
    </div>
  </ObjectCard>
</template>

<script>
import ObjectCard from "@/components/layouts/ObjectCard";

export default {
  props: {
    testSeries: {
      required: false,
      default: () => {
        return { name: "", price: "", new: true };
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
      editing: false,
      deleteDialog: false,
      loading: false,
      viewDialog: false,
      showActions: !this.new,
      meta: {
        type: "question bank",
        action: this.new ? "testSeries/create" : "testSeries/edit",
        new: this.new
      }
    };
  },
  components: {
    ObjectCard
  },
  methods: {
    updateStatus(newValue, oldValue) {
      this.loading =
        (newValue.removing && newValue.id === this.testSeries.id) ||
        (newValue.creating && this.new);

      if (newValue.removed && newValue.id === this.testSeries.id) {
        this.$destroy();
        this.$el.parentNode.removeChild(this.$el);
      }
    },
    save(e) {
      const { dispatch } = this.$store;
      var data = {
        name: this.testSeries.name,
        price: parseInt(this.testSeries.price)
      };
      var unwatch = this.$watch("status", this.updateStatus);
      dispatch(this.meta.action, data).then((this.editing = false), unwatch);
    },
    remove() {
      const { dispatch } = this.$store;
      var unwatch = this.$watch("status", this.updateStatus);
      dispatch("testSeries/remove", this.testSeries.id).then(
        (this.deleteDialog = false),
        unwatch
      );
    }
  },
  mounted() {}
};
</script>

<style module lang="stylus">
@require '~@/stylus/theme/colors';

.deleteDialog{
  border: 1px solid #dadce0;
  border-radius: 5px;
  font-family: 'Product Sans Light'
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

.textBox{
  border-radius: 8px;
  border: 1px solid #ddd;
  background: white;
  width: 100%;
  font: "Segoe UI Light";
  font-size: 15px;
  margin: auto;
  margin-top: 20px;
  padding: 8px;
}
</style>
