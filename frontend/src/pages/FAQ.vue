<template>
  <StandardLayout>
    <v-flex xs12 class="px-3">
      <v-card :class="[$style.stepCard, 'elevation-2']">
        <v-card-title :class="$style.title">FAQ</v-card-title>
        <v-expansion-panel>
          <v-expansion-panel-content
            :class="$style.stepCard"
            v-for="(step, i) in steps"
            :key="i"
          >
            <template v-slot:header v-if="step.show.includes(userType)" >
              <div :class="$style.step" >{{ step.title }}</div>
            </template >
            <v-card v-if="step.show.includes(userType)">
              <v-card-text :class="$style.description" >{{
                step.description
              }}</v-card-text>
            </v-card>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-card>
    </v-flex>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";

export default {
  data() {
    return {
      steps: [
      
        {
<<<<<<< HEAD
          title: "How to join eTests?",
          description: "Click on Login / Register button at the top."
=======
          title: "Can I attempt question bank tests multiple times?",
          description:
            "Yes, you can.",
            show:["student"]
>>>>>>> removed notification and completed FAQ
        },
     
        {
<<<<<<< HEAD
          title: "Can I attempt question bank tests any number of times?",
          description: "Yes, you can."
=======
          title: "Can I attempt tests multiple times?",
          description:
            "Yes, you can attempt. During the period the test is active you can attempt it once and rank will be generated for the same. After the ranks are declared you can attempt them any number of times for practise.",
            show:["student"]
        },
          {
          title: "How can you join a batch?",
          description:
            "You can Join a batch with the help of joining key shared by the institute you joined. The option is avialable in the dashboard.",
            show:["student"]
>>>>>>> removed notification and completed FAQ
        },
        {
          title: "How can you create a batch?",
          description:
            "You can create a batch from your dashboard. you can add students in the batch just by adding a list of roll numbers(seperated by space or new line) in the dialog. A key will be generated for each student which needs to be shared to respect students and they will be joined in the batch.The batches can be further used to register students of a batch in test.",
            show:["institute"]
        },
            {
          title: "How can I get money for the sales of question bank created by me ?",
          description:
            "There is buyers section in dashboard. This will show you the list of buyers of each test. The update of new buyers may take some time. It is generally updated in less than 3 hrs. According to the no of buyers and rate of question bank, Money will be credited to the account at the end of each week.",
            show:["institute"]
        },
               {
          title: "How can I Purchase a Question Bank ?",
          description:
            "You can search for question bank institute wise, examwise or namewise. Each Option is avialable is navigation bar. For purchasing it you need click on buy and make payment for question bank by one of the method.After completing the payment you need submit the transaction id and receipt in same dialog. The purchased question bank will appear in your dashboard shortly.",
            show:["student"]
        },
             {
          title: "How are Test different from a Question Bank?",
          description:
            "Tests are regular test which are conducted by Institute which you have joined. They are rated for which rank is generated after the institute declare ranks. Review and Analysis are generated only after the rank is declared for test. For Question Banks, the review and analysis are generated just after you submit the test. Any student can register for question bank of any institute.",
          show:["institute","student"]
        },

      ]
    };
  },
  components: {
    StandardLayout
  },
    computed: {
     userType() {
      return this.$store.state.authentication.user.type;
    },
  }
};
</script>

<style module lang="stylus">
@require '~@/stylus/theme/colors';

.stepCard {
  border-radius: 8px !important;
  font-family: 'Product Sans Light', Roboto, Arial, sans-serif;

  .step {
    font-size: 1.2rem;
    margin: auto;
  }

  .title {
    font-size: 1.875rem;
    line-height: 1.75rem;
    margin: 5px;
    color: #28cc9e;
  }

  .description {
    text-align: left;
    letter-spacing: 0.014em;
    font-size: 1.08rem;
    line-height: 1.25rem;
    color: #5f6368;
    margin: 0 15px;
  }
}
</style>
