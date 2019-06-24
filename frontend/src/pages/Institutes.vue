<template>
  <StandardLayout>
    <v-flex v-for="institute in institutes" :key="institute.id" xs12 md6 lg4>
      <v-card>
        <v-img :src="institute.src" height="200px">
          <template v-slot:placeholder>
            <v-layout fill-height align-center justify-center ma-0>
              <v-progress-circular
                indeterminate
                color="grey"
              ></v-progress-circular>
            </v-layout>
          </template>
        </v-img>

        <v-card-actions>
          <v-container fill-height fluid pa-2>
            <v-layout fill-height>
              <v-flex xs12 align-end flexbox>
                <span class="body1" v-text="institute.name"></span>
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
  </StandardLayout>
</template>

<script>
import StandardLayout from "@components/layouts/StandardLayout";

export default {
  data() {
    return {};
  },
  components: {
    StandardLayout
  },
  created() {
    this.$store.dispatch("institutes/getAll");
  },
  computed: {
    institutes() {
      var list = [];
      if (this.$store.state.institutes.all.items) {
        this.$store.state.institutes.all.items.forEach(function(item) {
          list.push({
            id: item.pk,
            name: item.user.name,
            src: "https://i.ytimg.com/vi/kUNxVtS5D7c/maxresdefault.jpg"
          });
        });
      }
      return list;
    }
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
