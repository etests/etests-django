<template>
  <TestLayout :sections="sections" :sectionIndex="sectionIndex">
    <template slot="controls">
      <v-chip class="transparent primary--text" flat>
        <v-text-field
          prepend-inner-icon="mdi-clock"
          type="time"
          v-model="test['time_alotted']"
          width="100px"
        />
      </v-chip>
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
        @click="deleteQuestion(questionIndex)"
      >
        <v-icon>mdi-delete</v-icon>
        <span v-if="!isSmallScreen">Delete question</span>
      </v-btn>
      <v-btn color="primary"
        round
        outline
        :icon="isSmallScreen"
        :small="!isSmallScreen"
        @click="solutionDialog = true"
      >
        <v-icon>mdi-eye</v-icon>
        <span v-if="!isSmallScreen">&nbsp; Solution</span>
      </v-btn>
      <v-bottom-sheet v-model="solutionDialog">
        <v-sheet class="pa-2" min-height="200px">
          <ckeditor
            :editor="questionEditor"
            :config="questionConfig"
            v-model="currentAnswer.solution"
          />
        </v-sheet>
      </v-bottom-sheet>
    </template>

    <template slot="info">
      <v-layout row wrap align-center justify-center>
        <v-flex xs4 md1>
          <v-menu
            v-if="currentQuestion.type !== 3"
            offset-y
            transition="slide-y-transition"
            bottom
            max-height="300"
          >
            <template v-slot:activator="{ on }">
              <v-btn icon large color="success" round outline v-on="on">
                <v-icon>mdi-plus</v-icon>
                <span> {{ currentQuestion.correctMarks }} &nbsp; </span>
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
        </v-flex>
        <v-flex xs4 md1 v-if="[1, 3].includes(currentQuestion.type)">
          <v-menu
            offset-y
            transition="slide-y-transition"
            bottom
            max-height="300"
          >
            <template v-slot:activator="{ on }">
              <v-btn icon large  color="blue" round outline v-on="on">
                <v-icon>mdi-plus</v-icon>
                <span> {{ currentQuestion.partialMarks }} &nbsp; </span>
              </v-btn>
            </template>
            <v-list>
              <v-list-tile
                v-for="n in 21"
                :key="n"
                @click="currentQuestion.partialMarks = n - 1"
              >
                <v-list-tile-title>{{ n - 1 }}</v-list-tile-title>
              </v-list-tile>
            </v-list>
          </v-menu>
        </v-flex>
        <v-flex xs4 md1>
          <v-menu offset-y transition="slide-y-transition" bottom max-height="300">
            <template v-slot:activator="{ on }">
              <v-btn icon large  color="error" round outline v-on="on">
                <v-icon>mdi-minus</v-icon>
                <span> {{ currentQuestion.incorrectMarks }} &nbsp; </span>
              </v-btn>
            </template>
            <v-list>
              <v-list-tile
                v-for="n in 20"
                :key="n"
                @click="currentQuestion.incorrectMarks = n"
              >
                <v-list-tile-title>{{ n }}</v-list-tile-title>
              </v-list-tile>
            </v-list>
          </v-menu>
        </v-flex>
        <v-flex xs12 md3>
          <v-menu offset-y transition="slide-y-transition" bottom>
            <template v-slot:activator="{ on }">
              <v-btn color="indigo" round outline v-on="on" style="width:95%">
                <span> {{ questionTypes[currentQuestion.type].text }} &nbsp; </span>
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
        </v-flex>
        <v-flex xs12 md3>
          <v-menu offset-y transition="slide-y-transition" bottom max-height="300px" max-width="300px">
            <template v-slot:activator="{ on }">
              <v-btn color="info" round outline v-on="on" style="width:95%">
                <span class="text-truncate"> 
                  {{ topics[currentSection.subjectIndex][currentQuestion.topicIndex] }} &nbsp; 
                </span>
                <v-icon>mdi-chevron-down</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-tile
                v-for="(topic, index) in topics[currentSection.subjectIndex]"
                :key="index"
                @click="changeTopic(index)"
              >
                <v-list-tile-title>
                  {{ topic }}
                </v-list-tile-title>
              </v-list-tile>
            </v-list>
          </v-menu>
        </v-flex>
      </v-layout>
    </template>

    <template slot="text-image">
      <ckeditor
        :editor="questionEditor"
        :config="questionConfig"
        v-model="currentQuestion.text"
      />
    </template>

    <v-layout slot="options">
      <v-radio-group
        row
        v-model="currentAnswer.answer"
        @change="saveQuestion(questionIndex)"
        :mandatory="false"
        v-if="currentQuestion.type == 0"
      >
        <template v-for="(option, i) in currentQuestion.options">
          <v-flex xs12 md3 :key="questionIndex + '-' + i">
            <v-text-field
              solo
              flat
              v-model="currentQuestion.options[i]"
              style="min-width: 100px;"
            >
              <v-radio
                slot="prepend-inner"
                :value="i"
                :on-icon="`mdi-alpha-${letter('a', i, true)}-circle`"
                :off-icon="`mdi-alpha-${letter('a', i, true)}-circle-outline`"
              />
            </v-text-field>
          </v-flex>
        </template>
      </v-radio-group>

      <v-layout v-else-if="currentQuestion.type == 1" py-4 my-1 row wrap>
        <v-flex
          xs12 md3
          v-for="(option, i) in currentQuestion.options"
          :key="questionIndex + '-' + i"
        >
          <v-text-field
            solo
            flat
            v-model="currentQuestion.options[i]"
            style="min-width: 100px;"
          >
            <v-checkbox
              slot="prepend-inner"
              v-model="currentAnswer.answer"
              multiple
              :value="i"
              :on-icon="`mdi-alpha-${letter('a', i, true)}-circle`"
              :off-icon="`mdi-alpha-${letter('a', i, true)}-circle-outline`"
              @change="saveQuestion(questionIndex)"
            />
          </v-text-field>
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



    <v-layout slot="clear">

      <v-btn
        color="red"
        round
        outline
        :small="!isSmallScreen"
        @click="clearQuestion(questionIndex)"
      >
        <v-icon>mdi-close</v-icon>
        <span>Clear</span>
      </v-btn>

    </v-layout>

    <template slot="footer">
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

    <template slot="test-name">{{ test.name }}</template>

    <template slot="sections">
      <v-flex xs12>
        <v-tab
          :class="index == sectionIndex ? 'primary--text' : ''"
          active-class="primary--text"
          v-for="(section, index) in sections"
          :key="index"
          @click="changeSection(index)"
        >
          {{ section.subject }}
        </v-tab>
      </v-flex>
    </template>

    <template slot="section-controls">
      <v-dialog v-model="editSectionDialog" max-width="400px">
        <template v-slot:activator="{ on }">
          <v-btn round outline small color="info" dark v-on="on" style="width: 200px">
            <v-icon>mdi-pencil</v-icon>
            Change subject
          </v-btn>
        </template>
        <v-card :class="$style.dialog">
          <v-card-title>
            <span :class="$style.title">Select a subject</span>
          </v-card-title>
          <v-card-text>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex xs12>
                  <v-autocomplete
                    v-model="subjectName"
                    :items="subjects"
                    :readonly="false"
                    label="Subject"
                    persistent-hint
                    prepend-icon="mdi-book"
                  />
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" flat @click="editSectionDialog = false">
              Cancel
            </v-btn>
            <v-btn
              color="primary"
              @click="
                changeSectionSubject(sectionIndex, subjectName);
                editSectionDialog = false;
              "
            >
              Done
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="newSectionDialog" max-width="400px">
        <template v-slot:activator="{ on }">
          <v-btn round outline small color="primary" dark v-on="on" style="width: 200px">
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
                  <v-autocomplete
                    v-model="newSectionSubject"
                    :items="subjects"
                    :readonly="false"
                    label="Subject"
                    persistent-hint
                    prepend-icon="mdi-book"
                  />
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" flat @click="newSectionDialog = false">
              Cancel
            </v-btn>
            <v-btn
              color="primary"
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
        style="width: 200px"
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
import TestLayout from "@/components/test/TestLayout.vue";
import { subjectTopics } from "@/js/subjects";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import CustomUploadAdapterPlugin from "@/js/customuploadadapter";

