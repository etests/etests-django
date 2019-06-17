<template>
  <SectionLayout>
    <template slot="heading">
      Featured Exams
    </template>
    <template slot="subheading">
      supporting major engineering and medical entrance exams
    </template>
    <v-layout
      row
      wrap
      justify-center
      justify-space-around
      slot="content"
      :class="$style.cardsContainer"
      :mt-5="!isSmallScreen"
    >
      <v-flex v-for="card in cards" :key="card.title" xs6 lg3>
        <v-card hover :class="$style.card">
          <v-img :src="card.src" :class="$style.icon" />
          <v-flex xs12 :class="$style.text">
            {{ card.title }}
          </v-flex>
        </v-card>
      </v-flex>
    </v-layout>
  </SectionLayout>
</template>

<script>
import SectionLayout from "@components/homepage/SectionLayout.vue";

export default {
  name: "Welcome",
  data() {
    return {
      isSmallScreen: this.$vuetify.breakpoint.smAndDown,
      cards: [
        {
          title: "JEE MAIN",
          src: require("@assets/images/exams/jeemain.png")
        },
        {
          title: "JEE ADVANCED",
          src: require("@assets/images/exams/jeeadvanced.png")
        },
        {
          title: "NEET",
          src: require("@assets/images/exams/neet.png")
        },
        {
          title: "AIIMS",
          src: require("@assets/images/exams/aiims.png")
        }
      ]
    };
  },
  components: {
    SectionLayout
  }
};
</script>

<style module lang="stylus">
.cardsContainer{
   margin: 25px auto;

  .card{
    margin: 5px auto 40px;
    border-radius: 8px;
    padding: 5px;
    width: 90%;
    max-width: 300px;
    height: auto;
    min-height: 150px;

    .icon{
      margin: auto;
      width: 60%;
      position: relative  ;
      top: -40px
    }

    .text{
      font-family: "Product Sans";
      font-size: 1.2rem;
      width: 100%
      text-align: center;
      position: relative  ;
      bottom: 10px
    }
  }
}
</style>
