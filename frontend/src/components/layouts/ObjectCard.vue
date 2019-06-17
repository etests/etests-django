<template>
  <v-flex xs12 sm6 md4 lg3>
    <v-card :class="$style.objectCard">
      <v-layout row wrap>
        <v-flex xs12 class="py-0 my-0 round-corners">
          <v-card :to="card.link" flat :class="$style.content">
            <slot name="content">
              <v-text-field
                autofocus
                placeholder="Name"
                v-model="card.name"
                :class="$style.editTitle"
                v-if="editing"
              />
              <v-card-title :class="$style.title" v-else>
                {{ card.name }}
              </v-card-title>
              <v-text-field
                v-model="card.description"
                :class="$style.editDescription"
                v-if="editing"
              />
              <v-card-text :class="$style.description" v-else>
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
    },
    editing: {
      required: false,
      default: false,
      type: Boolean
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
  letter-spacing: 0.06rem;

  .content{
    min-height: 160px;
    background-color: #fcfcfc;
    border-radius: 8px 8px 0 0;
    text-align: center;
    &:hover{
        background-color: #f5f5f5;
    }
   }
  .title, .editTitle{
    text-align: left;
    font-size: 1.375rem;
    line-height: 1.75rem;
    color: #7e777e;
  }

  .editTitle, .editDescription{
    padding: 12px 15px 0;
    margin: 0;
    input{
      color: #7e777e !important;
      letter-spacing: 0.06rem;
      border-color: #eee !important;
    }
  }

  .description, .editDescription{
    letter-spacing: .014em;
    text-align: left;
    font-size: 0.9rem;
    line-height: 1.25rem;
    color: #5f6368;
  }
}
</style>
