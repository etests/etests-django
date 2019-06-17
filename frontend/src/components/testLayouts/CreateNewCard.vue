<template>
  <ObjectCard :card="newObjectCard" :editing="editing">
    <div slot="content" v-if="!editing">
      <v-icon color="grey" class="display-4 mt-4" @click="editing = true">
        mdi-plus-circle
      </v-icon>
    </div>

    <div slot="actions" v-if="!editing">
      <v-btn flat disabled>new {{ objectType }}</v-btn>
    </div>
    <div slot="actions" v-else>
      <v-btn icon dark color="error lighten-1" @click="editing = false">
        <v-icon class="px-1">mdi-close</v-icon>
      </v-btn>
      <v-btn icon dark color="blue lighten-1" @click="editing = !editing">
        <v-icon class="px-1">mdi-content-save</v-icon>
      </v-btn>
    </div>
  </ObjectCard>
</template>

<script>
import ObjectCard from "@components/layouts/ObjectCard";

export default {
  props: {
    objectType: {
      required: false,
      default: "",
      type: String
    }
  },
  data() {
    return {
      newObjectCard: {
        name: "",
        description: ""
      },
      editing: false
    };
  },
  components: {
    ObjectCard
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
</style>
