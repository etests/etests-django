<template>
  <StandardLayout>
    <ObjectCard> </ObjectCard>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";
import ObjectCard from "@components/layouts/ObjectCard";

export default {
  data() {
    return {};
  },
  components: {
    StandardLayout,
    ObjectCard
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
</style>
