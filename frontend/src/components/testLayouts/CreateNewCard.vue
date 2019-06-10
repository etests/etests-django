<template>
  <ObjectCard :card="plusCard">
    <div slot="content">
      <v-icon color="grey" class="display-4 mt-4" @click="edit = true">
        mdi-plus-circle
      </v-icon>
    </div>
    <div slot="actions">
      <v-btn flat disabled>New Test Series</v-btn>
    </div>
  </ObjectCard>
</template>

<script>
import ObjectCard from "@components/layouts/ObjectCard";

export default {
  data() {
    return {
      plusCard: {
        required: true,
        type: Object
      },
      edit: false
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
