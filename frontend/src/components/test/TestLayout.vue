<template>
  <v-container fluid class="px-0 py-0 my-0 grey lighten-4">
    <Header :showDrawer="false" :temporaryDrawer="true">
      <v-layout slot="tools">
        <v-flex>
          <v-layout justify-end>
            <v-btn flat icon @click="toggleFullScreen()">
              <v-icon v-if="fullscreen">mdi-fullscreen-exit</v-icon>
              <v-icon v-else>mdi-fullscreen</v-icon>
            </v-btn>
          </v-layout>
        </v-flex>
      </v-layout>
    </Header>

    <v-content app :class="$style.content">
      <v-layout row wrap>
        <v-flex xs12>
          <v-card color="white" :class="$style.questionContainer">
            <v-sheet class="pt-2">
              <v-layout row justify-center mb-1>
                <slot name="controls"></slot>
              </v-layout>
            </v-sheet>
            <v-divider />
            <v-sheet
              :class="[$style.question, 'px-4 py-2']"
              :height="windowHeight"
            >
              <v-layout justify-center>
                <slot name="info"></slot>
              </v-layout>

              <slot name="text-image"></slot>

              <slot name="options"></slot>
            </v-sheet>
          </v-card>
        </v-flex>
      </v-layout>
    </v-content>

    <v-footer color="transparent" height="auto" fixed app inset>
      <v-layout>
        <v-flex xs12>
          <slot name="footer"></slot>
        </v-flex>
      </v-layout>

      <v-btn
        flat
        icon
        color="primary"
        @click="panel = !panel"
        :absolute="isSmallScreen"
        :right="isSmallScreen"
      >
        <v-icon v-if="panel">mdi-arrow-collapse-right</v-icon>
        <v-icon v-else>mdi-arrow-expand-left</v-icon>
      </v-btn>
    </v-footer>

    <v-navigation-drawer v-model="panel" app right>
      <v-flex>
        <v-toolbar-title class="subheading primary--text mt-3">
          <strong style="text-transform: uppercase;">
            <slot name="test-name"></slot>
          </strong>
        </v-toolbar-title>

        <slot name="sections"></slot>

        <slot name="section-controls"></slot>

        <v-divider class="my-3" />

        <slot name="questions-panel"></slot>
      </v-flex>
      <v-layout justify-center>
        <slot name="submit"></slot>

        <v-flex v-if="isSmallScreen">
          <v-btn
            flat
            icon
            dark
            color="primary"
            @click="panel = !panel"
            bottom
            right
            fixed
          >
            <v-icon v-if="panel">mdi-arrow-collapse-right</v-icon>
            <v-icon v-else>mdi-arrow-expand-left</v-icon>
          </v-btn>
        </v-flex>
      </v-layout>
    </v-navigation-drawer>
  </v-container>
</template>

<script>
import Header from "@components/Header.vue";
import Footer from "@components/Footer.vue";

export default {
  data() {
    return {
      windowHeight: window.innerHeight - 200,
      isSmallScreen: this.$vuetify.breakpoint.smAndDown,
      panel: null,
      drawer: false,
      fullscreen: false,
      swipeActions: {
        left: () => this.nextQuestion(),
        right: () => this.previousQuestion()
      }
    };
  },
  components: {
    Header,
    Footer
  },
  methods: {
    toggleFullScreen() {
      if (
        (document.fullScreenElement && document.fullScreenElement !== null) ||
        (!document.mozFullScreen && !document.webkitIsFullScreen)
      ) {
        if (document.documentElement.requestFullScreen) {
          document.documentElement.requestFullScreen();
        } else if (document.documentElement.mozRequestFullScreen) {
          document.documentElement.mozRequestFullScreen();
        } else if (document.documentElement.webkitRequestFullScreen) {
          document.documentElement.webkitRequestFullScreen(
            Element.ALLOW_KEYBOARD_INPUT
          );
        }
      } else {
        if (document.cancelFullScreen) {
          document.cancelFullScreen();
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
          document.webkitCancelFullScreen();
        }
      }
      this.fullscreen = !this.fullscreen;
    }
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener("resize", () => {
        this.windowHeight = window.innerHeight - 200;
      });
    });
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';
.questionInfo{
  border-bottom: 1px solid grey !important;
}
.content{
  margin-top: 20px;
  letter-spacing: 0.04em;
  font-family: 'Product Sans',Roboto,Arial,sans-serif;
  .questionContainer{
    text-align: left;
    border: 1px solid #c9cbd0;
    border-radius: 8px;
    margin: 0 15px;

    .question{
      overflow-y: auto;
    }
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
