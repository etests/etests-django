<template>
  <v-container fluid>
    <Header :disableDrawerClose="true" />
    <v-content app>
      <v-container>
        <v-card>
          <v-layout row wrap class="mb-4 py-1" justify-center>
            <v-flex xs12 lg4>
              <img src="~@assets/logos/etests.png" width="90%" />
            </v-flex>
            <v-flex xs12 lg8>
              <v-card-text>
                <v-text-field
                  v-model="user.name"
                  label="FirstName"
                ></v-text-field>
                <v-text-field v-model="user.phone" label="Phone"></v-text-field>
                <v-text-field
                  v-model="user.email"
                  label="Email Address"
                ></v-text-field>
                <v-text-field v-model="user.city" label="City"></v-text-field>
                <v-text-field v-model="user.state" label="State"></v-text-field>
              </v-card-text>
              <v-card-actions>
                <v-btn color="primary">
                  <v-icon left dark>check</v-icon>
                  Save Changes
                </v-btn>
              </v-card-actions>
            </v-flex>
          </v-layout>
        </v-card>
      </v-container>
      <Footer />
    </v-content>
  </v-container>
</template>

<script>
import Header from "@components/Header.vue";
import Footer from "@components/Footer.vue";

export default {
  computed: {
    user() {
      return this.$store.state.authentication.user;
    }
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
