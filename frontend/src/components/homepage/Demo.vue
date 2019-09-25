<template>
  <SectionLayout>
    <template slot="heading"
      >Free Demo</template
    >
    <template slot="subheading"
      >experience all the premium features for free</template
    >
    <v-layout row :wrap="isSmallScreen" justify-center slot="content">
      <v-flex xs12 md6>
        <v-sheet
          color="transparent"
          :class="$style.demoSheet"
          :height="!isSmallScreen ? '360' : ''"
        >
          <div :class="$style.heading">Institutes</div>
          <p :class="$style.description">{{ institute.description }}</p>
          <v-btn
            round
            dark
            large
            color="primary"
            @click="$router.push('/demo/edit')"
            >create demo test</v-btn
          >
        </v-sheet>
      </v-flex>
      <v-divider class="mx-3" inset vertical v-if="!isSmallScreen" />
      <v-flex xs12 md6>
        <v-sheet color="transparent" :class="$style.demoSheet">
          <div :class="$style.heading">Students</div>
          <p :class="$style.description">{{ student.description }}</p>
          <v-btn
            round
            dark
            large
            color="primary"
            @click="$router.push('/demo/0')"
            >attempt demo test</v-btn
          >
        </v-sheet>
      </v-flex>
    </v-layout>
  </SectionLayout>
</template>

<script>
import SectionLayout from "@/components/homepage/SectionLayout.vue";

export default {
  name: "Demo",
  data() {
    return {
      isSmallScreen: this.$vuetify.breakpoint.smAndDown,
      institute: {
        description:
          " Watch our demo video to learn about how to conduct an online test. Try it for free now."
      },
      student: {
        description: "Free demo test for JEE Mains, JEE Advance, NEET, AIIMS."
      }
    };
  },
  components: {
    SectionLayout
  }
};
</script>

<style module lang="stylus">
.demoSheet {
  padding: 30px 20px 0;
  min-height: 150px;

  .heading {
    font-family: 'Open Sans';
    font-size: 1.1rem;
    text-transform: uppercase;
  }

  .description {
    margin: 15px auto;
    max-width: 400px;
    font-family: 'Montserrat';
    font-size: 0.99rem;
  }
}
</style>
