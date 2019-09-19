<template>
  <StandardLayout>
    <v-layout row wrap>
      <SectionLayout heading="Batches">
        <BatchCard new />
        <BatchCard v-for="(batch, i) in batches" :key="i" :batch="batch" />
      </SectionLayout>
    </v-layout>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";
import SectionLayout from "@/components/layouts/SectionLayout";
import BatchCard from "@/components/institute/batches/BatchCard";

export default {
  data() {
    return {
      dialog: false,
      batchIndex: 0,
      rollNumber: 0,
      enrollmentId: 0,
      addDialog: false,
      deleteDialog: false,
      rollNumbers: ""
    };
  },
  components: {
    StandardLayout,
    SectionLayout,
    BatchCard
  },
  created() {
    this.$store.dispatch("batches/detailedList");
  },
  computed: {
    batches() {
      return this.$store.state.batches.items;
    }
  },
  methods: {}
};
</script>
