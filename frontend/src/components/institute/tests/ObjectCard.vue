<template>
  <v-flex xs12 sm6 md4 lg3>
    <v-card :class="$style.objectCard">
      <v-layout row wrap>
        <v-flex xs12 class="py-0 my-0 round-corners">
          <v-card flat>
            <slot name="content"> </slot>
          </v-card>
        </v-flex>
      </v-layout>
      <v-divider class="grey lighten-2" />
      <v-card min-height="40" class="text-xs-center">
        <slot name="actions"> </slot>
      </v-card>
    </v-card>
  </v-flex>
</template>

<style module lang="stylus">
@require '~@stylus/theme/colors';

.objectCard{
  border: 1px solid #dadce0;
  border-radius: 8px;
  margin: 10px;
  font-family: 'Product Sans Light',Roboto,Arial,sans-serif;
  letter-spacing: 0.06rem;

}
</style>
