<template>
  <div>
    <StandardLayout v-if="!started">
      <template v-if="status.loading">
        Loading...
      </template>
      <template v-else>
        <Instructions column />
        <v-btn color="primary" @click="startTest">
          Proceed
        </v-btn>
      </template>
    </StandardLayout>
    <template v-else-if="session !== null">
      <NewTest
        :sessionData="session"
        @update="updateSession"
        @end="submitTest"
      />
    </template>
  </div>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";
import Instructions from "./Instructions";
import NewTest from "./NewTest";
import { demoSession } from "@/js/demoTest";
import { mapState } from "vuex";

export default {
  props: {
    demo: {
      required: false,
      default: true
    }
  },
  data() {
    return {
      id: this.$route.params.id,
      session: null,
      started: false
    };
  },
  computed: {
    ...mapState({
      storedSession: state => state.sessions.session,
      status: state => state.sessions.status
    })
  },
  methods: {
    fetchSession(){
       this.$store.dispatch("sessions/get", this.id)
    },
    async startTest() {
      if (!this.demo) {
        if (
          !this.$store.state.sessions.status.exists ||
          this.$store.state.sessions.session.test.id !== this.id
        ) await this.fetchSession();

        setTimeout(_ => {
          this.session = this.storedSession;
          localStorage.setItem("session", JSON.stringify(this.storedSession));
          this.started = this;
        }, 500) 

      } else {
        this.started = true;
        this.session = demoSession;
        localStorage.setItem("session", JSON.stringify(demoSession));
      }
    },
    submitTest() {
      if (!this.session.completed) this.session.completed = true;
      this.syncSession();
      this.$router.push({ name: "result", params: { id: this.session.id } });
    },
    updateSession(newSession) {
      if (newSession.duration <= 0 && !newSession.completed) {
        this.submitTest();
        this.session.completed = true;
      }
      localStorage.session = JSON.stringify(newSession);
    },
    syncSession() {
      this.$store.dispatch("sessions/update", this.session);
    }
  },
  mounted() {
    // if (this.testType === "ranked")
    // setInterval(
    //   this.syncSession,
    //   parseInt(this.getRandom(18, 30) * 60 * 1000)
    // );
  },
  components: {
    StandardLayout,
    Instructions,
    NewTest
  }
};
</script>
