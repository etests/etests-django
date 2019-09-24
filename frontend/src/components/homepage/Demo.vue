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
          <h1 :class="$style.heading">Institutes</h1>
          <p :class="$style.description">{{ institute.description }}</p>
          <v-btn
            round
            dark
            large
            color="primary"
            @click="$router.push('/demo/edit-test')"
            >create demo test</v-btn
          >
        </v-sheet>
      </v-flex>
      <v-divider class="mx-3" inset vertical v-if="!isSmallScreen" />
      <v-flex xs12 md6>
        <v-sheet color="transparent" :class="$style.demoSheet">
          <h1 :class="$style.heading">Students</h1>
          <p :class="$style.description">{{ student.description }}</p>
          <v-btn
            round
            dark
            large
            color="primary"
            @click="$router.push('/test/demo/0')"
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
  //   methods: {
  //     showText(target, message, index, interval) {
  //       if (index < message.length) {
  //         $(target).append(message[index++]);
  //         setTimeout(function() {
  //           showText(target, message, index, interval);
  //         }, interval);
  //       }
  //     },
  //     mounted() {
  //       this.showText("#description1", "Hello, World!", 0, 500);
  //     }
  //   },
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
    font-family: 'Product Sans Light';
    font-size: 1.3rem;
    text-transform: uppercase;
  }

  .description {
    font-family: 'Product Sans';
    font-size: 1.08rem;
  }
}
</style>
