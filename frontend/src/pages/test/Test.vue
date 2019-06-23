<template>
  <TestLayout :sections="sections" :sectionIndex.sync="sectionIndex">
    <template slot="controls">
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
          markForReview(questionIndex);
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
        @click="clearQuestion(questionIndex)"
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
          saveQuestion(questionIndex);
          nextQuestion();
        "
      >
        <v-icon>mdi-content-save-move</v-icon>
        <span v-if="!isSmallScreen">Save response & next </span>
      </v-btn>
    </template>

    <template slot="info">
      <v-btn color="success lighten-1" class="subheading" small outline icon>
        +{{ currentQuestion.correctMarks }}
      </v-btn>
      <v-btn color="error lighten-1" class="subheading" small outline icon>
        -{{ currentQuestion.incorrectMarks }}
      </v-btn>
      <v-chip color="indigo" outline>
        {{ questionTypes[currentQuestion.type].text }}
      </v-chip>
    </template>

    <template slot="text-image">
      <v-img
        v-if="currentQuestion.image"
        :src="require(`@assets/logos/${currentQuestion.image}`)"
        class="mb-3"
      ></v-img>
      <v-chip color="grey darken-2" outline small>
        <strong> Q{{ questionIndex + 1 }} </strong>
      </v-chip>
      <span :class="$style.questionText">
        {{ currentQuestion.text }}
      </span>
    </template>

    <v-layout slot="options">
      <v-radio-group
        v-model="currentAnswer.answer"
        @change="saveQuestion(questionIndex)"
        :mandatory="false"
        v-if="currentQuestion.type == 0"
      >
        <v-radio
          v-for="(option, i) in currentQuestion.options"
          :key="questionIndex + '-' + i"
          :label="option"
          :value="i"
          :on-icon="`mdi-alpha-${letter('a', i, true)}-circle`"
          :off-icon="`mdi-alpha-${letter('a', i, true)}-circle-outline`"
        ></v-radio>
      </v-radio-group>

      <v-layout v-else-if="currentQuestion.type == 1" py-4 my-1 column>
        <v-checkbox
          v-for="(option, i) in currentQuestion.options"
          v-model="currentAnswer.answer"
          multiple
          height="0"
          class="mt-0 mb-1"
          :key="questionIndex + '-' + i"
          :label="option"
          :value="i"
          :on-icon="`mdi-alpha-${letter('a', i, true)}-circle`"
          :off-icon="`mdi-alpha-${letter('a', i, true)}-circle-outline`"
          @change="saveQuestion(questionIndex)"
        >
        </v-checkbox>
      </v-layout>
      <v-layout v-else-if="currentQuestion.type == 2" my-4>
        <v-flex xs12 sm6 md3>
          <v-text-field
            label="Enter your answer (0-999)"
            v-model="currentAnswer.answer"
            type="number"
            @keyup="saveQuestion(questionIndex)"
          ></v-text-field>
        </v-flex>
      </v-layout>
      <v-layout v-else-if="currentQuestion.type == 3" my-3 column>
        <v-layout row wrap justify-center>
          <v-flex xs6>
            <v-layout column justify-start>
              <v-flex
                v-for="(option, i) in currentQuestion.options"
                :key="`${questionIndex}-option-${i}`"
              >
                <v-layout row wrap align-start>
                  <v-flex xs8 :class="$style.option">
                    <v-icon :class="$style.optionLetter">
                      {{ `mdi-alpha-${letter("a", i, true)}-circle-outline` }}
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
                v-for="(answer, j) in currentQuestion.answers"
                :key="`${questionIndex}-answer-${j}`"
              >
                <v-layout row wrap align-start>
                  <v-flex xs8 :class="$style.option">
                    <v-icon :class="$style.optionLetter">
                      {{ `mdi-alpha-${letter("p", j, true)}-circle-outline` }}
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
                :off-icon="`mdi-alpha-${letter('a', i - 1, true)}-circle`"
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
                v-model="currentAnswer.answer[i - 1]"
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
    </v-layout>

    <template slot="footer">
      <input @keyup.left="previousQuestion" type="hidden" />
      <input @keyup.right="nextQuestion" type="hidden" />
      <v-btn icon color="primary" @click="previousQuestion()">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <v-btn icon color="primary" @click="nextQuestion()">
        <v-icon>mdi-arrow-right</v-icon>
      </v-btn>
    </template>

    <template slot="test-name">{{ test.name }}</template>

    <template slot="sections">
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
    </template>

    <template slot="questions-panel">
      <span v-for="(question, i) in questions" :key="i">
        <v-btn
          fab
          v-if="question.section == sectionIndex"
          dark
          small
          :flat="i != questionIndex"
          :class="statusColor(question.status)"
          @click="changeQuestion(i)"
        >
          <span>{{ i + 1 }}</span>
        </v-btn>
      </span>
    </template>

    <template slot="submit">
      <v-btn outline color="indigo" fixed bottom :left="isSmallScreen">
        <v-icon>mdi-exit-to-app</v-icon>
        <span>Submit this test</span>
      </v-btn>
    </template>
  </TestLayout>
</template>

<script>
import TestLayout from "@components/test/TestLayout.vue";

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
      isSmallScreen: this.$vuetify.breakpoint.smAndDown,
      time: "1:14:12",
      sectionIndex: 0,
      questionIndex: 0,
      emptyQuestion: {
        section: 0,
        text: "",
        image: null,
        type: 0,
        options: ["Option A", "Option B", "Option C", "Option D"],
        status: 0,
        correctMarks: 4,
        incorrectMarks: 1,
        answers: ["Answer P", "Answer Q", "Answer R", "Answer S", "Answer T"]
      }
    };
  },
  components: {
    TestLayout
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
    markForReview(i) {
      if (this.isEmpty(this.answers[i].answer)) this.questions[i].status = 2;
      else this.questions[i].status = 4;
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
        if (this.currentQuestion && this.currentQuestion.section !== i)
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
          this.answers[i].answer = [[], [], [], []];
        else this.answers[i].answer = [];
        this.questions[i].status = 1;
      }
    },
    saveQuestion(i) {
      if (this.validQuestionIndex(i) && !this.isEmpty(this.answers[i].answer))
        this.questions[i].status = 3;
      else this.clearQuestion(i);
    },
    updateStatus(i) {
      if (this.validQuestionIndex(i) && this.questions[i].status === 0)
        this.questions[i].status = 1;
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
      if (this.test.questions) return this.test.questions[this.questionIndex];
      else return this.emptyQuestion;
    },
    currentAnswer() {
      if (this.test.answers) return this.test.answers[this.questionIndex];
      else return [];
    },
    currentSection() {
      return this.test.sections[this.sectionIndex];
    }
  },
  created() {
    this.$store.dispatch("tests/get", this.id);
  },
  mounted() {}
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
.questionText{
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
</style>
