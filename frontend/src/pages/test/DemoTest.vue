<template>
  <div>
    <v-dialog v-model="submitDialog" max-width="400">
      <v-card :class="$style.submitDialog">
        <v-card-title :class="$style.title">
          Are you sure you want to submit the test?
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="info" flat @click="submitDialog = false">
            Cancel
          </v-btn>
          <v-btn
            dark
            color="indigo"
            @click="
              submitTest();
              submitDialog = false;
            "
          >
            Submit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <StandardLayout v-if="session && session.completed">
      <v-layout column align-center>
        <v-flex xs12 class="my-3">
          <v-btn round color="info" @click="reAttempt">
            Reattempt this test
          </v-btn>
        </v-flex>
        <Marks :questionWiseMarks="questionWiseMarks" :report="report" />
        <Analysis v-if="report && report.result" :report="report" />
        <v-card v-else :class="[$style.card, $style.message]">
          Analysis of your test is not generated yet.
        </v-card>
      </v-layout>
    </StandardLayout>
    <TestLayout v-else :sections="sections" :sectionIndex.sync="sectionIndex">
      <template slot="controls">
        <v-btn color="primary" flat>
          <v-icon> mdi-clock </v-icon>
          &nbsp; {{ this.time }}
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
          :src="require(`@/assets/logos/${currentQuestion.image}`)"
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
            :class="statusColor(response[i].status)"
            @click="changeQuestion(i)"
          >
            <span>{{ i + 1 }}</span>
          </v-btn>
        </span>
      </template>

      <template slot="submit">
        <v-btn
          outline
          color="indigo"
          fixed
          bottom
          :left="isSmallScreen"
          @click="submitDialog = true"
        >
          <v-icon>mdi-exit-to-app</v-icon>
          <span>Submit this test</span>
        </v-btn>
      </template>
    </TestLayout>
  </div>
</template>

<script>
import TestLayout from "@/components/test/TestLayout.vue";
import StandardLayout from "@/components/layouts/StandardLayout.vue";
import Marks from "./Marks";
import Analysis from "./Analysis";
import { demoTests } from "@/js/demoTests";

