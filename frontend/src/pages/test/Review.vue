<template>
  <div>
    <WideLayout v-if="loading || error">
      <v-card :class="$style.card">
        <v-layout column py-5 align-center>
          <template v-if="loading">
            <v-flex xs12 :class="$style.message">
              Loading Review...
            </v-flex>
            <v-flex xs12>
              <v-progress-circular
                :size="70"
                :width="5"
                color="grey darken-1"
                indeterminate
              />
            </v-flex>
          </template>
          <v-flex xs12 v-if="error" :class="$style.message">
            {{ this.status.error }}
          </v-flex>
        </v-layout>
      </v-card>
    </WideLayout>
    <TestLayout v-else :sections="sections" :sectionIndex.sync="sectionIndex">
      <template slot="controls">
        <v-btn color="primary" flat>
          <v-icon> mdi-clock </v-icon>
          &nbsp; {{ this.time }}
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
            disabled
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
            disabled
          >
          </v-checkbox>
        </v-layout>
        <v-layout v-else-if="currentQuestion.type == 2" my-4>
          <v-flex xs12 sm6 md3>
            <v-text-field
              label="Enter your answer (0-999)"
              v-model="currentAnswer.answer"
              type="number"
              disabled
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
                  disabled
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
    </TestLayout>
  </div>
</template>

<script>
import TestLayout from "@components/test/TestLayout.vue";
import WideLayout from "@components/layouts/WideLayout.vue";
import { mapState } from "vuex";

export default {
  data() {
    return {
      id: this.$route.params.id,
      loading:
        this.$store.state.reviews.status.loading ||
        !this.$store.state.reviews.status.exists,
      error: false,
      questionTypes: [
        { value: 0, text: "Single Correct" },
        { value: 1, text: "Multiple Correct" },
        { value: 2, text: "Numerical" },
        { value: 3, text: "Matrix Match" },
        { value: 4, text: "One Word Answer" },
        { value: 5, text: "Subjective" }
      ],
      isSmallScreen: this.$vuetify.breakpoint.smAndDown,
      sectionIndex: 0,
      questionIndex: 0
    };
  },
  components: {
    WideLayout,
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
    },
    previousQuestion() {
      this.changeQuestion(this.questionIndex - 1);
    },
    nextQuestion() {
      this.changeQuestion(this.questionIndex + 1);
    }
  },
  computed: {
    ...mapState({
      status: state => state.reviews.status
    }),
    session() {
      return this.$store.state.reviews.review;
    },
    test() {
      if (this.session) return this.session.test;
      else return {};
    },
    time() {
      if (this.session) return this.session.duration;
      else return null;
    },
    sections() {
      if (this.test) return this.test.sections;
      else return [];
    },
    questions() {
      if (this.test) return this.test.questions;
      else return [];
    },
    response() {
      if (this.session) return this.session.response;
      else return [];
    },
    answers() {
      if (this.response) return this.response;
      else return [];
    },
    currentQuestion() {
      if (this.test && this.test.questions)
        return this.test.questions[this.questionIndex];
      else return [];
    },
    currentAnswer() {
      if (this.session) return this.response[this.questionIndex];
      else return [];
    },
    currentSection() {
      if (this.session) return this.test.sections[this.sectionIndex];
      else return [];
    }
  },
  created() {
    if (!this.$store.state.reviews.status.exists) {
      this.$watch("status", function(newStatus, oldStatus) {
        this.loading = newStatus.loading;
        this.error = newStatus.error;
      });
      this.$store.dispatch(`reviews/get`, this.id);
    }
  },
  mounted() {}
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

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
