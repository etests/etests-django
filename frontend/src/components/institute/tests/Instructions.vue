<template>
  <div>
    <v-card-title class="title">
      Test Editor Help Manual
    </v-card-title>
    <v-card-text class="text-xs-left">
      <li>
        <span>
          The duration of your test can be set using using time field present at the top.
        </span>
        <v-btn outline color="primary" flat>
          <v-icon>mdi-clock</v-icon>
          <span> 03:00:00</span>
        </v-btn>
      </li>
      <li>
        The Save Button is present at bottom right corner for saving the test.
        <v-btn outline color="success">
          <v-icon>mdi-content-save</v-icon>
          <span>Save this test</span>
        </v-btn>
      </li>

      <li>
        The Questions Palette displayed on the right side of screen will show
        question in each section.
        <ul>
          <li>
            <v-btn fab dark small color="error"><span>1</span></v-btn
            >Answer is not set: You haven't set the answer for the question yet
          </li>
          <li>
            <v-btn fab dark small color="green"><span>2</span></v-btn
            >Answer is set: You have set the answer for the question
          </li>
        </ul>
      </li>
      <br />

      <li>
        For Navigation
        <ol type="a">
          <li>
            Click on
            <v-btn icon color="primary">
              <v-icon>mdi-arrow-right</v-icon>
            </v-btn>
            To save your answer for the current question and then go to the next
            question.
          </li>
          <li>
            Click on
            <v-btn icon color="primary">
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
            to save your answer for the current question go to the Previous question. 
          </li>
          <li>You can also click on numerical buttons on the right to move to specific questions.
          </li>
          <li>You can navigate through subjects by clicking on subject buttons on the right side
          </li>
        </ol>
      </li>
      <br />
      <li>
        Add New question helps you to add the question. After clicking on it you
        can select the type of question you want to add
        <v-btn color="info" round outline>
          <v-icon>mdi-plus</v-icon>
          <span>Add new question</span>
        </v-btn>
      </li>
      <li>
        You can clear your chosen answers by clicking on
        <v-btn color="red" round outline>
          <v-icon>mdi-close</v-icon>
          <span>Clear answer</span>
        </v-btn>
      </li>
      <li>
        To delete a question click on
        <v-btn color="error" round outline>
          <v-icon>mdi-delete</v-icon>
          <span>Delete question</span>
        </v-btn>
      </li>
      <li>
        Marking Scheme and Type of question is shown at the top of each
        question.
        <ol type="a">
          <li> For Correct Marks
            <v-btn color="success" round outline>
              <v-icon>mdi-plus</v-icon>
              <span> 4 </span> </v-btn
            >
          </li>
          <li> For Partial Marks
            <v-btn color="blue" round outline>
              <v-icon>mdi-plus</v-icon>
              <span> 1 </span> </v-btn
            >
          </li>
          <li> For Incorrect Marks
            <v-btn color="error" round outline>
              <v-icon>mdi-minus</v-icon>
              <span>1 </span>
            </v-btn>
          </li>
          <li> To change Question Type you can click on
          <v-btn color="indigo" round outline>
            <span> Single Correct </span>
            <v-icon>mdi-chevron-down</v-icon>
          </v-btn>
          </li>
          <li> To select the topic of question you can click on
          <v-btn color="info" flat style="width:150px;" round outline>
            <span> Topic </span>
            <v-icon>mdi-chevron-down</v-icon>
          </v-btn>
          </li>
        </ol>
      </li>
      <br />
      <li>
        Creating, changing and deleting sections. Note that section here corresponds to the
        subjects in the test.<br />
        <ol type="a">
         <li> For adding a section / subject
          <v-btn round outline small color="primary" dark>
            <v-icon>mdi-plus</v-icon>
            Add new section </v-btn
          >
         </li>
         <li> For changing subject / section
          <v-btn round outline small color="info" dark>
            <v-icon>mdi-pencil</v-icon>
            Change subject </v-btn
          >
         </li>
         <li> For deleting subject / section
          <v-btn round outline small color="error">
            <v-icon>mdi-delete</v-icon>
            Delete this section
          </v-btn>
         </li>
        </ol>
        <br/>
      </li>
      <li>
        You can create another test only after saving the current test.
      </li>
      <li v-if="instituteId">
        You can also send us PDF / images containing your questions and we will add them to the test.
        Fill out <a target="_blank" href="https://forms.gle/XuzzwBP31c3Z1dwn8">this form</a> with the following details: <br />
        <ul type="circle">
          <li> Institute Id: {{ instituteId }} </li>
          <li> Test Id: {{ testId }} </li>
        </ul>
      </li>
    </v-card-text>
  </div>
</template>

<script>
export default {
  data() {
    return {
      testId: this.$route.params.id
    };
  },
  computed: {
    instituteId() {
      if(
        this.$store.state.authentication.status.loggedIn &&
        this.$store.state.authentication.user.type == "institute"
      ){
        return this.$store.state.authentication.user.id;
      }
      else return false;
    }
  }
}
</script>