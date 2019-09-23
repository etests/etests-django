<template>
  <v-layout column>
    <v-card :class="[$style.card, 'elevation-2']">
      <v-card-title class="title">
        Instructions
      </v-card-title>
      <v-card-text class="text-xs-left">
        <div class="subheadin">Please read the instructions carefully</div>
        <br />
        <li>
          The on-screen computer countdown timer on the top middle corner of
          computer screen will display the remaining time available to you for
          completing the paper. When the on-screen countdown timer reaches zero,
          the paper will end by itself – No input from your side will be
          accepted after the timer reaches zero and whatever answers have been
          saved by you will automatically be submitted for evaluation.
        </li>
        <li>
          You cannot attempt any other test if another test is running (or
          paused).
        </li>
        <li>
          The “Submit” button present at the bottom right corner of the screen.
          Once you will click on the submt button the test will be submitted
        </li>
        <li>
          After The test is submitted you can only reattempt it after the result
          is declared. If the Test is question Bank you can attempt it at any
          time and see your result and review your responses solution
        </li>
        <li>
          The Questions Palette displayed on the right side of screen will show
          the status of each question using one of the following symbols:
          <ul>
            <li>
              <v-btn fab dark small><span>1</span></v-btn> Not Visited:You
              haven't visited the question yet
            </li>
            <li>
              <v-btn fab dark small color="error"><span>2</span></v-btn
              >Visited Unanswered: You have visited the question but not
              answered yet
            </li>
            <li>
              <v-btn fab dark small color="info"><span>3</span></v-btn
              >Unanswered and Marked: You haven't answered the question but
              marked it to review later.
            </li>
            <li>
              <v-btn fab dark small color="purple"><span>4</span></v-btn
              >Answered and Marked: You have Answered the question and marked it
              to review later
            </li>
            <li>
              <v-btn fab dark small color="green"><span>5</span></v-btn
              >Answered: You have answered the question
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
          Procedure for Answering a Question<br />
          a. To select your answer, click on the choice of the corresponding
          answer.<br />
          b. To deselect your chosen answer, click on the
          <v-btn color="error" round outline>
            <v-icon>mdi-close</v-icon>
            <span>Clear your response</span>
          </v-btn>
          button<br />
          c. To change your chosen answer, click on the button of another
          option<br />
          d. To save your answer and move to next question click on the
          <v-btn color="success" round outline>
            <v-icon>mdi-content-save-move</v-icon>
            <span>Save response & next </span>
          </v-btn>
          button.<br />
          e. To mark the question for review, click on
          <v-btn color="info" round outline>
            <v-icon>mdi-comment-eye-outline</v-icon>
            <span>Mark for review & next</span>
          </v-btn>
          button.
        </li>
        <br />
        <li>
          Marking Scheme and Type of question is shown at the top of each
          question
        </li>
        <br /><br />
        I have read and understood the instructions. All computer hardware
        allotted to me are in proper working condition. I declare that I am not
        in possession of / not wearing / not carrying any prohibited gadget like
        mobile phone, bluetooth devices etc. /any prohibited material with me
        into the Examination Hall.I agree that in case of not adhering to the
        instructions, I shall be liable to be debarred from this Test and/or to
        disciplinary action, which may include ban from future Tests /
        Examinations
      </v-card-text>
    </v-card>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {};
  }
};
</script>

<style module lang="stylus">
.card{
  padding: 10px 20px;
  width: 100%;
  border-radius: 8px;
  font: "Product Sans Light";
  margin-bottom: 12px;
}
</style>
