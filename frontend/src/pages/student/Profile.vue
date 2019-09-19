<template>
  <StandardLayout>
    <Notification position="top center" />
    <v-card :class="$style.profileCard">
      <v-layout row wrap justify-center>
        <v-flex xs12 lg6>
          <v-img
            class="white--text"
            height="250px"
            width="250px"
            src="https://www.theuiaa.org/wp-content/uploads/2017/12/2018_banner.jpg"
          />
        </v-flex>
        <v-flex xs12 lg6>
          <v-card-text>
            <v-text-field v-model="profile.name" label="Name"></v-text-field>
            <v-text-field v-model="profile.phone" label="Phone"></v-text-field>
            <v-text-field
              v-model="profile.birth_date"
              label="Birth Date"
            ></v-text-field>
            <v-text-field v-model="profile.city" label="City"></v-text-field>
            <v-text-field v-model="profile.state" label="State"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="save" color="primary" round>
              <v-icon left dark>check</v-icon>
              Save Changes
            </v-btn>
          </v-card-actions>
        </v-flex>
      </v-layout>
    </v-card>
  </StandardLayout>
</template>

<script>
import StandardLayout from "@/components/layouts/StandardLayout";

export default {
  computed: {
    profile() {
      return this.$store.state.authentication.user.profile;
    }
  },
  components: {
    StandardLayout
  },
  methods: {
    save(e) {
      var error = null;
      if (!this.profile.name) error = "Enter your name.";
      else if (this.profile.name.length > 100) error = "Your name is too long!";
      else if (!this.profile.phone) error = "Enter your phone number.";
      else if (!this.profile.birth_date) error = "Enter your birth date";
      else if (!this.profile.state) error = "Select your state.";
      else if (!this.profile.city) error = "Select your city.";

      if (error) {
        this.$notify({
          title: "Oops!",
          type: "warn",
          text: error
        });
      } else {
        var data = {
          name: this.profile.name,
          phone: this.profile.phone,
          birth_date: this.profile.birth_date,
          city: this.profile.city,
          state: this.profile.state
        };

        this.$store.dispatch("users/updateProfile", data);
      }
    }
  }
};
</script>

<style module lang="stylus">

.profileCard{
  margin: auto;
  width: 600px;
  max-width: 100%;
  padding: 20px;
}
</style>
