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
              title: "Create a Test or Question Bank",
              description:
                "Go to your dashboard and open test section. You can Create a new test here by filling the necessary details. While creating tests you can select eligible batches of your institute. For Creating a question Bank you need not add any batch. Any User who have purchased your question bank can attempt them. "
            },
            {
              title: "Add questions and Sections",
              description:
                "After The test is created you can add question to your test either by using our test editor or simply send us the pdf of your question paper. The test editor is very easy to use. You need to add sections which may be subjects. You need select the question type, Correct Marks, Incorrect Marks, partial marks(if any), topic and corresponding answer for each question."
            },
            {
              title: "Publish the test",
              description:
                "Click on save this test when you are done. You can take the demo of the test you have created. The test will be active after the activation time you provided during creation of test."
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
                "The Demo test is available in homepage. The test and question banks for which you are registered will appear on the dashboard. You can browse for question banks institute wise, examwise from navigation bar and purchase them from there. Some Question banks are free. To register for a test you simply need to join the batch with the help of joining key Provided by institute"
            },
            {
              title: "Attempt the test",
              description:
                "You can attempt any test from your dashboard. Instructions are displayed at the start of each test. Read it carefully to know the pattern of test. "
            },
            {
              title: "Analyse your performance",
              description:
                "After the completion of test you can see the marks in each subject and also the total marks. For Test of your institute the rank, detailed analysis(Topic wise performance, Subject wise Performance and Comparision with Others) and review(your Response, Correct Answer and time spent on each question) are generated after the test closing time is over. For question bank both analysis and review are generated just after the completion of test. Rank will not be generated for Question Banks."
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
