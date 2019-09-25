<template>
  <div>
    <StandardLayout v-if="!started || completed">
      <v-card
        v-if="demo && completed"
        :class="[$style.card, 'py-5 elevation-3']"
      >
        <v-card-title class="title">
          {{ test.name }}
        </v-card-title>
        <v-card-text class="subheading text-xs-left px-3">
          You have finished creating your demo test. Now you can go ahead and
          attempt the test you have created.
        </v-card-text>
        <v-layout mt-4>
          <v-flex xs12>
            <v-btn flat color="success" @click="attemptTest">
              Attempt the test
            </v-btn>
            <v-btn flat color="info" @click="completed = false">
              Re-edit this test
            </v-btn>
            <v-btn flat color="error" @click="deleteTest">
              Start afresh
            </v-btn>
          </v-flex>
        </v-layout>
      </v-card>
      <v-card v-else :class="[$style.card, 'elevation-3']">
        <v-layout column justify-center>
          <v-flex xs12 v-if="error" :class="[$style.error, $style.message]">
            {{ error }}
          </v-flex>
          <v-flex xs12 v-else-if="loading" :class="$style.loading">
            <v-progress-circular :size="50" color="primary" indeterminate />
          </v-flex>
          <v-flex xs12 v-else @keyup.enter="startEdit">
            <Instructions />
            <v-btn
              round
              style="width:160px;"
              class="primary mx-auto"
              @click="startEdit"
            >
              Start Editing
            </v-btn>
          </v-flex>
        </v-layout>
      </v-card>
    </StandardLayout>
    <template v-else-if="test !== null && !completed">
      <EditTest :testData="test" @update="updateTest" @save="saveTest" />
    </template>
  </div>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";
import Instructions from "@/components/institute/tests/Instructions.vue";
import EditTest from "./EditTest";
import Review from "./Review";
import Marks from "./Marks";
import Analysis from "./Analysis";
import { testTemplate } from "@/js/test";
import { demoTests } from "@/js/demoTests";
import { mapState } from "vuex";

export default {
  props: {
    demo: {
      required: false,
      default: false
    }
  },
  data() {
    return {
      id: parseInt(this.$route.params.id) || 75,
      test: null,
      started: false,
      loading: false,
      completed: false,
      error: null
    };
  },
  computed: {
    ...mapState({
      storedTest: state => state.tests.test,
      status: state => state.tests.status
    })
  },
  methods: {
    fetchTest() {
      this.$store.dispatch("tests/get", this.id);
    },
    async startEdit() {
      this.loading = true;
      this.$Progress.start();
      if (!this.demo) {
        if (
          !this.$store.state.tests.status.exists ||
          this.$store.state.tests.test.id !== this.id
        ) {
          await this.fetchTest();
        }
        var vm = this;
        setTimeout(_ => {
          if (vm.status.error) {
            vm.error = vm.status.error;
            this.$Progress.fail();
          } else {
            vm.test = vm.storedTest;
            localStorage.setItem("editing", this.id);
            vm.started = true;
            vm.loading = false;
            this.$Progress.finish();
          }
        }, 500);
      } else {
        var test = testTemplate;
        this.test = test;
        localStorage.setItem("editing", this.id);
        this.started = true;
        this.loading = false;
        this.$Progress.finish();
      }
    },
    updateTest(newTest) {
      this.test = newTest;
    },
    saveTest() {
      if (this.demo) {
        this.completed = true;
        localStorage.removeItem("editing");
      } else {
        this.$store.dispatch("tests/update", this.test);
      }
    },
    attemptTest() {
      var session = demoTests.newSession(this.test);
      session.testId = this.id;
      localStorage.setItem("session", JSON.stringify(session));
      this.$router.push(`/demo/${this.id}`);
    },
    deleteTest() {
      localStorage.removeItem("session");
      location.reload();
    }
  },
  components: {
    StandardLayout,
    Instructions,
    EditTest
  },
  created(){
    if(localStorage.getItem("editing")){
      if(parseInt(localStorage.getItem("editing")) === this.id)
        this.startEdit();
    }
  }
};
</script>

<style module lang="stylus">
@require '~@/stylus/components';
.card{
  width: 98%;
  margin: auto;
}
.loading, .error{
  margin-top: 150px;
  min-height: 250px;
}
</style>
