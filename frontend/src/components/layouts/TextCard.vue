<template>
  <v-flex xs12>
    <v-card :class="$style.displayCard" min-height="80">
      <v-layout row wrap>
        <v-flex xs12>
          <v-card-title :class="$style.title">
            {{ card.title }}
          </v-card-title>
          <v-card-text v-if="card.text" :class="$style.description">
            {{ card.text }}
          </v-card-text>
        </v-flex>
        <v-flex xs12>
          <v-card flat>
            <slot></slot>
          </v-card>
        </v-flex>
      </v-layout>
    </v-card>
  </v-flex>
</template>

<script>
export default {
  props: {
    card: {
      required: false,
      type: Object
    }
  },
  data() {
    return {};
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

.displayCard{
  border: 1px solid #dadce0;
  border-radius: 8px;
  .title{
    font-family: 'Product Sans Light',Roboto,Arial,sans-serif;
    font-size: 1.875rem;
    line-height: 1.75rem;
    color: #202124;
  }
  .description{
    text-align: left;
    letter-spacing: .014em;
    font-family: 'Product Sans Light',Roboto,Arial,sans-serif;
    font-size: 1.08rem;
    line-height: 1.25rem;
    color: #5f6368;
  }
}
</style>
