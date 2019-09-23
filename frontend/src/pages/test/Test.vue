<template>
  <v-flex xs12>
    <v-dialog v-model="submitDialog" max-width="400">
      <v-card :class="$style.submitDialog">
        <v-card-title :class="$style.title">
          Are you sure you want to submit the test?
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red" flat @click="submitDialog = false">
            Cancel
          </v-btn>
          <v-btn
            dark
            color="primary"
            :loading="submitting"
            @click="
              loader = 'loading';
              submitTest();
            "
          >
            Submit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
          :src="require(`@/assets/logos/${currentQuestion.image}`)"
          class="mb-3"
        ></v-img>
        <v-chip color="grey darken-2" outline small>
          <strong> Q{{ questionIndex + 1 }} </strong>
        </v-chip>
        <p
          :class="[$style.questionText, 'ck-content']"
          v-html="currentQuestion.text"
        ></p>
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
        <v-btn
          :disabled="this.questionIndex === 0"
          :outline="this.questionIndex === 0"
          icon
          color="primary"
          @click="previousQuestion()"
        >
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <v-btn
          :disabled="this.questionIndex === this.questions.length - 1"
          :outline="this.questionIndex === this.questions.length - 1"
          icon
          color="primary"
          @click="nextQuestion()"
        >
          <v-icon>mdi-arrow-right</v-icon>
        </v-btn>
      </template>

      <template slot="test-name">
        {{ test.name }}{{ session.practice ? " (Practice)" : "" }}
      </template>

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
  </v-flex>
</template>

<script>
import TestLayout from "@/components/test/TestLayout.vue";
import StandardLayout from "@/components/layouts/StandardLayout.vue";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import { mapState } from "vuex";

export default {
  props: ["sessionData"],
  data() {
    return {
      questionEditor: ClassicEditor,
      questionConfig: {
        toolbar: ["|"]
      },
      id: this.$route.params.id,
      loading:
        this.$store.state.sessions.status.loading ||
        !this.$store.state.sessions.status.exists,
      error: false,
      submitting: false,
      questionTypes: [
        { value: 0, text: "Single Correct" },
        { value: 1, text: "Multiple Correct" },
        { value: 2, text: "Numerical" },
        { value: 3, text: "Matrix Match" },
        { value: 4, text: "One Word Answer" },
        { value: 5, text: "Subjective" }
      ],
      isSmallScreen: this.$vuetify.breakpoint.smAndDown,
      submitDialog: false,
      session: this.sessionData
    };
  },
  components: {
    TestLayout
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

        var currentTime = new Date();
        var checkinTime = new Date(Date.parse(this.session.checkin_time));
        var durationSplit = this.session.test.time_alotted.split(":");
        var duration =
          (parseInt(durationSplit[0] * 60 * 60) +
            parseInt(durationSplit[1] * 60) +
            parseInt(durationSplit[2])) *
          1000;

        var clock = duration - (currentTime - checkinTime);

        var hours = Math.floor(clock / (1000 * 60 * 60));
        clock -= hours * 60 * 60 * 1000;
        var minutes = Math.floor(clock / (1000 * 60));
        clock -= minutes * 60 * 1000;
        var seconds = Math.floor(clock / 1000);

        this.session.duration =
          hours +
          ":" +
          ("0" + minutes).slice(-2) +
          ":" +
          ("0" + seconds).slice(-2);
      }
    },
    submitTest() {
      this.session.completed = true;
      this.submitting = true;
      var vm = this;
      setTimeout(_ => {
        vm.$emit("updateSession");
      }, 500);
    }
  },
  watch: {
    questionIndex: function(newQuestion, oldQuestion) {
      this.updateStatus(newQuestion);
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
      return this.test.questions[this.questionIndex];
    },
    currentAnswer() {
      return this.response[this.questionIndex];
    },
    currentSection() {
      return this.test.sections[this.sectionIndex];
    }
  },
  mounted() {
    setInterval(this.updateTime, 1000);
    var vm = this;
    setInterval(function() {
      vm.$emit("update", vm.session);
    }, 5000);
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
