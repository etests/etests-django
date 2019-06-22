<template>
  <ObjectCard
    :card="newObjectCard"
    :objectType="objectType"
    @save="handleSubmit"
  >
  </ObjectCard>
</template>

<script>
import ObjectCard from "@components/testLayouts/ObjectCard";

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
      }
    };
  },
  components: {
    ObjectCard
  },
  methods: {
    handleSubmit(e) {
      const { dispatch } = this.$store;
      var testData = { name: this.name, price: 0, questions: "[{}]" };
      console.log(testData);
      dispatch("unitTest/create", testData).then((this.editing = false));
    }
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
</style>
