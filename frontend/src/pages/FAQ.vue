<template>
  <StandardLayout>
    <v-flex xs12 class="px-3">
      <v-card :class="[$style.stepCard, 'elevation-2']">
        <v-card-title :class="$style.title">FAQ</v-card-title>
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
          title: "How to join eTests?",
          description:
            "Click on Login / Register button at the top."
        },
        {
          title: "Can I attempt question bank tests any number of times?",
          description:
            "Yes, you can."
        },
        {
          title: "How to add questions to a test?",
          description:
            "Go to tests and click on pencil icon to launch test editor or send us the questions on Google form link."
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
    margin: auto;
  }

  .title {
    font-size: 1.875rem;
    line-height: 1.75rem;
    margin: 5px;
    color: #28cc9e;
  }

  .description {
    text-align: left;
    letter-spacing: 0.014em;
    font-size: 1.08rem;
    line-height: 1.25rem;
    color: #5f6368;
    margin: 0 15px;
  }
}
</style>
