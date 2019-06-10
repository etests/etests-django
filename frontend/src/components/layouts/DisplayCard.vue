<template>
  <v-flex xs12 md6>
    <v-card :class="$style.displayCard" min-height="180">
      <v-layout row wrap>
        <v-flex xs12>
          <v-card-title :class="$style.title">
            {{ card.title }}
          </v-card-title>
          <v-card-text :class="$style.description">{{ card.text }}</v-card-text>
        </v-flex>
      </v-layout>
      <v-divider class="grey lighten-2" />
      <v-card
        flat
        :to="card.action.link"
        :class="[$style.action, `${card.action.color}--text`]"
        min-height="50"
      >
        <v-icon class="mx-2" :color="card.action.color">
          {{ card.action.icon }}
        </v-icon>
        {{ card.action.text }}
      </v-card>
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
  .action{
    padding: 10px;
    margin: 0;
    &:hover{
      background-color: #f5f5f5 ;
    }
  }
}
</style>
