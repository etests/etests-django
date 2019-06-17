<template>
  <v-container fluid>
    <Header :showDrawer="false" :temporaryDrawer="true">
      <v-layout slot="tools">
        <v-flex>
          <v-layout justify-end>
            <!-- <v-btn flat icon>
              <v-icon>mdi-account-network</v-icon>
            </v-btn>
            <v-btn flat icon>
              <v-icon>mdi-pause</v-icon>
            </v-btn> -->
            <v-btn flat icon @click="toggleFullScreen()">
              <v-icon v-if="fullscreen">mdi-fullscreen-exit</v-icon>
              <v-icon v-else>mdi-fullscreen</v-icon>
            </v-btn>
          </v-layout>
        </v-flex>
      </v-layout>
    </Header>

    <v-content app :class="$style.wideText">
      <v-layout row wrap>
        <v-flex xs12>
          <v-card color="white" :class="$style.questionContainer">
            <v-sheet class="pt-2">
              <v-layout row justify-center mb-1>
                <v-btn color="primary" flat>
                  <v-icon> mdi-clock </v-icon>
                  &nbsp; {{ time }}
                </v-btn>
                <v-btn
                  color="info"
                  round
                  outline
                  :icon="isSmallScreen"
                  :small="!isSmallScreen"
                  @click="
                    markForReview(currentQuestion);
                    nextQuestion();
                  "
                >
                  <v-icon>mdi-comment-eye-outline</v-icon>
                  <span v-if="!isSmallScreen">Mark for review & next</span>
                </v-btn>

                <v-btn
                  color="error"
                  round
                  outline
                  :icon="isSmallScreen"
                  :small="!isSmallScreen"
                  @click="clear(currentQuestion)"
                >
                  <v-icon>mdi-close</v-icon>
                  <span v-if="!isSmallScreen">Clear your response</span>
                </v-btn>
                <v-btn
                  color="success"
                  round
                  outline
                  :icon="isSmallScreen"
                  :small="!isSmallScreen"
                  @click="
                    save(currentQuestion);
                    nextQuestion();
                  "
                >
                  <v-icon>mdi-content-save-move</v-icon>
                  <span v-if="!isSmallScreen">Save response & next </span>
                </v-btn>
              </v-layout>
            </v-sheet>
            <v-divider />
            <v-tabs-items v-model="currentSection" :touch="swipeActions">
              <v-tab-item v-for="section in sections" :key="section.subject">
                <v-sheet
                  :class="[$style.question, 'px-4 py-2']"
                  :height="windowHeight"
                >
                  <v-layout justify-center>
                    <v-btn
                      color="success lighten-1"
                      class="subheading"
                      small
                      outline
                      icon
                    >
                      +{{ questions[currentQuestion].correctMarks }}
                    </v-btn>
                    <v-btn
                      color="error lighten-1"
                      class="subheading"
                      small
                      outline
                      icon
                    >
                      -{{ questions[currentQuestion].incorrectMarks }}
                    </v-btn>
                    <v-chip color="indigo" outline>
                      {{ questions[currentQuestion].type }} TYPE
                    </v-chip>
                  </v-layout>

                  <v-img
                    v-if="questions[currentQuestion].image"
                    :src="
                      require(`@assets/logos/${
                        questions[currentQuestion].image
                      }`)
                    "
                    class="mb-3"
                  ></v-img>
                  <v-chip color="grey darken-2" outline small>
                    <strong> Q{{ currentQuestion + 1 }} </strong>
                  </v-chip>
                  <span :class="$style.questionText">
                    {{ questions[currentQuestion].text }}
                  </span>

                  <v-radio-group
                    v-model="questions[currentQuestion].answer"
                    @change="save(currentQuestion)"
                    :mandatory="false"
                    v-if="questions[currentQuestion].type == 'SINGLE'"
                  >
                    <v-radio
                      v-for="(option, i) in questions[currentQuestion].options"
                      :key="currentQuestion + '-' + i"
                      :label="option"
                      :value="i"
                      :on-icon="`mdi-alpha-${letter('a', i, true)}-circle`"
                      :off-icon="
                        `mdi-alpha-${letter('a', i, true)}-circle-outline`
                      "
                    ></v-radio>
                  </v-radio-group>

                  <v-layout
                    v-else-if="questions[currentQuestion].type == 'MULTIPLE'"
                    py-4
                    my-1
                    column
                  >
                    <v-checkbox
                      v-for="(option, i) in questions[currentQuestion].options"
                      v-model="questions[currentQuestion].answer"
                      multiple
                      height="0"
                      class="mt-0 mb-1"
                      :key="currentQuestion + '-' + i"
                      :label="option"
                      :value="i"
                      :on-icon="`mdi-alpha-${letter('a', i, true)}-circle`"
                      :off-icon="
                        `mdi-alpha-${letter('a', i, true)}-circle-outline`
                      "
                      @change="save(currentQuestion)"
                    >
                    </v-checkbox>
                  </v-layout>
                  <v-layout
                    v-else-if="questions[currentQuestion].type == 'NUMBER'"
                    my-4
                  >
                    <v-flex xs12 sm6 md3>
                      <v-text-field
                        label="Enter your answer (0-999)"
                        v-model="questions[currentQuestion].answer"
                        type="number"
                        @keyup="save(currentQuestion)"
                      ></v-text-field>
                    </v-flex>
                  </v-layout>
                  <v-layout
                    v-else-if="questions[currentQuestion].type == 'MATRIX'"
                    my-3
                    column
                  >
                    <v-layout row wrap justify-center>
                      <v-flex xs6>
                        <v-layout column justify-start>
                          <v-flex
                            v-for="(option, i) in questions[currentQuestion]
                              .options"
                            :key="`${currentQuestion}-option-${i}`"
                          >
                            <v-layout row wrap align-start>
                              <v-flex xs8 :class="$style.option">
                                <v-icon :class="$style.optionLetter">
                                  {{
                                    `mdi-alpha-${letter(
                                      "a",
                                      i,
                                      true
                                    )}-circle-outline`
                                  }}
                                </v-icon>
                                {{ option }}
                              </v-flex>
                            </v-layout>
                          </v-flex>
                        </v-layout>
                      </v-flex>
                      <v-flex xs6>
                        <v-layout column justify-end>
                          <v-flex
                            v-for="(answer, j) in questions[currentQuestion]
                              .answers"
                            :key="`${currentQuestion}-answer-${j}`"
                          >
                            <v-layout row wrap align-start>
                              <v-flex xs8 :class="$style.option">
                                <v-icon :class="$style.optionLetter">
                                  {{
                                    `mdi-alpha-${letter(
                                      "p",
                                      j,
                                      true
                                    )}-circle-outline`
                                  }}
                                </v-icon>
                                {{ answer }}
                              </v-flex>
                            </v-layout>
                          </v-flex>
                        </v-layout>
                      </v-flex>
                    </v-layout>

                    <v-flex xs12 sm6 md3 mt-4>
                      <v-layout row>
                        <v-flex shrink mx-3> </v-flex>
                        <v-flex
                          shrink
                          v-for="j in questions[currentQuestion].answers.length"
                          :key="`${currentQuestion}-label-answer-${j}`"
                        >
                          <v-checkbox
                            height="0"
                            class="mt-0 mb-1"
                            :off-icon="`mdi-alpha-${letter('p', j - 1, true)}`"
                            disabled
                          >
                          </v-checkbox>
                        </v-flex>
                      </v-layout>
                      <v-layout
                        row
                        v-for="i in questions[currentQuestion].options.length"
                        :key="`${currentQuestion}-label-option-${i}`"
                        justify-start
                      >
                        <v-flex shrink>
                          <v-checkbox
                            height="0"
                            class="mt-0 mb-1"
                            :off-icon="
                              `mdi-alpha-${letter('a', i - 1, true)}-circle`
                            "
                            disabled
                          >
                          </v-checkbox>
                        </v-flex>

                        <v-flex
                          shrink
                          v-for="j in questions[currentQuestion].answers.length"
                          :key="`${currentQuestion}-${i}-${j}`"
                        >
                          <v-checkbox
                            v-model="questions[currentQuestion].answer[i - 1]"
                            multiple
                            height="0"
                            class="mt-0 mb-1"
                            :value="j - 1"
                            @change="save(currentQuestion)"
                            :on-icon="$vuetify.icons.radioOn"
                            :off-icon="$vuetify.icons.radioOff"
                          >
                          </v-checkbox>
                        </v-flex>
                      </v-layout>
                    </v-flex>
                  </v-layout>
                </v-sheet>
              </v-tab-item>
            </v-tabs-items>
          </v-card>
        </v-flex>
      </v-layout>
    </v-content>

    <v-footer color="white" height="auto" fixed app inset>
      <v-layout>
        <v-flex xs12>
          <input @keyup.left="previousQuestion" type="hidden" />
          <input @keyup.right="nextQuestion" type="hidden" />
          <v-btn icon color="primary" @click="previousQuestion()">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
          <v-btn icon color="primary" @click="nextQuestion()">
            <v-icon>mdi-arrow-right</v-icon>
          </v-btn>
        </v-flex>
      </v-layout>
      <v-btn
        flat
        icon
        color="primary"
        @click="panel = !panel"
        :absolute="isSmallScreen"
        :right="isSmallScreen"
      >
        <v-icon v-if="panel">mdi-arrow-collapse-right</v-icon>
        <v-icon v-else>mdi-arrow-expand-left</v-icon>
      </v-btn>
    </v-footer>

    <v-navigation-drawer v-model="panel" app right>
      <v-card-text>
        <v-toolbar-title class="subheading primary--text mt-3">
          <strong style="text-transform: uppercase;">{{ testName }}</strong>
        </v-toolbar-title>
        <v-tabs
          slot="tabs"
          v-model="currentSection"
          color="transparent"
          hide-slider
          centered
        >
          <v-tab
            active-class="primary--text"
            v-for="section in sections"
            :key="section.subject"
          >
            {{ section.subject }}
          </v-tab>
        </v-tabs>
        <span v-for="(question, i) in questions" :key="question.id">
          <v-btn
            fab
            v-if="question.section == currentSection"
            dark
            small
            :flat="i != currentQuestion"
            :class="statusColor(question.status)"
            @click="
              changeQuestion(i);
              isSmallScreen ? (panel = !panel) : '';
            "
          >
            <span>{{ i + 1 }}</span>
          </v-btn>
        </span>
      </v-card-text>
      <v-layout justify-center>
        <v-btn outline color="indigo" fixed bottom :left="isSmallScreen">
          <v-icon>mdi-exit-to-app</v-icon>
          <span>Submit this test</span>
        </v-btn>
        <v-flex v-if="isSmallScreen">
          <v-btn
            flat
            icon
            dark
            color="primary"
            @click="panel = !panel"
            bottom
            right
            fixed
          >
            <v-icon v-if="panel">mdi-arrow-collapse-right</v-icon>
            <v-icon v-else>mdi-arrow-expand-left</v-icon>
          </v-btn>
        </v-flex>
      </v-layout>
    </v-navigation-drawer>
  </v-container>
