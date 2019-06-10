<template>
  <ObjectCard :card="test">
    <div slot="actions">
      <v-btn icon flat color="success lighten-1">
        <v-icon class="px-1">mdi-eye</v-icon>
      </v-btn>
      <v-btn icon flat color="blue lighten-1">
        <v-icon class="px-1">mdi-pencil</v-icon>
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
            You will not be able restore this test if you continue.
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
    test: {
      required: true,
      type: Object
    }
  },
  data() {
    return {
      deleteDialog: false
    };
  },
  components: {
    ObjectCard
  }
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
</style>
