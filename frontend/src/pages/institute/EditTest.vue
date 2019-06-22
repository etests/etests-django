<template>
  <v-container fluid class="px-0">
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

    <v-content app :class="$style.content">
      <v-layout row wrap>
        <v-flex xs12>
          <v-card color="white" :class="$style.questionContainer">
            <v-sheet class="pt-2">
              <v-layout row justify-center mb-1>
                <v-btn color="primary" flat>
                  <v-icon> mdi-clock </v-icon>
                  &nbsp; {{ time }}
                </v-btn>

                <v-menu offset-y transition="slide-y-transition" bottom>
                  <template v-slot:activator="{ on }">
                    <v-btn
                      color="info"
                      round
                      outline
                      :icon="isSmallScreen"
                      :small="!isSmallScreen"
                      v-on="on"
                    >
                      <v-icon>mdi-plus</v-icon>
                      <span v-if="!isSmallScreen">Add new question</span>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-tile
                      v-for="(type, index) in questionTypes"
                      :key="index"
                      @click="addQuestion(type.value)"
                    >
                      <v-list-tile-title>{{ type.text }}</v-list-tile-title>
                    </v-list-tile>
                  </v-list>
                </v-menu>

                <v-btn
                  color="error"
                  round
                  outline
                  :icon="isSmallScreen"
                  :small="!isSmallScreen"
                  @click="clearQuestion(questionIndex)"
                >
                  <v-icon>mdi-close</v-icon>
                  <span v-if="!isSmallScreen">Clear answer</span>
                </v-btn>

                <v-btn
                  color="error"
                  round
                  outline
                  :icon="isSmallScreen"
                  :small="!isSmallScreen"
                  @click="deleteQuestion(questionIndex)"
                >
                  <v-icon>mdi-delete</v-icon>
                  <span v-if="!isSmallScreen">Delete question</span>
                </v-btn>

                <v-btn
                  color="success"
                  round
                  outline
                  :icon="isSmallScreen"
                  :small="!isSmallScreen"
                  @click="saveTest()"
                >
                  <v-icon>mdi-content-save</v-icon>
                  <span v-if="!isSmallScreen">Save this test</span>
                </v-btn>
              </v-layout>
            </v-sheet>
            <v-divider />
            <v-tabs-items v-model="sectionIndex" :touch="swipeActions">
              <v-sheet
                :class="[$style.question, 'px-4 py-2']"
                :height="windowHeight"
              >
                <v-tab-item v-for="section in sections" :key="section.subject">
                  <v-layout justify-center>
                    <v-btn
                      color="success lighten-1"
                      class="subheading"
                      small
                      outline
                      icon
                    >
                      +{{ currentQuestion.correctMarks }}
                    </v-btn>
                    <v-btn
                      color="error lighten-1"
                      class="subheading"
                      small
                      outline
                      icon
                    >
                      -{{ currentQuestion.incorrectMarks }}
                    </v-btn>
                    <v-chip color="indigo" outline>
                      <v-select
                        :items="questionTypes"
                        placeholder="Select question type"
                        v-model="currentQuestion.type"
                        @change="clearQuestion(questionIndex)"
                      ></v-select>
                    </v-chip>
                  </v-layout>

                  <v-img
                    v-if="currentQuestion.image"
                    :src="require(`@assets/logos/${currentQuestion.image}`)"
                    class="mb-3"
                  ></v-img>
                  <span :class="$style.questionText">
                    <v-textarea
                      rows="1"
                      :prepend-inner-icon="
                        `mdi-numeric-${questionIndex + 1}-circle`
                      "
                      placeholder="Question text"
                      v-model="currentQuestion.text"
                    ></v-textarea>
                  </span>

                  <v-radio-group
                    v-model="currentQuestion.answer"
                    @change="saveQuestion(questionIndex)"
                    :mandatory="false"
                    v-if="currentQuestion.type == 0"
                  >
                    <template v-for="(option, i) in currentQuestion.options">
                      <v-text-field
                        v-model="currentQuestion.options[i]"
                        :key="questionIndex + '-' + i"
                      >
                        <v-radio
                          slot="prepend-inner"
                          :value="i"
                          :on-icon="`mdi-alpha-${letter('a', i, true)}-circle`"
                          :off-icon="
                            `mdi-alpha-${letter('a', i, true)}-circle-outline`
                          "
                        />
                      </v-text-field>
                    </template>
                  </v-radio-group>

                  <v-layout v-else-if="currentQuestion.type == 1" py-4 my-1 row>
                    <v-flex xs12 md6 lg4>
                      <template v-for="(option, i) in currentQuestion.options">
                        <v-text-field
                          v-model="currentQuestion.options[i]"
                          :key="questionIndex + '-' + i"
                        >
                          <v-checkbox
                            slot="prepend-inner"
                            v-model="currentQuestion.answer"
                            multiple
                            height="0"
                            class="mt-0 mb-1"
                            :value="i"
                            :on-icon="
                              `mdi-alpha-${letter('a', i, true)}-circle`
                            "
                            :off-icon="
                              `mdi-alpha-${letter('a', i, true)}-circle-outline`
                            "
                            @change="saveQuestion(questionIndex)"
                          />
                        </v-text-field>
                      </template>
                    </v-flex>
                  </v-layout>
                  <v-layout v-else-if="currentQuestion.type == 2" my-4>
                    <v-flex xs12 sm6 md3>
                      <v-text-field
                        label="Answer (0-999)"
                        v-model="currentQuestion.answer"
                        type="number"
                        @keyup="saveQuestion(questionIndex)"
                      ></v-text-field>
                    </v-flex>
                  </v-layout>
                  <v-layout v-else-if="currentQuestion.type == 3" column>
                    <v-layout row wrap justify-center>
                      <v-flex xs6>
                        <v-layout column justify-start>
                          <v-flex
                            v-for="(option, i) in currentQuestion.options"
                            :key="`${questionIndex}-option-${i}`"
                          >
                            <v-layout row wrap justify-start>
                              <v-flex xs8 :class="$style.option">
                                <v-textarea
                                  rows="1"
                                  :prepend-inner-icon="
                                    `mdi-alpha-${letter(
                                      'a',
                                      i,
                                      true
                                    )}-circle-outline`
                                  "
                                  v-model="currentQuestion.options[i]"
                                  clearable
                                />
                              </v-flex>
                            </v-layout>
                          </v-flex>
                        </v-layout>
                      </v-flex>
                      <v-flex xs6>
                        <v-layout column justify-end>
                          <v-flex
                            v-for="(answer, j) in currentQuestion.answers"
                            :key="`${questionIndex}-answer-${j}`"
                          >
                            <v-layout row wrap align-start>
                              <v-flex xs8 :class="$style.option">
                                <v-textarea
                                  rows="1"
                                  :prepend-inner-icon="
                                    `mdi-alpha-${letter(
                                      'p',
                                      j,
                                      true
                                    )}-circle-outline`
                                  "
                                  v-model="currentQuestion.answers[j]"
                                  clearable
                                />
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
                          v-for="j in currentQuestion.answers.length"
                          :key="`${questionIndex}-label-answer-${j}`"
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
                        v-for="i in currentQuestion.options.length"
                        :key="`${questionIndex}-label-option-${i}`"
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
                          v-for="j in currentQuestion.answers.length"
                          :key="`${questionIndex}-${i}-${j}`"
                        >
                          <v-checkbox
                            v-model="currentQuestion.answer[i - 1]"
                            multiple
                            height="0"
                            class="mt-0 mb-1"
                            :value="j - 1"
                            @change="saveQuestion(questionIndex)"
                            :on-icon="$vuetify.icons.radioOn"
                            :off-icon="$vuetify.icons.radioOff"
                          >
                          </v-checkbox>
                        </v-flex>
                      </v-layout>
                    </v-flex>
                  </v-layout>
                </v-tab-item>
              </v-sheet>
            </v-tabs-items>
          </v-card>
        </v-flex>
      </v-layout>
    </v-content>

    <v-footer color="transparent" height="auto" fixed app inset>
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
          <strong style="text-transform: uppercase;">{{ test.name }}</strong>
        </v-toolbar-title>
        <v-tabs
          slot="tabs"
          v-model="sectionIndex"
          color="transparent"
          hide-slider
          centered
        >
          <v-tab
            active-class="primary--text"
            v-for="(section, index) in sections"
            :key="section.subject"
            @click="changeSection(index)"
          >
            {{ section.subject }}
          </v-tab>
        </v-tabs>

        <span>
          <v-dialog v-model="newSectionDialog" persistent max-width="400px">
            <template v-slot:activator="{ on }">
              <v-btn fab small color="primary" dark v-on="on">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </template>
            <v-card :class="$style.dialog">
              <v-card-title>
                <span :class="$style.title">Create new section</span>
              </v-card-title>
              <v-card-text>
                <v-container grid-list-md>
                  <v-layout wrap>
                    <v-flex xs12>
                      <v-text-field
                        label="Section name"
                        required
                      ></v-text-field>
                    </v-flex>
                  </v-layout>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="error" flat @click="newSectionDialog = false">
                  Cancel
                </v-btn>
                <v-btn
                  color="success"
                  @click="
                    createNewSection;
                    newSectionDialog = false;
                  "
                >
                  Create
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </span>
        <v-divider />
        <span v-for="(question, i) in questions" :key="i">
          <v-btn
            fab
            small
            v-if="question.section == sectionIndex"
            dark
            :flat="i != questionIndex"
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
  props: {
    id: {
      required: true
    }
  },
  data() {
    return {
      questionTypes: [
        { value: 0, text: "Single Correct" },
        { value: 1, text: "Multiple Correct" },
        { value: 2, text: "Numerical" },
        { value: 3, text: "Matrix Match" },
        { value: 4, text: "One Word Answer" },
        { value: 5, text: "Subjective" }
      ],
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
      sectionIndex: 0,
      questionIndex: 0,
      newSectionDialog: false
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
    validQuestionIndex(i) {
      return i >= 0 && i <= this.questions.length - 1;
    },
    validSectionIndex(i) {
      return i >= 0 && i <= this.sections.length - 1;
    },
    changeSection(i) {
      console.log("Changing section...");
      if (this.validSectionIndex(i)) {
        this.sectionIndex = i;
        if (this.currentQuestion.section !== i)
          this.changeQuestion(this.currentSection.start);
        console.log(`Changed to section ${i + 1}`);
      }
    },
    changeQuestion(i) {
      console.log("Changing question...");
      if (this.validQuestionIndex(i)) {
        this.questionIndex = i;
        if (this.currentQuestion.section !== this.sectionIndex)
          this.changeSection(this.currentQuestion.section);
        console.log(`Changed to question ${i + 1}`);
      }
      this.updateStatus(i);
    },
    previousQuestion() {
      this.changeQuestion(this.questionIndex - 1);
    },
    nextQuestion() {
      this.changeQuestion(this.questionIndex + 1);
    },
    clearQuestion(i) {
      if (this.validQuestionIndex(i)) {
        if (this.questions[i].type === "MATRIX")
          this.questions[i].answer = [[], [], [], []];
        else this.questions[i].answer = [];
        this.questions[i].status = 1;
      }
    },
    saveQuestion(i) {
      if (this.validQuestionIndex(i) && !this.isEmpty(this.questions[i].answer))
        this.questions[i].status = 3;
      else this.clear(i);
    },
    updateStatus(i) {
      if (this.validQuestionIndex(i) && this.questions[i].status === 0)
        this.questions[i].status = 1;
    },
    addQuestion(type) {
      var question = {
        section: this.sectionIndex,
        text: "",
        image: null,
        type: type,
        options: ["Option A", "Option B", "Option C", "Option D"],
        status: 0,
        correctMarks: 4,
        incorrectMarks: 1
      };
      if (type === 3) {
        question.answers = [
          "Answer P",
          "Answer Q",
          "Answer R",
          "Answer S",
          "Answer T"
        ];
        question.answer = [[], [], [], []];
      } else question.answer = [];
      this.currentSection.end++;
      for (var i = this.sectionIndex + 1; i < this.sections.length; i++) {
        this.sections[i].start++;
        this.sections[i].end++;
      }
      this.questions.splice(this.currentSection.end, 0, question);
      this.changeQuestion(this.currentSection.end);
    },
    deleteQuestion(i) {
      if (!this.validQuestionIndex) return;
      this.sectionIndex = this.questions[i].section;
      this.currentSection.end--;
      for (var j = this.sectionIndex + 1; j < this.sections.length; j++) {
        this.sections[j].start--;
        this.sections[j].end--;
        this.sections[j].questionIndex = Math.min(
          this.sections[j].questionIndex,
          this.sections[j].start
        );
      }
      this.questions.splice(i, 1);
      this.changeQuestion(i);
    },
    saveTest() {
      this.$store.dispatch("tests/update", this.test);
    }
  },
  watch: {
    questionIndex: function(newQuestion, oldQuestion) {
      this.updateStatus(newQuestion);
    }
  },
  computed: {
    test() {
      return this.$store.state.tests.test;
    },
    sections() {
      return this.test.sections;
    },
    questions() {
      return this.test.questions;
    },
    answers() {
      return this.test.answers;
    },
    currentQuestion() {
      return this.test.questions[this.questionIndex];
    },
    currentSection() {
      return this.test.sections[this.sectionIndex];
    }
  },
  created() {
    this.$store.dispatch("tests/get", this.id);
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
.content{
  letter-spacing: 0.04em;
  background-color: #f6f6f6;
  font-family: 'Product Sans',Roboto,Arial,sans-serif;
}
.questionContainer{
  text-align: left;
  border: 1px solid #c9cbd0;
  border-radius: 8px;
  margin: 0 15px;

  .question{
    overflow-y: auto;
    .questionText{
      font-size: 1.3rem;
      letter-spacing: 0.02em;
      color: #606164;
    }
    .option{
      position: relative;
      margin-bottom: 5px;
      color: #787878;

      .optionLetter{
        position: absolute;
        left: 0
      }
    }
  }
}

.dialog{
  border: 1px solid #dadce0;
  border-radius: 5px;
  font-family: 'Product Sans Light',Roboto,Arial,sans-serif;
  text-align: left;
  .title{
    font-size: 1.375rem;
    line-height: 1.75rem;
    color: #5e5766;
  }
}
</style>
<style scoped>
.v-text-field {
  padding-top: 0;
}
.v-chip {
  padding-top: 15px;
}
.v-menu__content {
  border-radius: 8px;
  font-family: "Product Sans Light";
  font-size: 1.3rem;
  min-width: 160px;
}
</style>
