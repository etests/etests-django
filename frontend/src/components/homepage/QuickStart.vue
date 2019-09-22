<template>
  <SectionLayout>
    <template slot="heading">
      Quick Start
    </template>
    <template slot="subheading">
      know eTests step by step
    </template>
    <v-layout row wrap my-3 justify-center slot="content">
      <v-flex xs12>
        <v-tabs
          hide-slider
          slot="tabs"
          v-model="showTab"
          color="transparent"
          centered
        >
          <v-tab v-for="(tab, i) in tabs" :key="i">
            <v-btn color="primary" :large="!isSmallScreen" round dark>
              <v-icon>{{ tab.icon }}</v-icon> &nbsp;
              <strong>{{ tab.title }}</strong>
            </v-btn>
          </v-tab>
        </v-tabs>
      </v-flex>
      <v-flex xs12>
        <v-tabs-items v-model="showTab">
          <v-tab-item v-for="(tab, i) in tabs" :key="i">
            <StepsLayout :steps="tab.steps" />
          </v-tab-item>
        </v-tabs-items>
      </v-flex>
    </v-layout>
  </SectionLayout>
</template>

<script>
import SectionLayout from "@/components/homepage/SectionLayout.vue";
import StepsLayout from "@/components/homepage/StepsLayout.vue";

export default {
  props: {
    authType: {
      required: false,
      default: 0
    }
  },
  data() {
    return {
      isSmallScreen: this.$vuetify.breakpoint.smAndDown,
      showTab: parseInt(this.authType),
      tabs: [
        {
          id: "institute",
          title: "Institutes",
          icon: "mdi-domain",
          steps: [
            {
              title: "Join eTests",
              description:
                "Let's start your awesome experience of online test creation. Go to signup page and register as Institute. Fill all the details and you are ready to create tests."
            },
            {
              title: "Create a test",
              description:
                "Go to tests section in your dashboard and click on add new button. Select exam type and target students."
            },
            {
              title: "Add questions",
              description:
                "Click on add button in the right panel and select question type from dropdown list. Type out the question text, options and chose the correct answer."
            },
            {
              title: "Publish the test",
              description:
                "Click on save when you are done. Now you can take a demo of this test or publish it."
            }
          ]
        },
        {
          id: "StudentServices",
          title: "Students",
          icon: "mdi-account-multiple",
          steps: [
            {
              title: "Join eTests",
              description:
                "Let's start your awesome experience of online tests. Go to signup page and register as Student. Fill all the details and you are ready to take tests."
            },
            {
              title: "Select a test",
              description:
                "Go to tests in your dashboard and chose a test published by your coaching. You can also select a demo test or search for tests by other coachings."
            },
            {
              title: "Attempt the test",
              description:
                "Once a test is active you can start answering the questions."
            },
            {
              title: "Analyse your performance",
              description:
                "See detailed analysis of your performance including your weak points. Get useful tips for improvement."
            }
          ]
        }
      ]
    };
  },
  components: {
    SectionLayout,
    StepsLayout
  }
};
</script>

<style module lang="stylus">
.cardsContainer{
   margin: 25px auto;
}
</style>
