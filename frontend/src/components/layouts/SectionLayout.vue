<template>
  <v-flex xs12 :class="$style.section">
    <v-flex xs12 :class="$style.heading">{{ heading }}</v-flex>
    <v-flex xs12> </v-flex>
    <v-layout row wrap>
      <slot></slot>
    </v-layout>
  </v-flex>
</template>

<script>
export default {
  props: {
    heading: {
      required: false,
      type: String
    }
  },
  data() {
    return {};
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

.section{
    font-family: 'Product Sans',Roboto,Arial,sans-serif;
    margin: 50px auto;
    .heading{
        text-align: left;
        letter-spacing: .014em;
        font-size: 2.08rem;
        line-height: 1.25rem;
        color: #5f6368;
    }
}
</style>
