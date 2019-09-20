<template>
  <StandardLayout>
    <v-flex xs12>
      <v-card class="elevation-2">
        <v-card-title class="title">FAQ</v-card-title>
        <v-expansion-panel>
          <v-expansion-panel-content
            :class="$style.stepCard"
            v-for="(step, i) in steps"
            :key="i"
          >
            <template v-slot:header>
              <div :class="$style.step">{{ step.title }}</div>
            </template>
            <v-card>
              <v-card-text :class="$style.description">{{
                step.description
              }}</v-card-text>
            </v-card>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-card>
    </v-flex>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";

export default {
  data() {
    return {
      steps: [
        {
          title: "Can the limit of a polynomial involving infinity be finite?",
          description:
            "I have been working around with limits involving infinity and was stuck with this limit: limx→∞[(x5+10x4+3)c−x] Can this limit have some finite value for any real value of c? If yes then what is c and the limit? I tried putting x=1/t and letting limt→0, then I used L'Hospital's Rule but ended up having another 0/0 form. Please help me."
        },
        {
          title: "Can the limit of a polynomial involving infinity be finite?",
          description:
            "I have been working around with limits involving infinity and was stuck with this limit: limx→∞[(x5+10x4+3)c−x] Can this limit have some finite value for any real value of c? If yes then what is c and the limit? I tried putting x=1/t and letting limt→0, then I used L'Hospital's Rule but ended up having another 0/0 form. Please help me."
        },
        {
          title: "Can the limit of a polynomial involving infinity be finite?",
          description:
            "I have been working around with limits involving infinity and was stuck with this limit: limx→∞[(x5+10x4+3)c−x] Can this limit have some finite value for any real value of c? If yes then what is c and the limit? I tried putting x=1/t and letting limt→0, then I used L'Hospital's Rule but ended up having another 0/0 form. Please help me."
        }
      ]
    };
  },
  components: {
    StandardLayout
  }
};
</script>

<style module lang="stylus">
@require '~@/stylus/theme/colors';

.stepCard {
  border-radius: 8px !important;
  font-family: 'Product Sans Light', Roboto, Arial, sans-serif;

  .step {
    font-size: 1.2rem;
    margin: 8px auto;
  }

  .title {
    font-size: 1.875rem;
    line-height: 1.75rem;
    color: #202124;
  }

  .description {
    text-align: left;
    letter-spacing: 0.014em;
    font-size: 1.08rem;
    line-height: 1.25rem;
    color: #5f6368;
  }
}
</style>