export default {
  data() {
    return {
      headers: [
        {
          text: "Subjects",
          align: "center",
          sortable: false,
          value: "name"
        },
        {
          text: "Marks Scored",
          value: "score",
          align: "center",
          sortable: true
        },
        {
          text: "Maximum Marks",
          value: "total_marks",
          align: "center",
          sortable: false
        }
      ],
      error: false,
      questionTypes: [
        { value: 0, text: "Single Correct" },
        { value: 1, text: "Multiple Correct" },
        { value: 2, text: "Numerical" },
        { value: 3, text: "Matrix Match" },
        { value: 4, text: "One Word Answer" },
        { value: 5, text: "Subjective" }
      ],
      report: localStorage.getItem("report")
        ? JSON.parse(localStorage.getItem("report"))
        : {},
      questionWiseMarks: [],
      isSmallScreen: this.$vuetify.breakpoint.smAndDown,
      submitDialog: false,
      session: localStorage.getItem("demoSession")
        ? JSON.parse(localStorage.getItem("demoSession"))
        : demoSession
    };
  },
  components: {
    StandardLayout,
    TestLayout,
    Marks,
    Analysis
  },
  methods: {
    getRandom(min, max) {
      return Math.random() * (max - min) + min;
    },
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
    startTest() {},
    markForReview(i) {
      if (this.isEmpty(this.answers[i].answer)) this.response[i].status = 2;
      else this.response[i].status = 4;
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
        if (this.questions[i].type === 3)
          this.answers[i].answer = [[], [], [], []];
        else this.answers[i].answer = [];
        this.response[i].status = 1;
      }
    },
    saveQuestion(i) {
      if (this.validQuestionIndex(i) && !this.isEmpty(this.answers[i].answer))
        this.response[i].status = 3;
      else this.clearQuestion(i);
    },
    updateStatus(i) {
      if (this.response) {
        if (this.validQuestionIndex(i) && this.response[i].status === 0)
          this.response[i].status = 1;
      }
    },
    updateTime() {
      if (this.session) {
        this.response[this.questionIndex].timeElapsed += 1;

        var duration = this.session.duration;
        duration = duration.split(":");
        duration =
          (parseInt(duration[0]) * 3600 +
            parseInt(duration[1]) * 60 +
            parseInt(duration[2]) -
            1) *
          1000;

        var hours = Math.floor(duration / (1000 * 60 * 60));
        duration -= hours * 60 * 60 * 1000;
        var minutes = Math.floor(duration / (1000 * 60));
        duration -= minutes * 60 * 1000;
        var seconds = Math.floor(duration / 1000);

        this.session.duration =
          hours +
          ":" +
          ("0" + minutes).slice(-2) +
          ":" +
          ("0" + seconds).slice(-2);
      }
    },
    submitTest() {
      if (!this.session.completed) this.session.completed = true;
      this.calculateResult();
    },
    calculateResult() {
      var responses = this.session.response;
      var answers = this.test.answers;
      var noOfSections = this.sections.length;
      var maxMarks = [];
      var sectionWise = [];
      var currentQuestion = {};
      var questionWiseMarks = [];
      var topicWiseMarks = [];
      var i = 0;
      for (i = 0; i < noOfSections; i++) {
        maxMarks.push(0);
        sectionWise.push(0);
      }
      maxMarks.push(0);
      var marks = { total: 0, maxMarks, sectionWise };
      for (i = 0; i < this.questions.length; i++) {
        questionWiseMarks.push({ marks: 0, status: 0 });
      }
      for (i = 0; i < this.sections.length; i++) {
        topicWiseMarks.push({});
      }
      var report = {
        test: {},
        response: [],
        result: {},
        marks
      };
      report.test = this.test;
      for (i = 0; i < this.questions.length; i++) {
        currentQuestion = this.questions[i];
        marks.maxMarks[noOfSections] += currentQuestion.correctMarks;
        marks.maxMarks[currentQuestion.section] += currentQuestion.correctMarks;
        if (
          this.session.test.questions[i].type === 0 &&
          responses[i].answer.length !== 0
        ) {
          if (responses[i].answer === answers[i].answer) {
            questionWiseMarks[i].marks = currentQuestion.correctMarks;
            questionWiseMarks[i].status = 2;
            report.marks.total += currentQuestion.correctMarks;
            report.marks.sectionWise[currentQuestion.section] +=
              currentQuestion.correctMarks;
          } else if (responses[i].answer !== answers[i].answer) {
            questionWiseMarks[i].marks = -currentQuestion.incorrectMarks;
            questionWiseMarks[i].status = 1;
            report.marks.total -= currentQuestion.incorrectMarks;
            report.marks.sectionWise[currentQuestion.section] -=
              currentQuestion.incorrectMarks;
          }
        } else if (
          this.questions[i].type === 1 &&
          responses[i].answer.length !== 0
        ) {
          var arrayOfChildrenNames = responses[i].answer;
          var arrayOfFamilyMemberNames = answers[i].answer;
          var isarrayOfNamesSubsetOfFamily = arrayOfChildrenNames.every(
            function(val) {
              return arrayOfFamilyMemberNames.indexOf(val) >= 0;
            }
          );
          if (
            isarrayOfNamesSubsetOfFamily &&
            arrayOfChildrenNames.length < arrayOfFamilyMemberNames.length &&
            currentQuestion.partialMarks !== 0
          ) {
            report.marks.total +=
              arrayOfChildrenNames.length * currentQuestion.partialMarks;
            questionWiseMarks[i].marks =
              currentQuestion.partialMarks * arrayOfChildrenNames.length;
            questionWiseMarks[i].status = 3;
            report.marks.sectionWise[currentQuestion.section] +=
              currentQuestion.partialMarks * arrayOfChildrenNames.length;
          } else if (isarrayOfNamesSubsetOfFamily) {
            questionWiseMarks[i].marks = currentQuestion.correctMarks;
            questionWiseMarks[i].status = 2;
            report.marks.total += currentQuestion.correctMarks;
            report.marks.sectionWise[currentQuestion.section] +=
              currentQuestion.correctMarks;
          } else {
            questionWiseMarks[i].marks = -currentQuestion.incorrectMarks;
            questionWiseMarks[i].status = 1;
            report.marks.total -= currentQuestion.incorrectMarks;
            report.marks.sectionWise[currentQuestion.section] -=
              currentQuestion.incorrectMarks;
          }
        } else if (
          this.questions[i].type === 2 &&
          responses[i].answer.length !== 0
        ) {
          if (
            parseFloat(responses[i].answer) / parseFloat(answers[i].answer) >=
            0.99 <=
            1.01
          ) {
            questionWiseMarks[i].marks = currentQuestion.correctMarks;
            questionWiseMarks[i].status = 2;
            report.marks.total += currentQuestion.correctMarks;
            report.marks.sectionWise[currentQuestion.section] +=
              currentQuestion.correctMarks;
          } else {
            questionWiseMarks[i].marks = -currentQuestion.incorrectMarks;
            questionWiseMarks[i].status = 1;
            report.marks.total -= currentQuestion.incorrectMarks;
            report.marks.sectionWise[currentQuestion.section] -=
              currentQuestion.incorrectMarks;
          }
        } else if (
          this.questions[i].type === 3 &&
          responses[i].answer.length !== 0
        ) {
          // For Matrix match for each part status 0 means unanswered 1 means incorrect 2 means correct
          var responsesMatrix = responses[i].answer;
          var answersMatrix = answers[i].answer;
          var curMarks = [];
          for (var j = 0; j < responsesMatrix.length; j++) {
            curMarks.push({ marks: 0, status: 0 });
          }
          for (j = 0; j < responsesMatrix.length; j++) {
            if (responsesMatrix[j].length !== 0) {
              responsesMatrix[j].sort();
              answersMatrix[j].sort();
              console.log(responsesMatrix[j], answersMatrix[j]);
              console.log(responsesMatrix[j] === answersMatrix[j]);

              if (
                JSON.stringify(responsesMatrix[j]) ===
                JSON.stringify(answersMatrix[j])
              ) {
                curMarks[j]["marks"] = currentQuestion.partialMarks;
                curMarks[j]["status"] = 2;
              } else {
                curMarks[j]["marks"] = currentQuestion.incorrectMarks * -1;
                console.log("Matrix incorrect");
                curMarks[j]["status"] = 1;
              }
            }
          }
          var totalMatrixMarks = 0;
          var matrixMarks = [];
          var matrixStatus = [];
          for (j = 0; j < curMarks.length; j++) {
            totalMatrixMarks += curMarks[j]["marks"];
            matrixMarks.push(curMarks[j]["marks"]);
            matrixStatus.push(curMarks[j]["status"]);
          }
          questionWiseMarks[i].marks = matrixMarks;
          questionWiseMarks[i].status = matrixStatus;
          report.marks.total += totalMatrixMarks;
          report.marks.sectionWise[currentQuestion.section] += totalMatrixMarks;
        }
        var currentTopic = topicWiseMarks[this.questions[i].section];
        var curTopicMarks = 0;
        if (Array.isArray(questionWiseMarks[i].marks))
          curTopicMarks = questionWiseMarks[i].marks.reduce((a, b) => a + b, 0);
        else curTopicMarks = questionWiseMarks[i].marks;
        if (
          Object.prototype.hasOwnProperty.call(
            currentTopic,
            this.questions[i].topicIndex
          )
        )
          currentTopic[this.questions[i].topicIndex] += curTopicMarks;
        else currentTopic[this.questions[i].topicIndex] = curTopicMarks;
      }
      report.result.questionWiseMarks = questionWiseMarks;
      report.result.topicWiseMarks = topicWiseMarks;
      this.report = report;
      localStorage.setItem("report", JSON.stringify(report));
    },
    reAttempt() {
      this.session = {
        response: [],
        test: this.test,
        duration: this.test.time_alotted,
        current: { questionIndex: 0, sectionIndex: 0 },
        completed: false
      };
      for (var i = 0; i < this.questions.length; i++) {
        this.session.response.push({
          answer: [],
          status: 0,
          timeElapsed: 0
        });
      }
      localStorage.demoSession = JSON.stringify(this.session);
      localStorage.removeItem("report");
    }
  },
  watch: {
    questionIndex: function(newQuestion, oldQuestion) {
      this.updateStatus(newQuestion);
    },
    session: {
      deep: true,
      handler(newSession, oldSession) {
        if (!this.oldSession || !this.oldSession.completed) {
          if (newSession.duration <= 0 && !newSession.completed) {
            this.submitTest();
            this.session.completed = true;
          }
          localStorage.demoSession = JSON.stringify(newSession);
        }
      }
    }
  },
  computed: {
    test() {
      return this.session.test;
    },
    time() {
      return this.session.duration;
    },
    sectionIndex: {
      get: function() {
        return this.session.current.sectionIndex;
      },
      set: function(value) {
        this.session.current.sectionIndex = value;
      }
    },
    questionIndex: {
      get: function() {
        return this.session.current.questionIndex;
      },
      set: function(value) {
        this.session.current.questionIndex = value;
      }
    },
    sections() {
      return this.test.sections;
    },
    questions() {
      return this.test.questions;
    },
    response() {
      return this.session.response;
    },
    answers() {
      return this.response;
    },
    currentQuestion() {
      return this.questions[this.questionIndex];
    },
    currentAnswer() {
      return this.response[this.questionIndex];
    },
    currentSection() {
      return this.test.sections[this.sectionIndex];
    }
  },
  created() {
    if (!localStorage.getItem("demoSession"))
      localStorage.setItem("demoSession", JSON.stringify(demoSession));
  },
  mounted() {
    if (!this.session.completed) setInterval(this.updateTime, 1000);
  }
};
</script>

<style module lang="stylus">
@require '~@/stylus/theme/colors';

.submitDialog, .card{
  border: 1px solid #dadce0;
  border-radius: 5px;
  font-family: 'Product Sans Light', Roboto, Arial, sans-serif;
  text-align: left;
  .title{
    padding: 20px 10px 70px;
    font-size: 1.375rem;
    line-height: 1.75rem;
    color: #5e5766;
  }
}

.card{
  width: 100%;
  min-height: 400px;
  padding: 25px auto;
}

.message{
  font-family: 'Product Sans Thin', Roboto, Arial, sans-serif;
  font-size: 22pt;
  margin: 10px auto;
}

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
