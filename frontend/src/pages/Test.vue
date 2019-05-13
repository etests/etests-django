<template>
  <v-container fluid class="px-0">
    <Header :showDrawer="false" :temporaryDrawer="true">
      <v-layout slot="tools">
        <v-flex>
          <v-layout justify-end>
            <v-btn color="white" flat>
              <v-icon> mdi-clock </v-icon>
              &nbsp; 2:30:10
            </v-btn>
            <v-btn flat icon>
              <v-icon>mdi-account-network</v-icon>
            </v-btn>
            <v-btn flat icon>
              <v-icon>mdi-pause</v-icon>
            </v-btn>
            <v-btn flat icon @click="toggleFullScreen()">
              <v-icon v-if="fullscreen">mdi-fullscreen-exit</v-icon>
              <v-icon v-else>mdi-fullscreen</v-icon>
            </v-btn>
            <v-btn flat icon @click="panel = !panel">
              <v-icon v-if="panel">mdi-arrow-expand-right</v-icon>
              <v-icon v-else>mdi-arrow-expand-left</v-icon>
            </v-btn>
          </v-layout>
        </v-flex>
      </v-layout>

      <v-tabs
        slot="tabs"
        v-model="currentSection"
        color="transparent"
        slider-color="white"
      >
        <v-tab v-for="section in sections" :key="section.subject">
          <strong>{{ section.subject }}</strong>
        </v-tab>
      </v-tabs>
    </Header>
    <v-divider></v-divider>

    <v-content app class="pt-5 mt-5">
      <v-layout coulumn wrap>
        <v-flex xs12>
          <v-sheet class="text-xs-left my-1 py-2 px-4">
            <v-chip color="grey darken-2" outline>
              Question {{ currentQuestion + 1 }}
            </v-chip>
            <v-chip color="success lighten-1" dark>
              +4
            </v-chip>
            <v-chip color="error lighten-1" dark>
              -1
            </v-chip>
          </v-sheet>
          <v-divider class="grey lighten-2"></v-divider>
        </v-flex>
        <v-flex xs12>
          <v-sheet
            min-height="300px"
            color="white"
            class="text-xs-left py-3 px-5"
          >
            <v-tabs-items v-model="currentSection">
              <v-tab-item v-for="section in sections" :key="section.subject">
                <span
                  class="title grey--text text--darken-3"
                  v-if="section.questions"
                >
                  {{ section.questions[currentQuestion].text }}

                  <v-radio-group
                    v-model="section.questions[currentQuestion].selected"
                    :mandatory="false"
                  >
                    <v-radio
                      v-for="(option, i) in section.questions[currentQuestion]
                        .options"
                      :key="i"
                      :label="option"
                      :value="i"
                    ></v-radio>
                  </v-radio-group>
                </span>
              </v-tab-item>
            </v-tabs-items>
          </v-sheet>

          <v-flex xs12>
            <v-sheet height="auto" class="py-2">
              <v-btn
                color="success"
                @click="
                  sections[currentSection].questions[
                    currentQuestion
                  ].status = 2;
                  currentQuestion += 1;
                "
              >
                <v-icon>mdi-content-save-move</v-icon>
                <span>Save and next </span>
              </v-btn>

              <v-btn color="info">
                <v-icon>mdi-comment-eye-outline</v-icon>
                <span>Mark for review</span>
              </v-btn>

              <v-btn
                color="error"
                @click="
                  sections[currentSection].questions[
                    currentQuestion
                  ].selected = null;
                  sections[currentSection].questions[
                    currentQuestion
                  ].status = 0;
                "
              >
                <v-icon>mdi-close</v-icon>
                <span>Clear response</span>
              </v-btn>

              <v-btn color="indigo" dark>
                <v-icon>mdi-exit-to-app</v-icon>
                <span>Submit this test</span>
              </v-btn>
            </v-sheet>
          </v-flex>
        </v-flex>
      </v-layout>
    </v-content>
    <v-navigation-drawer v-model="panel" app right>
      <v-card-text>
        <v-btn
          icon
          :color="`${statusColor(question.status)} lighten-3`"
          v-for="(question, i) in sections[currentSection].questions"
          :key="question.id"
          @click="currentQuestion = i"
        >
          <span>{{ i + 1 }}</span>
        </v-btn>
      </v-card-text>
    </v-navigation-drawer>
  </v-container>
</template>

<script>
import Header from "@components/Header.vue";
import Footer from "@components/Footer.vue";

export default {
  data() {
    return {
      panel: true,
      drawer: false,
      currentSection: 0,
      currentQuestion: 0,
      sections: [
        {
          start: 0,
          end: 1,
          subject: "Physics",
          questions: [
            {
              id: "1",
              text: "What is velocity?",
              image: null,
              type: "MCQS",
              options: ["Vector", "Scalar", "Tensor", "None"],
              selected: null,
              status: 0
            },
            {
              id: "2",
              text: "What is friction?",
              image: null,
              type: "MCQS",
              options: ["Vector", "Scalar", "Tensor", "None"],
              selected: null,
              status: 0
            }
          ]
        },
        { subject: "Chemistry" },
        { subject: "Maths" }
      ],
      timer: true,
      fullscreen: false
    };
  },
  components: {
    Header,
    Footer
  },
  methods: {
    statusColor(status) {
      switch (status) {
        case 0:
          return "grey";
        case 1:
          return "info";
        case 2:
          return "green";
        default:
          return "grey";
      }
    },
    toggleFullScreen() {
      if (
        (document.fullScreenElement && document.fullScreenElement !== null) ||
        (!document.mozFullScreen && !document.webkitIsFullScreen)
      ) {
        if (document.documentElement.requestFullScreen) {
          document.documentElement.requestFullScreen();
        } else if (document.documentElement.mozRequestFullScreen) {
          document.documentElement.mozRequestFullScreen();
        } else if (document.documentElement.webkitRequestFullScreen) {
          document.documentElement.webkitRequestFullScreen(
            Element.ALLOW_KEYBOARD_INPUT
          );
        }
      } else {
        if (document.cancelFullScreen) {
          document.cancelFullScreen();
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
          document.webkitCancelFullScreen();
        }
      }
      this.fullscreen = !this.fullscreen;
    }
  },
  mounted() {}
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
.questionInfo{
  border-bottom: 1px solid grey !important;
}
</style>
