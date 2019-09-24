<template>
  <div>
    <v-card-title class="title">
      Instructions For Creating Test
    </v-card-title>
    <v-card-text class="text-xs-left">
      <div class="subheadin">Please read the instructions carefully</div>
      <br />
      <li>
        <span>The Duration of your test can be set using using countdown timer present at the top.</span>
        <v-btn left icon color="primary" flat>
      <v-icon>mdi-clock</v-icon>
      <span> 03:00:00</span>
      </v-btn>
      </li>
      <li>
        The Save Button is present at bottom right corner for saving the test.  <v-btn
        outline
        color="success"
      >
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
            >Option Not Set: You haven't set correct option for the question 
            yet
          </li>
          <li>
            <v-btn fab dark small color="green"><span>2</span></v-btn
            >Option Set: You have set Correct answer for the question
          </li>
        </ul>
      </li>
      <br />

      <li>
        For Navigation<br />
        a. Click on
        <v-btn icon color="primary">
          <v-icon>mdi-arrow-right</v-icon>
        </v-btn>
        To save your answer for the current question and then go to the next
        question.<br />
        b. Click on
        <v-btn icon color="primary">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        to save your answer for the current question go to the Previous
        question.<br />
        c. You can also click on numerical buttons on the right to move to
        specific questions.<br />
        d. You can navigate through subjects by clicking on subject buttons on
        the right side
      </li>
      <br />
           <li>
     Add New question helps you to add the question. 
     After clicking on it you can select the type of question you want to add    <v-btn
            color="info"
            round
            outline
          >
            <v-icon>mdi-plus</v-icon>
            <span>Add new question</span>
          </v-btn>
      </li>
      <li>
        You can clear your chosen answers by clicking on 
      <v-btn
        color="red"
        round
        outline
      >
        <v-icon>mdi-close</v-icon>
        <span>Clear answer</span>
      </v-btn></li>
      <li>
       To delete a question click on
          <v-btn
        color="error"
        round
        outline
      >
        <v-icon>mdi-delete</v-icon>
        <span >Delete question</span>
      </v-btn>
      </li>
        .<br />
      <li>
        Marking Scheme and Type of question is shown at the top of each question<br/>
        a. For Correct Marks  <v-btn color="success" round outline>
            <v-icon>mdi-plus</v-icon>
            <span> 4 </span>
          </v-btn><br/>
        b. For Partial Marks  <v-btn color="blue" round outline v-on="on">
            <v-icon>mdi-plus</v-icon>
            <span> 1 </span>
          </v-btn><br/>
          c. For Incorrect Marks
             <v-btn color="error" round outline v-on="on">
            <v-icon>mdi-minus</v-icon>
            <span>1 </span>
          </v-btn>
          <br/>
          d. To change Question Type you can click on
            <v-btn color="indigo" round outline v-on="on">
            <span> Single Correct </span>
            <v-icon>mdi-chevron-down</v-icon>
          </v-btn>
          <br/>
          e. To select the topic of question you can click on
         <v-btn color="info" flat style="width:150px;" round outline >
            <span> Topic </span>
            <v-icon>mdi-chevron-down</v-icon>
          </v-btn>
      </li>
      <br />
      <li>
        For Creating, Changing and deleting Section. Section Corresponds to the subjects in paper.<br/>
        a. For adding a section/subject  
          <v-btn round outline small color="primary" dark >
            <v-icon>mdi-plus</v-icon>
            Add new section
          </v-btn><br/>
          b. For Changing Subject/Section <v-btn round outline small color="info" dark v-on="on">
            <v-icon>mdi-pencil</v-icon>
            Change subject
          </v-btn><br/>
          c. For Deleting Subject/Section
              <v-btn
        round
        outline
        small
        color="error"
      >
        <v-icon>mdi-delete</v-icon>
        Delete this section
      </v-btn>
      </li>
      <br/>
             <li>
        You can only create another Test after saving the current test.
      </li>
    </v-card-text>
  </div>
</template>

<script>
export default {
  data() {
    return {
      time_alloted:"03:00:00",
    };
  }
};
</script>
