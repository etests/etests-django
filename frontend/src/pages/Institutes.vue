<template>
  <v-container fluid>
    <Header :disableDrawerClose="true" />
    <v-content app>
      <div style="max-width: 80%; margin: auto;">
        <v-container fluid grid-list-lg>
          <v-layout row wrap>
            <v-flex
              v-for="card in cards"
              :key="card.title"
              v-bind="{ [`xs${card.flex}`]: true }"
            >
              <v-card>
                <v-img :src="card.src" height="200px"> </v-img>

                <v-card-actions>
                  <v-container fill-height fluid pa-2>
                    <v-layout fill-height>
                      <v-flex xs12 align-end flexbox>
                        <span class="title" v-text="card.title"></span>
                      </v-flex>
                    </v-layout>
                  </v-container>
                  <v-spacer></v-spacer>
                  <v-btn color="blue" icon flat>
                    <v-icon>share</v-icon>
                  </v-btn>
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
      cards: [
        {
          title: "Aakash Institute",
          src: "https://i.ytimg.com/vi/kUNxVtS5D7c/maxresdefault.jpg",
          flex: 6
        },
        {
          title: "Allen Career Institute",
          src: "https://i.ytimg.com/vi/kUNxVtS5D7c/maxresdefault.jpg",
          flex: 6
        },
        {
          title: "Resonance",
          src: "https://i.ytimg.com/vi/kUNxVtS5D7c/maxresdefault.jpg",
          flex: 6
        },
        {
          title: "Bansal Classes",
          src: "https://i.ytimg.com/vi/kUNxVtS5D7c/maxresdefault.jpg",
          flex: 6
        },
        {
          title: "FIITJEE",
          src: "https://i.ytimg.com/vi/kUNxVtS5D7c/maxresdefault.jpg",
          flex: 6
        },
        {
          title: "Narayana",
          src: "https://i.ytimg.com/vi/kUNxVtS5D7c/maxresdefault.jpg",
          flex: 6
        },
        {
          title: "Vibrant Academy",
          src: "https://i.ytimg.com/vi/kUNxVtS5D7c/maxresdefault.jpg",
          flex: 6
        },
        {
          title: "Vidya Mandir Classes",
          src: "https://i.ytimg.com/vi/kUNxVtS5D7c/maxresdefault.jpg",
          flex: 6
        },
        {
          title: "IITians PACE",
          src: "https://i.ytimg.com/vi/kUNxVtS5D7c/maxresdefault.jpg",
          flex: 6
        },
        {
          title: "Brilliant Tutorials",
          src: "https://i.ytimg.com/vi/kUNxVtS5D7c/maxresdefault.jpg",
          flex: 6
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
