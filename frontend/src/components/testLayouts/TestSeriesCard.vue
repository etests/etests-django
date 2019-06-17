<template>
  <ObjectCard :card="testSeries" :editing="editing">
    <div slot="actions">
      <v-btn icon flat color="success lighten-1" @click="viewDialog = true">
        <v-icon class="px-1">mdi-eye</v-icon>
      </v-btn>
      <v-btn
        icon
        dark
        :flat="!editing"
        color="blue lighten-1"
        @click="editing = !editing"
      >
        <v-icon class="px-1" v-if="!editing">mdi-pencil</v-icon>
        <v-icon class="px-1" v-else>mdi-content-save</v-icon>
      </v-btn>
      <v-btn icon flat color="error lighten-1" @click="deleteDialog = true">
        <v-icon class="px-1">mdi-delete</v-icon>
      </v-btn>

      <v-dialog
        v-model="viewDialog"
        fullscreen
        transition="dialog-bottom-transition"
      >
        <v-card :class="$style.dialog">
          <v-toolbar dark color="grey darken-2">
            <v-btn dark icon @click="viewDialog = false">
              <v-icon>close</v-icon>
            </v-btn>
            <v-toolbar-title>{{ testSeries.name }}</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-toolbar-items>
              <v-btn dark flat @click="viewDialog = false">Save</v-btn>
            </v-toolbar-items>
          </v-toolbar>
          <v-layout row wrap class="mx-4 my-5">
            <slot></slot>
          </v-layout>
        </v-card>
      </v-dialog>
      <v-dialog v-model="deleteDialog" max-width="290">
        <v-card :class="$style.dialog">
          <v-card-title :class="$style.title">
            Are you sure you want to delete {{ testSeries.name }}
          </v-card-title>
          <v-card-text>
            You will not be able to restore this test series if you continue.
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="info" flat @click="deleteDialog = false">
              Cancel
            </v-btn>
            <v-btn color="error" @click="deleteDialog = false">
              Delete
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </ObjectCard>
</template>

<script>
import ObjectCard from "@components/layouts/ObjectCard";

export default {
  props: {
    testSeries: {
      required: true,
      type: Object
    }
  },
  data() {
    return {
      editing: false,
      deleteDialog: false,
      viewDialog: false
    };
  },
  components: {
    ObjectCard
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

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
}
</style>
