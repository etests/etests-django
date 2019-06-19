<template>
  <SectionLayout>
    <template slot="heading">
      Welcome to eTests
    </template>
    <template slot="subheading">
      your online exam partner
    </template>
    <v-layout
      row
      wrap
      justify-center
      slot="content"
      :class="$style.cardsContainer"
    >
      <v-flex v-for="card in cards" :key="card.title" xs6 sm3>
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
      cards: [
        {
          title: "Create online tests",
          src: require("@assets/images/features/create.png")
        },
        {
          title: "Attempt online tests",
          src: require("@assets/images/features/attempt.png")
        },
        {
          title: "Detailed analysis of tests",
          src: require("@assets/images/features/analysis.png")
        },
        {
          title: "Sell your test series",
          src: require("@assets/images/features/sell.png")
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
   margin: 50px auto;

  .card{
    margin: 5px auto 40px;
    border-radius: 8px;
    padding: 5px;
    width: 90%;
    max-width: 300px;
    height: auto;
    min-height: 160px;

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