export default {
  props: ["testData"],
  data() {
    return {
      test: this.testData,
      questionEditor: ClassicEditor,
      questionConfig: {
        height: 400,
        toolbar: [
          "heading",
          "|",
          "bold",
          "italic",
          "bulletedList",
          "numberedList",
          "insertTable",
          "imageUpload",
          "undo",
          "redo"
        ],
        image: {
          toolbar: ["imageStyle:full", "imageStyle:side"]
        },
        extraPlugins: [CustomUploadAdapterPlugin]
      },
      questionTypes: [
        { value: 0, text: "Single Correct" },
        { value: 1, text: "Multiple Correct" },
        { value: 2, text: "Numerical" },
        { value: 3, text: "Matrix Match" }
        // { value: 4, text: "One Word Answer" },
        // { value: 5, text: "Subjective" }
      ],
      windowHeight: window.innerHeight - 200,
      isSmallScreen: this.$vuetify.breakpoint.smAndDown,
      swipeActions: {
        left: () => this.nextQuestion(),
        right: () => this.previousQuestion()
      },
      sectionIndex: 0,
      questionIndex: 0,
      editSectionDialog: false,
      newSectionDialog: false,
      solutionDialog: false,
      subjectName: "",
      newSectionSubject: "",
      emptyQuestion: {
        section: 0,
        text:
          "<p>Enter question text and options or insert image here.</p><p>&nbsp;</p>",
        type: 0,
        options: ["A", "B", "C", "D"],
        status: 0,
        correctMarks: 4,
        incorrectMarks: 1,
        partialMarks: 0,
        answers: ["P", "Q", "R", "S", "T"]
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
    changeSectionSubject(i, name) {
      this.sections[i].subject = name;
      this.sections[i].subjectIndex = this.subjects.indexOf(name);
    },
    changeSection(i) {
      if (this.validSectionIndex(i)) {
        this.sectionIndex = i;
        if (this.currentQuestion && this.currentQuestion.section !== i)
          this.changeQuestion(this.currentSection.start);
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
      if (this.validQuestionIndex(i)) {
        this.questionIndex = i;
        if (this.currentQuestion.section !== this.sectionIndex)
          this.changeSection(this.currentQuestion.section);
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
      this.$emit("save");
    },
    addSection(name) {
      this.sections.push({
        subject: name,
        start: this.questions.length,
        end: this.questions.length - 1,
        subjectIndex: this.subjects.indexOf(name)
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

        if(i>0) this.changeSection(i-1);

        this.questions.splice(start, len);
        this.answers.splice(start, len);

        if(i==0) this.changeSection(i+1);
        this.sections.splice(i, 1);
        return true;

      } else return false;
    },
    changeTopic(i) {
      var subjectIndex = this.sections[this.currentQuestion.section]
        .subjectIndex;
      this.currentQuestion.topicIndex = i;
      this.currentQuestion.topic = this.topics[i];
    }
  },
  watch: {
    questionIndex: function(newQuestion, oldQuestion) {
      this.updateStatus(newQuestion);
    }
  },
  computed: {
    subjects() {
      return subjectTopics.subjects;
    },
    topics() {
      return subjectTopics.topics;
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
    currentAnswer() {
      return this.test.answers[this.questionIndex];
    },
    currentSection() {
      return this.test.sections[this.sectionIndex];
    }
  },
  mounted() {
    var vm = this;
    setInterval(function() {
      vm.$emit("update", vm.test);
    }, 5000);
  }
};
</script>

<style module lang="stylus">
@require '~@/stylus/theme/colors';
.questionInfo{
  border-bottom: 1px solid grey !important;
}

.questionText{
  width:100%;
  margin-top:5px;
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
  border-radius: 8px;
  font-family: 'Open Sans',Roboto,Arial,sans-serif;
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
  font-size: 1.3rem;
  min-width: 160px;
}
</style>
