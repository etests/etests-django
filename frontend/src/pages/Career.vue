<template>
  <v-flex xs12>
    <header class="al-hero-header">
      <Header
        color="transparent"
        textColor="white"
        :temporaryDrawer="true"
        :disableDrawerClose="true"
        :showSearchBar="false"
        :dark="true"
        :isAbsolute="true"
      />
      <div class="al-hero-cta">
        <div class="text-xs-left mx-2">
          <h1 class="al-cta-title">
            Let's Make Conducting Online Tests Easier
          </h1>
          <p class="al-cta-desc">
            eTests is Online Testing platform that supports different patterns
            of exams including JEE Main, JEE Advanced, NEET, AIIMS and many
            more. We provide a complete solution to test creation and
            conduction. Join us and work from your own city.
          </p>
          <p class="al-cta-desc">Roles and responsibilites</p>
          <ul>
            <li>
              Contact institutes and tell them about our services.
            </li>
            <li>
              Help institutes for creation and conduction of tests hazzle free.
            </li>
          </ul>
          <br />
        </div>
        <v-btn round class="white mt-5" @click="toggleDialog">
          <template v-if="!dialog.length">
            Join Now
          </template>
          <template v-else>
            Close
          </template>
        </v-btn>
        <v-expansion-panel class="elevation-0" v-model="dialog" expand>
          <v-expansion-panel-content class="transparent px-0" hide-actions>
            <v-card class="transparent elevation-0">
              <v-card-text>
                <iframe
                  src="https://docs.google.com/forms/d/e/1FAIpQLSc1lTSlKR6X0Re4mHkUFd4Ixp0zAGrvj3-UUGSbjs2X_0Ay9Q/viewform?embedded=true"
                  width="100%"
                  height="1700px"
                  frameborder="0"
                  >Loading…</iframe
                >
              </v-card-text>
            </v-card>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </div>
      <svg viewBox="0 0 1150 110" class="shape">
        <path
          d="M682.2,39.6C418.5-11.1,140.2,9.9,0,30v96h1440V30C1252.7,52.2,1011,96.4,675.6,38.7z"
          fill="#ffffff"
        />
      </svg>
    </header>
  </v-flex>
</template>

<script>
import Header from "@/components/Header.vue";

export default {
  data() {
    return {
      dialog: []
    };
  },
  methods: {
    toggleDialog() {
      if (!this.dialog.length)
        this.dialog = [...Array(this.items).keys()].map(_ => true);
      else this.dialog = [];
    }
  },
  components: {
    Header
  }
};
</script>

<style scoped>
.al-hero-header {
  font-family: "Montserrat";
  background-image: linear-gradient(to right, #28cc9e, #31cea0);
}
.shape {
  position: relative;
  left: 0;
  bottom: -50px;
}
.al-hero-cta {
  font-family: "Montserrat";
  max-width: 750px;
  margin: 0 auto;
  padding: 60px 10px 0px;
}
.al-hero-cta .al-cta-title {
  font-family: "Open Sans";
  color: #fff;
  padding-top: 50px;
  padding-bottom: 0;
  font-weight: 900;
  font-size: 20pt;
}
.al-cta-desc {
  margin-left: 20px;
  text-align: justify;
}
.al-hero-cta .al-cta-desc,
ul,
li {
  font-family: "Montserrat";
  color: #fff;
  font-size: 12pt;
}
</style>
