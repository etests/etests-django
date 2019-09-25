<template>
  <v-container>
    <v-layout row wrap>
      <v-flex xs12 lg5 mb-3>
        <v-expansion-panel popout class="transparent">
          <v-expansion-panel-content
            :class="$style.stepCard"
            v-for="(step, i) in steps"
            :key="i"
            class="transparent"
          >
            <template v-slot:header>
              <div :class="$style.step">{{ step.title }}</div>
            </template>
            <v-card class="transparent">
              <v-card-text :class="$style.description">
                {{ step.description }}
              </v-card-text>
            </v-card>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-flex>

      <v-flex xs12 lg5 offset-lg2 :class="[$style.video, 'hidden-sm-and-down']">
        This will contain Video
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
export default {
  props: {
    steps: {
      required: true,
      type: Array
    }
  },
  data() {
    return {};
  }
};
</script>

<style module lang="stylus">

.stepCard{
    border-radius: 8px !importants;

    .step{
        font-family: "Open Sans";
        font-size: 1.1rem;
        margin: 8px auto;
    }

    .description{
        font-family: "Montserrat";
        text-align: left;
        font-size: 0.99rem;
    }
}
.video{
    font-family: "Open Sans";
    font-size: 1.08rem;
}
</style>
