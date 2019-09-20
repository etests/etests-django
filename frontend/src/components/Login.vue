<template>
  <v-card :class="$style.dialog">
    <Notification position="top center" />
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
          <form :class="$style.form" @keyup.enter="login">
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
            <v-btn round color="primary" @click="login">Login</v-btn>
          </v-layout>
        </v-card-actions>
      </v-tab-item>

      <v-tab-item>
        <v-card-text>
          <form :class="$style.form" @keyup.enter="register">
            <v-text-field v-model="name" label="Name" required />
            <v-select
              v-model="userType"
              :items="['Student', 'Institute']"
              :menu-props="{ maxHeight: '400' }"
              label="Register as"
              required
            ></v-select>
            <v-text-field v-model="email" label="Email" required />
            <v-text-field
              :append-icon="showPassword ? 'visibility' : 'visibility_off'"
              :type="showPassword ? 'text' : 'password'"
              v-model="registerPassword"
              name="input-10-2"
              label="Password"
              value=""
              class="input-group--focused"
              @click:append="showPassword = !showPassword"
              required
            />
          </form>
        </v-card-text>
        <v-card-actions>
          <v-layout justify-center>
            <v-btn round color="primary" @click="register">Register</v-btn>
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
      registerPassword: "",
      userType: "",
      showPassword: false
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
    isValidEmail(email) {
      return (
        email &&
        email.split("@").length === 2 &&
        email.split("@")[1].split(".").length >= 2 &&
        email.split("@")[1].split(".")[1]
      );
    },
    login(e) {
      var error = null;
      if (!this.username) error = "Enter your email or phone.";
      else if (!this.password) error = "Enter your password.";

      if (error) {
        this.$notify({
          title: "Oops!",
          type: "warn",
          text: error
        });
      } else {
        const { username, password } = this;
        if (username && password) {
          this.$store.dispatch("authentication/login", { username, password });
        }
      }
    },
    register(e) {
      var error = null;
      if (!this.name) error = "Enter your name.";
      else if (this.name.length > 100) error = "Your name is too long!";
      else if (!this.userType) error = "Enter registration type.";
      else if (!this.email) error = "Enter your email id.";
      else if (!this.isValidEmail(this.email)) error = "Email id is invalid!";
      else if (!this.registerPassword) error = "Enter a password.";
      else if (this.registerPassword.length < 8)
        error = "Password is too short!";

      if (error) {
        this.$notify({
          title: "Oops!",
          type: "warn",
          text: error
        });
      } else {
        var data = {
          name: this.name,
          email: this.email,
          password: this.registerPassword,
          is_student: false,
          is_institute: false
        };

        if (this.userType === "Student") data["is_student"] = true;
        else if (this.userType === "Institute") data["is_institute"] = true;
        this.$store.dispatch("authentication/register", data);
      }
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
