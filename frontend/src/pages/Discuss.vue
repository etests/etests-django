<template>
  <StandardLayout>
    <v-flex xs12 v-for="(post, i) in posts" :key="i">
      <v-card :class="$style.questionCard">
        <v-layout class="text-xs-left">
          <v-flex xs12>
            <v-card-title>
              <div>
                <div :class="$style.title">{{ post.title }}</div>
                <br />
                <div :class="$style.description">{{ post.description }}</div>
                <br />
                <div>{{ post.user }}</div>
              </div>
            </v-card-title>
          </v-flex>
        </v-layout>
        <v-divider light></v-divider>
        <v-card-actions class="pa-3">
          <v-btn flat small color="success">Answer this question</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";

export default {
  data() {
    return {
      posts: [
        {
          title: "Can the limit of a polynomial involving infinity be finite?",
          description:
            "I have been working around with limits involving infinity and was stuck with this limit: limx→∞[(x5+10x4+3)c−x] Can this limit have some finite value for any real value of c? If yes then what is c and the limit? I tried putting x=1/t and letting limt→0, then I used L'Hospital's Rule but ended up having another 0/0 form. Please help me.",
          user: "Piyush Maurya"
        },
        {
          title: "Can the limit of a polynomial involving infinity be finite?",
          description:
            "I have been working around with limits involving infinity and was stuck with this limit: limx→∞[(x5+10x4+3)c−x] Can this limit have some finite value for any real value of c? If yes then what is c and the limit? I tried putting x=1/t and letting limt→0, then I used L'Hospital's Rule but ended up having another 0/0 form. Please help me.",
          user: "Piyush Maurya"
        },
        {
          title: "Can the limit of a polynomial involving infinity be finite?",
          description:
            "I have been working around with limits involving infinity and was stuck with this limit: limx→∞[(x5+10x4+3)c−x] Can this limit have some finite value for any real value of c? If yes then what is c and the limit? I tried putting x=1/t and letting limt→0, then I used L'Hospital's Rule but ended up having another 0/0 form. Please help me.",
          user: "Piyush Maurya"
        }
      ]
    };
  },
  components: {
    StandardLayout
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';


.questionCard{
  border: 1px solid #dadce0;
  border-radius: 8px;
  .title{
    font-family: 'Product Sans Light',Roboto,Arial,sans-serif;
    font-size: 1.875rem;
    line-height: 1.75rem;
    color: #202124;
  }
  .description{
    text-align: left;
    letter-spacing: .014em;
    font-family: 'Product Sans Light',Roboto,Arial,sans-serif;
    font-size: 1.08rem;
    line-height: 1.25rem;
    color: #5f6368;
  }
}
</style>
