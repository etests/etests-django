<template>
  <v-card :class="$style.dialog">
    <v-tabs color="transparent" :class="$style.tabs" hide-slider centered>
      <v-tab active-class="primary--text">
        Login
      </v-tab>
      <v-tab active-class="primary--text">
        Register
      </v-tab>

      <v-tab-item>
        <v-card-title :class="$style.title">
          Login to eTests
        </v-card-title>
        <v-card-text>
          <form :class="$style.form">
            <v-text-field v-model="username" label="Email or phone" required />
            <v-text-field
              :append-icon="showPassword ? 'visibility' : 'visibility_off'"
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              name="input-10-2"
              label="Password"
              value=""
              class="input-group--focused"
              @click:append="showPassword = !showPassword"
            />
          </form>
        </v-card-text>
        <v-card-actions>
          <v-layout justify-center>
            <v-btn round color="info" @click="login">Login</v-btn>
          </v-layout>
        </v-card-actions>
      </v-tab-item>

      <v-tab-item>
        <v-card-text>
          <form :class="$style.form">
            <v-text-field v-model="name" label="Name" required />
            <v-select
              v-model="userType"
              :items="['Student', 'Institute']"
              :menu-props="{ maxHeight: '400' }"
              label="Register as"
            ></v-select>
            <v-text-field v-model="email" label="Email" required />
            <v-text-field
              :append-icon="showPassword ? 'visibility' : 'visibility_off'"
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              name="input-10-2"
              label="Password"
              value=""
              class="input-group--focused"
              @click:append="showPassword = !showPassword"
            />
          </form>
        </v-card-text>
        <v-card-actions>
          <v-layout justify-center>
            <v-btn round color="info" @click="register">Register</v-btn>
          </v-layout>
        </v-card-actions>
      </v-tab-item>
    </v-tabs>
  </v-card>
</template>

<script>
import { mapState } from "vuex";

export default {
  data: function() {
    return {
      username: "",
      password: "",
      name: "",
      email: "",
      userType: "",
      showPassword: false,
      submitted: false
    };
  },
  computed: {
    ...mapState({
      status: state => state.authentication.status
    })
  },
  watch: {
    status: function(newStatus, oldStatus) {
      if (!oldStatus.loggedIn && newStatus.loggedIn) {
        if (this.$store.state.authentication.user) {
          const type = this.$store.state.authentication.user.type;
          this.$router.push({ path: "/" + type + "/dashboard" });
        }
      }
    }
  },
  methods: {
    login(e) {
      this.submitted = true;
      const { username, password } = this;
      if (username && password) {
        this.$store.dispatch("authentication/login", { username, password });
      }
    },
    register(e) {
      this.submitted = true;

      var data = {
        name: this.name,
        email: this.email,
        password: this.password,
        is_student: false,
        is_institute: false
      };

      if (this.userType === "Student") data["is_student"] = true;
      else if (this.userType === "Institute") data["is_institute"] = true;
      this.$store.dispatch("authentication/register", data);
    }
  }
};
</script>

<style module lang="stylus">
.dialog{
  border-radius: 12px;
  font-family: 'Product Sans Light', Roboto;
  height: 450px;


  .tabs{
    border-radius: 0;
    padding-top: 20px;
    font-family: 'Product Sans Medium', Roboto;
  }

  .title{
    margin-left: 50px;
    text-align: left;
    font-family: 'Product Sans Light', Roboto;
    font-size: 1.4rem;
    color: #7e777e;
  }
  .form{
    margin: auto;
    width: 80%;
    min-width: 250px;
    max-width: 95%;
    border-radius: 8px;
    font-family: 'Product Sans Light', Roboto;
  }
}
</style>
