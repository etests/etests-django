<template>
  <div>
    <Review :report="report" :demo="demo" v-if="reviewing" />
    <StandardLayout v-else-if="!started || completed">
      <v-flex xs12 v-if="completed && report !== null">
        <Marks :report="report" :demo="demo" @review="reviewing = true" />
        <Analysis v-if="report && report.result" :report="report" />
        <v-card v-else :class="[$style.card, $style.message]">
          Analysis of your test is not generated yet.
        </v-card>
      </v-flex>
      <v-card v-else :class="[$style.card, 'elevation-3']">
        <v-layout column justify-center align-center>
          <v-flex xs12 v-if="error" :class="[$style.error, $style.message]">
            {{ error }}
          </v-flex>
          <v-flex xs12 v-else-if="loading" :class="$style.loading">
            <v-progress-circular :size="50" color="primary" indeterminate />
          </v-flex>
          <v-flex xs12 v-else @keyup.enter="startTest">
            <Instructions />
            <v-btn
              round
              style="width:160px;"
              class="primary mx-auto"
              @click="startTest"
            >
              Start Test
            </v-btn>
          </v-flex>
        </v-layout>
      </v-card>
    </StandardLayout>
    <template v-else-if="session !== null && !completed">
      <Test :sessionData="session" @update="updateSession" />
    </template>
  </div>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";
import Instructions from "./Instructions";
import Test from "./Test";
import Review from "./Review";
import Marks from "./Marks";
import Analysis from "./Analysis";
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
      id: parseInt(this.$route.params.id),
      session: null,
      started: false,
      loading: false,
      completed: false,
      reviewing: false,
      error: null,
      report: null
    };
  },
  computed: {
    ...mapState({
      storedSession: state => state.sessions.session,
      status: state => state.sessions.status
    })
  },
  methods: {
    fetchSession() {
      this.$store.dispatch("sessions/get", this.id);
    },
    async startTest() {
      this.loading = true;
      this.$Progress.start();
      if (!this.demo) {
        if (
          !this.$store.state.sessions.status.exists ||
          !this.$store.state.sessions.session.test ||
          this.$store.state.sessions.session.test.id !== this.id
        ) {
          await this.fetchSession();
        }
        var vm = this;
        setTimeout(_ => {
          if (vm.status.error) {
            vm.error = vm.status.error;
            this.$Progress.fail();
          } else {
            if (localStorage.getItem(session)) {
              var session = JSON.parse(localStorage.getItem(session));
              session.test = vm.storedSession.session;
              vm.session = session;
            } else {
              vm.session = vm.storedSession;
              var { test, ...session } = vm.storedSession;
              session.testId = this.id;
              session.isDemo= false;
              localStorage.setItem("session", JSON.stringify(session));
            }
            vm.started = true;
            vm.loading = false;
            this.$Progress.finish();
          }
        }, 500);

        if (this.session && !this.session.practice)
          setInterval(
            this.syncSession,
            parseInt(this.getRandom(18, 30) * 60 * 1000)
          );
      } else {
          if(
            localStorage.getItem("session") &&
            JSON.parse(localStorage.getItem("session")).test &&
            JSON.parse(localStorage.getItem("session")).testId == this.id
          ){
              this.session = JSON.parse(localStorage.getItem("session"));
              this.started = true;
              this.$Progress.finish();
          }
          else if (demoTests.tests.length > this.id) {
            var session = demoTests.newSession(demoTests.tests[this.id]);
            this.session = session;
            session.testId = this.id;
            localStorage.setItem("session", JSON.stringify(session));
            this.started = true;
            this.$Progress.finish();
          } else {
            this.error = "This test does not exist.";
            this.$Progress.fail();
          }
        } 
    },
    async submitTest() {
      this.loading = true;
      this.completed = true;
      this.$Progress.start();
      if (this.demo && this.session.isDemo) {
        this.report = demoTests.getResult(this.session);
        localStorage.removeItem("session");
        this.loading = false;
        this.$Progress.finish();
      } else {
        await this.syncSession();
        var vm = this;
        setTimeout(_ => {
          if (vm.status.updated) {
            vm.report = vm.storedSession;
            localStorage.removeItem("session");
            this.loading = false;
            this.$Progress.finish();
          }
        }, 500);
      }
    },
    updateSession(newSession) {
      this.session = newSession;
      var { test, ...session } = newSession;
      session.testId = test.id;
      localStorage.session = JSON.stringify(session);
      if (newSession.duration <= 0 || newSession.completed) {
        this.submitTest();
      }
    },
    syncSession() {
      this.$store.dispatch("sessions/update", this.session);
    }
  },
  created() {
    if (localStorage.getItem("session")) {
      var session = JSON.parse(localStorage.getItem("session"));
      if (
        session &&
        this.demo === session.isDemo &&
        session.testId === this.id
      ) {
        this.startTest();
      }
    }
  },
  components: {
    StandardLayout,
    Instructions,
    Test,
    Review,
    Marks,
    Analysis
  }
};
</script>

<style module lang="stylus">
@require '~@/stylus/components';
.card{
  width: 950px;
  max-width: 100%;
  margin: auto;
}
.loading, .error{
  margin-top: 150px;
  min-height: 250px;
}
</style>
