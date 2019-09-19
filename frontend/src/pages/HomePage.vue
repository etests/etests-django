<template>
  <HeroLayout>
    <full-page ref="fullpage" :options="options" v-if="!disableFullpage">
      <component v-for="section in sections" :key="section" :is="section" />
    </full-page>
    <v-flex xs12 v-else>
      <component v-for="section in sections" :key="section" :is="section" />
    </v-flex>
  </HeroLayout>
</template>

<script>
import HeroLayout from "@/components/layouts/HeroLayout.vue";
import SectionLayout from "@/components/homepage/SectionLayout.vue";

import Hero from "@/components/homepage/Hero.vue";
import Welcome from "@/components/homepage/Welcome.vue";
import QuickStart from "@/components/homepage/QuickStart.vue";
import Exams from "@/components/homepage/Exams.vue";
import Demo from "@/components/homepage/Demo.vue";
import Subscribe from "@/components/homepage/Subscribe.vue";
import Footer from "@/components/homepage/Footer.vue";

export default {
  data() {
    return {
      sections: [
        "Hero",
        "Welcome",
        "QuickStart",
        "Exams",
        "Demo",
        "Subscribe",
        "Footer"
      ],
      options: {
        licenseKey: null,
        scrollingSpeed: 500,
        parallax: true,
        verticalCentered: true,
        menu: "#menu",
        controlArrows: true,
        scrollBar: true
      }
    };
  },
  components: {
    Hero,
    HeroLayout,
    Welcome,
    QuickStart,
    Exams,
    Demo,
    Subscribe,
    SectionLayout,
    Footer
  },
  computed: {
    disableFullpage() {
      return (
        window.innerHeight <= 450 &&
        window.matchMedia("(orientation: landscape)").matches
      );
    },
    user() {
      return this.$store.state.authentication.user;
    }
  },
  mounted() {}
};
</script>

<style scoped>
.fullpage-wrapper {
  width: 100% !important;
}
</style>
