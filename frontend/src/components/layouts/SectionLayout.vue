<template>
  <v-flex xs12 :class="$style.section">
    <v-flex xs12 :class="$style.heading">{{ heading }}</v-flex>
    <v-divider class="mb-5" />
    <v-spacer />
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
@require '~@/stylus/theme/colors';

.section{
    font-family: 'Montserrat',Roboto,Arial,sans-serif;
    margin: 20px 10px;
    width: 100%;
    .heading{
      margin: 10px;
      text-align: left;
      letter-spacing: .014em;
      font-size: 2.08rem;
      line-height: 1.25rem;
      color: #5f6368;
      &:not(:first-child){
        margin-top: 50px;
      }
    }
}
</style>
