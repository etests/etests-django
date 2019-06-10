<template>
  <v-flex xs12 sm6 md4 lg3>
    <v-card :class="$style.objectCard">
      <v-layout row wrap>
        <v-flex xs12 class="py-0 my-0 round-corners">
          <v-card :to="card.link" flat :class="$style.content">
            <slot name="content">
              <v-card-title :class="$style.title">
                {{ card.name }}
              </v-card-title>
              <v-card-text :class="$style.description">
                {{ card.text }}
              </v-card-text>
            </slot>
          </v-card>
        </v-flex>
      </v-layout>
      <v-divider class="grey lighten-2" />
      <v-card min-height="40" class="text-xs-center">
        <slot name="actions"></slot>
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

.objectCard{
  border: 1px solid #dadce0;
  border-radius: 8px;
  margin: 10px;
  font-family: 'Product Sans Light',Roboto,Arial,sans-serif;

  .content{
    min-height: 160px;
    background-color: #fcfcfc;
    border-radius: 8px 8px 0 0;
    text-align: center;
    &:hover{
        background-color: #f5f5f5;
    }
   }
  .title{
    text-align: left;
    font-size: 1.375rem;
    line-height: 1.75rem;
    color: #7e7e7e;
  }
  .description{
    letter-spacing: .014em;
    text-align: left;
    font-size: 0.9rem;
    line-height: 1.25rem;
    color: #5f6368;
  }
}
</style>