</template>

<script>
import Header from "@components/Header.vue";
import Footer from "@components/Footer.vue";

export default {
  data() {
    return {
      windowHeight: window.innerHeight - 200,
      isSmallScreen: this.$vuetify.breakpoint.smAndDown,
      panel: null,
      drawer: false,
      time: "1:14:12",
      fullscreen: false,
      swipeActions: {
        left: () => this.nextQuestion(),
        right: () => this.previousQuestion()
      },
      testName: "Unit Test 1",
      currentSection: 0,
      currentQuestion: 0,
      sections: [
        { subject: "Physics", start: "0", end: "3", currentQuestion: 0 },
        { subject: "Chemistry", start: "4", end: "5", currentQuestion: 4 },
        { subject: "Maths", start: "6", end: "7", currentQuestion: 6 }
      ],
      questions: [
        {
          id: "1.4",
          section: 0,
          text:
            "Match the quantities on the left to their properties on the right.",
          image: null,
          type: "MATRIX",
          options: [
            "Velocity",
            "Current",
            "Work done by friction",
            "Gravitational work"
          ],
          answers: [
            "Vector",
            "Scalar",
            "Tensor",
            "Conservative",
            "Non-conservative"
          ],
          answer: [[], [], [], []],
          status: 1,
          correctMarks: 4,
          incorrectMarks: 2
        },
        {
          id: "1",
          section: 0,
          text: "What is velocity?",
          image: null,
          type: "SINGLE",
          options: ["Vector", "Scalar", "Tensor", "None"],
          answer: [],
          status: 0,
          correctMarks: 4,
          incorrectMarks: 1
        },
        {
          id: "2",
          section: 0,
          text: "What is escape velocity?",
          image: null,
          type: "NUMBER",
          answer: [],
          status: 0,
          correctMarks: 4,
          incorrectMarks: 1
        },
        {
          id: "1.3",
          section: 0,
          text: "What is friction?",
          image: null,
          type: "MULTIPLE",
          options: ["Vector", "Scalar", "Tensor", "None"],
          answer: [],
          status: 0,
          correctMarks: 4,
          incorrectMarks: 2
        },
        {
          id: "3",
          section: 1,
          text: "What is atom?",
          image: null,
          type: "SINGLE",
          options: ["Vector", "Scalar", "Tensor", "None"],
          answer: [],
          status: 0,
          correctMarks: 4,
          incorrectMarks: 1
        },
        {
          id: "4",
          section: 1,
          text: "What is molecule?",
          image: null,
          type: "SINGLE",
          options: ["Vector", "Scalar", "Tensor", "None"],
          answer: [],
          status: 0,
          correctMarks: 4,
          incorrectMarks: 1
        },
        {
          id: "5",
          section: 2,
          text: "What is parabola?",
          image: null,
          type: "SINGLE",
          options: ["Vector", "Scalar", "Tensor", "None"],
          answer: [],
          status: 0,
          correctMarks: 4,
          incorrectMarks: 1
        },
        {
          id: "6",
          section: 2,
          text: "What is matrix?",
          image: null,
          type: "SINGLE",
          options: ["Vector", "Scalar", "Tensor", "None"],
          answer: [],
          status: 0,
          correctMarks: 4,
          incorrectMarks: 1
        }
      ]
    };
  },
  components: {
    Header,
    Footer
  },
  methods: {
    letter(start, index, order) {
      const small = "abcdefghijklmnopqrstuvwxyz";
      const caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
      const size = small.length;
      return order
        ? small[(small.indexOf(start) + index) % size]
        : caps[(caps.indexOf(start) + index) % size];
    },
    isEmpty(x) {
      return (
        x == null || x === "" || (Array.isArray(x) && x.every(this.isEmpty))
      );
    },
    statusColor(status) {
      switch (status) {
        case 0:
          return "grey darken-2";
        case 1:
          return "error";
        case 2:
          return "info";
        case 3:
          return "green";
        case 4:
          return "purple";
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
    },
    changeQuestion(i) {
      if (i >= 0 && i <= this.questions.length - 1) {
        this.currentQuestion = i;
        this.currentSection = this.questions[i].section;
        this.sections[this.currentSection].currentQuestion = i;
      }
    },
    previousQuestion() {
      this.changeQuestion(this.currentQuestion - 1);
    },
    nextQuestion() {
      this.changeQuestion(this.currentQuestion + 1);
    },
    markForReview(i) {
      if (this.isEmpty(this.questions[i].answer)) this.questions[i].status = 2;
      else this.questions[i].status = 4;
    },
    clear(i) {
      if (this.questions[i].type === "MATRIX")
        this.questions[i].answer = [[], [], [], []];
      else this.questions[i].answer = [];
      this.questions[i].status = 1;
    },
    save(i) {
      // console.log(this.questions[i].answer);
      if (!this.isEmpty(this.questions[i].answer)) this.questions[i].status = 3;
      else this.clear(i);
    },
    updateStatus(i) {
      if (this.questions[i].status === 0) this.questions[i].status = 1;
    }
  },
  watch: {
    currentSection: function(newSection, oldSection) {
      this.currentQuestion = this.sections[newSection].currentQuestion;
    },
    currentQuestion: function(newQuestion, oldQuestion) {
      this.updateStatus(newQuestion);
    }
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener("resize", () => {
        this.windowHeight = window.innerHeight - 200;
      });
    });
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
.questionInfo{
  border-bottom: 1px solid grey !important;
}
.wideText{
  letter-spacing: 0.04em;
}
.questionContainer{
  text-align: left;
  border: 1px solid #c9cbd0;
  border-radius: 8px;

  .question{
    overflow-y: auto;
    .questionText{
      font-family: 'Product Sans',Roboto,Arial,sans-serif;
      font-size: 1.3rem;
      letter-spacing: 0.02em;
      color: #606164;
    }
    .option{
      position: relative;
      padding-left: 30px;
      margin-bottom: 5px;
      color: #787878;

      .optionLetter{
        position: absolute;
        left: 0
      }
    }
  }
}
</style>
