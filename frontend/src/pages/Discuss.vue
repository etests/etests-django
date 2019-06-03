<template>
  <v-container fluid>
    <Header :disableDrawerClose="true" />
    <v-content app>
      <div style="max-width: 80%; margin: auto;">
        <v-container fluid grid-list-lg>
          <v-layout row wrap>
            <v-flex xs12 v-for="(post, i) in posts" :key="i">
              <v-card>
                <v-layout class="text-xs-left">
                  <v-flex xs12>
                    <v-card-title primary-title>
                      <div>
                        <div class="title">{{ post.title }}</div>
                        <br />
                        <div>{{ post.description }}</div>
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
          </v-layout>
        </v-container>
      </div>
      <Footer />
    </v-content>
  </v-container>
</template>

<script>
import Header from "@components/Header.vue";
import Footer from "@components/Footer.vue";

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
    Header,
    Footer
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

.logo{
  width: 40px;
  float: left;
  margin: 0 5px;
}
</style>
