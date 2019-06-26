<template>
  <TestLayout :sections="sections" :sectionIndex="sectionIndex">
    <template slot="controls">
      <v-btn color="primary" flat>
        <v-text-field
          prepend-inner-icon="mdi-clock"
          v-model="test['time_alotted']"
        />
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
        color="red"
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
    </template>

    <template slot="info">
      <v-menu offset-y transition="slide-y-transition" bottom max-height="300">
        <template v-slot:activator="{ on }">
          <v-btn color="success" round outline v-on="on">
            <v-icon>mdi-plus</v-icon>
            <span v-if="!isSmallScreen">
              {{ currentQuestion.correctMarks }} &nbsp;
            </span>
          </v-btn>
        </template>
        <v-list>
          <v-list-tile
            v-for="n in 100"
            :key="n"
            @click="currentQuestion.correctMarks = n"
          >
            <v-list-tile-title>{{ n }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>
      <v-menu offset-y transition="slide-y-transition" bottom max-height="300">
        <template v-slot:activator="{ on }">
          <v-btn color="error" round outline v-on="on">
            <v-icon>mdi-minus</v-icon>
            <span v-if="!isSmallScreen">
              {{ currentQuestion.incorrectMarks }} &nbsp;
            </span>
          </v-btn>
        </template>
        <v-list>
          <v-list-tile
            v-for="n in 20"
            :key="n"
            @click="currentQuestion.correctMarks = n"
          >
            <v-list-tile-title>{{ n }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>
      <v-menu offset-y transition="slide-y-transition" bottom>
        <template v-slot:activator="{ on }">
          <v-btn color="indigo" round outline v-on="on">
            <span v-if="!isSmallScreen">
              {{ questionTypes[currentQuestion.type].text }} &nbsp;
            </span>
            <v-icon>mdi-chevron-down</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-tile
            v-for="(type, index) in questionTypes"
            :key="index"
            @click="
              currentQuestion.type = type.value;
              clearQuestion(questionIndex);
            "
          >
            <v-list-tile-title>{{ type.text }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>
    </template>

    <template slot="text-image">
      <v-img
        v-if="currentQuestion.image"
        :src="require(`@assets/logos/${currentQuestion.image}`)"
        class="mb-3"
      ></v-img>
      <span :class="$style.questionText">
        <v-textarea
          rows="1"
          :prepend-inner-icon="`mdi-numeric-${questionIndex + 1}-circle`"
          placeholder="Question text"
          v-model="currentQuestion.text"
        ></v-textarea>
      </span>
    </template>

    <v-layout slot="options">
      <v-radio-group
        v-model="currentAnswer.answer"
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
              :off-icon="`mdi-alpha-${letter('a', i, true)}-circle-outline`"
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
                v-model="currentAnswer.answer"
                multiple
                height="0"
                class="mt-0 mb-1"
                :value="i"
                :on-icon="`mdi-alpha-${letter('a', i, true)}-circle`"
                :off-icon="`mdi-alpha-${letter('a', i, true)}-circle-outline`"
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
            v-model="currentAnswer.answer"
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
                        `mdi-alpha-${letter('a', i, true)}-circle-outline`
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
                        `mdi-alpha-${letter('p', j, true)}-circle-outline`
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

    <template slot="section-controls">
      <v-dialog v-model="newSectionDialog" persistent max-width="400px">
        <template v-slot:activator="{ on }">
          <v-btn round outline small color="primary" dark v-on="on">
            <v-icon>mdi-plus</v-icon>
            Create new section
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
                    label="Subject"
                    v-model="newSectionSubject"
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
                addSection(newSectionSubject);
                newSectionDialog = false;
              "
            >
              Create
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-btn
        round
        outline
        small
        color="error"
        @click="deleteSection(sectionIndex)"
      >
        <v-icon>mdi-delete</v-icon>
        Delete this section
      </v-btn>
    </template>

    <template slot="questions-panel">
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
    </template>

    <template slot="submit">
      <v-btn
        outline
        color="success"
        fixed
        bottom
        :left="isSmallScreen"
        @click="saveTest()"
      >
        <v-icon>mdi-content-save</v-icon>
        <span>Save this test</span>
      </v-btn>
    </template>
  </TestLayout>
</template>

<script>
import TestLayout from "@components/test/TestLayout.vue";

export default {
  props: {
    testType: {
      required: true,
      validator: function(value) {
        return ["tests", "unitTests"].indexOf(value) !== -1;
      }
    }
  },
  data() {
    return {
      id: this.$route.params.id,
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
      swipeActions: {
        left: () => this.nextQuestion(),
        right: () => this.previousQuestion()
      },
      sectionIndex: 0,
      questionIndex: 0,
      newSectionDialog: false,
      newSectionSubject: "",
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
    validQuestionIndex(i) {
      return i >= 0 && i < this.questions.length;
    },
    validSectionIndex(i) {
      return i >= 0 && i < this.sections.length;
    },
    changeSection(i) {
      console.log(`Going to section ${i + 1}...`);
      if (this.validSectionIndex(i)) {
        this.sectionIndex = i;
        if (this.currentQuestion && this.currentQuestion.section !== i)
          this.changeQuestion(this.currentSection.start);
        console.log(`Changed to section ${i + 1}`);
        return true;
      } else return false;
    },
    previousSection() {
      return this.changeSection(this.sectionIndex - 1);
    },
    nextSection() {
      return this.changeSection(this.sectionIndex + 1);
    },
    changeQuestion(i) {
      console.log("Changing question...");
      if (this.validQuestionIndex(i)) {
        this.questionIndex = i;
        if (this.currentQuestion.section !== this.sectionIndex)
          this.changeSection(this.currentQuestion.section);
        console.log(`Changed to question ${i + 1}`);
        this.updateStatus(i);
        return true;
      } else return false;
    },
    previousQuestion() {
      return this.changeQuestion(this.questionIndex - 1);
    },
    nextQuestion() {
      return this.changeQuestion(this.questionIndex + 1);
    },
    clearQuestion(i) {
      if (this.validQuestionIndex(i)) {
        if (this.questions[i].type === 3)
          this.answers[i].answer = [[], [], [], []];
        else this.answers[i].answer = [];
        this.questions[i].status = 1;
      }
    },
    saveQuestion(i) {
      if (this.validQuestionIndex(i) && !this.isEmpty(this.answers[i]))
        this.questions[i].status = 3;
      else this.clear(i);
    },
    updateStatus(i) {
      if (this.validQuestionIndex(i) && this.questions[i].status === 0)
        this.questions[i].status = 1;
    },
    addQuestion(type) {
      let question = { ...this.emptyQuestion };
      question.type = type;
      question.section = this.sectionIndex;

      let answer = { answer: [] };
      if (type === 3) answer = { answer: [[], [], [], []] };

      this.currentSection.end++;
      for (let j = this.sectionIndex + 1; j < this.sections.length; j++) {
        this.sections[j].start++;
        this.sections[j].end++;
      }
      this.questions.splice(this.currentSection.end, 0, question);
      this.answers.splice(this.currentSection.end, 0, answer);
      this.changeQuestion(this.currentSection.end);
    },
    deleteQuestion(i) {
      let index = this.questions[i].section;
      let section = this.sections[index];
      if (!this.validQuestionIndex) return false;
      else if (section.end > section.start) {
        section.end--;
        for (let j = index + 1; j < this.sections.length; j++) {
          this.sections[j].start--;
          this.sections[j].end--;
        }
        this.questions.splice(i, 1);
        this.answers.splice(i, 1);
        if (!this.previousQuestion()) return this.nextQuestion();
        else return true;
      } else return false;
    },
    saveTest() {
      this.$store.dispatch(`${this.testType}/update`, this.test);
    },
    addSection(name) {
      this.sections.push({
        subject: name,
        start: this.questions.length,
        end: this.questions.length - 1
      });
      this.changeSection(this.sections.length - 1);
      this.addQuestion(0);
    },
    deleteSection(i) {
      if (this.sections.length > 1) {
        let start = this.sections[i].start;
        let end = this.sections[i].end;
        let len = end - start + 1;
        for (let j = end + 1; j < this.questions.length; j++) {
          this.questions[j].section--;
        }
        for (let j = i + 1; j < this.sections.length; j++) {
          this.sections[j].start -= len;
          this.sections[j].end -= len;
        }
        this.sections.splice(i, 1);
        this.questions.splice(start, len);
        this.answers.splice(start, len);
        console.log(this.currentSection);
      } else return false;
    }
  },
  watch: {
    questionIndex: function(newQuestion, oldQuestion) {
      this.updateStatus(newQuestion);
    }
  },
  computed: {
    test() {
      return this.$store.state[this.testType].test;
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
    this.$store.dispatch(`${this.testType}/get`, this.id);
  },
  mounted() {}
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
.questionInfo{
  border-bottom: 1px solid grey !important;
}

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
  font-family: "Product Sans Light";
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
